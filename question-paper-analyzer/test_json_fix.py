from app import analyze_with_ai, app
import json
import os
from dotenv import load_dotenv

load_dotenv()

sample_text = """
1. What is 2+2? (1 mark)
2. Explain photosynthesis in detail. (10 marks)
3. Solve the quadratic equation x^2 + 5x + 6 = 0. (5 marks)
"""

with app.app_context():
    print("Testing analyze_with_ai with forced JSON...")
    result = analyze_with_ai(sample_text)
    if isinstance(result, dict) and 'error' not in result:
        print("SUCCESS: JSON parsed correctly!")
        print(f"Keys: {list(result.keys())}")
    else:
        print("FAILURE: Result is not a valid dict or contains error")
        print(result)
