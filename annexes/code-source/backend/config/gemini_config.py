# config/gemini_config.py
import google.generativeai as genai
from config.settings import settings

# Configuration de l'API Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)

class GeminiConfig:
    MODEL_NAME = "gemini-2.0-flash"
    
    # Paramètres de génération
    GENERATION_CONFIG = {
        "temperature": 0.7,          # Créativité modérée
        "top_p": 0.95,              # Diversité des réponses
        "top_k": 40,                # Limitation du vocabulaire
        "max_output_tokens": 1024,  # Longueur maximale de réponse
    }
    
    # Instructions système
    SYSTEM_INSTRUCTION = """
    Tu es l'assistant intelligent de ZamaPay, une plateforme fintech au Burkina Faso.
    
    Règles strictes :
    - Réponds UNIQUEMENT sur les sujets liés à ZamaPay et aux services financiers
    - Si tu ne connais pas la réponse, dis-le clairement
    - Ne fournis JAMAIS de conseils financiers personnalisés non autorisés
    - Reste professionnel, courtois et précis
    - Utilise le français standard
    """
    
    @staticmethod
    def get_model():
        """Retourne une instance configurée du modèle"""
        return genai.GenerativeModel(
            model_name=GeminiConfig.MODEL_NAME,
            generation_config=GeminiConfig.GENERATION_CONFIG,
            system_instruction=GeminiConfig.SYSTEM_INSTRUCTION
        )