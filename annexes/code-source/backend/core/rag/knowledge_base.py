# core/rag/knowledge_base.py
from pathlib import Path
from typing import List
from core.rag.vector_store import VectorStore
from core.rag.embeddings import EmbeddingGenerator
from core.rag.document_processor import DocumentProcessor

class KnowledgeBase:
    def __init__(self, storage_path: str = "./storage/vector_db"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        self.vector_store = VectorStore()
        self.embedding_generator = EmbeddingGenerator()
        self.document_processor = DocumentProcessor()
        
        # Charger l'index existant si disponible
        if (self.storage_path / "index.faiss").exists():
            self.vector_store.load(str(self.storage_path))
            print("✅ Base de connaissances chargée depuis le disque")
    
    def add_documents_from_files(self, file_paths: List[str]):
        """Ajoute des documents depuis des fichiers"""
        for file_path in file_paths:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                self.add_document(content, source=file_path)
    
    def add_document(self, text: str, source: str):
        """Ajoute un document à la base de connaissances"""
        # Découpage en chunks
        chunks = self.document_processor.chunk_text(text)
        
        # Génération des embeddings
        embeddings = self.embedding_generator.batch_generate(chunks)
        
        # Métadonnées
        metadata = [{"source": source, "chunk_id": i} for i in range(len(chunks))]
        
        # Ajout à l'index
        self.vector_store.add_documents(embeddings, chunks, metadata)
        
        print(f"✅ Document ajouté : {len(chunks)} chunks depuis {source}")
    
    def rebuild_index(self, document_folder: str):
        """Reconstruit complètement l'index depuis un dossier"""
        print("🔄 Reconstruction de l'index...")
        self.vector_store = VectorStore()  # Réinitialisation
        
        doc_files = Path(document_folder).glob("*.txt")
        self.add_documents_from_files([str(f) for f in doc_files])
        
        # Sauvegarde
        self.save()
    
    def save(self):
        """Sauvegarde l'index sur disque"""
        self.vector_store.save(str(self.storage_path))
        print(f"💾 Base de connaissances sauvegardée dans {self.storage_path}")
        