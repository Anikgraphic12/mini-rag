# Mini RAG – Master 2 MD5

## Présentation

Ce projet est une implémentation d'un **Retrieval-Augmented Generation (RAG)** réalisée dans le cadre du mini-TP du Master 2 MD5 – Data & IA.

Le système repose sur une base vectorielle persistante construite avec **ChromaDB**, des embeddings générés par **Sentence Transformers**, un modèle de génération **Groq**, ainsi qu'un agent de modération chargé de détecter les tentatives de prompt injection.

---

## Architecture

```text
Utilisateur
      │
      ▼
Agent modérateur
      │
      ├── Injection détectée → Refus
      │
      ▼
Recherche vectorielle (ChromaDB)
      │
      ▼
Chunks les plus pertinents
      │
      ▼
Groq (LLM)
      │
      ▼
Réponse finale
```

---

## Structure du projet

```text
mini_rag/
├── prompts/
│   ├── moderator_prompt.txt
│   └── rag_prompt.txt
├── .env
├── .gitignore
├── build_index.py
├── config.py
├── main.py
├── moderator.py
├── rag.py
├── vector_db.py
├── requirements.txt
└── 05_corpus_rag.csv
```

---

## Technologies utilisées

* Python 3.11
* ChromaDB
* Sentence Transformers
* Groq API
* python-dotenv
* Pandas

---

## Installation

Créer un environnement virtuel :

```bash
python -m venv venv
```

L'activer sous Windows :

```bash
venv\Scripts\activate
```

Installer les dépendances :

```bash
pip install -r requirements.txt
```

Créer un fichier `.env` contenant :

```text
GROQ_API_KEY=VOTRE_CLE_API
```

---

## Construction de la base vectorielle

Indexer le corpus :

```bash
python build_index.py
```

Cette commande crée une base vectorielle ChromaDB persistante à partir du corpus CSV.

---

## Lancement du projet

```bash
python main.py
```

---

## Fonctionnalités

* Recherche sémantique dans une base vectorielle persistante
* Génération de réponses à partir des documents indexés
* Détection des tentatives de prompt injection
* Refus des questions hors corpus
* Détection des contradictions avec la base de connaissances

---

## Tests réalisés

Le système a été validé avec les scénarios suivants :

* Réponse correcte à une question présente dans le corpus.
* Détection d'une tentative de prompt injection.
* Refus d'une question hors corpus.
* Détection d'une contradiction avec les connaissances indexées.

---

## Auteur

Projet réalisé dans le cadre du Master 2 MD5 – Data & IA.
