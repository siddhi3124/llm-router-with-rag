from ..llm import chat
from ..rag.retrieve import retrieve

DRAFT_SYSTEM = """You are a grounded assistant.
Use the provided context to answer.
Cite sources like [1], [2] when using context.
If context is insufficient, say so clearly.
"""

FINAL_SYSTEM = """You are an editor.
You will be given a draft answer and the same context.
Task:
- Produce ONE final answer (no duplicated sections).
- Keep the output format exactly:
Answer:
<content>

Sources Used:
- [1] ...
- [2] ...
- Do not repeat "Answer:" twice.
- Ensure each major claim has citations [1], [2] where applicable.
- If draft contains duplicated lines, remove them.
"""

def answer(query: str):
    sources = retrieve(query, top_k=4) or []
    context_lines = []
    for i, s in enumerate(sources):
        src = s.get("source_name", "unknown")
        text = s.get("text") or s.get("preview", "")
        context_lines.append(f"[{i+1}] SOURCE: {src}\n{text}")
    context = "\n\n".join(context_lines)

    # Pass 1: Draft (grounded, longer)
    draft_user = f"""Query: {query}

Context:
{context}

Write a detailed answer with citations like [1], [2]. Use the structure:
- Definition
- Formula / Mechanism
- Why scaling by sqrt(d_k)
- Why it's used
- Where it appears in Transformers
Then include "Sources Used:" with [1], [2], etc.
"""
    draft, draft_latency = chat(
        [{"role": "system", "content": DRAFT_SYSTEM},
         {"role": "user", "content": draft_user}],
        temperature=0.2,
        max_output_tokens=1200,
    )

    # Pass 2: Final cleanup (dedupe + enforce single Answer block)
    final_user = f"""Context:
{context}

Draft answer:
{draft}

Rewrite into the final required format with no duplication.
"""
    final, final_latency = chat(
        [{"role": "system", "content": FINAL_SYSTEM},
         {"role": "user", "content": final_user}],
        temperature=0.0,
        max_output_tokens=1200,
    )

    return final.strip(), sources, (draft_latency + final_latency)