#!/usr/bin/env pwsh

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   AI Music Generator - Backend" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$BackendDir = $PSScriptRoot
$VenvPath = Join-Path $BackendDir "venv"

# Check if venv exists
if (-not (Test-Path $VenvPath)) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv $VenvPath
}

# Activate venv
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& "$VenvPath\Scripts\Activate.ps1"

Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -q -r requirements.txt

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Backend running at http://127.0.0.1:8000" -ForegroundColor Green
Write-Host "API Docs: http://127.0.0.1:8000/docs" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

python main.py
