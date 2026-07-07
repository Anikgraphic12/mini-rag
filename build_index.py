"""
build_index.py
--------------

Création d'une base vectorielle RAG à partir d'un vrai document PDF.

Pipeline :
PDF
 -> extraction du texte
 -> découpage en chunks
 -> génération des embeddings
 -> stockage dans ChromaDB
"""

from pathlib import Path
from pypdf import PdfReader

import config
from vector_db import VectorDB


PDF_PATH = "./documents/reglement_bordeaux.pdf"


def extraire_texte_pdf(pdf_path):
    """
    Extrait le texte page par page du PDF.
    Retourne une liste de pages avec leurs métadonnées.
    """

    reader = PdfReader(pdf_path)

    pages = []

    for numero_page, page in enumerate(reader.pages):
        texte = page.extract_text()

        if texte:
            pages.append({
                "page": numero_page + 1,
                "text": texte,
            })

    return pages


def decouper_en_chunks(pages, taille_chunk=500, overlap=100):
    """
    Découpe le document en morceaux avec chevauchement.

    Le chevauchement évite de perdre le contexte
    entre deux chunks.
    """

    chunks = []

    compteur = 0

    for page in pages:

        texte = page["text"]

        debut = 0

        while debut < len(texte):

            fin = debut + taille_chunk

            morceau = texte[debut:fin]

            chunks.append({
                "id": f"chunk_{compteur}",
                "text": morceau,
                "source": PDF_PATH,
                "categorie": "reglement_universite",
                "page": page["page"],
            })

            compteur += 1

            debut += taille_chunk - overlap

    return chunks


if __name__ == "__main__":

    print("Lecture du règlement PDF...")

    pages = extraire_texte_pdf(PDF_PATH)

    print(f"{len(pages)} pages extraites.")

    chunks = decouper_en_chunks(pages)

    print(f"{len(chunks)} chunks créés.")

    VectorDB(
        persist_path=config.CHROMA_PERSIST_PATH,
        collection_name=config.COLLECTION_NAME,
        embedding_model_name=config.EMBEDDING_MODEL_NAME,
        chunks=chunks,
    )

    print("Base vectorielle créée avec succès.")