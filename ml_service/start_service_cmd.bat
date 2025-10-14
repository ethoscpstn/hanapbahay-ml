@echo off
REM Start HanapBahay ML Service from CMD (without Anaconda Prompt)
REM This activates conda environment automatically

echo ========================================
echo HanapBahay ML Service
echo ========================================
echo.

cd /d "%~dp0"

REM Find conda installation
set "CONDA_PATH="

REM Check common Anaconda/Miniconda locations
if exist "%USERPROFILE%\miniconda3\Scripts\activate.bat" (
    set "CONDA_PATH=%USERPROFILE%\miniconda3"
)
if exist "%USERPROFILE%\anaconda3\Scripts\activate.bat" (
    set "CONDA_PATH=%USERPROFILE%\anaconda3"
)
if exist "C:\ProgramData\miniconda3\Scripts\activate.bat" (
    set "CONDA_PATH=C:\ProgramData\miniconda3"
)
if exist "C:\ProgramData\anaconda3\Scripts\activate.bat" (
    set "CONDA_PATH=C:\ProgramData\anaconda3"
)

if "%CONDA_PATH%"=="" (
    echo ERROR: Conda not found!
    echo Please install Miniconda or run from Anaconda Prompt
    pause
    exit /b 1
)

echo Found Conda at: %CONDA_PATH%
echo.

REM Set API key
set HANAPBAHAY_API_KEY=hanapbahay_ml_local_2024

REM Activate conda environment and run service
echo Starting ML service on http://127.0.0.1:8000
echo Press Ctrl+C to stop
echo.

call "%CONDA_PATH%\Scripts\activate.bat" hanapbahay
if %errorLevel% neq 0 (
    echo.
    echo ERROR: Could not activate 'hanapbahay' environment
    echo Please make sure you created it with:
    echo   conda create -n hanapbahay python=3.11 -y
    pause
    exit /b 1
)

python app.py

pause
