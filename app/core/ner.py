import re
from typing import Dict, List

class EntityExtractor:
    
    # Simple Regex Patterns for "Lite" extraction
    PATTERNS = {
        "MONEY": [
            r"Rs\.?\s*[\d,]+(\.\d{2})?",
            r"INR\s*[\d,]+",
            r"\$\s*[\d,]+"
        ],
        "DATE": [
            r"\d{1,2}(?:st|nd|rd|th)?\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[\s,]+\d{2,4}",
            r"\d{1,2}[\/\.-]\d{1,2}[\/\.-]\d{2,4}",
            r"(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}"
        ],
        "ORG": [
            r"(?i)(?:private limited|pvt\.? ltd\.?|limited|ltd\.?|inc\.?|corp\.?|llp|services)"  # Basic heuristic
        ],
        "JURISDICTION": [
             r"(?i)courts? (?:of|in) [A-Z][a-z]+"
        ]
    }

    @staticmethod
    def extract_entities(text: str) -> Dict[str, List[str]]:
        entities = {
            "ORG": [],
            "PERSON": [], # Hard via regex without NLP model
            "DATE": [],
            "MONEY": [],
            "GPE": [] 
        }
        
        for label, patterns in EntityExtractor.PATTERNS.items():
            for pat in patterns:
                matches = re.finditer(pat, text)
                for match in matches:
                    val = match.group(0).strip()
                    # Map to output keys
                    key = label if label in entities else "GPE" # Fallback
                    if label == "JURISDICTION": key = "GPE"
                    
                    if val not in entities[key]:
                        entities[key].append(val)
                    
        return entities
