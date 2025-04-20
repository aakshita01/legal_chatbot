import os
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# Load pretrained sentence embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Folder containing extracted .txt documents
folder = "extract_text"
embeddings = []
file_names = []

# Loop through all .txt files and generate embeddings
for file in os.listdir(folder):
    if file.endswith(".txt"):
        with open(os.path.join(folder, file), "r", encoding="utf-8") as f:
            content = f.read()
            if content.strip():  # Ignore empty files
                embedding = model.encode(content)
                embeddings.append(embedding)
                file_names.append(file)

# Convert list to numpy array
embeddings_np = np.array(embeddings).astype("float32")

# Build FAISS index
dimension = embeddings_np.shape[1]  # 384 for MiniLM
index = faiss.IndexFlatL2(dimension)
index.add(embeddings_np)

# Save index and file mapping
os.makedirs("embeddings", exist_ok=True)
faiss.write_index(index, "embeddings/faiss.index")

# Save file name mapping
with open("embeddings/files.txt", "w") as f:
    for name in file_names:
        f.write(name + "\n")

print("✅ FAISS index and file mapping saved!")
