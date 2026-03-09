# LLM Router with Retrieval-Augmented Generation (RAG)

A Retrieval-Augmented Generation project that routes user queries by intent and answers using retrieved document context.

## Features
- Document ingestion
- Vector search
- Intent-based routing
- FastAPI backend
- Streamlit frontend

---

## Tech Stack
- Python
- FastAPI
- Streamlit
- FAISS
- LLM API

---

## How to Run

### 1. Clone repo
git clone <repo-url>
cd llm-router-with-rag

### 2. Create virtual environment
python -m venv .venv
.venv\Scripts\activate

### 3. Install dependencies
pip install -r backend/requirements.txt
pip install -r frontend/requirements.txt

### 4. Add environment variables
Create a .env file and add required API keys.

### 5. Run backend
uvicorn backend.main:app --reload

### 6. Run frontend
streamlit run frontend/streamlit_app.py

---

## Current Limitations
- Still under active development
- Error handling and timeout handling need improvement

---

## Future Improvements
- Better retrieval evaluation
- Better UI
- More robust source attribution