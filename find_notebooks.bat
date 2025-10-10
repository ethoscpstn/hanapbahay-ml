@echo off
echo ============================================================
echo Finding Notebook Files
echo ============================================================
echo.

cd ..
dir *.ipynb /B /TC /OD

echo.
echo ============================================================
echo Model Information
echo ============================================================
type ml_service\artifacts\meta.json
echo.
echo.
echo ============================================================
echo Summary
echo ============================================================
echo.
echo Your model was created on: 2025-10-09 at 18:40:07 UTC
echo.
echo Compare this with the notebook modification dates above.
echo The notebook last modified BEFORE this time was used.
echo.
pause
