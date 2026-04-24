@echo off
REM KAB Bank - Supabase Backend Setup Script for Windows

echo.
echo ============================================================
echo KAB Banking System - Supabase Setup
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

echo [1/4] Checking Python installation...
python --version

echo.
echo [2/4] Installing dependencies...
pip install -r requirements_supabase.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo [3/4] Checking for .env file...
if not exist .env (
    echo Creating .env from .env.example...
    copy .env.example .env
    echo.
    echo WARNING: .env file created, but you MUST edit it with your Supabase credentials!
    echo.
    echo Steps:
    echo 1. Open .env in a text editor
    echo 2. Go to https://supabase.com and create a project
    echo 3. Copy SUPABASE_URL and SUPABASE_KEY from Settings ^> API
    echo 4. Paste them into .env file
    echo 5. Save and close
    echo.
    pause
) else (
    echo .env file found
)

echo.
echo [4/4] Starting server...
echo.
echo ============================================================
echo Server starting at http://localhost:5000
echo ============================================================
echo.
echo Press Ctrl+C to stop the server
echo.

python server_supabase.py

pause
