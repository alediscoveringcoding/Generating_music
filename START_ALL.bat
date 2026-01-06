@echo off
REM AI Music Generator - START ALL

set SCRIPT_DIR=%~dp0
set BACKEND_DIR=%SCRIPT_DIR%backend
set FRONTEND_DIR=%SCRIPT_DIR%frontend

echo.
echo 🎵 AI MUSIC GENERATOR
echo.

echo 🚀 Starting Backend...
start "Backend" cmd /k cd /d "%BACKEND_DIR%" ^& "%BACKEND_DIR%\venv314\Scripts\python.exe" main.py

timeout /t 2 /nobreak >nul

echo 🚀 Starting Frontend...
start "Frontend" cmd /k cd /d "%FRONTEND_DIR%" ^& python -m http.server 5500

echo.
echo ✅ STARTED!
echo Frontend: http://localhost:5500
echo Backend:  http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
pause
