import time
from typing import Any, Dict, Tuple

_CACHE: Dict[str, Tuple[float, Any]] = {}
TTL_SECONDS = 3600

def get(key: str):
    item = _CACHE.get(key)
    if not item:
        return None
    ts, val = item
    if time.time() - ts > TTL_SECONDS:
        _CACHE.pop(key, None)
        return None
    return val

def set(key: str, val: Any):
    _CACHE[key] = (time.time(), val)