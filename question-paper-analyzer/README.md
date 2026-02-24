# Question Paper Difficulty Analyzer

A modern, full-stack web application that analyzes exam question papers and classifies questions into Easy, Medium, and Hard difficulty levels based on predefined action verbs.

## 📋 Features

✅ **Text Input & File Upload**
- Paste question papers directly in a text area
- Upload `.txt` files for analysis
- Clean, intuitive user interface

✅ **Intelligent Analysis**
- Detects action verbs to classify question difficulty
- Easy: define, list, identify, name, what
- Medium: explain, describe, summarize, discuss
- Hard: analyze, evaluate, justify, compare, criticize

✅ **Comprehensive Results**
- Shows count and percentage of Easy/Medium/Hard questions
- Displays total question count
- Determines overall paper difficulty (Easy/Moderate/Tough)

✅ **Visual Representation**
- Interactive bar chart using Chart.js
- Color-coded difficulty levels
- Real-time result updates

✅ **Analysis History**
- SQLite database stores all previous analyses
- View historical data with timestamps
- Track multiple papers over time

## 🛠️ Tech Stack

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Backend**: Python with Flask
- **Database**: SQLite
- **Charting**: Chart.js
- **Server**: Flask development server

## 📁 Project Structure

```
question-paper-analyzer/
│
├── app.py                          # Flask application & routes
├── requirements.txt                # Python dependencies
├── database.db                     # SQLite database (auto-created)
│
├── templates/
│   ├── index.html                 # Home page with analyzer
│   └── history.html               # Analysis history page
│
└── static/
    ├── style.css                  # Modern UI styling
    └── script.js                  # Frontend functionality
```

## 🚀 Quick Start Guide

### Prerequisites

- Python 3.7 or higher installed
- pip (Python package manager)
- A modern web browser

### Installation Steps

#### 1. Navigate to the project directory

```bash
cd question-paper-analyzer
```

#### 2. Create a virtual environment (Recommended)

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install dependencies

```bash
pip install -r requirements.txt
```

#### 4. Run the application

```bash
python app.py
```

You should see output like:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

#### 5. Open in your browser

Visit: **http://127.0.0.1:5000**

## 📖 How to Use

### 1. **Analyze a Question Paper**
   - Go to the **Home** page
   - Either paste your questions in the text area OR upload a `.txt` file
   - Each question should be on a new line
   - Click **"Analyze Question Paper"**

### 2. **View Results**
   - See statistics: Easy/Medium/Hard counts and percentages
   - View a visual bar chart of difficulty distribution
   - Check the overall paper difficulty classification
   - Results are automatically saved to history

### 3. **View Analysis History**
   - Click on **"Analysis History"** in the navigation
   - See all previous analyses with dates and details
   - Track trends in question paper difficulty

## 🧠 How Difficulty Classification Works

The application scans each question for action verbs:

| Difficulty | Keywords |
|-----------|----------|
| **Easy** | define, list, identify, name, what |
| **Medium** | explain, describe, summarize, discuss |
| **Hard** | analyze, evaluate, justify, compare, criticize |

**Example:**
- "Define photosynthesis" → Easy (keyword: "define")
- "Explain the carbon cycle" → Medium (keyword: "explain")
- "Analyze climate change impacts" → Hard (keyword: "analyze")

## 📊 Overall Difficulty Categories

- **Easy Paper**: > 50% Easy questions
- **Moderate Paper**: Balanced distribution
- **Tough Paper**: > 50% Hard questions

## 🎨 Features Highlight

### Modern UI Design
- Gradient backgrounds with smooth animations
- Color-coded difficulty levels (Green/Yellow/Red)
- Responsive design for all screen sizes
- Smooth transitions and hover effects

### User-Friendly Interface
- Clear instructions and helper text
- Loading states and error messages
- One-click file upload
- Keyboard shortcuts (Ctrl+Enter to analyze)

### Database Management
- Auto-creation of SQLite database
- Efficient query execution
- Timestamp tracking for all analyses
- Full history retrieval without limits

## 🔧 Development Tips

### Customizing Difficulty Keywords

Edit the `DIFFICULTY_KEYWORDS` dictionary in `app.py`:

```python
DIFFICULTY_KEYWORDS = {
    'easy': ['define', 'list', 'identify', 'name', 'what'],
    'medium': ['explain', 'describe', 'summarize', 'discuss'],
    'hard': ['analyze', 'evaluate', 'justify', 'compare', 'criticize']
}
```

### Changing the Port

Modify the last line in `app.py`:

```python
if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='127.0.0.1', port=8000)  # Change 5000 to 8000
```

### Disabling Debug Mode (for Production)

Change in `app.py`:
```python
app.run(debug=False, host='0.0.0.0', port=5000)
```

## �часто 🐛 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'flask'"

**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: "Address already in use"

**Solution:**
- Another application is using port 5000
- Change the port in `app.py` or stop the other application

### Issue: Database errors

**Solution:**
- Delete `database.db` file
- Restart the application (it will recreate the database)

### Issue: File upload not working

**Solution:**
- Ensure `.txt` file format
- Check file size (must be reasonable)
- Try pasting content in text area instead

## 📁 File Descriptions

### `app.py`
- Flask configuration and routes
- Database initialization and management
- Question analysis logic
- API endpoints for frontend

### `templates/index.html`
- Home page layout
- Text area and file upload UI
- Results display section
- Responsive grid layout

### `templates/history.html`
- Analysis history table
- Date/time display
- Statistics overview
- Empty state handling

### `static/style.css`
- 400+ lines of modern CSS
- Gradient animations
- Responsive breakpoints
- Color-coded UI elements

### `static/script.js`
- Async analysis request handling
- Chart.js integration
- File upload management
- Form validation

## 🔐 Security Notes

- Input validation on both frontend and backend
- SQL injection prevention through parameterized queries
- No sensitive data stored
- Safe file handling

## 📈 Future Enhancement Ideas

- [ ] Support for PDF file uploads
- [ ] Question paper templates/examples
- [ ] Export analysis as PDF/CSV
- [ ] Question-level difficulty display
- [ ] Suggested question difficulty modifications
- [ ] Statistics visualization (histograms, etc.)
- [ ] User accounts and authentication
- [ ] Advanced NLP for better classification

## 📝 Example Question Papers

### Example 1: Easy Paper
```
1. Define osmosis
2. List the types of ecosystems
3. What is photosynthesis?
4. Identify the planets in our solar system
5. Name the organs in the digestive system
```

### Example 2: Balanced Paper
```
1. Define cellular respiration
2. Explain the water cycle
3. Describe the structure of DNA
4. Analyze the causes of deforestation
5. Compare mitochondrion and chloroplast
6. Discuss the importance of biodiversity
7. Evaluate environmental conservation methods
```

### Example 3: Tough Paper
```
1. Analyze the implications of genetic engineering
2. Evaluate the effectiveness of current climate policies
3. Justify the necessity of endangered species protection
4. Compare different evolutionary theories
5. Criticize the limitations of traditional medicine
```

## 🤝 Contributing

This is a complete, standalone project. Feel free to:
- Modify the UI/UX
- Add new difficulty keywords
- Implement additional features
- Customize colors and styling

## 📄 License

Free to use and modify for educational purposes.

## 🎓 Learning Outcomes

By working with this project, you'll learn:
- Flask web framework basics
- RESTful API design
- SQLite database management
- Frontend-backend communication (AJAX/Fetch API)
- HTML/CSS/JavaScript best practices
- Chart.js for data visualization
- File handling in web applications

## 💬 Support

For issues or questions:
1. Check the Troubleshooting section
2. Review the code comments
3. Verify Flask is running correctly
4. Check browser console for JavaScript errors

---

**Happy Analyzing! 🎉**

Built with ❤️ for educational purposes
