from pathlib import Path

# backend/app/paths.py
# __file__ = .../backend/app/paths.py
# parents: [app, backend, project_root, ...]
PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"
RAW_DOCS_DIR = DATA_DIR / "raw_docs"

STORAGE_DIR = PROJECT_ROOT / "storage" / "faiss_index"
LOGS_DIR = PROJECT_ROOT / "logs"