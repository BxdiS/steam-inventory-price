@echo off
python --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo Python is not installed or not in PATH.
    echo Please install Python 3.9+ from https://www.python.org/downloads/
    pause
    exit /b
)

echo Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt

echo Running script...
python main.py
pause
