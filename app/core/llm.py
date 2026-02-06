import os
import ollama
from dotenv import load_dotenv

load_dotenv()

class LLMService:
    def __init__(self):
        self.local_model = "mistral" 
        self.reasoning_model = "deepseek-r1" # Default thinking model
        self.active_model = None
        self.is_offline = False
        self.available_models = []
        
        # Check Local Availability
        try:
            models_response = ollama.list()
            
            # Handle response structure (dict vs object)
            if hasattr(models_response, 'models'):
                # Newer ollama library returns an object with .models
                model_list = models_response.models
            else:
                # Older library or raw dict
                model_list = models_response.get('models', [])

            # Extract model names safely
            self.available_models = []
            for m in model_list:
                if hasattr(m, 'model'):
                    self.available_models.append(m.model)
                elif hasattr(m, 'name'):
                    self.available_models.append(m.name)
                elif isinstance(m, dict):
                    self.available_models.append(m.get('model') or m.get('name'))
            
            if self.available_models:
                # Set defaults based on what's available
                # 1. Reasoner
                self.reasoning_model = next((m for m in self.available_models if 'deepseek-r1' in m), "deepseek-r1")
                
                # 2. Standard
                self.local_model = next((m for m in self.available_models if 'mistral' in m or 'llama3' in m or 'llama' in m), self.available_models[0])
                
                self.active_model = self.local_model # Default to standard
                self.is_offline = False
            else:
                self.is_offline = True
        except Exception as e:
            print(f"Ollama Error: {e}")
            self.is_offline = True

    def set_mode(self, mode="standard"):
        """Switches between Standard and Reasoning models"""
        if mode == "reasoning":
            self.active_model = self.reasoning_model
        else:
            self.active_model = self.local_model


    def explain_clause(self, text, context="business"):
        """
        Explains a legal clause.
        """
        if self.is_offline:
            return "AI Offline: Enable Ollama for explanations."

        prompt = f"Explain this legal clause in simple {context} terms for a non-lawyer. If the text is in Hindi, translate and explain in English. Max 2 sentences. Clause: {text}"
        
        try:
            response = ollama.chat(model=self.active_model, messages=[
                {'role': 'user', 'content': prompt},
            ])
            return response['message']['content']
        except:
            return "Error: Local LLM failed."

    def analyze_risk_depth(self, clause_text, risk_type):
        """
        Deep dive into risk with actionable advice.
        """
        if self.is_offline:
            return "AI Offline: Enable Ollama for risk analysis."

        prompt = (
            f"You are a legal expert for Indian SMEs. Analyze this '{risk_type}' clause.\n"
            f"Clause: {clause_text}\n"
            "Note: If the clause is in Hindi, analyze it and provide the response in English.\n\n"
            "Provide a valid response with exactly these three sections:\n"
            "1. **Implication**: What this means for the business owner.\n"
            "2. **Mitigation Strategy**: Specific steps to reduce this risk.\n"
            "3. **Alternative Clause**: A fairer version of this clause that protects the SME.\n"
            "Keep it concise and business-focused."
        )
        
        try:
            response = ollama.chat(model=self.active_model, messages=[
                {'role': 'user', 'content': prompt},
            ])
            return response['message']['content']
        except:
            return "Error: Local LLM failed."
            
    def generate_document_summary(self, full_text):
        """
        Generates a comprehensive yet simple summary of the entire document.
        """
        if self.is_offline:
            return "AI Summary Unavailable (Ollama not running)."
            
        # Truncate to avoid context limit issues (approx 3000 tokens)
        MAX_CHARS = 12000 
        safe_text = full_text[:MAX_CHARS]
        
        prompt = (
            f"Read this contract and explain it to me in plain English, like you are explaining it to a friend.\n"
            f"Text (truncated): {safe_text}\n"
            "Important: If the document is in Hindi, translate the insights and purely output in English.\n\n"
            "Focus on:\n"
            "1. What is this deal actually about?\n"
            "2. Who are the main people/companies involved?\n"
            "3. What are the most important things to watch out for (money, dates, rules)?\n\n"
            "Style Guide:\n"
            "- Use short, simple sentences.\n"
            "- Avoid 'Here is a summary' introduction.\n"
            "- Do not use legal jargon (e.g., instead of 'indemnification', say 'protection against lawsuits').\n"
            "- Write in a natural, conversational flow."
        )
        try:
            response = ollama.chat(model=self.active_model, messages=[
                {'role': 'user', 'content': prompt},
            ])
            return response['message']['content']
        except:
            return "Error generating detailed summary."

    def generate_summary(self, high_risks):
        if self.is_offline:
            return "AI Summary Unavailable (Ollama not running)."
            
        prompt = (
            f"Generate a strategic executive summary for a business owner based on these identified risks: {high_risks}\n"
            "Structure:\n"
            "- **Executive Overview**: 1 sentence overall assessment.\n"
            "- **Key Risks**: 3 bullet points highlighting critical issues.\n"
            "- **Negotiation Strategy**: 1 piece of advice for the next meeting."
        )
        try:
            response = ollama.chat(model=self.active_model, messages=[
                {'role': 'user', 'content': prompt},
            ])
            return response['message']['content']
        except:
            return "Error generating summary."

    def chat_with_document(self, query, document_text):
        """
        Interactive Q&A with the document context.
        """
        if self.is_offline:
            return "AI Offline: Enable Ollama to chat with the document."

        # Truncate context if too long (naive approach, can be improved)
        context_limit = 4000 
        safe_context = document_text[:context_limit]
        
        prompt = (
            f"Context: {safe_context}\n\n"
            f"User Question: {query}\n"
            "Instructions: Input may be in Hindi or English. Always answer in English.\n"
            "You are an expert Indian Corporate Lawyer. precise, professional, and helpful.\n"
            "Answer the question based strictly on the provided contract context above.\n"
            "If the information is not in the contract, say so. Cite specific clauses if possible."
        )
        
        try:
            response = ollama.chat(model=self.active_model, messages=[
                {'role': 'user', 'content': prompt},
            ])
            return response['message']['content']
        except Exception as e:
            return f"Error: {str(e)}"

# Singleton instance
llm_service = LLMService()
