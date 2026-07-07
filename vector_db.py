"""
vector_db.py
------------
Brique 1 : la base vectorielle persistante.
"""

import chromadb
from sentence_transformers import SentenceTransformer


class VectorDB:

    def __init__(
        self,
        persist_path,
        collection_name,
        embedding_model_name=None,
        chunks=None
    ):

        self.client = chromadb.PersistentClient(
            path=persist_path
        )

        try:
            self.collection = self.client.get_collection(
                name=collection_name
            )
            base_existe_deja = self.collection.count() > 0

        except Exception:
            self.collection = None
            base_existe_deja = False


        if base_existe_deja:

            meta = self.collection.metadata or {}

            modele = meta.get(
                "embedding_model",
                embedding_model_name
            )

            print(
                f"[VectorDB] Base existante rechargée. "
                f"Modèle : {modele}"
            )

            self.embedding_model = SentenceTransformer(modele)


        elif chunks:

            if not embedding_model_name:
                raise ValueError(
                    "embedding_model_name obligatoire"
                )

            self.embedding_model = SentenceTransformer(
                embedding_model_name
            )


            self.collection = self.client.get_or_create_collection(
                name=collection_name,
                metadata={
                    "embedding_model": embedding_model_name
                }
            )


            textes = [
                c["text"]
                for c in chunks
            ]

            ids = [
                c["id"]
                for c in chunks
            ]


            metadatas = [
                {
                    "source": c.get("source", ""),
                    "categorie": c.get("categorie", ""),
                    "page": c.get("page", "")
                }
                for c in chunks
            ]


            print(
                f"[VectorDB] Encodage de {len(textes)} chunks..."
            )


            vecteurs = self.embedding_model.encode(
                textes,
                batch_size=32,
                normalize_embeddings=True,
                show_progress_bar=True,
            )


            self.collection.add(
                ids=ids,
                documents=textes,
                embeddings=vecteurs.tolist(),
                metadatas=metadatas,
            )


            print(
                "[VectorDB] Base créée et indexée avec succès."
            )


        else:

            raise ValueError(
                "Aucune base existante et aucun chunk fourni."
            )


    def retrieve(self, question, n=3):

        vecteur_question = self.embedding_model.encode(
            [question],
            normalize_embeddings=True,
        )


        resultats = self.collection.query(
            query_embeddings=vecteur_question.tolist(),
            n_results=n,
            include=[
                "documents",
                "metadatas",
                "distances"
            ],
        )


        chunks_trouves = []


        documents = resultats["documents"][0]
        metadonnees = resultats["metadatas"][0]
        distances = resultats["distances"][0]


        for doc, meta, distance in zip(
            documents,
            metadonnees,
            distances
        ):

            chunks_trouves.append(
                {
                    "text": doc,
                    "source": meta.get("source", ""),
                    "categorie": meta.get("categorie", ""),
                    "page": meta.get("page", ""),
                    "distance": distance,
                }
            )


        return chunks_trouves