# Multi-Format File Support Guide
## Flask Question Paper Analyzer - PDF, DOCX, Images (OCR)

---

## Installation Instructions

Your `app.py` already has complete support for **PDF**, **DOCX**, **Text**, and **Images (OCR)**. Follow these steps to ensure all libraries are installed:

### Step 1: Activate Virtual Environment

```powershell
cd c:\Users\balar\OneDrive\Documents\QPA

# Activate venv
.\venv\Scripts\Activate.ps1
```

### Step 2: Install All Required Libraries

```bash
pip install -r requirements.txt
```

Or install individually:

```bash
pip install Flask==2.3.3
pip install Werkzeug==2.3.7
pip install pdfplumber==0.10.3
pip install python-docx==0.8.11
pip install Pillow==10.0.0
pip install pytesseract==0.3.10
```

### Step 3: Install Tesseract-OCR (Windows-Specific)

For **image OCR support** (JPG/PNG), you need the Tesseract executable:

**Option A: Using Chocolatey (Recommended)**
```powershell
choco install tesseract
```

**Option B: Manual Download**
1. Download from: https://github.com/UB-Mannheim/tesseract/wiki
2. Run the installer (select all language options)
3. Default installation path: `C:\Program Files\Tesseract-OCR`

**Option C: Verify Installation**
```powershell
tesseract --version
```

---

## Feature Overview

Your app now supports:

| Format | Library | Details |
|--------|---------|---------|
| **TXT** | Built-in | Direct file reading (UTF-8) |
| **PDF** | `pdfplumber` | Multi-page extraction, table support |
| **DOCX** | `python-docx` | Paragraphs + tables extraction |
| **JPG/PNG** | `pytesseract` + `Pillow` | OCR text extraction from images |

---

## How It Works

### File Upload Flow

```
User uploads file
        ↓
Flask receives file (POST /analyze)
        ↓
Checks file extension (allowed_file)
        ↓
extract_text_from_file() routes to appropriate extractor:
        ├─ .txt → extract_text_from_txt()
        ├─ .pdf → extract_text_from_pdf()
        ├─ .docx → extract_text_from_docx()
        └─ .jpg/.png → extract_text_from_image() [OCR]
        ↓
Analyzes extracted text (analyze_paper)
        ↓
Saves to history.json with metadata
        ↓
Returns JSON response with results
```

### Function Architecture

**Main Entry Point:**
```python
extract_text_from_file(file_path, filename)
    → Determines file type
    → Calls appropriate extraction function
    → Returns full text content
    → Handles errors gracefully
```

**Individual Extractors:**

1. **extract_text_from_txt()**
   - Opens file with UTF-8 encoding
   - Returns raw text content

2. **extract_text_from_pdf()**
   - Opens PDF with pdfplumber
   - Iterates through all pages
   - Extracts text from each page
   - Combines into single string

3. **extract_text_from_docx()**
   - Opens DOCX with python-docx
   - Extracts paragraphs
   - Extracts table content
   - Combines all text

4. **extract_text_from_image()**
   - Opens image with Pillow
   - Converts to grayscale (better OCR)
   - Uses pytesseract.image_to_string()
   - Returns recognized text

---

## Error Handling

Each extraction function includes try-except blocks:

```python
try:
    [Extraction logic]
    if not text.strip():
        raise Exception("No text extracted")
    return text
except Exception as e:
    raise Exception(f"Error message: {str(e)}")
```

**User-Friendly Error Messages:**
- "PDF support not installed. Install: pip install pdfplumber"
- "DOCX support not installed. Install: pip install python-docx"
- "Image OCR support not installed. Install: pip install Pillow pytesseract"
- "No text could be extracted from image (OCR failed). Try a clearer image."

---

## API Response Format

When you upload/analyze a file:

```json
{
  "total_questions": 25,
  "easy_count": 8,
  "medium_count": 10,
  "hard_count": 7,
  "easy_percentage": 32.0,
  "medium_percentage": 40.0,
  "hard_percentage": 28.0,
  "overall_difficulty": "Moderate Paper"
}
```

**Saved to history.json:**
```json
{
  "filename": "Sample_Physics_Paper.pdf",
  "date": "2026-02-12 15:30",
  "level": "Moderate Paper",
  "easy_count": 8,
  "easy": 32.0,
  "medium_count": 10,
  "medium": 40.0,
  "hard_count": 7,
  "hard": 28.0,
  "total_questions": 25
}
```

---

## Testing

### Test Case 1: Text Input
```
Input: "1. Define photosynthesis\n2. Explain the process\n3. Analyze the energy transfer"
Expected: Easy=1, Medium=1, Hard=1
```

### Test Case 2: PDF Upload
```
Upload: Sample question paper (multipage PDF)
Expected: Extracts text from all pages
```

### Test Case 3: DOCX Upload
```
Upload: Question paper in Word format
Expected: Extracts paragraphs + table content
```

### Test Case 4: Image OCR
```
Upload: Screenshot of handwritten questions (PNG/JPG)
Expected: OCR converts image to text, analyzes
```

---

## Troubleshooting

### Issue: "PDF support not installed"
```bash
pip install pdfplumber==0.10.3
```

### Issue: "DOCX support not installed"
```bash
pip install python-docx==0.8.11
```

### Issue: "Image OCR support not installed"
```bash
pip install Pillow==10.0.0 pytesseract==0.3.10
```

### Issue: OCR not working on images
```
1. Install Tesseract executable:
   choco install tesseract
   
2. Test: tesseract --version
   
3. Try with clearer image/screenshot
```

### Issue: File upload returns 413 error
```
File is too large. Max file size: 50MB
(Adjust MAX_FILE_SIZE in app.py if needed)
```

---

## Code Location Reference

**File Extraction Functions:**
- `extract_text_from_txt()` → Line ~60
- `extract_text_from_pdf()` → Line ~70
- `extract_text_from_docx()` → Line ~90
- `extract_text_from_image()` → Line ~115
- `extract_text_from_file()` → Line ~140 (Main router)

**Analysis Route:**
- `/analyze` endpoint → Line ~430
- History integration → Line ~475

**History Management:**
- `/history` endpoint → Line ~505
- `/clear_all_history` endpoint → Line ~525

---

## Supported File Types

| Extension | MIME Type | Status |
|-----------|-----------|--------|
| `.txt` | `text/plain` | ✅ Ready |
| `.pdf` | `application/pdf` | ✅ Ready |
| `.docx` | `application/vnd.openxmlformats-officedocument.wordprocessingml.document` | ✅ Ready |
| `.jpg` / `.jpeg` | `image/jpeg` | ✅ Ready (OCR) |
| `.png` | `image/png` | ✅ Ready (OCR) |

---

## Quick Start

1. **Install libraries:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Install Tesseract (Windows):**
   ```powershell
   choco install tesseract
   ```

3. **Run app:**
   ```bash
   python app.py
   ```

4. **Test upload:**
   - Go to `http://localhost:5000`
   - Upload a PDF/DOCX/Image
   - Check `/history` for results

---

## Production Ready ✅

Your application is fully configured for:
- ✅ Multi-format file support
- ✅ Graceful error handling
- ✅ Data persistence (history.json)
- ✅ Unified extraction pipeline
- ✅ User-friendly error messages
- ✅ OCR support for images

**No further configuration needed!**
