from app.core.ingestion import DocumentIngestor
from app.core.parsing import ClauseParser
from app.core.ner import EntityExtractor
from app.core.classification import ClauseClassifier
from app.core.risk import RiskEngine
from app.core.llm import llm_service
from app.utils.logger import log_audit

class ContractPipeline:
    
    @staticmethod
    def run(file_obj, file_type: str, enable_ai: bool = False):
        """
        Executes the full analysis pipeline.
        """
        results = {
            "metadata": {"filename": file_obj.name, "type": file_type},
            "entities": {},
            "clauses": [],
            "risk_summary": {"High": 0, "Medium": 0, "Low": 0},
            "ai_summary": "",
            "raw_text_sneak_peek": ""
        }
        
        # 1. Ingestion
        try:
            raw_text = DocumentIngestor.extract(file_obj, file_type)
            results["raw_text_sneak_peek"] = raw_text[:2000] # Capture first 2000 chars
            results["full_text"] = raw_text # Store full text for Q&A
        except Exception as e:
            return {"error": str(e)}
            
        # 2. Parsing
        clauses = ClauseParser.parse(raw_text)
        
        # 3. Global Entity Extraction
        results["entities"] = EntityExtractor.extract_entities(raw_text)
        
        # 4. Clause Analysis
        for clause in clauses:
            # Classification
            clause_type = ClauseClassifier.classify(clause["text"])
            
            # Risk
            risk_level, risk_reason = RiskEngine.evaluate(clause["text"])
            
            # Update Summary
            results["risk_summary"][risk_level] += 1
            
            # Enrich Clause Data
            clause_data = {
                "id": clause["id"],
                "text": clause["text"],
                "type": clause_type,
                "risk": risk_level,
                "risk_reason": risk_reason,
                "explanation": None,
                "remedy": None
            }
            
            # AI Enrichment
            if enable_ai:
                # STRATEGY: Explain EVERYTHING that is not a boring definition
                # This ensures the user "understands" the contract, as requested.
                should_explain = (
                    risk_level in ["High", "Medium"] or 
                    clause_type in ["Obligation", "Prohibition", "Right"] or
                    len(clause["text"].split()) > 30 # Explain long texts too
                )
                
                if should_explain:
                    clause_data["explanation"] = llm_service.explain_clause(clause["text"])
                
                # Risk Analysis remains for High/Medium
                if risk_level in ["High", "Medium"]:
                    clause_data["remedy"] = llm_service.analyze_risk_depth(clause["text"], risk_level)
            
            results["clauses"].append(clause_data)
        
        # Generate Executive Summary if AI is on
        if enable_ai:
            high_risks = [c["risk_reason"] for c in results["clauses"] if c["risk"] == "High"]
            if high_risks:
                results["ai_summary"] = llm_service.generate_summary(high_risks)
            else:
                results["ai_summary"] = "No high-severity risks detected. The contract appears standard based on the configured risk criteria."
            
            # Generate Comprehensive Summary
            results["comprehensive_summary"] = llm_service.generate_document_summary(raw_text)
            
        # Audit Log
        log_audit("Analysis Complete", {
            "filename": file_obj.name, 
            "clause_count": len(clauses),
            "high_risks": results["risk_summary"]["High"],
            "ai_enabled": enable_ai
        })
        
        return results
