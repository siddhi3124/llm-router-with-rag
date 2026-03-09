from __future__ import annotations

from pathlib import Path
import json
from typing import List, Tuple, Any, Optional

import numpy as np
import faiss

from ..paths import STORAGE_DIR

INDEX_FILE = STORAGE_DIR / "docs.index"
META_FILE = STORAGE_DIR / "docs_meta.json"


def save_index(index: faiss.Index, meta: list) -> None:
    STORAGE_DIR.mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, str(INDEX_FILE))
    META_FILE.write_text(
        json.dumps(meta, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def load_index():
    if not INDEX_FILE.exists() or not META_FILE.exists():
        return None, []
    index = faiss.read_index(str(INDEX_FILE))
    meta = json.loads(META_FILE.read_text(encoding="utf-8"))
    return index, meta


def build_index(embeddings: List[List[float]]) -> faiss.Index:
    """
    Builds a cosine-similarity-like index by using:
    - IndexFlatIP (inner product)
    - L2 normalization on vectors
    """
    if not embeddings:
        raise ValueError("No embeddings provided to build_index().")

    vecs = np.array(embeddings, dtype="float32")
    if vecs.ndim != 2:
        raise ValueError(f"Embeddings array must be 2D, got shape={vecs.shape}")

    dim = vecs.shape[1]
    index = faiss.IndexFlatIP(dim)
    faiss.normalize_L2(vecs)
    index.add(vecs)
    return index


def search(index: faiss.Index, query_embedding: List[float], top_k: int = 4):
    """
    Returns (ids, scores) where:
    - ids: list[int]
    - scores: list[float] (higher is better; ~cosine similarity due to normalization)
    """
    q = np.array([query_embedding], dtype="float32")
    faiss.normalize_L2(q)
    scores, ids = index.search(q, top_k)
    return ids[0].tolist(), scores[0].tolist()