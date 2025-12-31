import os
from dotenv import load_dotenv

load_dotenv()   # loads .env into environment

API_KEY = os.getenv("GEMINI_API_KEY")
DEBUG = os.getenv("DEBUG") == "True"
PORT = int(os.getenv("PORT", 8000))

if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY not set")

print("API KEY:", API_KEY)
print("DEBUG:", DEBUG)
print("PORT:", PORT)
