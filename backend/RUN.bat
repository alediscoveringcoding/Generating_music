@echo off
REM AI Music Generator - Quick Backend Startup
REM Activates venv and runs FastAPI server

echo.
echo ========================================
echo   AI Music Generator - Backend
echo ========================================
echo.

cd /d "%~dp0"

REM Check if venv exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate venv and start backend
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing dependencies...
pip install -q -r requirements.txt

echo.
echo ========================================
echo Backend running at http://127.0.0.1:8000
echo API Docs: http://127.0.0.1:8000/docs
echo ========================================
echo.

python main.py
pause
