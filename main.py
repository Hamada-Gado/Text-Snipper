import easyocr
import pytesseract

import cv2
import numpy as np
from PIL import Image, ImageGrab

import pyperclip

from sys import argv

from typing import Callable

class ImageToText:
    
    def __init__(self, mode: str, preprocess_modes: list[str]) -> None:
        self.image: Image.Image | None = None
        self.image_array: np.ndarray | None = None
        self.text: str | None = None
        
        self.kernel = np.ones((5,5),np.uint8)

        self.preprocess_modes: dict[str, Callable] = {"-g": self.get_grayscale, "-r": self.remove_noise, "-t": self.thresholding, "-d": self.dilate, "-e": self.erode, "-o": self.opening, "-c": self.canny, "-s": self.skew}
        self.preprocess_mode: list[str] = preprocess_modes if preprocess_modes[0] != "" else []
        
        self.models: dict[str, Callable] = {"easyocr": self.easyocr_mode, "tesseract": self.tesseract_mode}    
        self.model: str = mode
    
    def getTextFromImage(self) -> None:
        print("Reading image from clipboard...")
        if not self.getImageFromClipboard():
            print("No image found in clipboard!")
            return
        
        print("Preprocessing image...")
        self.preprocess()
        
        print("Reading text from image...")
        self.models[self.model]() 
        
        print("Copying text to clipboard...")
        self.copyTextToClipboard()
            
        print("DONE!")
        
    def getImageFromClipboard(self) -> bool:
        self.image = ImageGrab.grabclipboard()
        self.image_array = np.array(self.image)
        return self.image is not None
    
    def copyTextToClipboard(self) -> None:
        assert self.text is not None
        pyperclip.copy(self.text)
    
    def easyocr_mode(self) -> None:
        reader: easyocr.Reader = easyocr.Reader(['en'])

        # detial = 0 returns only the text
        self.text = "\n".join(reader.readtext(self.image_array, detail= 0)) # type: ignore

    def tesseract_mode(self) -> None:
        pytesseract.pytesseract.tesseract_cmd = r'.\Tesseract-OCR\tesseract.exe' # path to tesseract.exe

        self.text = pytesseract.image_to_string(self.image_array, lang='eng')

    def preprocess(self) -> None:
        assert self.image_array is not None
        for mode in self.preprocess_mode:
            self.image_array = self.preprocess_modes[mode]()

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

    
def print_usage() -> None:
    print("Usage: python main.py (<model> | -h) <preprocess modes>")
    print("-h: help\n")
    print("Modes: easyocr, tesseract\n")
    print("Preprocess modes: -a, -g, -r, -t, -d, -e, -o, -c, -s")
    print("-a: all, -g: grayscale, -r: remove noise, -t: thresholding, -d: dilate, -e: erode, -o: opening, -c: canny, -s: skew\n")
    print("Example: python main.py easyocr -g\n")
    
def check_argv(args: list) -> bool:
    # return if no args are given with default args and print usage
    if len(args) < 2:
        print_usage()
        args += ["easyocr", "-g"]
        print("WARNING! No model is given.")
        print("Defaulting to easyocr model and -g flag is set.")
        return True
    
    # return if help flag is set or wrong model is given    
    if args[1] not in ["easyocr", "tesseract"]:
        print_usage()
        return False
    
    # add empty string to args if no preprocess modes are given, or add all modes if -a flag is set
    if len(args) < 3:
        args += [""]
    elif args[2] == "-a":
        args.remove("-a")
        args += ["-g", "-r", "-t", "-d", "-e", "-o", "-c", "-s"]
        
    # return if wrong preprocess modes are given
    for arg in args[2:]:
        if arg not in ["-g", "-r", "-t", "-d", "-e", "-o", "-c", "-s"]:
            print_usage()
            return False
        
    return True
    

def main() -> None:
    if check_argv(argv):
        ImageToText(argv[1], argv[2:]).getTextFromImage()
    
if __name__ == "__main__":
    main()
