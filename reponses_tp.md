# Réponses – Section 6 : Mise à l'épreuve

## 1. Qui intercepte cette entrée, et à quel moment exact du pipeline ?

La tentative de prompt injection est interceptée par l'agent modérateur. La question est analysée dès son entrée dans le système, avant toute recherche dans la base vectorielle ChromaDB et avant tout appel au modèle de génération Groq. Si une tentative d'injection est détectée, le pipeline est interrompu et le LLM principal n'est pas sollicité.

## 2. Que se passerait-il sans agent modérateur ?

Sans l'agent modérateur, les questions seraient directement envoyées au pipeline RAG. Le modèle de génération recevrait alors les tentatives de prompt injection et pourrait produire des réponses non conformes aux consignes du système. Le modérateur constitue donc une première couche de sécurité.

## 3. Le système respecte-t-il la consigne de dire qu'il ne sait pas pour une question hors corpus ?

Oui. Lors du test avec la question « Quelle est la capitale du Japon ? », le système indique qu'il ne dispose d'aucune information pertinente dans les documents indexés et répond qu'il ne sait pas, conformément aux consignes du prompt.

## 4. Le comportement prévu se déclenche-t-il en cas de contradiction ?

Oui. Lors du test avec l'affirmation « Le chat de Bob est vert », le système détecte la contradiction avec les informations présentes dans la base de connaissances. Il corrige l'utilisateur en indiquant que le chat de Bob s'appelle Henri et qu'il est bleu, conformément aux données du corpus.
