import pdfplumber
from langchain_text_splitters import RecursiveCharacterTextSplitter

def extraire_et_chunker(pdf_path, chunk_size=500, chunk_overlap=100):
    
    #Extrait le texte d'un PDF et le découpe en chunks
   
    texte_complet = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            texte = page.extract_text()
            if texte:
                texte_complet += texte + "\n"
    
    print(f"Texte extrait : {len(texte_complet)} caractères")
    
    # Création du splitter
    chunking_model = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    
    # Découpage en chunks
    chunks = chunking_model.split_text(texte_complet)
    
    print(f"{len(chunks)} chunks générés")
    
    return chunks
