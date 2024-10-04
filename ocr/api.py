from dataclasses import dataclass
import pytesseract
import numpy as np
import utils.logger as logger

TESSERACT_CONFIG = r'--oem 3 --psm 6 -l spa'

@dataclass
class TextBox:
    text: str
    x: int
    y: int
    w: int
    h: int

    def __str__(self):
        return f"Text: {self.text}, x: {self.x}, y: {self.y}, w: {self.w}, h: {self.h}"

    def __repr__(self):
        return self.__str__()


class PyTesseractAPI:
    def __init__(self, tesseract_path: str = None, config: str = TESSERACT_CONFIG):
        pytesseract.pytesseract.tesseract_cmd = tesseract_path
        self.config = config

    def recognize_text(self, image: np.ndarray, lang: str = "spa", debug : bool = False) -> str:
        full_text = pytesseract.image_to_string(image, lang=lang, config=self.config)
        if debug:
            logger.log("OCR text", full_text)
        
        return full_text
    
    def recognise_text_to_data(self, image: np.ndarray, lang: str = "spa", debug: bool = False) -> tuple[str, list[TextBox]]:
        data =  pytesseract.image_to_data(image, lang=lang, config=self.config, output_type=pytesseract.Output.DICT)

        full_text = ' '.join(data['text'])
        if debug:
            logger.log("OCR text", full_text)

        text_boxes = []
        for i in range(len(data['level'])):
            text_boxes.append(
                TextBox(
                    data['text'][i], 
                    data['left'][i], 
                    data['top'][i], 
                    data['width'][i], 
                    data['height'][i]
                )
            )

        return full_text, text_boxes
    