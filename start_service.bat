@echo off
REM HanapBahay ML Service Startup Script
REM Run this to start the local Python ML service

echo ========================================
echo HanapBahay ML Service
echo ========================================

REM Change to script directory
cd /d "%~dp0"

REM Set API key (change this for production security)
set HANAPBAHAY_API_KEY=hanapbahay_ml_local_2024

REM Optional: Set database connection if you want to train models locally
REM set DB_TYPE=mysql
REM set DB_HOST=localhost
REM set DB_PORT=3306
REM set DB_NAME=u412552698_dbhanapbahay
REM set DB_USER=root
REM set DB_PASS=yourpassword

echo Starting ML service on http://127.0.0.1:8000
echo Press Ctrl+C to stop
echo.

REM Start the service
python app.py

pause
