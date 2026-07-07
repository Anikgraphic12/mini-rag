"""
rag.py
------
Brique 2 : le RAG qui orchestre tout.

À l'initialisation : charge le .env, crée le client Groq, instancie le
modérateur, ouvre la base vectorielle (rechargée depuis le disque).

La méthode answer_question() déroule le pipeline complet :
1. Modération de la question (sécurité AVANT tout le reste)
2. Récupération des chunks pertinents
3. Construction du prompt système à trous
4. Appel au LLM de génération
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

import config
from vector_db import VectorDB
from moderator import Moderator


class RAG:
    def __init__(self):
        # 1. Charger les variables d'environnement (.env -> GROQ_API_KEY)
        load_dotenv()
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY introuvable. Vérifie ton fichier .env.")

        # 2. Client Groq
        self.client = Groq(api_key=api_key)

        # 3. Le modérateur
        self.moderator = Moderator(
            groq_client=self.client,
            model_name=config.MODERATION_MODEL_NAME,
        )

        # 4. La base vectorielle (rechargée depuis le disque : on suppose
        # qu'elle a déjà été créée une première fois via build_index.py)
        self.vector_db = VectorDB(
            persist_path=config.CHROMA_PERSIST_PATH,
            collection_name=config.COLLECTION_NAME,
        )

        # 5. Le prompt système "à trous", lu depuis son fichier texte
        self.prompt_template = Path("prompts/rag_prompt.txt").read_text(encoding="utf-8")

    def answer_question(self, question):
        # --- Étape sécurité : AVANT tout appel au LLM principal ---
        moderation = self.moderator.moderate(question)
        if moderation.get("is_prompt_injection"):
            return "⛔ Cette question a été détectée comme une tentative de manipulation du système. Je ne peux pas y répondre."

        # --- Retrieval ---
        chunks = self.vector_db.retrieve(question, n=config.TOP_K_CHUNKS)

        # On formate les chunks trouvés en texte lisible pour le prompt
        texte_chunks = "\n".join(
            f"- {c['text']} (source : {c['source']})" for c in chunks
        )

        # --- Construction du prompt système en remplaçant le marqueur ---
        prompt_final = self.prompt_template.replace("{{Chunks}}", texte_chunks)

        # --- Appel au LLM de génération ---
        reponse = self.client.chat.completions.create(
            model=config.GENERATION_MODEL_NAME,
            messages=[
                {"role": "system", "content": prompt_final},
                {"role": "user", "content": question},
            ],
        )

        return reponse.choices[0].message.content
