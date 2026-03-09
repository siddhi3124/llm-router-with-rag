import sqlite3
from pathlib import Path
from typing import Dict, List, Tuple
import json

from ..paths import STORAGE_DIR

DB_PATH = STORAGE_DIR / "embeddings_cache.sqlite"

def _connect() -> sqlite3.Connection:
    STORAGE_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    # Always ensure schema exists (idempotent)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS embeddings (
            chunk_hash TEXT PRIMARY KEY,
            dim INTEGER NOT NULL,
            vector_json TEXT NOT NULL
        )
    """)
    conn.commit()
    return conn

def get_many(hashes: List[str]) -> Dict[str, List[float]]:
    if not hashes:
        return {}

    conn = _connect()
    q_marks = ",".join(["?"] * len(hashes))
    rows = conn.execute(
        f"SELECT chunk_hash, vector_json FROM embeddings WHERE chunk_hash IN ({q_marks})",
        hashes
    ).fetchall()
    conn.close()

    out: Dict[str, List[float]] = {}
    for h, vec_json in rows:
        out[h] = json.loads(vec_json)
    return out

def put_many(items: List[Tuple[str, List[float]]]) -> None:
    if not items:
        return

    conn = _connect()
    conn.executemany(
        "INSERT OR REPLACE INTO embeddings(chunk_hash, dim, vector_json) VALUES (?, ?, ?)",
        [(h, len(v), json.dumps(v)) for h, v in items]
    )
    conn.commit()
    conn.close()