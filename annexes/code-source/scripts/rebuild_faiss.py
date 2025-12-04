# scripts/rebuild_faiss.py
"""
Script de reconstruction de l'index FAISS
À exécuter après ajout/suppression de documents

Usage:
    python scripts/rebuild_faiss.py --docs-folder ./knowledge_base
"""

import sys
sys.path.append('..')

from core.rag.knowledge_base import KnowledgeBase
import argparse

def main():
    parser = argparse.ArgumentParser(description='Reconstruit l\'index FAISS')
    parser.add_argument(
        '--docs-folder',
        type=str,
        required=True,
        help='Dossier contenant les documents (.txt, .pdf)'
    )
    args = parser.parse_args()
    
    print("🔄 Début de la reconstruction de l'index FAISS...")
    
    kb = KnowledgeBase()
    kb.rebuild_index(args.docs_folder)
    
    print("✅ Index reconstruit avec succès !")
    print(f"📁 Sauvegardé dans : {kb.storage_path}")

if __name__ == "__main__":
    main()
    