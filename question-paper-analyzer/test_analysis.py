import requests
import json

url = "http://127.0.0.1:5000/analyze"
# We need to be logged in, so we might need to skip auth for testing or simulate login.
# But let's see if we can just call it (it has @login_required).

# Instead of calling the API over network, let's just call the function in a script.
from app import analyze_with_ai, app
import os
from dotenv import load_dotenv

load_dotenv()

with app.app_context():
    print("Testing analyze_with_ai directly...")
    result = analyze_with_ai("What is the capital of France?")
    print(json.dumps(result, indent=2))
