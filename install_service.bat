@echo off
REM HanapBahay ML Service - Installation Script
REM This installs the ML service as a Windows service using NSSM

echo ========================================
echo HanapBahay ML Service Installer
echo ========================================
echo.

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: This script must be run as Administrator
    echo Right-click and select "Run as administrator"
    pause
    exit /b 1
)

cd /d "%~dp0"

REM Find Python executable
where python >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: Python not found in PATH
    echo Please install Python 3.9 or higher
    pause
    exit /b 1
)

echo Found Python:
python --version
echo.

REM Install dependencies
echo Installing Python dependencies...
python -m pip install -r requirements.txt
if %errorLevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo Dependencies installed successfully
echo.

REM Check for model files
if not exist "artifacts\model_latest.joblib" (
    echo WARNING: Model file not found!
    echo Please download model artifacts from Colab first
    echo See SETUP_INSTRUCTIONS.md for details
    echo.
    pause
)

echo ========================================
echo Installation Options:
echo ========================================
echo.
echo 1. Run manually (start_service.bat)
echo 2. Install as Windows Service (requires NSSM)
echo.
set /p choice="Enter choice (1 or 2): "

if "%choice%"=="1" (
    echo.
    echo Manual installation complete!
    echo Run start_service.bat to start the ML service
    pause
    exit /b 0
)

if "%choice%"=="2" (
    REM Check if NSSM exists
    where nssm >nul 2>&1
    if %errorLevel% neq 0 (
        echo.
        echo ERROR: NSSM not found
        echo Download NSSM from https://nssm.cc/download
        echo Extract nssm.exe to a folder in your PATH
        pause
        exit /b 1
    )

    REM Get Python path
    for /f "delims=" %%i in ('where python') do set PYTHON_PATH=%%i
    set APP_PATH=%~dp0app.py

    echo.
    echo Installing Windows service...
    nssm install HanapBahayML "%PYTHON_PATH%" "%APP_PATH%"
    nssm set HanapBahayML AppDirectory "%~dp0"
    nssm set HanapBahayML AppEnvironmentExtra HANAPBAHAY_API_KEY=hanapbahay_ml_local_2024

    echo Starting service...
    nssm start HanapBahayML

    echo.
    echo Service installed and started successfully!
    echo.
    echo Service management commands:
    echo   nssm start HanapBahayML
    echo   nssm stop HanapBahayML
    echo   nssm restart HanapBahayML
    echo   nssm remove HanapBahayML confirm
    echo.
    pause
    exit /b 0
)

echo Invalid choice
pause
exit /b 1
