@echo off
REM HanapBahay ML Service - Conda Version
REM Use this if you installed via Anaconda/Miniconda

echo ========================================
echo HanapBahay ML Service (Conda)
echo ========================================

cd /d "%~dp0"

REM Set API key
set HANAPBAHAY_API_KEY=hanapbahay_ml_local_2024

echo Activating conda environment...
call conda activate hanapbahay

if %errorLevel% neq 0 (
    echo.
    echo ERROR: Could not activate conda environment
    echo Please run these commands first:
    echo   conda create -n hanapbahay python=3.11 -y
    echo   conda activate hanapbahay
    echo   conda install -c conda-forge scikit-learn pandas numpy joblib -y
    echo   pip install fastapi uvicorn[standard] pydantic python-multipart
    echo.
    pause
    exit /b 1
)

echo Starting ML service on http://127.0.0.1:8000
echo Press Ctrl+C to stop
echo.

python app.py

pause
