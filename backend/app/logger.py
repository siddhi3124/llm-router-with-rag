import json, time
from pathlib import Path
from typing import Any, Dict
from .paths import LOGS_DIR

LOG_PATH = LOGS_DIR / "events.jsonl"

def log_event(event: Dict[str, Any]) -> None:
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    event["ts"] = int(time.time())
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False, default=str) + "\n")