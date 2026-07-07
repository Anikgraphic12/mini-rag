# Mini RAG - Master 2 MD5

## Description

Ce projet est une implémentation d'un système **Retrieval-Augmented Generation (RAG)** réalisée dans le cadre du mini-TP du Master 2 MD5.

Le système repose sur :

* ChromaDB pour la base vectorielle persistante
* Sentence Transformers pour les embeddings
* Groq comme modèle de génération
* Un agent de modération détectant les tentatives de prompt injection

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

## Installation

Créer un environnement virtuel :

```bash
python -m venv venv
```

Activation sous Windows :

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

## Construction de la base vectorielle

```bash
python build_index.py
```

Cette commande crée la base ChromaDB persistante à partir du corpus CSV.

## Lancement

```bash
python main.py
```

## Fonctionnalités

* Recherche sémantique dans une base vectorielle
* Génération de réponses avec Groq
* Refus des prompt injections
* Refus des questions hors corpus
* Détection des contradictions avec la base de connaissances

## Technologies utilisées

* Python 3.11
* ChromaDB
* Sentence Transformers
* Groq API
* python-dotenv
* Pandas
