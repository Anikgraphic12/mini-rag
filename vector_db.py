"""
vector_db.py
------------
Brique 1 : la base vectorielle persistante.

La classe VectorDB se comporte différemment selon la situation :
- si une base existe déjà sur disque -> elle la recharge
- sinon, si on lui fournit des chunks -> elle la crée
- sinon -> elle refuse de démarrer avec une erreur explicite
"""

import os
import chromadb
from sentence_transformers import SentenceTransformer


class VectorDB:
    def __init__(self, persist_path, collection_name, embedding_model_name=None, chunks=None):
        """
        persist_path        : dossier où ChromaDB stocke ses données sur disque
        collection_name     : nom de la collection à créer/recharger
        embedding_model_name: nom du modèle d'embedding (obligatoire seulement
                               si on CRÉE la base pour la première fois)
        chunks               : liste de dicts {"id":..., "text":..., "source":...}
                               à indexer si la base n'existe pas encore
        """
        # Client persistant : les données survivent à l'arrêt du programme
        self.client = chromadb.PersistentClient(path=persist_path)

        # ATTENTION : PersistentClient crée déjà le dossier et un fichier
        # sqlite dès son instanciation, même s'il n'y a aucune collection
        # dedans. On ne peut donc PAS se fier à l'existence du dossier
        # pour savoir si une base a déjà été indexée : il faut vérifier
        # si la collection existe ET contient réellement des documents.
        try:
            self.collection = self.client.get_collection(name=collection_name)
            base_existe_deja = self.collection.count() > 0
        except Exception:
            self.collection = None
            base_existe_deja = False

        if base_existe_deja:
            # --- CAS 1 : rechargement ---
            # (self.collection a déjà été récupérée ci-dessus)

            # Détail malin : on relit le nom du modèle d'embedding dans les
            # métadonnées de LA COLLECTION elle-même, et pas dans config.py.
            # Pourquoi c'est important : si un jour on change le modèle
            # d'embedding dans config.py sans réindexer, une question serait
            # encodée avec un nouveau modèle alors que les chunks stockés
            # utilisent l'ancien -> les vecteurs ne seraient plus comparables
            # entre eux (dimensions ou espace différents), et ChromaDB
            # renverrait des résultats n'importe quoi SANS lever d'erreur.
            # C'est un bug silencieux, très difficile à diagnostiquer.
            meta = self.collection.metadata or {}
            modele_a_utiliser = meta.get("embedding_model", embedding_model_name)
            print(f"[VectorDB] Base existante rechargée. Modèle d'embedding utilisé : {modele_a_utiliser}")
            self.embedding_model = SentenceTransformer(modele_a_utiliser)

        elif chunks:
            # --- CAS 2 : création ---
            if not embedding_model_name:
                raise ValueError("embedding_model_name est requis pour créer une nouvelle base.")

            self.embedding_model = SentenceTransformer(embedding_model_name)

            # On enregistre le nom du modèle DANS les métadonnées de la
            # collection, pour pouvoir le relire au rechargement.
            self.collection = self.client.get_or_create_collection(
                name=collection_name,
                metadata={"embedding_model": embedding_model_name},
            )

            textes = [c["text"] for c in chunks]
            ids = [c["id"] for c in chunks]
            metadatas = [{"source": c.get("source", ""), "categorie": c.get("categorie", "")} for c in chunks]

            print(f"[VectorDB] Encodage de {len(textes)} chunks...")
            vecteurs = self.embedding_model.encode(
                textes,
                batch_size=32,
                normalize_embeddings=True,  # nécessaire pour comparer par similarité cosinus
                show_progress_bar=True,
            )

            self.collection.add(
                ids=ids,
                documents=textes,
                embeddings=vecteurs.tolist(),
                metadatas=metadatas,
            )
            print("[VectorDB] Base créée et indexée avec succès.")

        else:
            # --- CAS 3 : rien à faire, erreur explicite ---
            raise ValueError(
                "Aucune base existante trouvée à ce chemin, et aucun chunk fourni "
                "pour en créer une nouvelle. Impossible de démarrer."
            )

    def retrieve(self, question, n=3):
        """
        Encode la question avec le même modèle que celui utilisé pour indexer,
        puis interroge ChromaDB pour récupérer les n chunks les plus proches.
        Retourne une liste de dicts {"text":..., "source":..., "categorie":...}
        """
        vecteur_question = self.embedding_model.encode(
            [question],
            normalize_embeddings=True,
        )

        resultats = self.collection.query(
            query_embeddings=vecteur_question.tolist(),
            n_results=n,
        )

        chunks_trouves = []
        documents = resultats["documents"][0]
        metadonnees = resultats["metadatas"][0]

        for doc, meta in zip(documents, metadonnees):
            chunks_trouves.append({
                "text": doc,
                "source": meta.get("source", ""),
                "categorie": meta.get("categorie", ""),
            })

        return chunks_trouves
