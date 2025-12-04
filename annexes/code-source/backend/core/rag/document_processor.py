# core/rag/document_processor.py
from typing import List, Dict
import re

class DocumentProcessor:
    def __init__(self, chunk_size: int = 500, overlap: int = 50):
        """
        Args:
            chunk_size: Taille maximale d'un chunk en tokens
            overlap: Chevauchement entre chunks pour préserver le contexte
        """
        self.chunk_size = chunk_size
        self.overlap = overlap
    
    def chunk_text(self, text: str) -> List[str]:
        """
        Découpe un texte en chunks de taille optimale
        
        Stratégie :
        1. Découpe par paragraphes
        2. Si un paragraphe > chunk_size, découpe par phrases
        3. Ajoute un overlap entre chunks
        """
        # Nettoyage du texte
        text = self.clean_text(text)
        
        # Découpe par paragraphes
        paragraphs = text.split('\n\n')
        
        chunks = []
        current_chunk = ""
        
        for para in paragraphs:
            # Si le paragraphe est petit, l'ajouter au chunk actuel
            if len(current_chunk.split()) + len(para.split()) < self.chunk_size:
                current_chunk += "\n\n" + para
            else:
                # Sauvegarder le chunk actuel
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = para
        
        # Ajouter le dernier chunk
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def clean_text(self, text: str) -> str:
        """Nettoie le texte des caractères indésirables"""
        # Suppression des espaces multiples
        text = re.sub(r'\s+', ' ', text)
        # Suppression des caractères spéciaux
        text = re.sub(r'[^\w\s\.\,\;\:\!\?\-\n]', '', text)
        return text.strip()
    
    def extract_metadata(self, text: str, source: str) -> Dict:
        """Extrait les métadonnées d'un document"""
        return {
            "source": source,
            "length": len(text.split()),
            "first_words": " ".join(text.split()[:10]),
        }
        