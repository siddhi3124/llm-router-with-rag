import os
from dotenv import load_dotenv
from .gemini_provider import GeminiProvider

load_dotenv()

def get_provider():
    provider = os.getenv("PROVIDER", "gemini").lower()

    if provider == "gemini":
        api_key = os.getenv("GEMINI_API_KEY", "")
        if not api_key:
            raise RuntimeError("Missing GEMINI_API_KEY in .env")

        chat_model = os.getenv("GEMINI_CHAT_MODEL", "gemini-1.5-flash")
        embed_model = os.getenv("GEMINI_EMBED_MODEL", "models/text-embedding-004")
        return GeminiProvider(api_key=api_key, chat_model=chat_model, embed_model=embed_model)

    raise RuntimeError(f"Unsupported PROVIDER={provider}")