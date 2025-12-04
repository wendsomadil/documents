# core/rag/retriever.py
from core.rag.vector_store import VectorStore
from core.rag.embeddings import EmbeddingGenerator

class ContextRetriever:
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store
        self.embedding_generator = EmbeddingGenerator()
    
    def retrieve_context(self, user_query: str, top_k: int = 5) -> str:
        """
        Recherche et formate le contexte pertinent pour l'IA
        
        Args:
            user_query: Question de l'utilisateur
            top_k: Nombre de documents à retourner
            
        Returns:
            Contexte formaté pour injection dans le prompt
        """
        # Génération de l'embedding de la requête
        query_embedding = self.embedding_generator.generate_query_embedding(user_query)
        
        # Recherche des documents pertinents
        results = self.vector_store.search(query_embedding, k=top_k)
        
        # Formatage du contexte
        context_parts = []
        for i, result in enumerate(results, 1):
            context_parts.append(f"""
Document {i} (Pertinence: {1 / (1 + result['score']):.2f}):
Source: {result['metadata'].get('source', 'Inconnu')}
Contenu: {result['document']}
---
            """)
        
        return "\n".join(context_parts) if context_parts else "Aucun contexte trouvé."
    
    def retrieve_with_filtering(self, user_query: str, category: str = None) -> str:
        """Recherche avec filtrage par catégorie"""
        # Logique de filtrage par métadonnées
        pass
    