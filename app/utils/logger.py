import logging
import json
from datetime import datetime
from pathlib import Path
from app.core.config import DATA_DIR

# Setup Logging Directory
LOG_DIR = DATA_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Configure Logger
logger = logging.getLogger("LegalAuditLog")
logger.setLevel(logging.INFO)

# File Handler for Audit Trail (JSON Lines format)
audit_files_path = LOG_DIR / "audit_trail.jsonl"
file_handler = logging.FileHandler(audit_files_path)
file_formatter = logging.Formatter('%(message)s')
file_handler.setFormatter(file_formatter)

logger.addHandler(file_handler)

def log_audit(action: str, details: dict, user_id: str = "local_user"):
    """
    Logs an action to the audit trail in JSON format.
    """
    entry = {
        "timestamp": datetime.now().isoformat(),
        "user_id": user_id,
        "action": action,
        "details": details
    }
    logger.info(json.dumps(entry))

def get_logger():
    return logger
