@echo off
REM TalentScout Hiring Assistant - Quick Setup Script for Windows
REM This script automates the setup process

echo ========================================
echo TalentScout Hiring Assistant Setup
echo ========================================
echo.

REM Check Python installation
echo [1/5] Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from python.org
    pause
    exit /b 1
)
echo Python found!
echo.

REM Install dependencies
echo [2/5] Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo Dependencies installed successfully!
echo.

REM Check for .env file
echo [3/5] Checking environment configuration...
if not exist .env (
    echo WARNING: .env file not found!
    echo Creating .env from template...
    copy .env.example .env
    echo.
    echo IMPORTANT: Please edit .env file and add your GEMINI_API_KEY
    echo You can get a Gemini API key from: https://makersuite.google.com/app/apikey
    echo.
    pause
)
echo Environment file exists!
echo.

REM Create data directory
echo [4/5] Creating data directories...
if not exist data\candidates mkdir data\candidates
echo Data directories created!
echo.

REM All done
echo [5/5] Setup complete!
echo.
echo ========================================
echo Next Steps:
echo ========================================
echo 1. Edit .env file and add your GEMINI_API_KEY
echo 2. Run the application with: streamlit run app.py
echo 3. Access the chatbot at http://localhost:8501
echo.
echo For more information, see README.md
echo ========================================
pause
