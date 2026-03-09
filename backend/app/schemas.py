from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional


class AskRequest(BaseModel):
    query: str


class AskResponse(BaseModel):
    intent: str
    answer: str
    retrieved_sources: List[Dict[str, Any]] = Field(default_factory=list)
    eval: Optional[Dict[str, Any]] = None
    request_id: Optional[str] = None
    latency_ms: int
    model_latency_ms: Optional[int] = None