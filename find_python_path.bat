@echo off
REM Find the Python path for the hanapbahay environment

echo ========================================
echo Finding Python Path
echo ========================================
echo.

REM Check common locations
set "FOUND=0"

echo Checking common Conda locations...
echo.

if exist "%USERPROFILE%\miniconda3\envs\hanapbahay\python.exe" (
    echo Found: %USERPROFILE%\miniconda3\envs\hanapbahay\python.exe
    set "FOUND=1"
)

if exist "%USERPROFILE%\anaconda3\envs\hanapbahay\python.exe" (
    echo Found: %USERPROFILE%\anaconda3\envs\hanapbahay\python.exe
    set "FOUND=1"
)

if exist "C:\ProgramData\miniconda3\envs\hanapbahay\python.exe" (
    echo Found: C:\ProgramData\miniconda3\envs\hanapbahay\python.exe
    set "FOUND=1"
)

if exist "C:\ProgramData\anaconda3\envs\hanapbahay\python.exe" (
    echo Found: C:\ProgramData\anaconda3\envs\hanapbahay\python.exe
    set "FOUND=1"
)

if "%FOUND%"=="0" (
    echo.
    echo No Python found in common locations.
    echo.
    echo Run this in Anaconda Prompt to find it:
    echo   conda activate hanapbahay
    echo   where python
    echo.
)

echo.
echo ========================================
echo Copy the path above and use it in:
echo   start_service_direct.bat
echo ========================================
pause
