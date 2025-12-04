# core/rag/embeddings.py
import google.generativeai as genai
import numpy as np

class EmbeddingGenerator:
    def __init__(self, model_name: str = "models/embedding-001"):
        self.model_name = model_name
    
    def generate_embedding(self, text: str) -> np.ndarray:
        """
        Génère un embedding pour un texte donné
        
        Returns:
            Vecteur numpy de dimension 768
        """
        result = genai.embed_content(
            model=self.model_name,
            content=text,
            task_type="retrieval_document"
        )
        return np.array(result['embedding'])
    
    def generate_query_embedding(self, query: str) -> np.ndarray:
        """Génère un embedding optimisé pour une requête"""
        result = genai.embed_content(
            model=self.model_name,
            content=query,
            task_type="retrieval_query"  # Optimisé pour les requêtes
        )
        return np.array(result['embedding'])
    
    def batch_generate(self, texts: list) -> np.ndarray:
        """Génère des embeddings en batch pour optimiser les performances"""
        embeddings = []
        for text in texts:
            embedding = self.generate_embedding(text)
            embeddings.append(embedding)
        return np.array(embeddings)
