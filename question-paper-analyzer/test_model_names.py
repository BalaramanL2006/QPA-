import requests
import json
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

print("Testing with gemini-2.0-flash...")
try:
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents="Say hello!"
    )
    print(f"Success: {response.text}")
except Exception as e:
    print(f"Error: {e}")

print("\nTesting with gemini-flash-latest...")
try:
    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents="Say hello!"
    )
    print(f"Success: {response.text}")
except Exception as e:
    print(f"Error: {e}")
