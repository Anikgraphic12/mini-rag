import os
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq

import config
from vector_db import VectorDB
from moderator import Moderator


class RAG:

    def __init__(self):

        load_dotenv()

        api_key = os.environ.get(
            "GROQ_API_KEY"
        )

        if not api_key:
            raise ValueError(
                "GROQ_API_KEY introuvable"
            )


        self.client = Groq(
            api_key=api_key
        )


        self.moderator = Moderator(
            groq_client=self.client,
            model_name=config.MODERATION_MODEL_NAME,
        )


        self.vector_db = VectorDB(
            persist_path=config.CHROMA_PERSIST_PATH,
            collection_name=config.COLLECTION_NAME,
        )


        self.prompt_template = Path(
            "prompts/rag_prompt.txt"
        ).read_text(
            encoding="utf-8"
        )



    def answer_question(self, question):


        moderation = self.moderator.moderate(
            question
        )


        if moderation.get(
            "is_prompt_injection"
        ):

            return (
                "⛔ Tentative de prompt injection détectée."
            )


        chunks = self.vector_db.retrieve(
            question,
            n=config.TOP_K_CHUNKS
        )


        if not chunks:

            return (
                "Je n'ai pas trouvé "
                "d'information suffisante."
            )


        sources = "\n\nSources utilisées :\n"

        for c in chunks:

            sources += (
                f"- Page {c['page']} "
                f"(distance : {c['distance']:.3f})\n"
            )


        texte_chunks = "\n".join(
            [
                f"- {c['text']}"
                for c in chunks
            ]
        )


        prompt_final = self.prompt_template.replace(
            "{{Chunks}}",
            texte_chunks
        )


        reponse = self.client.chat.completions.create(
            model=config.GENERATION_MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": prompt_final
                },
                {
                    "role": "user",
                    "content": question
                },
            ],
        )


        return (
            reponse.choices[0].message.content
            + sources
        )