# pip Install & Command Reference

## quickest Installation

Copy and run this single command:

```bash
pip install -r requirements.txt
```

---

## Individual Package Installation

If you need to install packages separately:

### Flask Web Framework
```bash
pip install Flask==2.3.3
```

### PDF Extraction
```bash
pip install pdfplumber==0.10.3
```

### Word Document Reading
```bash
pip install python-docx==0.8.11
```

### Image Processing
```bash
pip install Pillow==10.0.0
```

### OCR Library (for image text extraction)
```bash
pip install pytesseract==0.3.10
```

### Web Server
```bash
pip install Werkzeug==2.3.7
```

---

## All in One Line

```bash
pip install Flask==2.3.3 Werkzeug==2.3.7 pdfplumber==0.10.3 python-docx==0.8.11 Pillow==10.0.0 pytesseract==0.3.10
```

---

## Tesseract OCR (Optional - Windows)

For image OCR support:

```powershell
choco install tesseract
```

Or download from: https://github.com/UB-Mannheim/tesseract/wiki

---

## Verify Installation

After installing, verify all libraries work:

```bash
python test_extraction.py
```

Expected output:
```
✅ Flask imported successfully
✅ pdfplumber imported successfully
✅ python-docx imported successfully
✅ Pillow imported successfully
✅ pytesseract imported successfully
✅ Werkzeug imported successfully
```

---

## Run the Application

```bash
python app.py
```

Then open: http://localhost:5000

---

## Requirements File

**File:** `requirements.txt`

```
Flask==2.3.3
Werkzeug==2.3.7
pdfplumber==0.10.3
python-docx==0.8.11
Pillow==10.0.0
pytesseract==0.3.10
```

---

## Package Purposes

| Package | Version | Purpose |
|---------|---------|---------|
| Flask | 2.3.3 | Web framework for the app |
| Werkzeug | 2.3.7 | WSGI utility library |
| pdfplumber | 0.10.3 | Extract text from PDF files |
| python-docx | 0.8.11 | Read .docx (Word) files |
| Pillow | 10.0.0 | Image processing & manipulation |
| pytesseract | 0.3.10 | Python wrapper for Tesseract OCR |

---

## Supported File Formats

After installation, you can upload and analyze:

- ✅ `.txt` files (text documents)
- ✅ `.pdf` files (PDF documents - multipage)
- ✅ `.docx` files (Word documents)
- ✅ `.jpg` files (images - requires Tesseract)
- ✅ `.jpeg` files (images - requires Tesseract)
- ✅ `.png` files (images - requires Tesseract)

---

## Troubleshooting Installation

### Issue: "Permission Denied"
```bash
pip install --user -r requirements.txt
```

### Issue: Outdated pip
```bash
python -m pip install --upgrade pip
```

### Issue: Need to reinstall
```bash
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

### Issue: Check what's installed
```bash
pip list
```

### Issue: Show package details
```bash
pip show pdfplumber
pip show python-docx
pip show pytesseract
```

---

## Complete Setup Workflow

```powershell
# 1. Navigate to project folder
cd c:\Users\balar\OneDrive\Documents\QPA\question-paper-analyzer

# 2. Activate virtual environment
..\venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install -r requirements.txt

# 4. Verify installation
python test_extraction.py

# 5. (Optional) Install Tesseract for OCR
choco install tesseract

# 6. Run the application
python app.py

# 7. Open browser
http://localhost:5000
```

---

## What Gets Installed

When you run `pip install -r requirements.txt`, these packages are installed:

```
✅ Flask 2.3.3
✅ Werkzeug 2.3.7
✅ Jinja2 3.1.6 (dependency of Flask)
✅ itsdangerous 2.2.0 (dependency of Flask)
✅ click 8.3.1 (dependency of Flask)
✅ blinker 1.9.0 (dependency of Flask)
✅ MarkupSafe 3.0.3 (dependency of Werkzeug)
✅ pdfplumber 0.10.3
✅ pdfminer.six 20221105 (dependency of pdfplumber)
✅ pypdfium2 5.4.0 (dependency of pdfplumber)
✅ python-docx 0.8.11
✅ lxml 6.0.2 (dependency of python-docx)
✅ Pillow 10.0.0
✅ pytesseract 0.3.10
✅ packaging 26.0 (dependency of pytesseract)
```

---

## After Installation

✅ **All packages installed? Then:**

```bash
python app.py
```

Application starts at: **http://localhost:5000**

You can now:
- ✅ Upload PDF files
- ✅ Upload DOCX files
- ✅ Analyze text
- ✅ Upload images (if Tesseract installed)
- ✅ View history
- ✅ Export analytics

---

## Production Setup (Optional)

For production deployment:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

---

## Check Versions

Verify correct versions are installed:

```bash
pip show Flask | grep Version
pip show pdfplumber | grep Version
pip show python-docx | grep Version
pip show Pillow | grep Version
pip show pytesseract | grep Version
```

---

## Need Help?

1. Run verification: `python test_extraction.py`
2. Check documentation files in this folder
3. Verify all packages with: `pip list`
4. Reinstall if needed: `pip install -r requirements.txt --force-reinstall`

---

## ✅ You're All Set!

After running:
```bash
pip install -r requirements.txt
python app.py
```

Visit: http://localhost:5000 and start analyzing question papers! 🚀

For OCR support, also run:
```bash
choco install tesseract
```
