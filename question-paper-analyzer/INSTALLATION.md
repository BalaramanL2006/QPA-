# Installation & Setup Guide

Complete step-by-step guide to set up and run the Question Paper Difficulty Analyzer.

## Prerequisites

Before you begin, ensure you have:
- Windows 10/11, macOS, or Linux
- Python 3.7 or higher installed
- At least 100 MB of free disk space
- A modern web browser (Chrome, Firefox, Safari, Edge)

### Check Python Installation

Open a terminal/command prompt and run:

```bash
python --version
```

or on macOS/Linux:

```bash
python3 --version
```

You should see output like `Python 3.9.0` or higher.

If Python is not installed, download it from: https://www.python.org/

---

## Quick Setup (Automatic)

### On Windows:

1. Navigate to the `question-paper-analyzer` folder
2. Double-click `run.bat`
3. The application will automatically:
   - Create a virtual environment
   - Install all dependencies
   - Start the Flask server
4. Open your browser to: http://127.0.0.1:5000

### On macOS/Linux:

1. Open Terminal in the `question-paper-analyzer` folder
2. Run:
   ```bash
   chmod +x run.sh
   ./run.sh
   ```
3. The application will automatically set up and start
4. Open your browser to: http://127.0.0.1:5000

---

## Manual Setup (Step-by-Step)

### Step 1: Open Terminal/Command Prompt

**Windows:**
- Press `Win + R`, type `cmd`, and press Enter
- Or search for "Command Prompt" in the Start menu

**macOS:**
- Press `Cmd + Space`, type `Terminal`, and press Enter

**Linux:**
- Press `Ctrl + Alt + T`

### Step 2: Navigate to Project Directory

```bash
cd "path/to/question-paper-analyzer"
```

Replace `path/to/` with your actual folder path. For example:
- Windows: `cd "C:\Users\YourName\OneDrive\Documents\QPA\question-paper-analyzer"`
- macOS: `cd ~/Documents/QPA/question-paper-analyzer`

### Step 3: Create Virtual Environment

This isolates the project dependencies from your system Python.

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

After activation, you should see `(venv)` at the start of your terminal line.

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs Flask and other required packages.

### Step 5: Run the Application

```bash
python app.py
```

or on macOS/Linux:

```bash
python3 app.py
```

You should see output like:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

### Step 6: Access the Application

Open your web browser and go to: **http://127.0.0.1:5000**

---

## Testing the Application

### Using Sample Questions

1. Open `SAMPLE_QUESTIONS.txt` in a text editor
2. Copy the content
3. Paste it into the text area on the home page
4. Click "Analyze Question Paper"
5. View the results and chart

Expected Results:
- Easy: 7 questions (25.93%)
- Medium: 6 questions (22.22%)
- Hard: 6 questions (22.22%)
- Mixed: 10 questions (29.63%)
- Overall: **Moderate Paper** (balanced distribution)

### Using Your Own Questions

1. Create a `.txt` file with one question per line
2. Use action verbs from Easy/Medium/Hard lists
3. Upload the file or paste the content
4. Click Analyze

---

## Deactivating Virtual Environment

When you're done, to deactivate the virtual environment:

**On Windows:**
```bash
venv\Scripts\deactivate
```

**On macOS/Linux:**
```bash
deactivate
```

---

## Troubleshooting

### Error: "Python is not found" or "command not found: python3"

**Solution:**
- Ensure Python is installed correctly
- On Windows, check "Add Python to PATH" during installation
- Use the full path to Python executable
- Restart your terminal after installing Python

### Error: "No module named 'flask'"

**Solution:**
```bash
pip install -r requirements.txt
```

Make sure:
- Virtual environment is activated (you see `(venv)` in terminal)
- You're in the project directory
- You have internet connection

### Error: "Address already in use"

**Solution:**
Port 5000 is being used by another application.

Option 1: Stop the other application
Option 2: Change the port in `app.py`:
```python
if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='127.0.0.1', port=8000)  # Changed from 5000 to 8000
```

Then access at: http://127.0.0.1:8000

### Error: "Database locked"

**Solution:**
- Close the application and restart it
- Delete `database.db` file (it will be recreated)
- Make sure only one instance of the app is running

### Error: "FileNotFoundError: templates/index.html"

**Solution:**
- Ensure you're running the app from the correct directory
- The command should be run from `question-paper-analyzer` folder
- Check that `templates` folder exists and contains all HTML files

### Port 5000 Won't Open in Browser

**Solution:**
- Wait a few seconds for Flask to fully start
- Check that you see "Running on http://127.0.0.1:5000" in terminal
- Try a different browser or clear browser cache
- Try accessing with IP: http://localhost:5000

---

## System Requirements

| Component | Requirement |
|-----------|------------|
| OS | Windows 7+, macOS 10.12+, Linux |
| Python | 3.7+ |
| RAM | 512 MB minimum (1 GB recommended) |
| Disk Space | 100 MB |
| Browser | Any modern browser (2020+) |
| Internet | Not required (runs locally) |

---

## File Permissions (macOS/Linux)

If you get permission errors on macOS/Linux:

```bash
chmod +x run.sh
chmod -R 755 .
```

---

## Next Steps

Once the application is running:

1. **Analyze Questions** - Use the home page to analyze question papers
2. **View History** - Check previous analyses in the history page
3. **Customize Keywords** - Edit difficulty keywords in `app.py`
4. **Modify Settings** - Adjust configuration in `config.py`

---

## Uninstalling

To completely remove the application:

1. Delete the project folder
2. No system-wide changes were made
3. If you want to free up virtual environment space, delete the `venv` folder

---

## Support & Help

If you encounter issues:

1. Check the Troubleshooting section above
2. Review the README.md file
3. Check Flask terminal output for error messages
4. Verify all files are present in the project structure
5. Ensure you followed the exact steps in order

---

**Successfully Installed! 🎉**

You're now ready to analyze question papers. Happy analyzing!
