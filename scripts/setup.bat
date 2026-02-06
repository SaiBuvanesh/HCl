@echo off
echo Installing dependencies...
pip install -r requirements.txt

echo Downloading spaCy model...
python -m spacy download en_core_web_sm

echo Setup Complete!
echo Run the app with: streamlit run app/main.py
pause
