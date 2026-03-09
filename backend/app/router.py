import re


def classify_intent(query: str) -> str:
    """
    Heuristic intent classifier for routing:
    - summarization
    - research
    - coding
    - knowledge (default)
    """
    q = (query or "").lower().strip()
    if not q:
        return "knowledge"

    # --- Summarization triggers ---
    # Examples: "summarize this", "tl;dr", "give me a summary", "in brief"
    if (
        re.search(r"^\s*(summarize|summarise|tl;dr)\b", q)
        or re.search(r"\b(give me a summary|summary|in brief|short version|key points)\b", q)
        or "summarize:" in q
        or "summarise:" in q
    ):
        return "summarization"

    # --- Research triggers (checked BEFORE coding) ---
    # Prevents "SQL vs NoSQL" from becoming coding just because it contains "sql".
    if re.search(
        r"\b(compare|vs|versus|trade-?offs?|pros and cons|evaluate|benchmark|design|approach|strategy)\b",
        q,
    ):
        return "research"

    # --- Coding triggers ---
    # Strong signals: errors/tracebacks, debug/fix/bug, or explicit "write/implement code"
    if (
        re.search(r"\b(error|exception|traceback|stack trace|segfault|crash)\b", q)
        or re.search(r"\b(debug|fix|bug)\b", q)
        or re.search(r"\b(write|implement)\b.*\b(code|function|script|api|endpoint)\b", q)
        or re.search(r"\b(code|pydantic|fastapi|python|typescript|regex)\b", q)
    ):
        return "coding"

    # Default: knowledge (RAG)
    return "knowledge"