from ..llm import chat
from ..rag.retrieve import retrieve
from ..config import ENABLE_RESEARCH_PLAN

def answer(query: str):
    # Retrieve context for research answers (same grounding idea as knowledge bot)
    sources = retrieve(query, top_k=5)
    context = "\n\n".join([s.get("text", "") for s in sources if s.get("text")])

    if ENABLE_RESEARCH_PLAN:
        # Optional extra call (more agent-like, costs more quota)
        plan_text, _plan_latency = chat([
            {"role":"system","content":"Create a short research plan (3-5 steps)."},
            {"role":"user","content": query}
        ], temperature=0.2)
        plan_block = f"Plan:\n{plan_text}\n\n"
    else:
        plan_block = ""

    answer, model_latency = chat([
        {
            "role": "system",
            "content": "You are a research assistant. If context is provided, use it. Be explicit about tradeoffs and when each method is appropriate. Cite sources [1], [2] if used."
        },
        {
            "role": "user",
            "content": f"""Query: {query}

            {plan_block}Context:
            {context}

            Write a structured comparison with:
            - When to use RAG
            - When to use fine-tuning
            - Cost/latency
            - Data requirements
            - Risks
            - A simple decision checklist."""
        }
    ], temperature=0.2)

    return answer, sources, model_latency