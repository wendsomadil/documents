# core/ai/context_manager.py
from typing import List, Dict
from datetime import datetime

class ContextManager:
    def __init__(self, max_history: int = 10):
        """
        Args:
            max_history: Nombre maximum de messages à garder en mémoire
        """
        self.max_history = max_history
        self.conversation_history: List[Dict] = []
    
    def add_message(self, role: str, content: str):
        """
        Ajoute un message à l'historique
        
        Args:
            role: 'user' ou 'assistant'
            content: Contenu du message
        """
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        self.conversation_history.append(message)
        
        # Limiter la taille de l'historique
        if len(self.conversation_history) > self.max_history * 2:
            self.conversation_history = self.conversation_history[-self.max_history * 2:]
    
    def get_history_for_gemini(self) -> List[Dict]:
        """
        Formate l'historique pour l'API Gemini
        
        Returns:
            Liste compatible avec start_chat(history=...)
        """
        return [
            {"role": msg["role"], "parts": [msg["content"]]}
            for msg in self.conversation_history
        ]
    
    def get_conversation_summary(self) -> str:
        """Génère un résumé textuel de la conversation"""
        summary = []
        for msg in self.conversation_history[-6:]:  # 3 derniers échanges
            role_display = "👤 Utilisateur" if msg["role"] == "user" else "🤖 Assistant"
            summary.append(f"{role_display}: {msg['content'][:100]}...")
        
        return "\n".join(summary)
    
    def clear_history(self):
        """Réinitialise l'historique"""
        self.conversation_history = []
        