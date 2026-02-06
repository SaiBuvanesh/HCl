import os
import ollama
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class LLMService:
    def __init__(self):
        self.local_model = "mistral" 
        self.reasoning_model = "deepseek-r1" # Default thinking model
        self.active_model = None
        self.is_offline = False
        self.provider = "ollama" # 'ollama' or 'gemini'
        self.gemini_model = None
        self.available_models = []

        # 1. Check for Google Gemini
        self.gemini_available = False
        self.gemini_model_name = None
        api_key = os.getenv("GOOGLE_API_KEY")
        if api_key:
            try:
                genai.configure(api_key=api_key)
                
                # Dynamic Model Selection
                chosen_model = None
                try:
                    for m in genai.list_models():
                        if 'generateContent' in m.supported_generation_methods:
                            # Prefer flash or pro
                            if 'flash' in m.name:
                                chosen_model = m.name
                                break
                            elif 'pro' in m.name and not chosen_model:
                                chosen_model = m.name
                    
                    if not chosen_model:
                         # Fallback to first available if no preference met
                         for m in genai.list_models():
                            if 'generateContent' in m.supported_generation_methods:
                                chosen_model = m.name
                                break
                except:
                    chosen_model = 'gemini-1.5-flash' # Hard fallback

                print(f"LLM Service: Gemini Available - {chosen_model}")
                self.gemini_model = genai.GenerativeModel(chosen_model)
                self.gemini_model_name = chosen_model
                self.gemini_available = True
            except Exception as e:
                print(f"Gemini Connection Error: {e}")
        
        # 2. Check Local Availability (Always check, don't skip)
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
                
                print(f"LLM Service: Ollama Available - {len(self.available_models)} models")
            else:
                print("LLM Service: No Ollama models found.")
        except Exception as e:
            print(f"Ollama Error: {e}")
        
        # 3. Set default provider based on what's available
        if self.gemini_available:
            self.provider = "gemini"
            self.active_model = self.gemini_model_name
            self.is_offline = False
            print(f"LLM Service: Using Gemini by default ({self.active_model})")
        elif self.available_models:
            self.provider = "ollama"
            self.active_model = self.local_model
            self.is_offline = False
            print(f"LLM Service: Using Ollama by default ({self.active_model})")
        else:
            self.provider = None
            self.active_model = "No LLM Available"
            self.is_offline = True
            print("LLM Service: No LLM available.")

    def switch_provider(self, provider="gemini"):
        """Switch between gemini and ollama providers"""
        if provider == "gemini" and self.gemini_available:
            self.provider = "gemini"
            self.active_model = self.gemini_model_name
            self.is_offline = False
        elif provider == "ollama" and hasattr(self, 'available_models') and self.available_models:
            self.provider = "ollama"
            self.active_model = self.local_model
            self.is_offline = False
        else:
            print(f"Cannot switch to {provider} - not available")
    
    def set_mode(self, mode="standard"):
        """Switches between Standard and Reasoning models (Ollama only)"""
        if self.provider == "gemini":
            return # Gemini handles everything for now
            
        if mode == "reasoning":
            self.active_model = self.reasoning_model
        else:
            self.active_model = self.local_model

    def _call_llm(self, prompt):
        """Unified method to call the active LLM provider."""
        if self.is_offline:
            raise Exception("AI is offline.")

        if self.provider == "gemini":
            try:
                response = self.gemini_model.generate_content(prompt)
                return response.text
            except Exception as e:
                return f"Gemini Error: {str(e)}"
        else:
            # Ollama
            try:
                response = ollama.chat(model=self.active_model, messages=[
                    {'role': 'user', 'content': prompt},
                ])
                return response['message']['content']
            except Exception as e:
                return f"Ollama Error: {str(e)}"

    def explain_clause(self, text, context="business"):
        """
        Explains a legal clause.
        """
        if self.is_offline:
            return "AI Offline: Enable Cloud API or local Ollama."

        prompt = f"Explain this legal clause in simple {context} terms for a non-lawyer. If the text is in Hindi, translate and explain in English. Max 2 sentences. Clause: {text}"
        
        return self._call_llm(prompt)

    def analyze_risk_depth(self, clause_text, risk_type):
        """
        Deep dive into risk with actionable advice.
        """
        if self.is_offline:
            return "AI Offline: Enable Cloud API or local Ollama."

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
        
        return self._call_llm(prompt)
            
    def generate_document_summary(self, full_text):
        """
        Generates a comprehensive yet simple summary of the entire document.
        """
        if self.is_offline:
            return "AI Summary Unavailable."
            
        # Truncate to avoid context limit issues 
        # Gemini 1.5 has large context window, but good to be safe. Ollama depends on model.
        MAX_CHARS = 30000 if self.provider == "gemini" else 12000
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
        return self._call_llm(prompt)

    def generate_summary(self, high_risks):
        if self.is_offline:
            return "AI Summary Unavailable."
            
        prompt = (
            f"Generate a strategic executive summary for a business owner based on these identified risks: {high_risks}\n"
            "Structure:\n"
            "- **Executive Overview**: 1 sentence overall assessment.\n"
            "- **Key Risks**: 3 bullet points highlighting critical issues.\n"
            "- **Negotiation Strategy**: 1 piece of advice for the next meeting."
        )
        return self._call_llm(prompt)

    def chat_with_document(self, query, document_text):
        """
        Interactive Q&A with the document context.
        """
        if self.is_offline:
            return "AI Offline: Enable Cloud API or local Ollama."

        # Truncate context
        MAX_CHARS = 30000 if self.provider == "gemini" else 4000
        safe_context = document_text[:MAX_CHARS]
        
        prompt = (
            f"Context: {safe_context}\n\n"
            f"User Question: {query}\n"
            "Instructions: Input may be in Hindi or English. Always answer in English.\n"
            "You are an expert Indian Corporate Lawyer. precise, professional, and helpful.\n"
            "Answer the question based strictly on the provided contract context above.\n"
            "If the information is not in the contract, say so. Cite specific clauses if possible."
        )
        
        return self._call_llm(prompt)

# Singleton instance
llm_service = LLMService()
