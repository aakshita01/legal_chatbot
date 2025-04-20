# 🧠 RAG-Based Legal Chatbot

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-brightgreen)
![React](https://img.shields.io/badge/React-Frontend-blue)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

An intelligent legal assistant that answers questions based on uploaded legal contracts using Retrieval-Augmented Generation (RAG), FAISS similarity search, and a locally hosted Mistral LLM.

---

## 📁 Project Structure

```
RAG-LEGAL-CHATBOT/
├── backend/
│   ├── main.py                  # FastAPI backend with chat + upload endpoints
│   ├── rag_mistral_chatbot.py  # RAG logic (retrieval + generation)
│   ├── extract_text.py         # AWS Textract/local text extraction
│   ├── generate_embedding.py   # FAISS index builder
│   ├── requirements.txt        # Python dependencies
│   ├── embeddings/             # FAISS index + file list
│   ├── extracted_text/         # Extracted legal texts (txt)
│   └── models/                 # LLM .gguf model file
├── frontend/
│   ├── src/
│   │   ├── App.jsx             # Main React UI
│   │   └── App.css             # Styling
│   ├── public/
│   ├── package.json
│   └── vite.config.js

---

## ✨ Features

- 📄 Upload `.txt` legal contracts
- 🔍 Generate embeddings and index them in FAISS
- 🤖 Ask legal questions based on uploaded docs
- 🧠 Uses a local Mistral 7B GGUF model (via llama-cpp-python)
- 💬 Responsive real-time chat interface
- 🌐 FastAPI backend with React frontend

---

## 🖥️ Chatbot Preview

<img width="959" alt="Image" src="https://github.com/user-attachments/assets/3bb20335-ecd8-4813-bd09-85412788dc55" />

---

## 🛠️ Getting Started

### 🧪 Backend (FastAPI + Mistral)

```bash
# Install Python packages
pip install -r requirements.txt

# Run backend
uvicorn main:app --reload
```

> ⛰️ Make sure your GGUF model is present inside `models/` and path is correct in `main.py`

---

### 💻 Frontend (React + Vite)

```bash
cd frontend
npm install
npm run dev
```

Then visit: `http://localhost:5173`

---

## 🤖 Model Used

- **Name:** Mistral 7B Instruct  
- **Format:** GGUF (`.gguf`)  
- **Quantization:** `Q4_K_M`  
- **Loaded with:** llama-cpp-python  

---

## 📦 Uploading a File

- Click **Choose File** and upload `.txt` file
- File is saved and embedded on the backend
- You can now ask legal questions based on that content

---

## 🧠 Sample Q&A

```
Question: Can the contract be terminated early?

Answer: If the provider fails to meet their obligations under the agreement, the recipient may terminate the service...
```

---

## 🚁 Deployment

### Option A: Local  
Run both frontend and backend locally (default).

### Option B: Render + Netlify  
- Backend: Upload to [Render](https://render.com/)
- Frontend: Deploy using [Netlify](https://netlify.com/)  
(Ensure proper `CORS` handling and public APIs)

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

---

## 😋 Author

**Akshita Aluru**  
📧 aakshitareddy@gmail.com  
🌐 [LinkedIn](https://www.linkedin.com/in/akshita-aluru-7664a1217)

