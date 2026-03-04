from app import analyze_with_ai, app
import os
from dotenv import load_dotenv

load_dotenv()

# Simulate a complex paper
complex_text = """
SECTION A
1. Answer all questions.
2. What is the unit of force? (1 mark)
3. Define momentum. (2 marks)
4. A car travels at 60 km/h. How far does it go in 10 minutes? (5 marks)
... repeat ...
""" * 50 # Make it long

with app.app_context():
    print(f"Testing analyze_with_ai with {len(complex_text)} characters...")
    result = analyze_with_ai(complex_text)
    print("RESULT TYPE:", type(result))
    if 'error' in result:
        print("ERROR:", result['error'])
        if os.path.exists("ai_errors.log"):
            print("Log entry found!")
    else:
        print("SUCCESS")
