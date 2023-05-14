# Text-Snipping

* pip install requirements.txt
* download tesseract.exe if you want to use it's mode, and add it to your path or add it's location to. Download it from [here](https://digi.bib.uni-mannheim.de/tesseract/?ref=nanonets.com).
* copy image to clipboard using any snipping tool, for instance, on windows, use windows + shift + s.
* then run the script, with easyocr or tesseract as an argument, for instance:
```python main.py easyocr```
* the text will be copied to your clipboard!
* NOTE: if it is the first time you run the script with easyocr it will take a while to download the model, but after that it will be cached and it will be fast.