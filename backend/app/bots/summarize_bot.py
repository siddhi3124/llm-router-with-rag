from ..llm import chat

def answer(query: str):
    messages = [
        {"role":"system","content":"Summarize clearly with bullet points and a 1-line TL;DR."},
        {"role":"user","content": query}
    ]
    answer, model_latency = chat(messages, temperature=0.2)
    return answer, [], model_latency