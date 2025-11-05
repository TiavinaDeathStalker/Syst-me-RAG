from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import PyPDF2
import os

app = FastAPI()

origins = ["http://localhost:8080"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "data"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Si c'est un PDF, extraire le texte
    text = ""
    if file.filename.endswith(".pdf"):
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() + "\n"

    return {"status": "uploaded", "text_preview": text[:500]}  # renvoie un aperçu

@app.post("/ask")
async def ask(payload: dict):
    # Exemple simple : juste répondre avec le texte du PDF si question contient un mot clé
    question = payload.get("question", "")
    # Ici tu pourrais implémenter une recherche simple dans le texte
    return {"answer": f"Vous avez demandé : '{question}' (traitement futur du texte du PDF)"}
