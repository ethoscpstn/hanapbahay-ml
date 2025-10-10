@echo off
REM Verify ML Service Setup

echo ========================================
echo HanapBahay ML Service - Setup Verification
echo ========================================
echo.

cd /d "%~dp0"

echo [1/4] Checking directory structure...
if exist "app.py" (
    echo   ✓ app.py found
) else (
    echo   ✗ app.py NOT found
)

if exist "artifacts" (
    echo   ✓ artifacts folder exists
) else (
    echo   ✗ artifacts folder NOT found - creating it...
    mkdir artifacts
)

echo.
echo [2/4] Checking model files...
if exist "artifacts\model_latest.joblib" (
    echo   ✓ model_latest.joblib found
    for %%A in ("artifacts\model_latest.joblib") do echo     Size: %%~zA bytes
) else (
    echo   ✗ model_latest.joblib NOT found
    echo     Please download from Colab and extract to artifacts\
)

if exist "artifacts\meta.json" (
    echo   ✓ meta.json found
) else (
    echo   ✗ meta.json NOT found
    echo     Please download from Colab and extract to artifacts\
)

echo.
echo [3/4] Checking Python packages...
call conda activate hanapbahay 2>nul
if %errorLevel% equ 0 (
    echo   ✓ Conda environment 'hanapbahay' activated
    python -c "import sklearn" 2>nul && echo   ✓ scikit-learn installed || echo   ✗ scikit-learn NOT installed
    python -c "import pandas" 2>nul && echo   ✓ pandas installed || echo   ✗ pandas NOT installed
    python -c "import numpy" 2>nul && echo   ✓ numpy installed || echo   ✗ numpy NOT installed
    python -c "import fastapi" 2>nul && echo   ✓ fastapi installed || echo   ✗ fastapi NOT installed
) else (
    echo   ✗ Conda environment 'hanapbahay' not found
    echo     Please create it with: conda create -n hanapbahay python=3.11 -y
)

echo.
echo [4/4] Setup Summary
echo ========================================

if exist "artifacts\model_latest.joblib" if exist "artifacts\meta.json" (
    echo Status: ✓ READY TO START
    echo.
    echo Next step: Run start_service_conda.bat
) else (
    echo Status: ✗ NOT READY
    echo.
    echo Missing model files. Please:
    echo 1. Run the Colab cell to download artifacts
    echo 2. Extract hanapbahay_artifacts.zip
    echo 3. Copy model_latest.joblib and meta.json to:
    echo    %~dp0artifacts\
)

echo.
pause
