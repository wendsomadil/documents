# core/rag/vector_store.py
import faiss
import numpy as np
import pickle
from pathlib import Path

class VectorStore:
    def __init__(self, dimension: int = 768):
        """
        Initialise le vector store FAISS
        
        Args:
            dimension: Dimension des embeddings (768 pour Gemini)
        """
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.documents = []  # Liste des documents originaux
        self.metadata = []   # Métadonnées associées
    
    def add_documents(self, embeddings: np.ndarray, documents: list, metadata: list):
        """Ajoute des documents vectorisés à l'index"""
        self.index.add(embeddings.astype('float32'))
        self.documents.extend(documents)
        self.metadata.extend(metadata)
        print(f"✅ {len(documents)} documents ajoutés à l'index")
    
    def search(self, query_embedding: np.ndarray, k: int = 5) -> list:
        """
        Recherche les k documents les plus similaires
        
        Returns:
            Liste de tuples (document, score, metadata)
        """
        distances, indices = self.index.search(
            query_embedding.reshape(1, -1).astype('float32'), 
            k
        )
        
        results = []
        for idx, dist in zip(indices[0], distances[0]):
            if idx != -1:  # Index valide
                results.append({
                    "document": self.documents[idx],
                    "score": float(dist),
                    "metadata": self.metadata[idx]
                })
        
        return results
    
    def save(self, path: str):
        """Sauvegarde l'index sur disque"""
        faiss.write_index(self.index, f"{path}/index.faiss")
        with open(f"{path}/documents.pkl", "wb") as f:
            pickle.dump({"documents": self.documents, "metadata": self.metadata}, f)
    
    def load(self, path: str):
        """Charge l'index depuis le disque"""
        self.index = faiss.read_index(f"{path}/index.faiss")
        with open(f"{path}/documents.pkl", "rb") as f:
            data = pickle.load(f)
            self.documents = data["documents"]
            self.metadata = data["metadata"]
