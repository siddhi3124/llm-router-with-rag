# backend/app/llm.py

import os
import time
import random
from typing import List, Optional, Tuple

from google import genai
from google.genai import types
from google.genai.errors import ClientError

from .config import GEMINI_API_KEY, CHAT_MODEL, EMBED_MODEL

# -----------------------------
# Configuration
# -----------------------------
EMBED_PROVIDER = os.getenv("EMBED_PROVIDER", "gemini").strip().lower()
LOCAL_EMBED_MODEL = os.getenv("LOCAL_EMBED_MODEL", "all-MiniLM-L6-v2").strip()

_client = None


def _get_client():
    global _client
    if _client is None:
        if not GEMINI_API_KEY:
            raise RuntimeError("GEMINI_API_KEY missing. Add it to .env to use chat (Gemini).")
        _client = genai.Client(api_key=GEMINI_API_KEY)
    return _client


# Lazy-loaded local embedding model
_local_embedder = None


def _normalize_model_name(name: str) -> str:
    """
    Gemini SDK typically accepts model names as 'models/<id>'.
    This makes env values robust if you pass 'gemini-2.0-flash' etc.
    """
    name = (name or "").strip()
    if not name:
        return name
    if not name.startswith("models/"):
        return "models/" + name
    return name


# -----------------------------
# Chat (Gemini)
# -----------------------------
def chat(messages, temperature: float = 0.2, max_output_tokens: int = 600) -> Tuple[str, int]:
    prompt_lines = []
    for m in messages:
        role = m.get("role", "user").upper()
        prompt_lines.append(f"{role}:\n{m.get('content','')}")
    prompt = "\n\n".join(prompt_lines)

    model = _normalize_model_name(CHAT_MODEL)

    max_retries = 6
    for attempt in range(1, max_retries + 1):
        try:
            t0 = time.time()
            client = _get_client()
            resp = client.models.generate_content(
                model=model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=temperature,
                    max_output_tokens=max_output_tokens,
                ),
            )
            model_latency_ms = int((time.time() - t0) * 1000)
            return resp.text or "", model_latency_ms

        except ClientError as e:
            msg = str(e)
            # Retry on rate limit / quota
            if "429" in msg or "RESOURCE_EXHAUSTED" in msg:
                sleep_s = min(60, (2 ** attempt)) + random.random()
                time.sleep(sleep_s)
                continue
            raise

        except Exception as e:
            msg = str(e)
            # Retry on transient 503-ish errors
            if "503" in msg or "UNAVAILABLE" in msg or "high demand" in msg:
                sleep_s = min(60, (2 ** attempt)) + random.random()
                time.sleep(sleep_s)
                continue
            raise

    raise RuntimeError("rate-limited")


# -----------------------------
# Embeddings (Gemini or Local)
# -----------------------------
def _embed_local(texts: List[str]) -> List[List[float]]:
    """
    Unlimited embeddings using a local sentence-transformers model.
    Normalized embeddings are better for cosine similarity / dot product.
    """
    global _local_embedder
    if _local_embedder is None:
        from sentence_transformers import SentenceTransformer
        _local_embedder = SentenceTransformer(LOCAL_EMBED_MODEL)

    vecs = _local_embedder.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=False,
    )
    return vecs.tolist()


def _embed_gemini(texts: List[str], batch_size: int = 16, max_retries: int = 6) -> List[List[float]]:
    """
    Batched + retry/backoff embeddings via Gemini.
    """
    model = _normalize_model_name(EMBED_MODEL)
    vectors: List[List[float]] = []

    client = _get_client()

    for i in range(0, len(texts), batch_size):
        batch = texts[i : i + batch_size]
        attempt = 0

        while True:
            try:
                resp = client.models.embed_content(
                    model=model,
                    contents=batch,  # list => batched request
                )
                for e in resp.embeddings:
                    vectors.append(e.values)
                break

            except ClientError as e:
                msg = str(e)
                if "429" not in msg and "RESOURCE_EXHAUSTED" not in msg:
                    raise

                attempt += 1
                if attempt > max_retries:
                    raise RuntimeError(
                        "Gemini embeddings rate-limited/quota exhausted. "
                        "Switch EMBED_PROVIDER=local for ingestion."
                    ) from e

                sleep_s = min(60, (2 ** attempt)) + random.random()
                time.sleep(sleep_s)

    return vectors


def embed(texts: List[str], batch_size: int = 16, max_retries: int = 6) -> List[List[float]]:
    """
    Main embeddings entrypoint used by the rest of the app.
    Controlled via EMBED_PROVIDER env var:
      - EMBED_PROVIDER=local
      - EMBED_PROVIDER=gemini
    """
    if not texts:
        return []

    provider = EMBED_PROVIDER
    if provider == "local":
        return _embed_local(texts)
    if provider == "gemini":
        return _embed_gemini(texts, batch_size=batch_size, max_retries=max_retries)

    raise ValueError(f"Unknown EMBED_PROVIDER={provider}. Use 'local' or 'gemini'.")