"""
moderator.py
------------
Brique 3 : l'agent modérateur.

Avant toute chose, on demande à un modèle spécialisé (dédié à la sécurité)
si la question de l'utilisateur est une tentative de prompt injection.

Pourquoi un modèle DÉDIÉ plutôt que d'ajouter "refuse les injections" dans
le prompt du RAG lui-même ? Parce qu'un seul prompt qui doit à la fois
répondre aux questions ET se défendre contre les attaques est plus facile
à contourner (l'attaquant n'a qu'un seul système à tromper). En séparant
les deux rôles, l'attaquant doit tromper deux modèles indépendants, et le
modèle de modération n'a qu'une seule tâche = il est plus fiable dessus.
"""

import json
from pathlib import Path


class Moderator:
    def __init__(self, groq_client, model_name, prompt_path="prompts/moderator_prompt.txt"):
        self.client = groq_client
        self.model_name = model_name
        self.system_prompt = Path(prompt_path).read_text(encoding="utf-8")

    def moderate(self, question):
        """
        Interroge le modèle de modération et retourne un dict
        {"is_prompt_injection": True/False}
        """
        reponse = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": question},
            ],
            response_format={"type": "json_object"},  # force une sortie JSON
        )

        contenu_json = reponse.choices[0].message.content

        try:
            resultat = json.loads(contenu_json)
        except json.JSONDecodeError:
            # Sécurité : si le modèle ne renvoie pas un JSON valide,
            # on considère par prudence que ce n'est PAS une injection
            # (on ne bloque pas l'utilisateur à cause d'une erreur technique),
            # mais on log l'anomalie.
            print(f"[Moderator] Réponse JSON invalide reçue : {contenu_json}")
            resultat = {"is_prompt_injection": False}

        return resultat
