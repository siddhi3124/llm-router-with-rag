from typing import List, Dict, Protocol

class LLMProvider(Protocol):
    def generate(self, messages: List[Dict[str, str]], temperature: float = 0.2) -> str:
        ...

    def embed(self, texts: List[str]) -> List[List[float]]:
        ...