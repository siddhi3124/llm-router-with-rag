import json
from ..llm import chat

def evaluate(query: str, answer: str) -> dict:
    judge_prompt = f"""
Return STRICT JSON only.

User query:
{query}

Assistant answer:
{answer}

JSON schema:
{{
  "helpfulness": 1-10,
  "correctness": 1-10,
  "hallucination_risk": 1-10,
  "short_feedback": "string <= 20 words"
}}
"""
    raw_text, _model_latency_ms = chat(
        [{"role": "user", "content": judge_prompt}],
        temperature=0.0
    )
    raw = (raw_text or "").strip()
    try:
        return json.loads(raw)
    except Exception:
        return {"helpfulness": 6, "correctness": 6, "hallucination_risk": 6, "short_feedback": "Judge JSON parse failed."}