"""
build_index.py
---------------
À exécuter UNE SEULE FOIS (ou après avoir supprimé le dossier chroma_db/)
pour créer la base vectorielle à partir du fichier CSV du corpus.

Usage : python build_index.py
"""

import csv
import config
from vector_db import VectorDB


def charger_chunks_depuis_csv(chemin_csv):
    chunks = []
    with open(chemin_csv, encoding="utf-8") as f:
        lecteur = csv.DictReader(f)
        for ligne in lecteur:
            chunks.append({
                "id": ligne["id"],
                "text": ligne["text"],
                "source": ligne.get("source", ""),
                "categorie": ligne.get("categorie", ""),
            })
    return chunks


if __name__ == "__main__":
    print("Lecture du corpus CSV...")
    chunks = charger_chunks_depuis_csv(config.CORPUS_CSV_PATH)
    print(f"{len(chunks)} chunks trouvés.")

    VectorDB(
        persist_path=config.CHROMA_PERSIST_PATH,
        collection_name=config.COLLECTION_NAME,
        embedding_model_name=config.EMBEDDING_MODEL_NAME,
        chunks=chunks,
    )
    print("Index créé avec succès dans", config.CHROMA_PERSIST_PATH)
