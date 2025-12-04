# services/chat_service.py
from core.rag.knowledge_base import KnowledgeBase
from core.rag.retriever import ContextRetriever
from core.ai.gemini_client import GeminiClient
from core.ai.context_manager import ContextManager
from core.ai.response_validator import ResponseValidator
from core.security.content_filter import ContentFilter
from database.repositories.message_repository import MessageRepository
from typing import Dict

class ChatService:
    def __init__(self):
        # Initialisation des composants
        self.knowledge_base = KnowledgeBase()
        self.retriever = ContextRetriever(self.knowledge_base.vector_store)
        self.gemini_client = GeminiClient()
        self.context_manager = ContextManager()
        self.message_repo = MessageRepository()
    
    async def process_message(
        self, 
        user_id: str, 
        message: str, 
        session_id: str
    ) -> Dict:
        """
        Traite un message utilisateur de bout en bout
        
        Returns:
            {
                "response": str,
                "sources": List[Dict],
                "message_id": str
            }
        """
        # 1. Filtrage de sécurité
        is_safe, reason = ContentFilter.is_safe(message)
        if not is_safe:
            return {
                "response": f"⚠️ Message bloqué : {reason}",
                "sources": [],
                "message_id": None
            }
        
        # 2. Ajout du message utilisateur à l'historique
        self.context_manager.add_message("user", message)
        
        # 3. Recherche RAG de contexte pertinent
        context = self.retriever.retrieve_context(message, top_k=5)
        
        # 4. Génération de la réponse par Gemini
        response = self.gemini_client.generate_response(message, context)
        
        # 5. Validation de la réponse
        is_valid, validated_response = ResponseValidator.validate_response(
            response, message
        )
        
        if not is_valid:
            validated_response = "Je ne peux pas fournir cette réponse. Contactez le support."
        
        # 6. Ajout de la réponse à l'historique
        self.context_manager.add_message("assistant", validated_response)
        
        # 7. Sauvegarde en base de données
        message_id = await self.message_repo.save_message(
            user_id=user_id,
            session_id=session_id,
            user_message=message,
            bot_response=validated_response,
            context_used=context
        )
        
        return {
            "response": validated_response,
            "sources": self._extract_sources(context),
            "message_id": str(message_id)
        }
    
    def _extract_sources(self, context: str) -> List[Dict]:
        """Extrait les sources depuis le contexte RAG"""
        # Parse le contexte pour extraire les sources
        # Format attendu : "Source: <nom_fichier>"
        import re
        sources = re.findall(r'Source: (.+)', context)
        return [{"source": s.strip()} for s in sources]
    