@echo off
echo [STOPPING STALE PROCESSES]
taskkill /F /IM python.exe /T 2>nul
taskkill /F /IM streamlit.exe /T 2>nul

echo [INSTALLING DEPENDENCIES - PLEASE WAIT]
C:\Python314\python.exe -m pip install spacy==3.7.5 pydantic==1.10.15 streamlit google-generativeai python-docx pdfplumber python-dotenv
if %ERRORLEVEL% NEQ 0 (
    echo "Pip Install Failed. Installing with --user..."
    C:\Python314\python.exe -m pip install --user spacy==3.7.5 pydantic==1.10.15 streamlit google-generativeai python-docx pdfplumber python-dotenv
)

echo [DOWNLOADING SPACY MODEL]
C:\Python314\python.exe -m pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.1/en_core_web_sm-3.7.1-py3-none-any.whl
if %ERRORLEVEL% NEQ 0 (
    echo "Model Install Failed. Installing with --user..."
    C:\Python314\python.exe -m pip install --user https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.1/en_core_web_sm-3.7.1-py3-none-any.whl
)


cd /d "%~dp0.."

echo [STARTING APPLICATION]
C:\Python314\python.exe -m streamlit run app/ui/main.py
