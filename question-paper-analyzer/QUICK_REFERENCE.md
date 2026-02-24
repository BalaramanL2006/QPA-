# 🚀 Flask Question Paper Analyzer - Quick Reference & pip Commands

## Installation & Setup

### One-Command Install
```bash
pip install -r requirements.txt
```

### Verify Installation
```bash
python test_extraction.py
```

### Optional OCR (Tesseract)
```powershell
choco install tesseract
```

### Run Application
```bash
python app.py
```

### Access Application
```
http://localhost:5000
```

---

## Supported File Formats

| Format | Status | Command | Notes |
|--------|--------|---------|-------|
| **Text** | ✅ Ready | `pip install flask` | Built-in support |
| **PDF** | ✅ Ready | `pip install pdfplumber` | Multi-page extraction |
| **DOCX** | ✅ Ready | `pip install python-docx` | Tables + paragraphs |
| **JPG/PNG** | ⚠️ Optional | `choco install tesseract` | Requires Tesseract |

---

## pip Install Commands

### Install All (Recommended)
```bash
pip install -r requirements.txt
```

### Individual Packages
```bash
pip install Flask==2.3.3
pip install pdfplumber==0.10.3
pip install python-docx==0.8.11
pip install Pillow==10.0.0
pip install pytesseract==0.3.10
```

### One-Liner Install
```bash
pip install Flask==2.3.3 pdfplumber==0.10.3 python-docx==0.8.11 Pillow==10.0.0 pytesseract==0.3.10
```

### Upgrade Existing
```bash
pip install --upgrade -r requirements.txt
```

### Install from requirements (with options)
```bash
pip install -r requirements.txt --upgrade --no-cache-dir
```

---

## Windows
```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run Flask
python app.py
```

## 🌐 Access Points

| Purpose | URL |
|---------|-----|
| Analyzer | http://127.0.0.1:5000 |
| Alternative | http://localhost:5000 |
| History | http://127.0.0.1:5000/history |

## 📚 Difficulty Keywords

### Easy (Knowledge)
- define
- list
- identify
- name
- what
- state
- write

### Medium (Comprehension/Application)
- explain
- describe
- summarize
- discuss
- illustrate
- outline
- distinguish

### Hard (Analysis/Synthesis/Evaluation)
- analyze
- evaluate
- justify
- compare
- criticize
- synthesis
- create

## 📂 Key Files

| File | Purpose | Size |
|------|---------|------|
| `app.py` | Backend logic | ~500 lines |
| `index.html` | Home page | ~200 lines |
| `history.html` | History page | ~100 lines |
| `style.css` | Styling | ~400 lines |
| `script.js` | Frontend logic | ~200 lines |
| `database.db` | SQLite database | Auto-created |

## 🔧 Common Customizations

### Change Port
Edit `app.py` last line:
```python
app.run(debug=True, host='127.0.0.1', port=8000)  # Change 5000 to desired port
```

### Add Keywords
Edit `DIFFICULTY_KEYWORDS` in `app.py`:
```python
DIFFICULTY_KEYWORDS = {
    'easy': ['define', 'list', ...],
    'medium': ['explain', ...],
    'hard': ['analyze', ...]
}
```

### Change Difficulty Thresholds
Edit `analyze_paper()` function:
```python
if easy_percentage > 50:  # Change 50 to desired threshold
    overall_difficulty = 'Easy Paper'
```

## 📊 API Endpoints

### POST /analyze
```json
Request:
{
    "paper_text": "Define X\nExplain Y\nAnalyze Z"
}

Response (Success):
{
    "total_questions": 3,
    "easy_count": 1,
    "medium_count": 1,
    "hard_count": 1,
    "easy_percentage": 33.33,
    "medium_percentage": 33.33,
    "hard_percentage": 33.33,
    "overall_difficulty": "Moderate Paper"
}

Response (Error):
{
    "error": "Error message here"
}
```

### GET /api/history
```json
Response:
[
    {
        "id": 1,
        "timestamp": "2024-02-12 10:30:45",
        "total_questions": 10,
        "easy_count": 5,
        "medium_count": 3,
        "hard_count": 2,
        "easy_percentage": 50.0,
        "medium_percentage": 30.0,
        "hard_percentage": 20.0,
        "overall_difficulty": "Easy Paper"
    },
    ...
]
```

## 🆘 Quick Troubleshooting

| Error | Solution |
|-------|----------|
| `ModuleNotFoundError: flask` | Run `pip install -r requirements.txt` |
| `Address already in use` | Change port in `app.py` |
| `Python not found` | Install Python or add to PATH |
| `Permission denied: run.sh` | Run `chmod +x run.sh` |
| `Cannot find templates` | Ensure running from project root |
| Database locked | Delete `database.db` and restart |

## 🎯 Example Analysis

### Input
```
1. Define photosynthesis
2. Explain cellular respiration
3. Analyze climate change
4. Compare evolution theories
5. What is osmosis?
```

### Processing
- Line 1: "define" → Easy
- Line 2: "explain" → Medium
- Line 3: "analyze" → Hard
- Line 4: "compare" → Hard
- Line 5: "what" → Easy

### Output
- Easy: 2 (40%)
- Medium: 1 (20%)
- Hard: 2 (40%)
- **Result: Moderate Paper** (balanced)

## 📋 Checklist for First Run

- [ ] Python 3.7+ installed
- [ ] Project folder downloaded
- [ ] Terminal opened in project directory
- [ ] Virtual environment activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Flask running (`python app.py`)
- [ ] Browser opened to http://127.0.0.1:5000
- [ ] Sample questions pasted or uploaded
- [ ] Analyze button clicked
- [ ] Results and chart displayed
- [ ] History page accessible

## 📞 Common Commands

```bash
# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Deactivate virtual environment
deactivate

# Install new package
pip install package_name

# List installed packages
pip list

# Run Flask app
python app.py

# Exit Flask (in terminal)
Ctrl + C
```

## 🎓 Learning Path

1. **Beginner**: Run the app, analyze samples
2. **Intermediate**: Modify keywords, customize UI
3. **Advanced**: Add authentication, export features
4. **Expert**: Deploy to cloud, add ML features

## 📚 Documentation Files

- **README.md** - Project overview
- **INSTALLATION.md** - Setup guide
- **DEVELOPERS.md** - Code documentation
- **QUICK_REFERENCE.md** - This file

## 🌟 Tips & Tricks

### Multiple Analyses
- Click "Analyze Another Paper" to reset
- Check history to see all previous analyses

### Keyboard Shortcuts
- **Ctrl+Enter** - Submit analysis (on home page)
- **Tab** - Navigate between fields
- **Enter** - Submit file if focused

### Performance
- Large papers (500+ questions) may take a few seconds
- Results are cached in memory within session
- Database stores all analyses indefinitely

### Testing
- Use `SAMPLE_QUESTIONS.txt` to test
- Try empty input to test error handling
- Use keywords outside the list (default to medium)

## 🔗 External Resources

- **Flask**: https://flask.palletsprojects.com/
- **Chart.js**: https://www.chartjs.org/
- **SQLite**: https://www.sqlite.org/
- **Python**: https://www.python.org/

---

**Last Updated**: February 2024
**Version**: 1.0
**Status**: ✅ Production Ready
