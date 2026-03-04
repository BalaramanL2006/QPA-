import os
from dotenv import load_dotenv
from google import genai
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
models_to_try = [
    "gemini-2.0-flash",
    "gemini-2.5-flash",
    "gemini-pro-latest",
    "gemini-2.0-flash-lite",
    "gemini-1.5-flash-8b", # Just in case
]
for m in models_to_try:
    try:
        print(f"Probing {m}...")
        res = client.models.generate_content(model=m, contents="hi")
        print(f"SUCCESS with {m}: {res.text}")
        break
    except Exception as e:
        print(f"FAILED {m}: {e}")
