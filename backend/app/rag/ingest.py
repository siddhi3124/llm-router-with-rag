import hashlib
import os
import re
from pathlib import Path
from typing import List, Dict, Any

from pypdf import PdfReader

from ..llm import embed
from ..paths import RAW_DOCS_DIR
from .embed_cache import get_many, put_many
from .store import build_index, save_index


def _normalize_text(text: str) -> str:
    # Normalize whitespace for more stable chunk hashes and better retrieval
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def hash_chunk(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _source_name(p: Path) -> str:
    # Display-friendly identifier for citations/UI
    return p.name


def load_docs() -> List[Dict[str, Any]]:
    RAW_DOCS_DIR.mkdir(parents=True, exist_ok=True)
    docs: List[Dict[str, Any]] = []

    for p in RAW_DOCS_DIR.glob("**/*"):
        if not p.is_file():
            continue

        suffix = p.suffix.lower()

        # Markdown / text
        if suffix in [".txt", ".md"]:
            text = p.read_text(encoding="utf-8", errors="ignore")
            text = _normalize_text(text)
            if text:
                docs.append({
                    "id": str(p),                  # full path (debug)
                    "source_path": str(p),
                    "source_name": _source_name(p), # filename (display)
                    "text": text,
                    "doc_type": suffix.lstrip("."),
                })

        # PDF
        elif suffix == ".pdf":
            try:
                reader = PdfReader(str(p))
                # Skip encrypted PDFs gracefully
                if getattr(reader, "is_encrypted", False):
                    continue

                parts = []
                for page in reader.pages:
                    extracted = page.extract_text() or ""
                    extracted = extracted.strip()
                    if extracted:
                        parts.append(extracted)

                text = _normalize_text("\n\n".join(parts))
                if text:
                    docs.append({
                        "id": str(p),
                        "source_path": str(p),
                        "source_name": _source_name(p),
                        "text": text,
                        "doc_type": "pdf",
                    })

            except Exception:
                # Don't break ingestion for one bad PDF
                continue

    return docs


def chunk_text(text: str, chunk_size: int = 900, overlap: int = 150) -> List[str]:
    """
    Character-based chunking with overlap.
    Good enough for a portfolio RAG; stable + fast.
    """
    if chunk_size <= overlap:
        raise ValueError("chunk_size must be greater than overlap")

    chunks: List[str] = []
    i = 0
    n = len(text)

    while i < n:
        chunk = text[i:i + chunk_size].strip()
        if chunk:
            chunks.append(chunk)
        i += (chunk_size - overlap)

    return chunks


def ingest():
    docs = load_docs()
    if not docs:
        raise RuntimeError(
            f"No documents found in {RAW_DOCS_DIR}. "
            f"Add .md/.txt/.pdf files to data/raw_docs/ and try again."
        )

    chunks: List[str] = []
    meta: List[Dict[str, Any]] = []
    chunk_hashes: List[str] = []

    for d in docs:
        doc_id = d["source_name"]  # stable and pretty (filename)
        for idx, c in enumerate(chunk_text(d["text"])):
            h = hash_chunk(c)

            chunks.append(c)
            chunk_hashes.append(h)

            meta.append({
                "source": doc_id,
                "source_name": doc_id,
                "source_path": d.get("source_path"),
                "doc_type": d.get("doc_type", "unknown"),
                "chunk_index": idx,          # keep index as a separate field
                "chunk_id": f"{doc_id}::chunk_{idx}",
                "hash": h,
                "text": c,                   # FULL chunk text for grounding
                "preview": c[:260],
            })

    # 1) pull cached embeddings
    cached = get_many(chunk_hashes)

    # 2) embed only missing hashes
    embeddings_by_hash = dict(cached)
    missing_texts: List[str] = []
    missing_hashes: List[str] = []

    for c, h in zip(chunks, chunk_hashes):
        if h not in embeddings_by_hash:
            missing_texts.append(c)
            missing_hashes.append(h)

    if missing_texts:
        new_vectors = embed(missing_texts, batch_size=16)
        put_many(list(zip(missing_hashes, new_vectors)))
        for h, v in zip(missing_hashes, new_vectors):
            embeddings_by_hash[h] = v

    # 3) rebuild aligned embeddings list
    embs = [embeddings_by_hash[h] for h in chunk_hashes]

    index = build_index(embs)
    save_index(index, meta)

    return {
        "docs_loaded": len(docs),
        "chunks_total": len(chunks),
        "cache_hits": len(cached),
        "embedded_new": len(missing_texts),
        "embedding_provider": os.getenv("EMBED_PROVIDER", "gemini"),
    }