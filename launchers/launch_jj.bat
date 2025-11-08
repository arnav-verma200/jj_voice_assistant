@echo off
REM JJ Voice Assistant Launcher with Virtual Environment Support
REM This batch file runs at Windows startup

title JJ Voice Assistant Launcher

REM Change to the script directory
cd /d "%~dp0"

echo ============================================================
echo JJ Voice Assistant - Batch Launcher
echo ============================================================
echo.
echo Current Directory: %CD%
echo.

REM Check if .venv exists and activate it
if exist ".venv\Scripts\python.exe" (
    echo Found virtual environment: .venv
    echo Activating virtual environment...
    echo.
    
    REM Set the virtual environment paths
    set "VIRTUAL_ENV=%CD%\.venv"
    set "PATH=%CD%\.venv\Scripts;%PATH%"
    
    REM Use the venv Python directly
    set "PYTHON_EXE=%CD%\.venv\Scripts\python.exe"
    
    echo Virtual environment activated!
    "%PYTHON_EXE%" --version
    echo Python location: %PYTHON_EXE%
    echo.
    
) else if exist "venv\Scripts\python.exe" (
    echo Found virtual environment: venv
    echo Activating virtual environment...
    echo.
    
    REM Set the virtual environment paths
    set "VIRTUAL_ENV=%CD%\venv"
    set "PATH=%CD%\venv\Scripts;%PATH%"
    
    REM Use the venv Python directly
    set "PYTHON_EXE=%CD%\venv\Scripts\python.exe"
    
    echo Virtual environment activated!
    "%PYTHON_EXE%" --version
    echo Python location: %PYTHON_EXE%
    echo.
    
) else (
    echo WARNING: No virtual environment found (.venv or venv)
    echo Using system Python...
    set "PYTHON_EXE=python"
    echo.
)

REM Check if Python is available
"%PYTHON_EXE%" --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not available
    echo Please create virtual environment with: python -m venv .venv
    echo Then install dependencies with: .venv\Scripts\pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

REM Check if startup_launcher.py exists
if not exist "startup_launcher.py" (
    echo ERROR: startup_launcher.py not found in current directory
    echo Expected location: %CD%\startup_launcher.py
    echo.
    pause
    exit /b 1
)

echo startup_launcher.py found!
echo.

REM Check if main.py exists
if not exist "main.py" (
    echo ERROR: main.py not found in current directory
    echo Expected location: %CD%\main.py
    echo.
    pause
    exit /b 1
)

echo main.py found!
echo.
echo Starting JJ Voice Assistant...
echo ============================================================
echo.

REM Run the launcher using the correct Python
"%PYTHON_EXE%" startup_launcher.py

echo.
echo ============================================================
echo JJ Voice Assistant has closed
echo ============================================================
pause