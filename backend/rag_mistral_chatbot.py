from llama_cpp import Llama
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load Mistral model from GGUF file
llm = Llama(
    model_path=r"C:\Users\A.Akshita\rag-legal-chatbot\models\mistral-7b-instruct-v0.2.Q4_K_M.gguf",
    n_ctx=8192,
    chat_format="mistral-instruct"
)

# Load MiniLM for embedding
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

# Load FAISS index
index = faiss.read_index("embeddings/faiss.index")
with open("embeddings/files.txt", "r") as f:
    file_names = f.read().splitlines()

# Get top-k most relevant text chunks
def get_top_k_chunks(query, k=3):
    query_vec = embed_model.encode(query).astype("float32").reshape(1, -1)
    D, I = index.search(query_vec, k)
    chunks = []
    for i in I[0]:
        with open(f"extract_text/{file_names[i]}", "r", encoding="utf-8") as f:
            chunks.append(f.read())
    return chunks

# Ask the bot
def ask_legal_bot(query, max_tokens=100, max_prompt_tokens=7000):
    docs = get_top_k_chunks(query)
    
    # Build context safely under token limit
    combined_docs = ""
    for doc in docs:
        temp_combined = combined_docs + doc + "\n---\n"
        token_count = len(llm.tokenize(temp_combined.encode("utf-8")))
        if token_count < max_prompt_tokens:
            combined_docs = temp_combined
        else:
            break

    system_prompt = "You are a helpful and precise legal assistant."
    user_prompt = f"""Read the following legal documents and answer the question.

Documents:
{combined_docs}

Question: {query}
Answer:"""

    # Use chat format (safer + preferred)
    output = llm.create_chat_completion(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        max_tokens=max_tokens,
        temperature=0.7,
    )

    return output["choices"][0]["message"]["content"].strip()

query = "What is the termination clause in these contracts?"
response = ask_legal_bot(query)
print("\n🧠 Legal Bot Answer:\n", response)
