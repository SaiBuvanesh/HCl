@echo off
echo ========================================
echo Starting Ngrok Tunnel for Ollama
echo ========================================
echo.
echo This will expose your local Ollama to the internet
echo so Streamlit Cloud can access it.
echo.
echo IMPORTANT: Keep this window open!
echo.
echo ========================================

REM Start ngrok tunnel to Ollama port
d:\HCL\ngrok\ngrok.exe http 11434

pause
