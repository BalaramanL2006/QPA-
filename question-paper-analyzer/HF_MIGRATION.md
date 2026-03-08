# Question Paper Analyzer - Hugging Face Migration

The project has been migrated from Google Gemini to Hugging Face Mistral-7B.

## 🛠️ Changes Implemented

- Removed `google-genai` and `GEMINI_API_KEY`.
- Integrated `requests` with `mistralai/Mistral-7B-Instruct-v0.2`.
- Updated `.env` and `requirements.txt`.
- Refactored `app.py` for new prompt and compatibility mapping.
- Handled API 429 and JSON parsing.

## 🚀 Setup

1. Add your Hugging Face Token to `.env`:
   ```env
   HUGGINGFACE_API_KEY=your_token_here
   ```
2. Run `pip install -r requirements.txt`.
3. Run `python app.py`.
