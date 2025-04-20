from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from llama_cpp import Llama
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import os
import shutil
from fastapi.middleware.cors import CORSMiddleware

# --- Load Models ---
llm = Llama(
    model_path=r"C:\\Users\\A.Akshita\\rag-legal-chatbot\\models\\mistral-7b-instruct-v0.2.Q4_K_M.gguf",
    n_ctx=8192,
    chat_format="mistral-instruct"
)
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

# --- Embedding directory ---
EMBEDDING_DIR = "embeddings"
TEXT_DIR = "extracted_text"
INDEX_PATH = os.path.join(EMBEDDING_DIR, "faiss.index")
FILE_LIST_PATH = os.path.join(EMBEDDING_DIR, "files.txt")

# --- Load FAISS ---
def load_faiss_index():
    global index, file_names
    index = faiss.read_index(INDEX_PATH)
    with open(FILE_LIST_PATH, "r") as f:
        file_names = f.read().splitlines()

# --- Save embeddings after new upload ---
def regenerate_index():
    all_files = []
    all_texts = []

    os.makedirs(TEXT_DIR, exist_ok=True)
    os.makedirs(EMBEDDING_DIR, exist_ok=True)

    for file in os.listdir(TEXT_DIR):
        if file.endswith(".txt"):
            with open(os.path.join(TEXT_DIR, file), "r", encoding="utf-8") as f:
                text = f.read()
                if text.strip():
                    all_files.append(file)
                    all_texts.append(text)

    embeddings = embed_model.encode(all_texts, convert_to_numpy=True).astype("float32")
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    faiss.write_index(index, INDEX_PATH)

    with open(FILE_LIST_PATH, "w", encoding="utf-8") as f:
        for file in all_files:
            f.write(file + "\n")

    load_faiss_index()

load_faiss_index()

# --- FastAPI Setup ---
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    query: str

def get_top_k_chunks(query, k=3):
    query_vec = embed_model.encode(query).astype("float32").reshape(1, -1)
    D, I = index.search(query_vec, k)
    chunks = []
    for i in I[0]:
        file_path = os.path.join(TEXT_DIR, file_names[i])
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                chunks.append(f.read())
    return chunks

def ask_legal_bot(query, max_tokens=100, max_prompt_tokens=7000):
    docs = get_top_k_chunks(query)
    combined = ""
    clause_refs = []

    for doc in docs:
        temp = combined + doc + "\n---\n"
        token_count = len(llm.tokenize(temp.encode("utf-8")))
        if token_count < max_prompt_tokens:
            combined = temp
            # Attempt to extract clause numbers
            for line in doc.split("\n"):
                if any(clause in line.lower() for clause in ["section", "clause"]):
                    clause_refs.append(line.strip())
        else:
            break

    system_prompt = "You are a helpful legal assistant. Include relevant clause or section numbers from the document in your response."
    user_prompt = f"""Read the following legal documents and answer the question.

Documents:
{combined}

Question: {query}
Answer:"""

    output = llm.create_chat_completion(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        max_tokens=max_tokens,
        temperature=0.7
    )

    answer = output["choices"][0]["message"]["content"].strip()

    if clause_refs:
        answer += "\n\n📌 Referenced Clauses:\n" + "\n".join(clause_refs[:3])

    return answer

@app.post("/ask")
def ask(query: Query):
    answer = ask_legal_bot(query.query)
    return {"answer": answer}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    os.makedirs(TEXT_DIR, exist_ok=True)
    file_path = os.path.join(TEXT_DIR, file.filename)

    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    regenerate_index()
    return {"message": f"{file.filename} uploaded and indexed successfully."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

