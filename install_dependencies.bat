@echo off
REM Install ML Service Dependencies (Windows-friendly)

echo ========================================
echo Installing HanapBahay ML Dependencies
echo ========================================
echo.

cd /d "%~dp0"

REM Check Python version
echo Checking Python installation...
python --version
if %errorLevel% neq 0 (
    echo.
    echo ERROR: Python not found!
    echo.
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo.
echo Upgrading pip...
python -m pip install --upgrade pip setuptools wheel

echo.
echo ========================================
echo Installing dependencies...
echo ========================================
echo.

REM Try to install from pre-built wheels (faster, no compilation)
echo [1/9] Installing FastAPI...
python -m pip install --prefer-binary fastapi==0.115.0

echo [2/9] Installing Uvicorn...
python -m pip install --prefer-binary "uvicorn[standard]==0.30.6"

echo [3/9] Installing Pydantic...
python -m pip install --prefer-binary pydantic==2.9.0

echo [4/9] Installing python-multipart...
python -m pip install --prefer-binary python-multipart==0.0.12

echo [5/9] Installing NumPy...
python -m pip install --prefer-binary "numpy>=1.24.0,<2.0.0"

echo [6/9] Installing pandas...
python -m pip install --prefer-binary "pandas>=2.0.0"

echo [7/9] Installing joblib...
python -m pip install --prefer-binary joblib>=1.3.0

echo [8/9] Installing scikit-learn...
python -m pip install --prefer-binary "scikit-learn>=1.3.0"

echo.
echo ========================================
echo Optional: Database Connectors
echo ========================================
echo.
set /p install_db="Install database connectors? (y/n): "

if /i "%install_db%"=="y" (
    echo.
    echo [9/9] Installing database connectors...
    python -m pip install --prefer-binary psycopg2-binary mysql-connector-python
    echo Database connectors installed!
) else (
    echo Skipping database connectors (you can train in Colab)
)

echo.
echo ========================================
echo Installation Summary
echo ========================================
echo.
python -m pip list | findstr /i "fastapi uvicorn pydantic scikit numpy pandas joblib"

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Download model artifacts from Colab
echo 2. Extract to ml_service\artifacts\
echo 3. Run: start_service.bat
echo.
pause
