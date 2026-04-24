@echo off
REM Run Supabase Backend for KAB Bank

cd /d "%~dp0"

echo.
echo ============================================================
echo KAB Banking System - Supabase Backend
echo ============================================================
echo.

REM Check if .env exists
if not exist .env (
    echo ERROR: .env file not found!
    echo.
    echo Please create .env file with your Supabase credentials:
    echo 1. Copy .env.example to .env
    echo 2. Edit .env with your Supabase URL and key
    echo 3. Run this script again
    echo.
    pause
    exit /b 1
)

echo Starting server...
echo Server will be available at: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.

python server_supabase.py

pause
