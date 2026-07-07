"""
config.py
---------
Toutes les constantes du projet au même endroit : noms des modèles,
chemins de fichiers. Le but : si on veut changer de modèle, on ne
modifie qu'ici, jamais dans le code métier.
"""

# Modèle d'embedding (encodage des phrases en vecteurs).
# Multilingue et léger, comme demandé dans le sujet.
EMBEDDING_MODEL_NAME = "distiluse-base-multilingual-cased-v2"

# Modèle de génération (le LLM qui répond à la question), comme demandé
# dans le sujet.
# NOTE (à mentionner si besoin) : Groq a annoncé le 17/06/2026 la
# dépréciation de ce modèle, avec un arrêt effectif prévu le 16/08/2026.
# Il fonctionne donc normalement pour l'instant. Si jamais il ne répond
# plus après cette date, remplacer par "openai/gpt-oss-120b".
GENERATION_MODEL_NAME = "llama-3.3-70b-versatile"

# Modèle de modération (détection de prompt injection).
# NOTE : la famille "llama-guard" a été dépréciée le 05/03/2026 en faveur
# de "openai/gpt-oss-safeguard-20b", qui est la famille "safeguard"
# actuelle chez Groq (llama-guard n'est donc plus accessible du tout).
MODERATION_MODEL_NAME = "openai/gpt-oss-safeguard-20b"

# Chemin où ChromaDB persiste sa base sur le disque
CHROMA_PERSIST_PATH = "./chroma_db"

# Nom de la collection ChromaDB
COLLECTION_NAME = "corpus_rag"

# Fichier CSV source du corpus (phrases absurdes)
CORPUS_CSV_PATH = "./05_corpus_rag.csv"

# Nombre de chunks à récupérer à chaque question
TOP_K_CHUNKS = 3
