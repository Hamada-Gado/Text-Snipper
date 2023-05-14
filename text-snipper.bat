@echo off

REM This line is used to run the python file with the arguments passed to it but minimize the command prompt window
if not DEFINED IS_MINIMIZED set IS_MINIMIZED=1 && start "Text Snipper" /min "%~dpnx0" %* && exit

REM Change the path to the project directory if it is in different driver change to that driver first
F:
cd "F:\GitHub Repos\Text-Snipping"

REM Call python.exe of the virtual environment if using one or just python.exe
REM The second argument is the name of the python file to run
REM The %* are the arguments to pass to the python file
REM you can add more arguments if you want to pass them to the python file without typing them when calling the batch file
REM Example: python.exe main.py tesseract -g %*
python.exe main.py %*

REM Pause the command prompt window if the program exited with an error
if not %ERRORLEVEL%==0 pause

exit