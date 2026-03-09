from ..llm import chat

def answer(query: str):
    messages = [
        {"role":"system","content":"You are a senior software engineer. Give correct, runnable code and brief explanation."},
        {"role":"user","content": query}
    ]
    answer, model_latency = chat(messages, temperature=0.2)
    return answer, [], model_latency