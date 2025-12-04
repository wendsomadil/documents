# core/security/content_filter.py
import re
from typing import Tuple

class ContentFilter:
    """Filtre les contenus inappropriés avant traitement"""
    
    # Mots-clés bloqués (en français et anglais)
    BLOCKED_KEYWORDS = [
        # Injures et harcèlement
        "connard", "salope", "pute", "fdp",
        # Tentatives d'injection
        "ignore previous instructions",
        "system prompt",
        "you are now",
        # Demandes inappropriées
        "hack", "pirate", "voler", "frauder",
    ]
    
    # Patterns suspects
    SUSPICIOUS_PATTERNS = [
        r"<script>.*</script>",  # XSS
        r"'; DROP TABLE",         # SQL Injection
        r"\.\.\/\.\.\/",         # Path traversal
    ]
    
    @staticmethod
    def is_safe(user_input: str) -> Tuple[bool, str]:
        """
        Vérifie si un message utilisateur est sûr
        
        Returns:
            (is_safe, reason_if_blocked)
        """
        user_input_lower = user_input.lower()
        
        # Vérification des mots-clés bloqués
        for keyword in ContentFilter.BLOCKED_KEYWORDS:
            if keyword in user_input_lower:
                return False, f"Contenu inapproprié détecté : '{keyword}'"
        
        # Vérification des patterns suspects
        for pattern in ContentFilter.SUSPICIOUS_PATTERNS:
            if re.search(pattern, user_input, re.IGNORECASE):
                return False, "Pattern suspect détecté (sécurité)"
        
        # Vérification de la longueur
        if len(user_input) > 5000:
            return False, "Message trop long (limite : 5000 caractères)"
        
        return True, ""
    
    @staticmethod
    def sanitize_input(user_input: str) -> str:
        """Nettoie et échappe les caractères dangereux"""
        # Suppression des balises HTML
        sanitized = re.sub(r'<[^>]+>', '', user_input)
        
        # Suppression des caractères de contrôle
        sanitized = "".join(char for char in sanitized if ord(char) >= 32 or char == '\n')
        
        return sanitized.strip()
    