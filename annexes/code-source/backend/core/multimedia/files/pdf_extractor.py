# core/multimedia/files/pdf_extractor.py
import PyPDF2
from pathlib import Path

class PDFExtractor:
    @staticmethod
    def extract_text(pdf_path: str) -> str:
        """
        Extrait tout le texte d'un PDF
        
        Returns:
            Texte extrait du PDF
        """
        try:
            text = ""
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                for page_num, page in enumerate(pdf_reader.pages):
                    page_text = page.extract_text()
                    text += f"\n\n--- Page {page_num + 1} ---\n{page_text}"
            
            return text.strip()
        
        except Exception as e:
            print(f"❌ Erreur extraction PDF : {e}")
            return ""
    
    @staticmethod
    def get_metadata(pdf_path: str) -> dict:
        """Extrait les métadonnées d'un PDF"""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                metadata = pdf_reader.metadata
                
                return {
                    "title": metadata.get("/Title", "Inconnu"),
                    "author": metadata.get("/Author", "Inconnu"),
                    "num_pages": len(pdf_reader.pages),
                }
        except:
            return {}
        