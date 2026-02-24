# Installation & Setup Guide

## Quick Install Command

Run this single command to install all required dependencies:

```bash
pip install -r requirements.txt
```

**Or install individually:**
```bash
pip install Flask==2.3.3 Werkzeug==2.3.7 pdfplumber==0.10.3 python-docx==0.8.11 Pillow==10.0.0 pytesseract==0.3.10
```

---

## Verification

After installation, verify everything is working:

```bash
python test_extraction.py
```

Expected output:
```
✅ Flask imported successfully
✅ pdfplumber imported successfully (Version: 0.10.3)
✅ python-docx imported successfully
✅ Pillow imported successfully (Version: 10.0.0)
✅ pytesseract imported successfully
⚠️  Tesseract executable not found (Optional)
✅ Werkzeug imported successfully
```

---

## Optional: Tesseract OCR Installation

For **image OCR support** (reading text from PNG/JPG screenshots):

### Windows with Chocolatey (Recommended)
```powershell
choco install tesseract
```

### Windows Manual Installation
1. Download: https://github.com/UB-Mannheim/tesseract/wiki/Downloads
2. Run installer
3. Accept prompts (install language packs if desired)
4. Default location: `C:\Program Files\Tesseract-OCR`

### Verify Tesseract Installation
```powershell
tesseract --version
```

---

## Requirements File

**Location:** `requirements.txt`

**Contents:**
```
Flask==2.3.3
Werkzeug==2.3.7
pdfplumber==0.10.3
python-docx==0.8.11
Pillow==10.0.0
pytesseract==0.3.10
```

---

## What Each Package Does

| Package | Version | Purpose |
|---------|---------|---------|
| **Flask** | 2.3.3 | Web framework for the application |
| **Werkzeug** | 2.3.7 | Flask WSGI utility library |
| **pdfplumber** | 0.10.3 | Extract text from PDF files |
| **python-docx** | 0.8.11 | Read DOCX (Word) files |
| **Pillow** | 10.0.0 | Image processing and manipulation |
| **pytesseract** | 0.3.10 | Python wrapper for Tesseract OCR |

---

## Installation Steps

### Step 1: Activate Virtual Environment
```powershell
cd c:\Users\balar\OneDrive\Documents\QPA
.\venv\Scripts\Activate.ps1
```

### Step 2: Install Dependencies
```bash
cd question-paper-analyzer
pip install -r requirements.txt
```

### Step 3: Verify Installation
```bash
python test_extraction.py
```

### Step 4: (Optional) Install Tesseract
```powershell
choco install tesseract
```

### Step 5: Run the Application
```bash
python app.py
```

### Step 6: Access the Application
Open browser and go to:
```
http://localhost:5000
```

---

## Troubleshooting

### Issue: "No module named 'pdfplumber'"
```bash
pip install pdfplumber==0.10.3
```

### Issue: "No module named 'docx'"
```bash
pip install python-docx==0.8.11
```

### Issue: "No module named 'PIL'"
```bash
pip install Pillow==10.0.0
```

### Issue: "No module named 'pytesseract'"
```bash
pip install pytesseract==0.3.10
```

### Issue: OCR not working on images
```powershell
# Option 1: Install via Chocolatey
choco install tesseract

# Option 2: Manual download and install
# https://github.com/UB-Mannheim/tesseract/wiki
```

### Issue: Permission denied during installation
```bash
pip install --user -r requirements.txt
```

---

## File Support Matrix

| Format | Status | Notes |
|--------|--------|-------|
| `.txt` | ✅ Ready | Direct file reading |
| `.pdf` | ✅ Ready | Multi-page support |
| `.docx` | ✅ Ready | Paragraphs + tables |
| `.jpg` | ⚠️ Optional | Requires Tesseract |
| `.jpeg` | ⚠️ Optional | Requires Tesseract |
| `.png` | ⚠️ Optional | Requires Tesseract |

---

## System Requirements

- **Python:** 3.7+ (3.12 recommended)
- **RAM:** 2GB minimum
- **Disk:** 500MB for dependencies
- **Windows:** 10 or later (other OS compatible)

---

## Post-Installation Check

```bash
# Verify Flask app runs
python app.py

# You should see:
# * Running on http://127.0.0.1:5000
# * Press CTRL+C to quit

# Visit in browser:
http://localhost:5000

# Test file upload:
# - Upload a .txt file → Should work
# - Upload a .pdf file → Should work if pdfplumber installed
# - Upload a .docx file → Should work if python-docx installed
# - Upload a .png file → Works if Tesseract installed
```

---

## Useful Commands

### Upgrade pip
```bash
python -m pip install --upgrade pip
```

### Check installed packages
```bash
pip list
```

### Show package details
```bash
pip show pdfplumber
pip show python-docx
pip show pytesseract
```

### Update all packages
```bash
pip install --upgrade -r requirements.txt
```

### Uninstall all and reinstall
```bash
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

---

## Support Links

- **Flask:** https://flask.palletsprojects.com/
- **pdfplumber:** https://github.com/jsvine/pdfplumber
- **python-docx:** https://github.com/python-openxml/python-docx
- **Pillow:** https://pillow.readthedocs.io/
- **pytesseract:** https://github.com/madmaze/pytesseract
- **Tesseract-OCR:** https://github.com/UB-Mannheim/tesseract/wiki

---

## You're All Set! ✅

When you see this after `pip install -r requirements.txt`:
```
Requirement already satisfied: Flask==2.3.3 in .../venv/lib/site-packages
Requirement already satisfied: pdfplumber==0.10.3 in .../venv/lib/site-packages
Requirement already satisfied: python-docx==0.8.11 in .../venv/lib/site-packages
Requirement already satisfied: Pillow==10.0.0 in .../venv/lib/site-packages
Requirement already satisfied: pytesseract==0.3.10 in .../venv/lib/site-packages
```

**You're ready to go! 🚀**

Next steps:
1. `python app.py`
2. Visit `http://localhost:5000`
3. Upload or analyze a paper
4. Check `/history` for results
