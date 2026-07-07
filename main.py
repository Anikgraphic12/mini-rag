"""
main.py
-------
Point d'entrée en ligne de commande.
Lance une boucle où on peut poser des questions au RAG.

Usage : python main.py
(assure-toi d'avoir lancé build_index.py au moins une fois avant)
"""

from rag import RAG

if __name__ == "__main__":
    print("Initialisation du RAG (chargement des modèles, connexion Groq)...")
    rag = RAG()
    print("Prêt ! Tape 'quit' pour quitter.\n")

    while True:
        question = input("Ta question : ").strip()
        if question.lower() in ("quit", "exit"):
            break
        if not question:
            continue

        reponse = rag.answer_question(question)
        print(f"\n>> {reponse}\n")
