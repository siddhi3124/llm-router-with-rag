import time
from fastapi import FastAPI, HTTPException
import uuid

from .config import ENABLE_EVAL
from .schemas import AskRequest, AskResponse
from .router import classify_intent
from .logger import log_event
from .eval.judge import evaluate
from .rag.ingest import ingest
from .rag.store import load_index

from .bots.knowledge_bot import answer as knowledge_answer
from .bots.code_bot import answer as code_answer
from .bots.summarize_bot import answer as summarize_answer
from .bots.research_bot import answer as research_answer

from .cache import get as cache_get, set as cache_set

app = FastAPI(title="Mini-Poe (Gemini): Router + RAG + Agent + Eval")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ingest")
def run_ingest():
    # Optional: measure ingest time too
    t0 = time.time()
    out = ingest()
    out["latency_ms"] = int((time.time() - t0) * 1000)
    return out


@app.post("/ask", response_model=AskResponse)
def ask(req: AskRequest):
    request_id = str(uuid.uuid4())
    t0 = time.time()
    model_latency_ms = None
    try:
        query = (req.query or "").strip()
        if not query:
            raise HTTPException(status_code=400, detail="Query cannot be empty.")

        intent = classify_intent(query)

        # Cache key: stable + normalized
        cache_key = f"{intent}:{' '.join(query.lower().split())}"
        cached = cache_get(cache_key)

        if cached:
            ans, sources, model_latency_ms = cached
            cache_hit = True
        else:
            cache_hit = False
            if intent == "coding":
                ans, sources, model_latency_ms = code_answer(query)
            elif intent == "summarization":
                ans, sources, model_latency_ms = summarize_answer(query)
            elif intent == "research":
                ans, sources, model_latency_ms = research_answer(query)
            else:
                ans, sources, model_latency_ms = knowledge_answer(query)

            cache_set(cache_key, (ans, sources, model_latency_ms))

        ev = evaluate(query, ans) if ENABLE_EVAL else None
        latency_ms = int((time.time() - t0) * 1000)

        # Log (great for debugging + resume)
        try:
            log_event({
                "request_id" : request_id,
                "query": query,
                "intent": intent,
                "cache_hit": cache_hit,
                "num_sources": len(sources) if sources else 0,
                "latency_ms": latency_ms,
                "model_latency_ms": model_latency_ms,
                "eval": ev,
            })
        except Exception:
            # logging must never break the request
            pass

        # Return an AskResponse-shaped dict (or AskResponse object)
        return AskResponse(
            request_id=request_id,
            intent=intent,
            answer=ans,
            retrieved_sources=sources or [],
            eval=ev,
            latency_ms=latency_ms,
            model_latency_ms=model_latency_ms,
        )

    except RuntimeError as e:
        # Your llm.chat raises RuntimeError("rate-limited") sometimes
        if "rate-limited" in str(e).lower():
            raise HTTPException(status_code=429, detail="Rate limited. Please retry shortly.")
        elif "503" in str(e) or "UNAVAILABLE" in str(e):
            raise HTTPException(status_code=503, detail="LLM provider temporarily unavailable. Please retry.")
        raise HTTPException(status_code=500, detail="Internal error while generating response.")

@app.get("/rag/status")
def rag_status():
    index, meta = load_index()
    return {
        "index_loaded": index is not None,
        "num_chunks": len(meta) if meta else 0
    }