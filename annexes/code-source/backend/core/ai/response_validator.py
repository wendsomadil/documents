# core/ai/response_validator.py
import re
from typing import Tuple

class ResponseValidator:
    """Valide les réponses avant envoi à l'utilisateur"""
    
    # Mots-clés interdits ou nécessitant validation
    SENSITIVE_KEYWORDS = [
        "investir tout votre argent",
        "prêt garanti",
        "risque zéro",
        "riche rapidement",
    ]
    
    FORBIDDEN_PATTERNS = [
        r"je te recommande d'investir dans",  # Conseils d'investissement non autorisés
        r"ton mot de passe est",              # Fuite de données sensibles
    ]
    
    @staticmethod
    def validate_response(response: str, user_query: str) -> Tuple[bool, str]:
        """
        Valide une réponse générée par l'IA
        
        Returns:
            (is_valid, validated_response or error_message)
        """
        # Vérification des mots-clés sensibles
        response_lower = response.lower()
        for keyword in ResponseValidator.SENSITIVE_KEYWORDS:
            if keyword in response_lower:
                return False, "⚠️ Cette réponse contient des informations sensibles non validées."
        
        # Vérification des patterns interdits
        for pattern in ResponseValidator.FORBIDDEN_PATTERNS:
            if re.search(pattern, response_lower):
                return False, "⚠️ Réponse potentiellement inappropriée détectée."
        
        # Vérification de la cohérence financière
        if not ResponseValidator._check_financial_coherence(response):
            return False, "⚠️ Incohérence financière détectée dans la réponse."
        
        return True, response
    
    @staticmethod
    def _check_financial_coherence(response: str) -> bool:
        """Vérifie la cohérence des informations financières"""
        # Exemple : Vérifier que les montants mentionnés sont réalistes
        amounts = re.findall(r'(\d+(?:,\d+)?)\s*(?:FCFA|francs)', response)
        
        for amount in amounts:
            amount_int = int(amount.replace(',', ''))
            if amount_int > 10_000_000_000:  # 10 milliards FCFA
                return False  # Montant irréaliste
        
        return True
    
    @staticmethod
    def add_disclaimer(response: str, query_type: str = "general") -> str:
        """Ajoute un disclaimer si nécessaire"""
        disclaimers = {
            "financial_advice": "\n\n⚠️ *Ceci est une information générale, pas un conseil financier personnalisé.*",
            "transaction": "\n\n💡 *Pour toute question spécifique, contactez notre support.*"
        }
        
        return response + disclaimers.get(query_type, "")
    