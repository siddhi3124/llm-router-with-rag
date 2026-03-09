import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
CHAT_MODEL = os.getenv("CHAT_MODEL", "gemini-2.0-flash")
EMBED_MODEL = os.getenv("EMBED_MODEL", "text-embedding-004")
ENABLE_EVAL = os.getenv("ENABLE_EVAL", "0") == "1"
ENABLE_RESEARCH_PLAN = os.getenv("ENABLE_RESEARCH_PLAN", "0") == "1"

REQUIRE_GEMINI_FOR_CHAT = os.getenv("REQUIRE_GEMINI_FOR_CHAT", "1") == "1"