import numpy as np
import cv2
from ocr.api import TextBox

class Anonymiser:
    def anonymise(self, image: np.array, text_boxes: list[TextBox], sensitive_words: list[str], margin: int = 10) -> np.array:
        for text_box in text_boxes:
            if any(sensitive_word in text_box.text for sensitive_word in sensitive_words):
                # Calculate the new coordinates with margin
                x1 = max(text_box.x - margin, 0)
                y1 = max(text_box.y - margin, 0)
                x2 = min(text_box.x + text_box.w + margin, image.shape[1])
                y2 = min(text_box.y + text_box.h + margin, image.shape[0])

                # Extract the region of interest (ROI) with the margin
                roi = image[y1:y2, x1:x2]
                blurred_roi = cv2.GaussianBlur(roi, (15, 15), 30)
                image[y1:y2, x1:x2] = blurred_roi
        
        return image