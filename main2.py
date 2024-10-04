import cv2
from analyser.analyser import OCRAnalyser
from ocr.anonymiser import Anonymiser
from ocr.api import PyTesseractAPI
from ocr.preprocessor import OCRPreprocessor
from ocr.api import TextBox
import click
import os
import numpy as np
import time
import ffmpeg

start = time.time()

SCALING_FACTOR = 1.0


def retrieve_tesseract_path() -> str:
    tesseract_path = os.getenv('TESSERACT_PATH')

    if tesseract_path:
        tesseract_path = r'{}'.format(tesseract_path)
    else:
        print("Tesseract executable not found. Please set the path to the tesseract executable in the TESSERACT_PATH environment variable.")
        os._exit(1)
    return tesseract_path

@click.command()
@click.option(
    '--input', '-i', 
    help = 'Path to the image to obfuscate', 
    required = True, 
    type = str
)
@click.option('--output', '-o', 
    help = 'Path to save the obfuscated image', 
    required = False, 
    type = str, 
    default = 'obfuscated_image.png'
)
@click.option('--recognizer', '-r',
    help = 'Recognizers to register. Default includes all recognizers' , 
    required = False,
    multiple = True, 
    type = click.Choice(["DOB", "DNI", "PHONE", "ADDRESS", "POSTAL_CODE_CITY", "PERSON", "LOCATION", "ORG", "EMAIL"]), 
    default = None
)
@click.option('--exclude-recognizer', '-e', 
    help = 'Recognizers to exclude. Default includes all recognizers' , 
    required = False, 
    multiple = True, 
    type = click.Choice(["DOB", "DNI", "PHONE", "ADDRESS", "POSTAL_CODE_CITY", "PERSON", "LOCATION", "ORG", "EMAIL"]), 
    default = None
)
@click.option('--filter', '-f', 
    help = 'obfuscate a given word', 
    required = False, 
    multiple = True,
    type = str, 
    default = None
)
@click.option('--unfilter', '-u', 
    help = 'un-obfuscate a given word', 
    required = False,
    multiple = True, 
    type = str, 
    default = None
)
@click.option('--frame-diff-threshold', '-t',
    help = 'Threshold for frame change percentage',
    required = False,
    type = int,
    default = 2
)
@click.option('--verbose', '-v', 
    help = 'Enable verbose mode for additional logging', 
    required = False,
    is_flag = True,
    default = False
)
def main(input, output, recognizer, exclude_recognizer, filter, unfilter, frame_diff_threshold, verbose):
    # read tesseract path from env
    tesseract_path = retrieve_tesseract_path()
    tesseract_api = PyTesseractAPI(tesseract_path = tesseract_path)

    # Initialise image preprocessor
    image_preprocessor = OCRPreprocessor(scaling_factor=SCALING_FACTOR)

    # Initialize OCR analyser and anonymiser
    analyser = OCRAnalyser(recognizers=recognizer, excluded_recognizers=exclude_recognizer, filtered_words=filter, unfiltered_words=unfilter)
    anonymiser = Anonymiser()

    if input.endswith(('.jpg', '.jpeg', '.png')):
        # run image pipeline
        image_pipeline(image_preprocessor, tesseract_api, analyser, anonymiser, input, output, verbose)
    elif input.endswith(('.mp4')):
        # run video pipeline
        video_pipeline(image_preprocessor, tesseract_api, analyser, anonymiser, input, output, frame_diff_threshold, verbose)
    end = time.time()
    print(f'time taken: ',end-start)

def image_pipeline(image_preprocessor: OCRPreprocessor, tesseract_api: PyTesseractAPI, analyser: OCRAnalyser, anonymiser: Anonymiser, input: str, output: str, verbose: bool):
    # read image and extract text
    img = cv2.imread(input)
    preprocessed_image = image_preprocessor.preprocess_image(img)

    # extract text
    ocr_text, text_boxes = tesseract_api.recognise_text_to_data(img, lang="spa", debug=verbose)
    # text_boxes = translate_image_scale(text_boxes, SCALING_FACTOR)

    # analyse text
    sensitive_words = analyser.analyse_text_to_string(ocr_text, "es", debug=verbose)
    # anonymise image
    img = anonymiser.anonymise(img, text_boxes, sensitive_words)

    # save image
    cv2.imwrite(output, img)


def frame_difference(prev_frame, curr_frame, threshold=30):
    # Convert frames to grayscale
    gray_prev = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    gray_curr = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)
    
    # Compute the absolute difference between the current frame and the previous frame
    frame_diff = cv2.absdiff(gray_prev, gray_curr)
    
    # Threshold the difference
    _, thresh = cv2.threshold(frame_diff, threshold, 255, cv2.THRESH_BINARY)
    
    # Calculate the percentage of changed pixels
    non_zero_count = np.count_nonzero(thresh)
    changed_percentage = (non_zero_count * 100) / thresh.size
    
    return changed_percentage


def apply_obfuscation_to_background(frame, prev_obfuscated_frame, mask):
    # Apply the obfuscation only to the background
    obfuscated_frame = frame.copy()
    obfuscated_frame[mask == 0] = prev_obfuscated_frame[mask == 0]
    return obfuscated_frame


def video_pipeline(image_preprocessor: OCRPreprocessor, tesseract_api: PyTesseractAPI, analyser: OCRAnalyser, anonymiser: Anonymiser, input: str, output: str, frame_diff_threshold: int, verbose: bool):
    # read video
    cv2.namedWindow('preview', cv2.WINDOW_NORMAL)
    cap = cv2.VideoCapture(input)

    # check if video is opened
    if not cap.isOpened():
        print("Error: Could not open video.")
        os._exit(1)

    # get video properties
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_rate = int(cap.get(5))

    # create video writer
    tmp_output = "tmp_" + output
    out = cv2.VideoWriter(tmp_output, cv2.VideoWriter_fourcc(*'mp4v'), frame_rate, (frame_width, frame_height))

    prev_frame = None
    frame_change_threshold = frame_diff_threshold  # Set the threshold for frame change percentage (antes: 5)
    previous_text_boxes = None
    previous_sensitive_words = None

    # Create background subtractor
    back_sub = cv2.createBackgroundSubtractorMOG2()

    while True:
        ret, frame = cap.read()

        if frame is None:
            print("End of video")
            break

        # Apply background subtraction
        fg_mask = back_sub.apply(frame)

        if prev_frame is not None:
            change_percentage = frame_difference(prev_frame, frame)
            if change_percentage < frame_change_threshold:
                frame = anonymiser.anonymise(frame, previous_text_boxes, previous_sensitive_words)
            else:
                # If change is significant, run OCR and Presidio
                preprocessed_image = image_preprocessor.preprocess_image(frame)
                ocr_text, text_boxes = tesseract_api.recognise_text_to_data(preprocessed_image, lang="spa", debug=verbose)
                sensitive_words = analyser.analyse_text_to_string(ocr_text, "es", debug=verbose)
                frame = anonymiser.anonymise(frame, text_boxes, sensitive_words)
                previous_text_boxes = text_boxes
                previous_sensitive_words = sensitive_words
        else:
            # For the first frame, run OCR and Presidio
            preprocessed_image = image_preprocessor.preprocess_image(frame)
            ocr_text, text_boxes = tesseract_api.recognise_text_to_data(preprocessed_image, lang="spa", debug=verbose)
            sensitive_words = analyser.analyse_text_to_string(ocr_text, "es", debug=verbose)
            frame = anonymiser.anonymise(frame, text_boxes, sensitive_words)
            previous_text_boxes = text_boxes
            previous_sensitive_words = sensitive_words

        prev_frame = frame.copy()

        cv2.imshow("preview", frame)

        # Wait for a key event for 1 ms
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # write frame to video
        out.write(frame)

    # release video capture and writer
    cap.release()
    out.release()

    input_video = ffmpeg.input(tmp_output)
    input_audio = ffmpeg.input(input)

    ffmpeg.concat(input_video, input_audio, v=1, a=1).output(output).overwrite_output().run()

    # remove temporary file
    os.remove(tmp_output)

    # close all windows
    cv2.destroyAllWindows()

def translate_image_scale(text_boxes: list[TextBox], scaling_factor: float) -> list[TextBox]:
    for text_box in text_boxes:
        text_box.x = int(text_box.x / scaling_factor)
        text_box.y = int(text_box.y / scaling_factor)
        text_box.w = int(text_box.w / scaling_factor)
        text_box.h = int(text_box.h / scaling_factor)
    return text_boxes


if __name__ == '__main__':
    main()