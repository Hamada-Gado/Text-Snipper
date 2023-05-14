# Text-Snipping
A simple script to snip text from images using easyocr or tesseract.
## Setup
* pip install -r requirements.txt
* download tesseract.exe if you want to use it's mode, and add it to your environment variables or add it's location to TesseractPath variable in TextSnipper class.
* Download tesseract it from [here](https://digi.bib.uni-mannheim.de/tesseract/?ref=nanonets.com).

## Usage
* Run the script, with -h for help to find the right usage, for instance:
```python main.py -h```
* When the app run select the area you want to snip or click any where to snip whole screen, then the text will be copied to your clipboard!
* NOTE: if it is the first time you run the script with easyocr it will take a while to download the model, but after that it will be cached and it will be faster.

# A way to run the script without opening the terminal

## Windows
* I added a batch file to run the script without opening the terminal, you can use it by:
1. Add the file to the environment variables.
2. Run the script by typing text-snipper in the run window (Win + R).
* Explanation of the batch file is in the file itself (**REM** is a comment in batch files).