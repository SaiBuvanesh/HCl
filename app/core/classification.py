class ClauseClassifier:
    
    PATTERNS = {
        "Obligation": ["shall", "must", "will", "is required to", "agrees to"],
        "Prohibition": ["shall not", "must not", "will not", "is prohibited from", "agrees not to"],
        "Right": ["may", "has the right to", "is entitled to", "can"]
    }

    @staticmethod
    def classify(text: str) -> str:
        """
        Determines the legal nature of the clause.
        """
        text_lower = text.lower()
        
        # Check Prohibitions first (negative logic)
        for term in ClauseClassifier.PATTERNS["Prohibition"]:
            if term in text_lower:
                return "Prohibition"
                
        # Check Obligations
        for term in ClauseClassifier.PATTERNS["Obligation"]:
            if term in text_lower:
                return "Obligation"
                
        # Check Rights
        for term in ClauseClassifier.PATTERNS["Right"]:
            if term in text_lower:
                return "Right"
                
        return "Definition/Neutral"
