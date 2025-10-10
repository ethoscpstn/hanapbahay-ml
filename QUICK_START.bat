@echo off
REM Quick Start - Install dependencies manually in Command Prompt

echo ========================================
echo HanapBahay ML - Quick Install Guide
echo ========================================
echo.
echo Copy and paste these commands ONE BY ONE into Command Prompt:
echo.
echo ----------------------------------------
echo Step 1: Upgrade pip
echo ----------------------------------------
echo python -m pip install --upgrade pip setuptools wheel
echo.
echo ----------------------------------------
echo Step 2: Install core packages
echo ----------------------------------------
echo python -m pip install fastapi uvicorn pydantic python-multipart joblib
echo.
echo ----------------------------------------
echo Step 3: Install NumPy (pre-compiled)
echo ----------------------------------------
echo python -m pip install numpy
echo.
echo ----------------------------------------
echo Step 4: Install pandas (pre-compiled)
echo ----------------------------------------
echo python -m pip install pandas
echo.
echo ----------------------------------------
echo Step 5: Install scikit-learn (pre-compiled)
echo ----------------------------------------
echo python -m pip install scikit-learn
echo.
echo ----------------------------------------
echo Step 6: Verify installation
echo ----------------------------------------
echo python -c "import sklearn, pandas, numpy, fastapi; print('All packages installed successfully!')"
echo.
echo ========================================
echo.
pause
