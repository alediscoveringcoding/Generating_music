#!/usr/bin/env pwsh
# ============================================
# AI Music Generator - START ALL SERVICES
# FastAPI Backend + Simple HTTP Server
# ============================================

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   AI MUSIC GENERATOR - START ALL" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$BackendDir = Join-Path $ScriptDir "backend"
$FrontendDir = Join-Path $ScriptDir "frontend"

Write-Host "📁 Project Path: $ScriptDir" -ForegroundColor Yellow
Write-Host ""

# Check if venv exists
$VenvPath = Join-Path $BackendDir "venv"
if (-not (Test-Path $VenvPath)) {
    Write-Host "❌ ERROR: Virtual Environment not found at $VenvPath" -ForegroundColor Red
    Write-Host ""
    Write-Host "Solution:" -ForegroundColor Yellow
    Write-Host "  1. Create venv: python -m venv $VenvPath"
    Write-Host "  2. Then run this script again"
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "✅ Virtual Environment found" -ForegroundColor Green

# Check if main.py exists
$MainPy = Join-Path $BackendDir "main.py"
if (-not (Test-Path $MainPy)) {
    Write-Host "❌ ERROR: Backend main.py not found!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "✅ Backend found" -ForegroundColor Green

# Check if index.html exists
$IndexHtml = Join-Path $FrontendDir "index.html"
if (-not (Test-Path $IndexHtml)) {
    Write-Host "❌ ERROR: Frontend index.html not found!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "✅ Frontend found" -ForegroundColor Green
Write-Host ""

Write-Host "========================================" -ForegroundColor Green
Write-Host "Starting Services..." -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

$PythonExe = Join-Path $VenvPath "Scripts\python.exe"

# Start Backend
Write-Host "🚀 Starting Backend (FastAPI)..." -ForegroundColor Green
Write-Host "   URL: http://localhost:8000" -ForegroundColor Cyan
Write-Host "   API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""

Start-Process -WorkingDirectory $BackendDir -FilePath $PythonExe -ArgumentList "main.py" -WindowStyle Normal -PassThru

Start-Sleep -Seconds 3

# Start Frontend
Write-Host "🚀 Starting Frontend (HTTP Server)..." -ForegroundColor Green
Write-Host "   URL: http://localhost:5500" -ForegroundColor Cyan
Write-Host ""

Start-Process -WorkingDirectory $FrontendDir -FilePath "python" -ArgumentList "-m http.server 5500" -WindowStyle Normal -PassThru

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "✅ SERVICES STARTED!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Frontend:  http://localhost:5500" -ForegroundColor Yellow
Write-Host "Backend:   http://localhost:8000" -ForegroundColor Yellow
Write-Host "API Docs:  http://localhost:8000/docs" -ForegroundColor Yellow
Write-Host ""
Write-Host "Both windows will open automatically..." -ForegroundColor Cyan
Write-Host ""
