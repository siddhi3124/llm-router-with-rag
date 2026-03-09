from google import genai
from backend.app.config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

for m in client.models.list():
    name = getattr(m, "name", "")
    supported = getattr(m, "supported_actions", None) or getattr(m, "supported_methods", None)
    print(name, supported)