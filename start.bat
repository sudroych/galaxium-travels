@echo off
REM Galaxium Travels - Start Script for Windows
REM Starts both backend and frontend servers

echo.
echo 🚀 Starting Galaxium Travels...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8+ first.
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is not installed. Please install Node.js 18+ first.
    pause
    exit /b 1
)

REM Start Backend
echo 📡 Starting Backend Server...
cd booking_system_backend

REM Check if virtual environment exists, create if not
if not exist ".venv" (
    echo Creating Python virtual environment...
    python -m venv .venv
)

REM Activate virtual environment and install dependencies
call .venv\Scripts\activate.bat
pip install -q -r requirements.txt

REM Start backend server in new window
start "Galaxium Backend" cmd /k "python server.py"
cd ..

echo ✅ Backend started on http://localhost:8000
echo.

REM Wait a moment for backend to start
timeout /t 3 /nobreak >nul

REM Start Frontend
echo 🎨 Starting Frontend Server...
cd booking_system_frontend

REM Install dependencies if node_modules doesn't exist
if not exist "node_modules" (
    echo Installing frontend dependencies...
    call npm install
)

REM Start frontend server in new window
start "Galaxium Frontend" cmd /k "npm run dev"
cd ..

echo ✅ Frontend started on http://localhost:5173
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo 🌟 Galaxium Travels is running!
echo.
echo    Backend:  http://localhost:8000
echo    Frontend: http://localhost:5173
echo    API Docs: http://localhost:8000/docs
echo.
echo Both servers are running in separate windows.
echo Close those windows to stop the servers.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
pause

@REM Made with Bob
