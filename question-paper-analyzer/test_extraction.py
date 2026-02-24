"""
Quick validation script to test all file extraction functions.
Run this to verify your setup before using the app.

Usage:
    python test_extraction.py
"""

import os
import sys

print("=" * 60)
print("Flask Question Paper Analyzer - Library Check")
print("=" * 60)

# Test 1: Flask & Core
print("\n[1] Core Libraries...")
try:
    import flask
    print("  ✅ Flask imported successfully")
except ImportError as e:
    print(f"  ❌ Flask not found: {e}")
    sys.exit(1)

# Test 2: PDF Support
print("\n[2] PDF Support (pdfplumber)...")
try:
    import pdfplumber
    print("  ✅ pdfplumber imported successfully")
    print(f"     Version: {pdfplumber.__version__}")
except ImportError:
    print("  ⚠️  pdfplumber NOT installed")
    print("     Install: pip install pdfplumber")

# Test 3: DOCX Support
print("\n[3] DOCX Support (python-docx)...")
try:
    from docx import Document
    print("  ✅ python-docx imported successfully")
except ImportError:
    print("  ⚠️  python-docx NOT installed")
    print("     Install: pip install python-docx")

# Test 4: Image Support (Pillow)
print("\n[4] Image Processing (Pillow)...")
try:
    from PIL import Image
    print("  ✅ Pillow imported successfully")
    print(f"     Version: {Image.__version__}")
except ImportError:
    print("  ⚠️  Pillow NOT installed")
    print("     Install: pip install Pillow")

# Test 5: OCR Support (pytesseract)
print("\n[5] OCR Support (pytesseract)...")
try:
    import pytesseract
    print("  ✅ pytesseract imported successfully")
    
    # Check if Tesseract executable is available
    try:
        version = pytesseract.get_tesseract_version()
        print(f"     Tesseract found: {version}")
    except Exception as e:
        print("  ⚠️  Tesseract executable not found")
        print("     Install Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki")
        print("     Windows (Chocolatey): choco install tesseract")
except ImportError:
    print("  ⚠️  pytesseract NOT installed")
    print("     Install: pip install pytesseract")

# Test 6: Other Dependencies
print("\n[6] Other Dependencies...")
try:
    import werkzeug
    print("  ✅ Werkzeug imported successfully")
except ImportError:
    print("  ⚠️  Werkzeug NOT installed")

print("\n" + "=" * 60)
print("Verification Complete!")
print("=" * 60)

print("""
Quick Install Command:
  pip install -r requirements.txt
  
For OCR (Windows):
  choco install tesseract
  
Or download manually:
  https://github.com/UB-Mannheim/tesseract/wiki
""")
