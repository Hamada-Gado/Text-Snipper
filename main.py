from text_snipper import TextSnipper

from sys import argv

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
        args += ["easyocr", "-g"]
        print("WARNING! No model is given.")
        print("Defaulting to easyocr model and -g mode is used.\n")
        print_usage()
        return True
    
    # return if help flag is set or wrong model is given    
    if args[1] not in ["easyocr", "tesseract"]:
        print("ERROR! Wrong model is given.")
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
        if arg not in ["", "-g", "-r", "-t", "-d", "-e", "-o", "-c", "-s"]:
            print("ERROR! Wrong preprocess mode is given.")
            print_usage()
            return False
        
    return True

def main() -> None:
    if check_argv(argv):
        TextSnipper(argv[1], argv[2:]).getTextFromImage()
    
if __name__ == "__main__":
    main()
