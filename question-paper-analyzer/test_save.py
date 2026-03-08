from app import save_analysis, init_db # type: ignore

# Ensure DB is init
init_db()

res = {
    'total_questions': 5,
    'easy_questions': 2,
    'medium_questions': 2,
    'hard_questions': 1,
    'easy_percentage': 40.0,
    'medium_percentage': 40.0,
    'hard_percentage': 20.0,
    'overall_difficulty': 'Mixed Analysis'
}

text = "Sample question text"
fname = "test_run.pdf"

print("Starting test save...")
save_analysis(res, text, fname)
print("Test save finished.")
