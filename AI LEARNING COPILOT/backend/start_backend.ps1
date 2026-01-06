# CodeCore AI Backend Startup Script
# Run this script to start the backend server

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  CodeCore AI Backend Starting..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Change to backend directory
Set-Location $PSScriptRoot
Write-Host "[OK] Working directory: $PSScriptRoot" -ForegroundColor Green

# Check if .env file exists
if (Test-Path ".env") {
    Write-Host "[OK] .env file found" -ForegroundColor Green
}
else {
    Write-Host "[ERROR] .env file not found!" -ForegroundColor Red
    Write-Host "  Please create .env file with GEMINI_API_KEY" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "Starting FastAPI server..." -ForegroundColor Yellow
Write-Host "Backend URL: http://127.0.0.1:8000" -ForegroundColor Cyan
Write-Host "API Docs: http://127.0.0.1:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Gray
Write-Host ""

# Start uvicorn
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
