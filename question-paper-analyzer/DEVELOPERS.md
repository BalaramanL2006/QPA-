# Developer's Guide

Complete documentation of the codebase for developers and contributors.

## 🏗️ Architecture Overview

```
Frontend (Browser)
    ├── HTML (index.html, history.html)
    ├── CSS (style.css)
    └── JavaScript (script.js)
          ↓ (AJAX/Fetch API)
Backend (Flask)
    ├── Routes (/)
    ├── Logic (app.py)
    └── Database (SQLite/database.db)
```

---

## 📁 Directory Structure with Details

```
question-paper-analyzer/
│
├── app.py                    # Main Flask application (500+ lines)
│   ├── Configuration
│   ├── Database Functions
│   ├── Analysis Logic
│   └── Routes
│
├── config.py                 # Configuration settings (customizable)
│
├── requirements.txt          # Python dependencies
│   ├── Flask==2.3.3
│   └── Werkzeug==2.3.7
│
├── database.db              # SQLite database (auto-created)
│
├── templates/               # HTML templates
│   ├── index.html           # Home page (analyzer + results)
│   └── history.html         # Analysis history page
│
├── static/                  # Static assets
│   ├── style.css            # 400+ lines of CSS
│   └── script.js            # Frontend JavaScript logic
│
├── Documentation
│   ├── README.md            # Project overview
│   ├── INSTALLATION.md      # Setup guide
│   └── DEVELOPERS.md        # This file
│
├── Helper Scripts
│   ├── run.bat              # Windows quick start
│   ├── run.sh               # macOS/Linux quick start
│   └── SAMPLE_QUESTIONS.txt # Test data
│
└── .gitignore              # Git ignore patterns
```

---

## 🔧 Key Files Explained

### `app.py` - Core Backend Logic

#### Imports & Constants
```python
from flask import Flask, render_template, request, jsonify
import sqlite3
import os
from datetime import datetime
```

#### Database Schema
```sql
CREATE TABLE analysis_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    total_questions INTEGER,
    easy_count INTEGER,
    medium_count INTEGER,
    hard_count INTEGER,
    easy_percentage REAL,
    medium_percentage REAL,
    hard_percentage REAL,
    overall_difficulty TEXT,
    paper_text TEXT
)
```

#### Key Functions

**`classify_question_difficulty(question)`**
- Scans question for action verbs
- Returns 'easy', 'medium', or 'hard'
- Uses keyword matching algorithm

**`analyze_paper(paper_text)`**
- Splits paper by newlines
- Classifies each question
- Calculates percentages
- Determines overall difficulty
- Returns analysis results dictionary

**`save_analysis(analysis_result, paper_text)`**
- Inserts results into database
- Handles SQL execution safely

#### Routes

| Route | Method | Purpose |
|-------|--------|---------|
| `/` | GET | Render home page |
| `/analyze` | POST | Analyze paper (JSON) |
| `/history` | GET | Render history page |
| `/api/history` | GET | Get history as JSON |

### `templates/index.html` - Home Page

#### Sections
1. **Header** - Title and subtitle
2. **Navigation** - Links to pages
3. **Input Section**
   - Text area for pasting questions
   - File upload input
4. **Results Section** (initially hidden)
   - Overall difficulty display
   - Statistics cards (Easy/Medium/Hard)
   - Chart container
5. **Footer** - Copyright and info

#### Key Elements
- `#paper_text` - Main textarea
- `#file_upload` - File input
- `#analyze_btn` - Analysis button
- `#results_section` - Results container
- `#difficultyChart` - Chart canvas

### `templates/history.html` - History Page

#### Features
- Table display of all analyses
- Timestamp for each analysis
- Question statistics
- Overall difficulty classification
- No data message if history is empty

#### Data Displayed
- Row number
- Analysis date and time
- Total questions
- Easy/Medium/Hard counts
- Percentage breakdown
- Overall difficulty badge

### `static/style.css` - Styling

#### Color Scheme
```css
:root {
    --primary-color: #4f46e5;      /* Influent/Brand Blue */
    --easy-color: #10b981;         /* Green */
    --medium-color: #f59e0b;       /* Yellow/Amber */
    --hard-color: #ef4444;         /* Red */
}
```

#### Key Sections
1. **Global Styles** - Font, body, defaults
2. **Header** - Title styling
3. **Navigation** - Menu styling
4. **Input Section** - Textarea and file upload
5. **Results Display** - Cards and stats
6. **Chart Section** - Chart container sizing
7. **History Table** - Table styling
8. **Responsive Design** - Mobile breakpoints (768px, 480px)

#### Important Classes
- `.input-section` - Input container
- `.stat-card` - Individual statistic card
- `.difficulty-badge` - Overall difficulty display
- `.history-table` - Analysis history table
- `.btn-primary` - Main action button

### `static/script.js` - Frontend Logic

#### Key Functions

**`analyzeQuestion()`**
- Validates input
- Sends POST request to `/analyze`
- Handles response and errors
- Displays results

**`displayResults(data)`**
- Updates statistics in DOM
- Updates difficulty badge
- Calls chart creation function

**`createChart(easyCount, mediumCount, hardCount)`**
- Creates Chart.js bar chart
- Shows question distribution
- Destroys previous chart if exists
- Uses color-coded bars

**`resetAnalyzer()`**
- Clears textarea and file input
- Hides results section
- Scrolls to top
- Focuses on input

#### Event Listeners
- File input change
- Analyze button click
- Keyboard shortcuts (Ctrl+Enter)

#### AJAX Communication
```javascript
fetch('/analyze', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({paper_text: paperText})
})
```

---

## 📊 Data Flow Diagram

```
User Input (HTML)
    ↓
JavaScript Validation
    ↓
AJAX POST Request to /analyze
    ↓
Flask analyze_paper()
    ↓
Keyword Classification
    ↓
Calculate Statistics
    ↓
Save to Database
    ↓
Return JSON Response
    ↓
JavaScript displayResults()
    ↓
Update DOM & Create Chart
    ↓
Visual Results to User
```

---

## 🔐 Security Considerations

### Input Validation
- Frontend: HTML5 validation, JavaScript checks
- Backend: Python validation before processing

### Database Security
- Parameterized queries prevent SQL injection
- No sensitive data stored
- File operations use safe methods

### File Handling
- Accept only `.txt` files
- Validate file size (configurable)
- Read as text, no binary execution

---

## 🧪 Testing Guide

### Unit Testing Example

```python
# Test classification
def test_classify_question():
    assert classify_question_difficulty("Define photosynthesis") == "easy"
    assert classify_question_difficulty("Explain the process") == "medium"
    assert classify_question_difficulty("Analyze the impact") == "hard"

# Test analysis
def test_analyze_paper():
    paper = "Define X\nExplain Y\nAnalyze Z"
    result = analyze_paper(paper)
    assert result['total_questions'] == 3
    assert result['easy_count'] == 1
    assert result['medium_count'] == 1
    assert result['hard_count'] == 1
```

### Manual Testing Checklist

- [ ] Paste sample questions
- [ ] Upload .txt file
- [ ] Verify analysis results
- [ ] Check chart display
- [ ] View analysis history
- [ ] Test with edge cases (empty, no keywords)
- [ ] Test responsive design on mobile
- [ ] Verify database persistence
- [ ] Test file format validation

---

## 🚀 Performance Optimization Tips

### Frontend Optimization
```javascript
// Debounce frequent operations
function debounce(func, delay) {
    let timeoutId;
    return function(...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => func(...args), delay);
    };
}
```

### Backend Optimization
```python
# Index database for faster queries
cursor.execute('CREATE INDEX idx_timestamp ON analysis_history(timestamp)')

# Limit query results for pagination
cursor.execute('SELECT * FROM analysis_history ORDER BY timestamp DESC LIMIT 50')
```

### CSS Performance
- Minimize reflows by grouping DOM changes
- Use CSS transforms instead of position for animations
- Lazy load images if added in future

---

## 🔄 Extending the Application

### Adding New Difficulty Levels

Edit `DIFFICULTY_KEYWORDS` in `app.py`:
```python
DIFFICULTY_KEYWORDS = {
    'entry': ['list', 'name'],        # New level
    'intermediate': ['explain'],      # Renamed
    'advanced': ['analyze'],          # Renamed
    'expert': ['criticize', 'evaluate']  # New level
}
```

### Adding Export Functionality

```python
@app.route('/export/<int:analysis_id>')
def export_analysis(analysis_id):
    # Fetch from database
    # Generate PDF/CSV
    # Return file
    pass
```

### Adding User Accounts

```python
# Add to database schema
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    email TEXT
)

# Add authentication
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)
```

---

## 🐛 Debugging Tips

### Enable Debug Logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug(f"Analyzing: {paper_text[:50]}...")
```

### Browser DevTools
- Open with F12 or Right-click → Inspect
- Console tab for JavaScript errors
- Network tab to inspect requests
- Application tab to view local storage

### Flask Debug Toolbar
```bash
pip install flask-debugtoolbar
```

### Database Inspection
Install DB browser:
```bash
pip install sqlite3  # Built-in
# Or use: https://sqlitebrowser.org/
```

---

## 📚 Learning Resources

### Flask Documentation
- Official: https://flask.palletsprojects.com/
- Quickstart: https://flask.palletsprojects.com/quickstart/

### JavaScript & DOM
- MDN Web Docs: https://developer.mozilla.org/
- Chart.js Docs: https://www.chartjs.org/

### SQLite
- Official: https://www.sqlite.org/docs.html

### CSS
- MDN CSS: https://developer.mozilla.org/en-US/docs/Web/CSS/

---

## 🔮 Future Enhancement Ideas

- [ ] User authentication & personal dashboards
- [ ] PDF file upload support
- [ ] Advanced NLP for better classification
- [ ] Export to CSV/PDF
- [ ] Statistics dashboard
- [ ] Difficulty trend analysis
- [ ] Question suggestion engine
- [ ] Multi-language support
- [ ] Mobile app version
- [ ] Database optimization for large datasets

---

## 📝 Code Style Guidelines

### Python
```python
# Follow PEP 8
# Use meaningful variable names
# Add docstrings to functions
# Keep functions to < 50 lines

def analyze_paper(paper_text):
    """
    Analyze a question paper.
    
    Args:
        paper_text (str): The full question paper
        
    Returns:
        dict: Analysis results
    """
    pass
```

### JavaScript
```javascript
// Use camelCase for functions/variables
// Use const/let instead of var
// Add comments for complex logic
// Keep functions focused

function analyzeQuestion() {
    // Implementation
}
```

### HTML/CSS
```html
<!-- Use semantic HTML -->
<!-- Use descriptive IDs/classes -->
<!-- Indent properly -->
<!-- BEM naming convention for classes -->

<div class="input-section__field">
```

---

## 🤝 Contributing Guidelines

1. **Fork** the repository
2. **Create** a feature branch
3. **Make** changes with clear commits
4. **Test** thoroughly
5. **Submit** a pull request
6. **Describe** your changes

---

## 📄 License

This project is open source and free to use, modify, and distribute for educational purposes.

---

**Happy Coding! 💻**

For questions or issues, refer to the README and INSTALLATION guides.
