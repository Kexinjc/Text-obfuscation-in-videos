from PIL import Image, ImageFilter, ImageOps
import numpy as np
import cv2


class OCRPreprocessor:
    def __init__(self, scaling_factor: float = 1.0):
        self.scaling_factor = scaling_factor

    def preprocess_image(self, image: np.array) -> np.array:
        '''
        Preprocess the image before passing it to the OCR API
        '''
        # Resize the image
        processed_img = self._resize(image, self.scaling_factor)

        # Convert the image to grayscale
        processed_img = self._grayscale(processed_img)

        # Apply adaptive thresholding
        # processed_img = self._adaptive_threshold(processed_img, 11, 2)

        # # Apply median blur to remove noise
        # processed_img = self._median_blur(processed_img, 3)

        # Increase the sharpness of the image
        processed_img = self._sharpen(processed_img)

        return processed_img


    def _resize(self, image: np.array, scaling_factor: float) -> np.array:
        '''
        Resize the given image by the given scaling factor
        '''
        new_width = int(image.shape[1] * scaling_factor)
        new_height = int(image.shape[0] * scaling_factor)
        return cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_LINEAR)

    def _grayscale(self, image: Image.Image) -> Image.Image:
        '''
        Convert the given image to grayscale
        '''
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    def _adaptive_threshold(self, image: np.array, block_size: int, C: int) -> np.array:
        '''
        Apply adaptive thresholding to the given image
        '''
        return cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, 
                                         cv2.THRESH_BINARY, block_size, C)

    def _median_blur(self, image: np.array, kernel_size: int) -> np.array:
        '''
        Apply median blur to the given image
        '''
        return cv2.medianBlur(image, kernel_size)
    
    def _sharpen(self, image: np.array) -> np.array:
        '''
        Increase the sharpness of the given image
        '''
        # Define a sharpening kernel
        kernel = np.array([[0, -1, 0],
                        [-1, 5,-1],
                        [0, -1, 0]])
        
        # Apply the sharpening kernel to the image
        sharpened_image = cv2.filter2D(image, -1, kernel)
        
        return sharpened_image