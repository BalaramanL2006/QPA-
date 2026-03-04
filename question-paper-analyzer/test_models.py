import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY"),
    http_options={'api_version': 'v1'}
)

print("Listing models with v1 API version...")
try:
    for model in client.models.list():
        print(f"Name: {model.name}, Supported Methods: {model.supported_generation_methods}")
except Exception as e:
    print(f"Error listing models: {e}")

print("\nListing models WITHOUT explicit API version (default)...")
client_default = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
try:
    for model in client_default.models.list():
        print(f"Name: {model.name}, Supported Methods: {model.supported_generation_methods}")
except Exception as e:
    print(f"Error listing models (default): {e}")
