@echo off
REM AI Music Generator - Start Script pentru Windows
REM Porneste automat backend si deschide frontend

echo.
echo ========================================
echo   🎵 AI Music Generator - Startup
echo ========================================
echo.

REM Verifica daca sunt in directorul corect
if not exist "backend\" (
    echo ❌ Error: Executa din root dir ai-music-generator
    pause
    exit /b 1
)

echo ✓ Directoare verificate
echo.

REM Verifica Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python nu gasit. Instaleaza Python 3.14+
    pause
    exit /b 1
)
echo ✓ Python gasit

REM Verifica venv
if not exist "backend\venv\" (
    echo 📦 Creez mediu virtual...
    cd backend
    python -m venv venv
    cd ..
)
echo ✓ Virtual environment exista

echo.
echo ========================================
echo   Pornire Backend (FastAPI)...
echo ========================================
echo.

REM Start backend in nou window
start cmd /k "cd backend && .\venv\Scripts\activate.bat && echo Instaleaza dependente... && pip install -q -r requirements.txt 2>nul && echo. && echo ✓ Backend pornit pe http://127.0.0.1:8000 && echo. && uvicorn main:app --reload --host 127.0.0.1 --port 8000"

echo ✓ Backend window deschis
echo.

REM Asteapta backend sa se porneasca
echo Asteapta 5 secunde sa se porneasca backend...
timeout /t 5 /nobreak

echo.
echo ========================================
echo   Deschidere Frontend
echo ========================================
echo.

REM Deschide frontend in browser
start http://127.0.0.1:5500
echo ✓ Browser deschis pe http://127.0.0.1:5500

echo.
echo ========================================
echo   ✨ Instalare completa!
echo ========================================
echo.
echo 📖 Docs: Citeste README.md pentru detalii
echo 🎹 Start: Alege un gen si apasa Generate
echo 🛑 Stop: Inchide ambele cmd windows
echo.
pause
