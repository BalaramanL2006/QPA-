#!/bin/bash
# Question Paper Difficulty Analyzer - Quick Start Script for macOS/Linux

echo ""
echo "========================================"
echo "   Question Paper Difficulty Analyzer"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3.7+ from https://www.python.org/"
    exit 1
fi

echo "[1] Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "Error: Failed to create virtual environment"
    exit 1
fi

echo "[2] Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "Error: Failed to activate virtual environment"
    exit 1
fi

echo "[3] Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Error: Failed to install dependencies"
    exit 1
fi

echo ""
echo "========================================"
echo "   Setup Complete!"
echo "========================================"
echo ""
echo "[4] Starting the application..."
echo ""
echo "The app will open at: http://127.0.0.1:5000"
echo "Press Ctrl+C to stop the server"
echo ""

python3 app.py
