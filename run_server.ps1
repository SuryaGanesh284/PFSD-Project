# Indian Constitution Learning Platform - Development Server Startup (PowerShell)
# This script starts the Django development server

# Check if virtual environment exists
if (-not (Test-Path "venv\Scripts\Activate.ps1")) {
    Write-Host "Error: Virtual environment not found!" -ForegroundColor Red
    Write-Host "Please run setup first" -ForegroundColor Yellow
    exit 1
}

# Activate virtual environment
& "venv\Scripts\Activate.ps1"

# Start development server
Write-Host "Starting Django development server..." -ForegroundColor Green
Write-Host "Access the application at: http://127.0.0.1:8000/" -ForegroundColor Cyan
Write-Host "Admin panel at: http://127.0.0.1:8000/admin/" -ForegroundColor Cyan
Write-Host "Admin credentials: username=admin, password=(set during first login)" -ForegroundColor Yellow
Write-Host ""

python manage.py runserver

# Pause to keep console open
Read-Host "Press Enter to exit"
