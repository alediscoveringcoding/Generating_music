# AI Music Generator - START ALL
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$BackendDir = Join-Path $ScriptDir "backend"
$FrontendDir = Join-Path $ScriptDir "frontend"

Write-Host "`n🎵 AI MUSIC GENERATOR`n" -ForegroundColor Cyan

# Start Backend
Write-Host "🚀 Starting Backend..." -ForegroundColor Green
$PythonExe = Join-Path $BackendDir "venv314\Scripts\python.exe"
Start-Process -WorkingDirectory $BackendDir -FilePath $PythonExe -ArgumentList "main.py"

Start-Sleep -Seconds 2

# Start Frontend
Write-Host "🚀 Starting Frontend..." -ForegroundColor Green
Start-Process -WorkingDirectory $FrontendDir -FilePath "python" -ArgumentList "-m http.server 5500"

Write-Host "`n✅ STARTED!" -ForegroundColor Green
Write-Host "Frontend: http://localhost:5500" -ForegroundColor Yellow
Write-Host "Backend:  http://localhost:8000" -ForegroundColor Yellow
Write-Host "API Docs: http://localhost:8000/docs`n" -ForegroundColor Yellow
