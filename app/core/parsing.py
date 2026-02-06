import re
from typing import List, Dict, Any

class ClauseParser:
    """
    Parses raw contract text into structured clauses.
    """
    
    # Common clause patterns
    CLAUSE_PATTERNS = [
        r"^\s*(\d{1,2}\.\d{1,2}(\.\d{1,2})?)\s+(.+)",  # 1.1, 1.1.1
        r"^\s*(\d{1,2}\.)\s+(.+)",                      # 1.
        r"^\s*(Article\s+[IVX]+)\s*[:\.-]?\s*(.+)",    # Article I
        r"^\s*([a-z]\))\s+(.+)",                        # a) - usually sub-clause
        r"^\s*(\([a-z]\))\s+(.+)"                       # (a)
    ]

    @staticmethod
    def parse(text: str) -> List[Dict[str, Any]]:
        """
        Splits text into clauses.
        Returns a list of dicts: {'id': '1.1', 'text': '...'}
        """
        lines = text.split('\n')
        clauses = []
        current_clause = {"id": "Intro", "text": "", "type": "preamble"}
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            match = ClauseParser._match_clause_start(line)
            if match:
                # Save previous clause if it has content
                if current_clause['text']:
                    clauses.append(current_clause)
                
                # Start new clause
                clause_id = match[0]
                content = match[1]
                current_clause = {
                    "id": clause_id,
                    "text": content,
                    "type": "clause"
                }
            else:
                # Append to current clause
                current_clause["text"] += " " + line
        
        # Add final clause
        if current_clause['text']:
            clauses.append(current_clause)
            
        # FALLBACK: If regex found nothing (or only intro)
        if len(clauses) <= 1:
            # Strategy 1: Double Newlines (Paragraphs)
            raw_paragraphs = [p.strip() for p in text.split('\n\n') if len(p.strip()) > 20]
            
            # Strategy 2: Single Newlines (Lines)
            if not raw_paragraphs:
                 raw_paragraphs = [p.strip() for p in text.split('\n') if len(p.strip()) > 10]
            
            # Strategy 3: Just take the text as one big chunk if it's short
            if not raw_paragraphs and len(text) > 10:
                raw_paragraphs = [text]

            if raw_paragraphs:
                clauses = [] # Reset
                for i, para in enumerate(raw_paragraphs, 1):
                    clauses.append({
                        "id": f"Section {i}",
                        "text": para,
                        "type": "clause"
                    })
            
        return clauses

    @staticmethod
    def _match_clause_start(line: str):
        """
        Checks if a line starts with a clause identifier.
        """
        for pattern in ClauseParser.CLAUSE_PATTERNS:
            match = re.match(pattern, line, re.IGNORECASE)
            if match:
                # Return tuple (ID, Remaining Text)
                # Some patterns have 1 group (Article), others 2 (1.1 Text)
                # This logic simplifies extraction
                groups = match.groups()
                # Remove None groups
                groups = [g for g in groups if g]
                
                if len(groups) >= 2:
                    return groups[0], groups[-1] # ID, Text
        return None
