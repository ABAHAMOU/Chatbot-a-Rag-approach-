from pathlib import Path
import chromadb
from chunking import extraire_et_chunker


# Connexion à la base de données :

client = chromadb.PersistentClient(path="./srm_db")

# On repart d'une collection vide à chaque reconstruction, pour ne jamais
# garder des chunks issus d'une ancienne version buggée de chunking.py
# (sinon collection.add() ignore silencieusement les IDs déjà présents
# et les anciens chunks restent mélangés aux nouveaux).
try:
    client.delete_collection(name="srm_faq")
except Exception:
    pass  # la collection n'existait pas encore, rien à supprimer
collection = client.get_or_create_collection(name="srm_faq")

# Traitement de tous les PDFs
dossier = "library"

for pdf in Path(dossier).glob("*.pdf"):
    if chunks := extraire_et_chunker(str(pdf)):
        collection.add(
            ids=[f"{pdf.stem}_{i}" for i in range(len(chunks))],
            documents=chunks
        )
        print(f"{pdf.name} : {len(chunks)} chunks ajoutés")