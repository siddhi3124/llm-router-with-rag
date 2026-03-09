from __future__ import annotations

from typing import List, Dict, Any
import os

from ..llm import embed
from .store import load_index, search


def _clean_source(src: str) -> str:
    if not src:
        return "unknown"
    src = str(src)
    src_norm = src.replace("\\", "/").rstrip("/")
    base = os.path.basename(src_norm)
    return base if base else src_norm


def retrieve(query: str, top_k: int = 4) -> List[Dict[str, Any]]:
    query = (query or "").strip()
    if not query:
        return []

    index, meta = load_index()
    if index is None or not meta:
        return []

    q_vecs = embed([query])
    if not q_vecs:
        return []
    q_emb = q_vecs[0]

    ids, scores = search(index, q_emb, top_k=top_k)

    results: List[Dict[str, Any]] = []
    for idx, score in zip(list(ids), list(scores)):
        if idx is None or idx == -1:
            continue
        if idx < 0 or idx >= len(meta):
            continue

        m = meta[idx] or {}
        src = m.get("source", "unknown")

        chunk_text = m.get("text") or m.get("chunk") or ""
        results.append(
            {
                "score": float(score),
                "source": src,
                "source_name": _clean_source(src),
                "doc_type": m.get("doc_type", "unknown"),
                "text": chunk_text,
                "preview": m.get("preview", ""),
                "hash": m.get("hash", None),
            }
        )

    results.sort(key=lambda x: x["score"], reverse=True)
    return results