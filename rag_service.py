## "fastapi dev main.py" to launch the server  

import ollama

from processor import collection


def generer_reponse(question):

    # Recherche des chunks pertinents dans ChromaDB
    resultats = collection.query(query_texts=[question], n_results=5)
    chunks = resultats['documents'][0]
    texte = "\n\n".join(chunks)

    response = ollama.chat(
        model="llama3.1:8b",
        messages=[
            {
                "role": "user",
                "content": (
                    "Tu es l'assistant virtuel de SRM Agadir. Réponds à la question "
                    "en te basant uniquement sur les informations ci-dessous, mais "
                    "réponds directement et naturellement, comme si tu connaissais "
                    "l'information toi-même. Ne dis jamais des choses comme "
                    "\"d'après le texte\", \"selon le document\" ou \"le contexte "
                    "indique que\" — parle simplement comme un assistant qui répond "
                    "à un client. Si l'information n'est pas disponible ci-dessous, "
                    "dis que tu ne disposes pas de cette information et invite "
                    "l'utilisateur à contacter le service client SRM Agadir.\n\n"
                    f"Informations disponibles :\n{texte}\n\n"
                    f"Question du client : {question}"
                )
            }
        ]
    )

    return response['message']['content']