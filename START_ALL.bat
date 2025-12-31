@echo off
REM ============================================
REM   AI Music Generator - START ALL SERVICES
REM   FastAPI Backend + Simple HTTP Server
REM ============================================

setlocal enabledelayedexpansion

color 0B
cls

echo.
echo ========================================
echo   AI MUSIC GENERATOR - START ALL
echo ========================================
echo.

REM Get absolute paths
set SCRIPT_DIR=%~dp0
set BACKEND_DIR=%SCRIPT_DIR%backend
set FRONTEND_DIR=%SCRIPT_DIR%frontend

echo 📁 Project Path: %SCRIPT_DIR%
echo.

REM Check if venv exists
if not exist "%BACKEND_DIR%\venv" (
    echo ❌ ERROR: Virtual Environment not found!
    echo.
    echo Solution:
    echo   1. Create venv: python -m venv %BACKEND_DIR%\venv
    echo   2. Then run this script again
    pause
    exit /b 1
)

echo ✅ Virtual Environment found
echo.

REM Check if backend exists
if not exist "%BACKEND_DIR%\main.py" (
    echo ❌ ERROR: Backend main.py not found!
    pause
    exit /b 1
)

echo ✅ Backend found
echo.

REM Check if frontend exists
if not exist "%FRONTEND_DIR%\index.html" (
    echo ❌ ERROR: Frontend index.html not found!
    pause
    exit /b 1
)

echo ✅ Frontend found
echo.

echo ========================================
echo Starting Services...
echo ========================================
echo.

REM Start Backend in new window
echo 🚀 Starting Backend (FastAPI)...
echo    URL: http://localhost:8000
echo    API Docs: http://localhost:8000/docs
echo.
start "AI Music Generator - Backend" cmd /k cd /d "%BACKEND_DIR%" ^& "%BACKEND_DIR%\venv\Scripts\python.exe" main.py

timeout /t 3 /nobreak

REM Start Frontend in new window
echo 🚀 Starting Frontend (HTTP Server)...
echo    URL: http://localhost:5500
echo.
start "AI Music Generator - Frontend" cmd /k cd /d "%FRONTEND_DIR%" ^& python -m http.server 5500

echo.
echo ========================================
echo ✅ SERVICES STARTED!
echo ========================================
echo.
echo Frontend:  http://localhost:5500
echo Backend:   http://localhost:8000
echo API Docs:  http://localhost:8000/docs
echo.
echo Press any key to close this window...
pause
