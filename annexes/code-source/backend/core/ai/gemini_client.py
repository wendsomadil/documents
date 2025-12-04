# core/ai/gemini_client.py
import google.generativeai as genai
from config.gemini_config import GeminiConfig
from typing import Optional

class GeminiClient:
    def __init__(self):
        self.model = GeminiConfig.get_model()
        self.chat_session = None
    
    def start_chat(self, history: list = None):
        """Démarre une nouvelle session de chat avec historique optionnel"""
        self.chat_session = self.model.start_chat(history=history or [])
        return self.chat_session
    
    def generate_response(self, prompt: str, context: str = "") -> str:
        """
        Génère une réponse à partir d'un prompt et d'un contexte RAG
        
        Args:
            prompt: Question de l'utilisateur
            context: Contexte récupéré par le système RAG
            
        Returns:
            Réponse générée par Gemini
        """
        # Construction du prompt enrichi
        full_prompt = f"""
Contexte pertinent issu de la base de connaissances :
{context}

---

Question de l'utilisateur :
{prompt}

---

Instructions :
- Base ta réponse UNIQUEMENT sur le contexte fourni
- Si le contexte ne contient pas l'information, dis-le clairement
- Reste factuel et précis
"""
        
        try:
            if self.chat_session:
                response = self.chat_session.send_message(full_prompt)
            else:
                response = self.model.generate_content(full_prompt)
            
            return response.text
        
        except Exception as e:
            print(f"❌ Erreur Gemini : {e}")
            return "Désolé, une erreur est survenue lors de la génération de la réponse."
    
    def count_tokens(self, text: str) -> int:
        """Compte le nombre de tokens dans un texte"""
        return self.model.count_tokens(text).total_tokens
    