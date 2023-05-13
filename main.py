import easyocr
import pytesseract

import numpy as np
from PIL import Image, ImageGrab

import pyperclip

from sys import argv

from typing import Callable

class ImageToText:
    
    def __init__(self, mode: str = "easyocr") -> None:
        self.image: Image.Image | None = None
        self.text: str | None = None
        self.mode: str = mode
        self.modes: dict[str, Callable] = {"easyocr": self.easyocr_mode, "tesseract": self.tesseract_mode}    
    
    def getTextFromImage(self) -> None:
        print("Reading image from clipboard...")
        if not self.getImageFromClipboard():
            print("No image found in clipboard!")
            return
        
        print("Reading text from image...")
        self.modes[self.mode]() 
        
        print("Copying text to clipboard...")
        self.copyTextToClipboard()
            
        print("DONE!")
        
    def getImageFromClipboard(self) -> bool:
        self.image = ImageGrab.grabclipboard()
        return self.image is not None
    
    def copyTextToClipboard(self) -> None: 
        pyperclip.copy(self.text)
    
    def easyocr_mode(self) -> None:
        reader: easyocr.Reader = easyocr.Reader(['en'])

        self.text = "\n".join(reader.readtext(np.array(self.image), detail= 0)) # type: ignore

    def tesseract_mode(self):
        pytesseract.pytesseract.tesseract_cmd = r'.\Tesseract-OCR\tesseract.exe' # path to tesseract.exe

        self.text = pytesseract.image_to_string(np.array(self.image), lang='eng')
    
def main():
    if len(argv) != 2:
        print("Usage: python main.py <mode>")
        print("Modes: easyocr, tesseract")
        return
    ImageToText(argv[1]).getTextFromImage()
    
    
if __name__ == "__main__":
    main()
