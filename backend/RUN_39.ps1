# Script pentru a rula AI Music Generator cu Python 3.9
# Activează venv39 și pornește backend-ul

Write-Host "🎵 AI Music Generator - Python 3.9 Startup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Activează virtual environment
Write-Host "📦 Activez Python 3.9 virtual environment..." -ForegroundColor Yellow
& "$PSScriptRoot\venv39\Scripts\Activate.ps1"

# Verific versiunea
Write-Host "✅ Python Version:" -ForegroundColor Green
python --version
Write-Host ""

# Pornesc servrul FastAPI
Write-Host "🚀 Porniesc FastAPI Backend..." -ForegroundColor Green
Write-Host "URL: http://localhost:8000" -ForegroundColor Cyan
Write-Host ""

python main.py
