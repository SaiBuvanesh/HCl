import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "app" / "data"
UPLOAD_DIR = DATA_DIR / "uploads"
PROCESSED_DIR = DATA_DIR / "processed"

# Create directories if they don't exist
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# Application Settings
APP_NAME = "GenAI Legal Intelligence"
VERSION = "1.0.0"

# NLP Settings
SPACY_MODEL = "en_core_web_sm"

# LLM Settings
LOCAL_MODEL = "mistral" # or qwen2.5:14b
API_MODEL = "gpt-4"

# Risk Levels
RISK_LOW = "Low"
RISK_MEDIUM = "Medium"
RISK_HIGH = "High"

# Supported Extensions
SUPPORTED_EXTENSIONS = ["pdf", "docx", "txt"]
