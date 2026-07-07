from rag import RAG


if __name__ == "__main__":

    print(
        "Initialisation du RAG..."
    )

    rag = RAG()

    print(
        "Prêt ! Tape 'quit' pour quitter.\n"
    )


    while True:

        question = input(
            "Ta question : "
        ).strip()


        if question.lower() in (
            "quit",
            "exit"
        ):
            break


        if not question:
            continue


        reponse = rag.answer_question(
            question
        )


        print(
            "\n>>",
            reponse,
            "\n"
        )