# Mini-Poe (Gemini): AI Router + RAG + Agent + Evaluation

A production-style applied AI system inspired by Poe’s architecture.

This project demonstrates:

- Intent-based AI routing
- Retrieval-Augmented Generation (RAG)
- Agentic workflow (plan → retrieve → synthesize)
- LLM-as-judge evaluation
- Observability and logging
- Modular bot abstraction

---

## Why This Project?

Modern AI systems require:

- Multi-bot routing
- Grounded knowledge retrieval
- Hallucination control
- Evaluation and reliability
- End-to-end ownership

This project simulates a simplified version of such a system.

---

## System Architecture

User (Streamlit UI)
↓
FastAPI Backend (/ask)
↓
Intent Classifier
↓
Router
↓
Selected Bot
- Knowledge (RAG)
- Coding
- Summarization
- Research Agent
↓
LLM Response
↓
LLM-as-Judge Evaluation
↓
JSONL Logging


---

## Features

### 1. Intent-Based Routing

User queries are classified into:

- knowledge
- coding
- summarization
- research

Routing enables specialized behavior per task.

---

### 2. Retrieval-Augmented Generation (RAG)

- Documents ingested and chunked
- Embedded using Gemini embeddings
- Indexed in FAISS
- Top-k similarity search at runtime
- Answers include citations

---

### 3. Agentic Workflow (Research Bot)

Research flow:

1. Generate plan
2. Retrieve context
3. Synthesize answer
4. Validate output

---

### 4. Evaluation Layer

LLM-as-judge scoring:

- helpfulness (1–10)
- correctness (1–10)
- hallucination_risk (1–10)
- short_feedback

---

### 5. Observability

All requests logged in:
logs/events.jsonl


Each log includes:

- Query
- Intent
- Retrieved sources
- Final answer
- Evaluation metrics
- Latency

---

## How to Run

### 1. Install dependencies
pip install -r backend/requirements.txt

### 2. Add .env file
GEMINI_API_KEY=your_key_here


### 3. Start backend
uvicorn backend.app.main:app --reload

### 4. Start frontend
streamlit run frontend/streamlit_app.py

---

## Example Queries

- "Explain RAG and chunking tradeoffs."
- "Write a FastAPI endpoint with Pydantic schema."
- "Summarize the following text..."
- "Compare RAG vs fine-tuning approaches."

---

## Technical Highlights

- Modular bot abstraction
- Provider-agnostic LLM wrapper (Gemini)
- FAISS vector similarity search
- Prompt-constrained JSON evaluation
- Production-style logging

---

## Future Improvements

- Hybrid retrieval (BM25 + vector)
- Caching embeddings
- Multi-model routing
- Structured output enforcement
- Tool calling
- Real-time monitoring dashboard

---

## Skills Demonstrated

- Applied LLM Engineering
- RAG Systems
- Prompt Engineering
- Agent Workflows
- Model Evaluation
- FastAPI
- Vector Databases
- Observability Design



PDF extraction may lose mathematical formatting.