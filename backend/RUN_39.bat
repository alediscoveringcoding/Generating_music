@echo off
REM Script pentru a rula AI Music Generator cu Python 3.9

color 0B
cls

echo.
echo ========================================
echo   AI Music Generator - Python 3.9
echo ========================================
echo.

REM Activează venv39
echo Activez Python 3.9 virtual environment...
call venv39\Scripts\activate.bat

REM Verific versiunea
echo.
echo Python Version:
python --version
echo.

REM Pornesc serverul
echo Porniesc FastAPI Backend...
echo URL: http://localhost:8000
echo.

python main.py

pause
