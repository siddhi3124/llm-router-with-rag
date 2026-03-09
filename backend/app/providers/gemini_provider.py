from typing import List, Dict
import google.generativeai as genai

class GeminiProvider:
    def __init__(self, api_key: str, chat_model: str, embed_model: str):
        genai.configure(api_key=api_key)
        self.chat_model_name = chat_model
        self.embed_model_name = embed_model
        self.chat_model = genai.GenerativeModel(self.chat_model_name)

    def generate(self, messages: List[Dict[str, str]], temperature: float = 0.2) -> str:
        # Convert chat-style messages to a single prompt.
        # This keeps provider differences isolated here.
        prompt_parts = []
        for m in messages:
            role = m.get("role", "user").upper()
            content = m.get("content", "")
            prompt_parts.append(f"{role}:\n{content}")
        prompt = "\n\n".join(prompt_parts)

        resp = self.chat_model.generate_content(
            prompt,
            generation_config={"temperature": temperature}
        )
        return resp.text or ""

    def embed(self, texts: List[str]) -> List[List[float]]:
        vectors: List[List[float]] = []
        for t in texts:
            r = genai.embed_content(model=self.embed_model_name, content=t)
            vectors.append(r["embedding"])
        return vectors