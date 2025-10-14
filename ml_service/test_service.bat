@echo off
REM Test the ML service endpoints

echo ========================================
echo HanapBahay ML Service - Test Script
echo ========================================
echo.

set BASE_URL=http://127.0.0.1:8000
set API_KEY=hanapbahay_ml_local_2024

echo Testing ML service at %BASE_URL%
echo.

REM Test 1: Version endpoint (no auth)
echo [1/3] Testing /version endpoint (no auth required)...
curl -s %BASE_URL%/version
echo.
echo.

REM Test 2: Health endpoint (with auth)
echo [2/3] Testing /health endpoint (with auth)...
curl -s -H "X-API-KEY: %API_KEY%" %BASE_URL%/health
echo.
echo.

REM Test 3: Prediction endpoint (with auth)
echo [3/3] Testing /predict endpoint (with auth)...
curl -s -X POST %BASE_URL%/predict ^
  -H "Content-Type: application/json" ^
  -H "X-API-KEY: %API_KEY%" ^
  -d "{\"inputs\":[{\"Capacity\":2,\"Bedroom\":1,\"unit_sqm\":20,\"cap_per_bedroom\":2,\"Type\":\"Apartment\",\"Kitchen\":\"Yes\",\"Kitchen type\":\"Private\",\"Gender specific\":\"Mixed\",\"Pets\":\"Allowed\",\"Location\":\"Quezon City\"}]}"
echo.
echo.

echo ========================================
echo Tests completed!
echo ========================================
echo.
echo If all tests passed, your ML service is working correctly.
echo If tests failed:
echo   1. Make sure the service is running (start_service.bat)
echo   2. Check that model files are in artifacts/
echo   3. Verify Python dependencies are installed
echo.
pause
