import easyocr
import pytesseract

import cv2
import numpy as np
from PIL import Image, ImageGrab

import pyperclip

from typing import Callable

class TextSnipper:
    
    TesseractPath: str = r'C:\My Program Files\Tesseract-OCR\tesseract.exe' # path to tesseract.exe
    
    def __init__(self, mode: str, preprocess_modes: list[str]) -> None:
        self.image: Image.Image | None = None
        self.image_array: np.ndarray | None = None
        self.text: str | None = None
        
        self.kernel = np.ones((5,5),np.uint8)

        self.preprocess: dict[str, Callable] = {"-g": self.get_grayscale, "-r": self.remove_noise, "-t": self.thresholding, "-d": self.dilate, "-e": self.erode, "-o": self.opening, "-c": self.canny, "-s": self.skew}
        self.preprocess_modes: list[str] = preprocess_modes if preprocess_modes[0] != "" else []
        
        self.models: dict[str, Callable] = {"easyocr": self.easyocr_mode, "tesseract": self.tesseract_mode}    
        self.model: str = mode
    
    def getTextFromImage(self, box: tuple[int, int, int, int] | None) -> None:
        print("Getting image...")
        self.getImage(box)
        
        print("Preprocessing image...")
        self.preprocessing()
        
        print("Reading text from image...")
        self.models[self.model]() 
        
        print("Copying text to clipboard...")
        self.copyTextToClipboard()
            
        print("DONE!")
        
    def getImage(self, box: tuple[int, int, int, int] | None) -> None:
        self.image = ImageGrab.grab(bbox= box)
        self.image_array = np.array(self.image)
    
    def copyTextToClipboard(self) -> None:
        assert self.text is not None
        pyperclip.copy(self.text)
    
    def easyocr_mode(self) -> None:
        reader: easyocr.Reader = easyocr.Reader(['en'])

        # detail = 0 returns only the text
        self.text = "\n".join(reader.readtext(self.image_array, detail= 0)) # type: ignore

    def tesseract_mode(self) -> None:
        pytesseract.pytesseract.tesseract_cmd = self.TesseractPath

        self.text = pytesseract.image_to_string(self.image_array, lang='eng')

    def preprocessing(self) -> None:
        assert self.image_array is not None
        for mode in self.preprocess_modes:
            self.image_array = self.preprocess[mode]()

    # get grayscale image
    def get_grayscale(self) -> np.ndarray:
        assert self.image_array is not None
        return cv2.cvtColor(self.image_array, cv2.COLOR_BGR2GRAY)

    # noise removal
    def remove_noise(self) -> np.ndarray:
        assert self.image_array is not None
        return cv2.medianBlur(self.image_array,5)
    
    #thresholding    
    def thresholding(self) -> np.ndarray:
        assert self.image_array is not None
        return cv2.threshold(self.image_array, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    
    #dilation
    def dilate(self) -> np.ndarray:
        assert self.image_array is not None
        return cv2.dilate(self.image_array, self.kernel, iterations = 1)
        
    #erosion
    def erode(self) -> np.ndarray:
        assert self.image_array is not None
        return cv2.erode(self.image_array, self.kernel, iterations = 1)

    #opening - erosion followed by dilation
    def opening(self) -> np.ndarray:
        assert self.image_array is not None
        return cv2.morphologyEx(self.image_array, cv2.MORPH_OPEN, self.kernel)

    #canny edge detection
    def canny(self) -> np.ndarray:
        assert self.image_array is not None
        return cv2.Canny(self.image_array, 100, 200)

    #skew correction
    def skew(self) -> np.ndarray:
        assert self.image_array is not None
        coords = np.column_stack(np.where(self.image_array > 0))
        angle = cv2.minAreaRect(coords)[-1]
        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle
        (h, w) = self.image_array.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(self.image_array, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        return rotated

    #template matching
    def match_template(self, template: cv2.Mat) -> cv2.Mat:
        assert self.image_array is not None
        return cv2.matchTemplate(self.image_array, template, cv2.TM_CCOEFF_NORMED)