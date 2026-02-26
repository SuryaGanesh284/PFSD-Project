@echo off
REM Indian Constitution Learning Platform - Development Server Startup
REM This script activates the virtual environment and starts the Django development server

setlocal enabledelayedexpansion

REM Check if virtual environment exists
if not exist venv\Scripts\activate.bat (
    echo Error: Virtual environment not found!
    echo Please run setup first
    pause
    exit /b 1
)

REM Activate virtual environment and start server
call venv\Scripts\activate.bat
python manage.py runserver

pause
