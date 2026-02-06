from typing import Tuple

class RiskEngine:
    
    # Generic simplistic rules for demo
    RISK_RULES = [
        {"keyword": "terminate without cause", "level": "High", "reason": "Unilateral termination right."},
        {"keyword": "terminate at any time", "level": "High", "reason": "Unilateral termination right."},
        {"keyword": "indemnify", "level": "Medium", "reason": "Potential uncapped liability."},
        {"keyword": "unlimited liability", "level": "High", "reason": "Dangerous financial exposure."},
        {"keyword": "arbitration", "level": "Medium", "reason": "Dispute resolution cost check required."},
        {"keyword": "non-compete", "level": "High", "reason": "Restricts future business opportunities."},
        {"keyword": "exclusivity", "level": "Medium", "reason": "Limits market freedom."}
    ]

    @staticmethod
    def evaluate(text: str) -> Tuple[str, str]:
        """
        Returns (RiskLevel, Reason)
        """
        text_lower = text.lower()
        
        highest_risk = "Low"
        risk_reason = "Standard clause."
        
        # Prioritize High risks
        for rule in RiskEngine.RISK_RULES:
            if rule["keyword"] in text_lower:
                if rule["level"] == "High":
                    return "High", rule["reason"]
                if rule["level"] == "Medium":
                    highest_risk = "Medium"
                    risk_reason = rule["reason"]
        
        return highest_risk, risk_reason
