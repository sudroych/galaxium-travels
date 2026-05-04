#!/bin/bash

# Galaxium Travels - Start Script
# Starts both backend and frontend servers

echo "🚀 Starting Galaxium Travels..."
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    exit 1
fi

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Shutting down servers..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

trap cleanup SIGINT SIGTERM

# Start Backend
echo -e "${BLUE}📡 Starting Backend Server...${NC}"
cd booking_system_backend

# Check if virtual environment exists, create if not
if [ ! -d ".venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment and install dependencies
source .venv/bin/activate
pip install -q -r requirements.txt

# Start backend server in background
python server.py &
BACKEND_PID=$!
cd ..

echo -e "${GREEN}✅ Backend started on http://localhost:8000${NC}"
echo ""

# Wait a moment for backend to start
sleep 2

# Start Frontend
echo -e "${BLUE}🎨 Starting Frontend Server...${NC}"
cd booking_system_frontend

# Install dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install
fi

# Start frontend server in background
npm run dev &
FRONTEND_PID=$!
cd ..

echo -e "${GREEN}✅ Frontend started on http://localhost:5173${NC}"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🌟 Galaxium Travels is running!"
echo ""
echo "   Backend:  http://localhost:8000"
echo "   Frontend: http://localhost:5173"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all servers"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID

# Made with Bob
