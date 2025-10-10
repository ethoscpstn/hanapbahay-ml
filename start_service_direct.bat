@echo off
REM Start ML Service using direct Python path (no conda activation needed)
REM EDIT THE PYTHON_PATH BELOW WITH YOUR ACTUAL PATH

echo ========================================
echo HanapBahay ML Service (Direct Mode)
echo ========================================
echo.

cd /d "%~dp0"

REM ============================================================
REM EDIT THIS PATH - Find your path by running: find_python_path.bat
REM ============================================================
set "PYTHON_PATH=%USERPROFILE%\miniconda3\envs\hanapbahay\python.exe"

REM Check if Python exists
if not exist "%PYTHON_PATH%" (
    echo ERROR: Python not found at: %PYTHON_PATH%
    echo.
    echo Run find_python_path.bat to get the correct path
    echo Then edit this file and update PYTHON_PATH variable
    pause
    exit /b 1
)

REM Set API key
set HANAPBAHAY_API_KEY=hanapbahay_ml_local_2024

echo Using Python: %PYTHON_PATH%
echo Starting ML service on http://127.0.0.1:8000
echo Press Ctrl+C to stop
echo.

REM Run the service
"%PYTHON_PATH%" app.py

pause
