import easyocr
import pyperclip
import numpy as np
from PIL import Image, ImageGrab

reader: easyocr.Reader = easyocr.Reader(['en'])

def main():
    print("Reading image from clipboard...")
    image: Image.Image | None = ImageGrab.grabclipboard()
    
    if image is None:
        print("No image in clipboard")
        return
    
    print("Reading text from image...")
    text = "\n".join(
            reader.readtext(np.array(image), detail= 0))# type: ignore
    
    print("Copying text to clipboard...")
    pyperclip.copy(text)
    
    print("Done!")
    
if __name__ == "__main__":
    main()
