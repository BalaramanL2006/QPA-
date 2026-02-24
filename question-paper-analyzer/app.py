"""
Question Paper Difficulty Analyzer - Flask Backend (Enhanced Edition)
This application analyzes question papers and classifies questions based on difficulty level.
Supports multiple file formats: TXT, PDF, DOCX, and Images (JPG, PNG) with OCR.
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for  # type: ignore[import]
import sqlite3
import os
from datetime import datetime
import json
from werkzeug.utils import secure_filename  # type: ignore[import]
from werkzeug.security import generate_password_hash, check_password_hash  # type: ignore[import]
import traceback
import re
from functools import wraps
from dotenv import load_dotenv  # type: ignore[import]
import requests

# Load environment variables
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY")

# Debug logging
print(f"HF Key Loaded: {HUGGINGFACE_API_KEY is not None}")

if not HUGGINGFACE_API_KEY:
    print("\n" + "!"*50)
    print("ERROR: HUGGINGFACE_API_KEY is missing from .env file!")
    print("AI Analysis features will not work.")
    print("!"*50 + "\n")

if not FLASK_SECRET_KEY:
    print("\n" + "!"*50)
    print("CRITICAL ERROR: FLASK_SECRET_KEY is missing from .env file!")
    print("Sessions and security features will NOT function correctly.")
    print("!"*50 + "\n")

# HF API Configuration
HF_MODEL_URL = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
HF_HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

# Direct imports for file handling libraries
import pdfplumber  # type: ignore[import]
from docx import Document  # type: ignore[import]
from PIL import Image  # type: ignore[import]
import pytesseract  # type: ignore[import]

app = Flask(__name__)

# Securely load secret key from environment
app.secret_key = FLASK_SECRET_KEY or "fallback-unsecure-key-for-dev-only"

if not FLASK_SECRET_KEY:
    # Additional warning if using fallback
    app.logger.warning("Using insecure fallback secret key. This is NOT safe for production.")

# Configuration
DATABASE = 'database.db'
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx', 'jpg', 'jpeg', 'png'}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

# Create upload folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Action verbs for difficulty classification
DIFFICULTY_KEYWORDS = {
    'easy': ['define', 'list', 'identify', 'name', 'what', 'write', 'state', 'recall', 'recognize'],
    'medium': ['explain', 'describe', 'summarize', 'discuss', 'illustrate', 'outline', 'distinguish', 'compare'],
    'hard': ['analyze', 'evaluate', 'justify', 'criticize', 'synthesize', 'create', 'assess', 'argue']
}


def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_text(file_path):
    """
    Universal text extraction function for all supported file types.
    
    Supports: .txt, .pdf, .docx, .png, .jpg, .jpeg
    
    Args:
        file_path (str): Path to the file to extract text from
        
    Returns:
        str: Extracted text from the file
        
    Raises:
        Exception: If extraction fails with descriptive error message
    """
    try:
        # Get file extension
        file_ext = file_path.rsplit('.', 1)[1].lower()
        
        # Extract text based on file type
        if file_ext == 'txt':
            # Read plain text file
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            if not text.strip():
                raise Exception("Text file is empty")
            return text
        
        elif file_ext == 'pdf':
            # Extract from PDF using pdfplumber
            text = ""
            try:
                with pdfplumber.open(file_path) as pdf:
                    if len(pdf.pages) == 0:
                        raise Exception("PDF file is empty (no pages found)")
                    
                    for page_num, page in enumerate(pdf.pages):
                        try:
                            page_text = page.extract_text()
                            if page_text:
                                text += page_text + "\n"
                        except Exception as e:
                            print(f"Warning: Could not extract page {page_num + 1}: {str(e)}")
                            continue
                
                if not text.strip():
                    raise Exception("No text could be extracted from PDF. PDF may be image-only or corrupted.")
                return text
            
            except Exception as e:
                if "password" in str(e).lower():
                    raise Exception("PDF is password-protected. Please provide an unprotected PDF.")
                raise Exception(f"PDF extraction failed: {str(e)}")
        
        elif file_ext == 'docx':
            # Extract from DOCX using python-docx
            text = ""
            try:
                doc = Document(file_path)
                
                # Extract all paragraphs
                for paragraph in doc.paragraphs:
                    if paragraph.text.strip():
                        text += paragraph.text + "\n"
                
                # Extract all tables
                for table in doc.tables:
                    for row in table.rows:
                        for cell in row.cells:
                            if cell.text.strip():
                                text += cell.text + "\n"
                
                if not text.strip():  # type: ignore[attr-defined]
                    raise Exception("No text could be extracted from DOCX file")
                return text
            
            except Exception as e:
                raise Exception(f"DOCX extraction failed: {str(e)}")
        
        elif file_ext in {'png', 'jpg', 'jpeg'}:
            # Extract from image using pytesseract OCR
            text = ""
            try:
                # Open image
                image = Image.open(file_path)
                
                # Convert to grayscale for better OCR
                if image.mode != 'L':
                    image = image.convert('L')
                
                # Extract text using Tesseract OCR
                text = pytesseract.image_to_string(image)
                
                if not text.strip():
                    raise Exception("No text detected in image. Try a clearer image or increase contrast.")
                return text
            
            except pytesseract.TesseractNotFoundError:
                raise Exception(
                    "Tesseract OCR not found. Install with: choco install tesseract (Windows) "
                    "or brew install tesseract (Mac) or apt-get install tesseract-ocr (Linux)"
                )
            except Exception as e:
                raise Exception(f"Image OCR failed: {str(e)}")
        
        else:
            raise Exception(f"File type '.{file_ext}' is not supported. Allowed: " + ", ".join(ALLOWED_EXTENSIONS))
    
    except Exception as e:
        raise Exception(f"Failed to extract text from file: {str(e)}")


def init_db():
    """Initialize the SQLite database with required tables."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create analysis history table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS analysis_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
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
    ''')
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            school TEXT,
            mobile TEXT,
            password TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()


def get_connection():
    """Get a database connection."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def classify_question_difficulty(question):
    """
    Classify a single question based on action verbs.
    
    Args:
        question (str): The question text to classify
        
    Returns:
        str: 'easy', 'medium', or 'hard'
    """
    question_lower = question.lower()
    
    # Remove common punctuation and extra spaces for better matching
    question_clean = re.sub(r'[^\w\s]', ' ', question_lower)
    
    # Check for hard keywords first (most specific)
    for keyword in DIFFICULTY_KEYWORDS['hard']:
        if re.search(r'\b' + keyword + r'\b', question_clean):
            return 'hard'
    
    # Check for medium keywords
    for keyword in DIFFICULTY_KEYWORDS['medium']:
        if re.search(r'\b' + keyword + r'\b', question_clean):
            return 'medium'
    
    # Check for easy keywords
    for keyword in DIFFICULTY_KEYWORDS['easy']:
        if re.search(r'\b' + keyword + r'\b', question_clean):
            return 'easy'
    
    # Default to medium if no keywords found
    return 'medium'


def calculate_overall_difficulty(easy_pct, medium_pct, hard_pct):
    """
    Calculate overall difficulty based on percentages.
    
    Rules:
    - If Hard > 35%, overall = 'Hard Paper'
    - If Easy > 50%, overall = 'Easy Paper'
    - Otherwise = 'Moderate Paper'
    
    Args:
        easy_pct (float): Easy percentage
        medium_pct (float): Medium percentage
        hard_pct (float): Hard percentage
        
    Returns:
        str: Overall difficulty level
    """
    if hard_pct > 35:
        return 'Hard Paper'
    elif easy_pct > 50:
        return 'Easy Paper'
    else:
        return 'Moderate Paper'


def analyze_paper(paper_text):
    """
    Analyze a question paper and return difficulty distribution.
    
    Args:
        paper_text (str): The full question paper text
        
    Returns:
        dict: Analysis results with counts, percentages, and overall difficulty
    """
    # Split by lines and filter empty lines
    lines = [line.strip() for line in paper_text.split('\n') if line.strip()]
    
    # Remove question numbers if present
    questions = []
    for line in lines:
        cleaned = re.sub(r'^[\d\.\)\-\s]+', '', line).strip()
        if cleaned:
            questions.append(cleaned)
    
    # Get syllabus from session
    syllabus_topics = [s.strip() for s in session.get('syllabus', '').split(',') if s.strip()]
    
    # Use AI for analysis
    return analyze_with_ai(questions, syllabus_topics)

def clean_ai_json(response_text):
    """
    Cleans AI response text if it's wrapped in markdown code blocks.
    
    Args:
        response_text (str): Raw response from AI
        
    Returns:
        dict: Parsed JSON data
    """
    try:
        # Try to find JSON block if wrapped in markdown
        json_match = re.search(r'```(?:json)?\s*([\s\S]+?)\s*```', response_text)
        if json_match:
            clean_text = json_match.group(1).strip()
        else:
            clean_text = response_text.strip()
            
        return json.loads(clean_text)
    except json.JSONDecodeError as e:
        print(f"DEBUG: JSON parsing failed: {e}")
        print(f"DEBUG: Raw response: {response_text}")
        return None

def analyze_with_ai(questions, syllabus_topics):
    """
    Analyzes questions using Hugging Face (Meta-Llama-3-8B-Instruct) for semantic understanding.
    """
    if not questions:
        return {'error': 'No questions provided for analysis.'}
        
    if not HUGGINGFACE_API_KEY:
        return {'error': 'Hugging Face API Key is not set in the .env file. Please add it to enable AI analysis.'}

    # Construct llama3-instruct prompt
    prompt = f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
    You are an expert academic auditor and question paper analyzer. Respond ONLY in strict JSON. Do not include any explanation or conversational text.
    <|eot_id|><|start_header_id|>user<|end_header_id|>
    Analyze the following question paper against the provided syllabus topics.
    
    SYLLABUS TOPICS:
    {json.dumps(syllabus_topics)}
    
    QUESTIONS:
    {json.dumps(questions)}
    
    REQUIREMENTS:
    1. For EACH question, determine: Bloom's Taxonomy Level, Bloom Score (1-6), Difficulty (Easy, Moderate, Hard, Very Hard), and Syllabus Relevance.
    2. Calculate summary statistics: percentages and counts for difficulty, syllabus coverage, and overall paper difficulty.
    3. Return ONLY a valid JSON object matching the structure below.
    
    JSON STRUCTURE:
    {{
        "total_questions": 0,
        "easy_count": 0, "moderate_count": 0, "hard_count": 0, "very_hard_count": 0,
        "easy_percent": 0.0, "moderate_percent": 0.0, "hard_percent": 0.0, "very_hard_percent": 0.0,
        "syllabus_coverage_percent": 0.0, "out_of_syllabus_percent": 0.0,
        "average_bloom_score": 0.0,
        "overall_difficulty": "String",
        "detailed_analysis": [
            {{
                "question": "text",
                "bloom_level": "Level",
                "bloom_score": 0,
                "difficulty": "Level",
                "is_in_syllabus": true
            }}
        ]
    }}
    <|eot_id|><|start_header_id|>assistant<|end_header_id|>"""

    try:
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 2500,
                "temperature": 0.1,
                "top_p": 0.9,
                "return_full_text": False
            },
            "options": {
                "wait_for_model": True
            }
        }
        
        response = requests.post(HF_MODEL_URL, headers=HF_HEADERS, json=payload, timeout=90)
        
        if response.status_code == 401:
            return {'error': 'Invalid Hugging Face API Key. Please check your .env file.'}
        elif response.status_code == 429:
            return {'error': 'Hugging Face API Rate Limit Exceeded. Please try again in a few minutes.'}
        elif response.status_code == 503:
            return {'error': 'Hugging Face Model is currently loading. Please wait a moment and try again.'}
        elif response.status_code != 200:
            return {'error': f'Hugging Face API Error ({response.status_code}): {response.text}'}
            
        data = response.json()
        
        # Extract generated text from HF response format
        if isinstance(data, list) and len(data) > 0:
            raw_content = data[0].get('generated_text', '')
        else:
            raw_content = str(data)

        if not raw_content:
            return {'error': 'Empty response from Hugging Face API.'}
            
        result = clean_ai_json(raw_content)
        if not result:
            return {
                'error': 'Invalid AI response: Failed to parse JSON.',
                'raw_response': raw_content
            }
        
        # Map keys for UI compatibility with existing frontend charts
        total = result.get('total_questions', len(questions))
        result['easy_percentage'] = result.get('easy_percent', 0)
        result['medium_percentage'] = result.get('moderate_percent', 0)
        result['hard_percentage'] = result.get('hard_percent', 0)
        
        # Mapping for syllabus coverage display
        result['covered_percentage'] = result.get('syllabus_coverage_percent', 0)
        result['out_percentage'] = result.get('out_of_syllabus_percent', 0)
        result['uncovered_percentage'] = 100 - (result['covered_percentage'] + result['out_percentage'])
        
        # Calculate counts
        result['from_covered_syllabus'] = int(total * (result['covered_percentage'] / 100))
        result['out_of_syllabus'] = int(total * (result['out_percentage'] / 100))
        result['from_uncovered_syllabus'] = total - (result['from_covered_syllabus'] + result['out_of_syllabus'])
        
        # Ensure 'overall_difficulty' mapping is consistent
        if 'overall_paper_difficulty' in result and 'overall_difficulty' not in result:
            result['overall_difficulty'] = result['overall_paper_difficulty']

        return result
        
    except requests.exceptions.Timeout:
        return {'error': 'The AI analysis request timed out (Hugging Face API).'}
    except Exception as e:
        print(f"CRITICAL: Hugging Face Analysis Exception")
        traceback.print_exc()
        return {'error': f'AI Analysis failed: {str(e)}'}




def save_to_history(entry):
    """
    Save analysis result to history.json file (permanent persistent storage).
    Appends new entry to the history list in JSON format.
    
    Args:
        entry (dict): Entry dictionary with all required fields
    """
    try:
        history_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'history.json')
        
        # Load existing history or create new list
        if os.path.exists(history_file):
            try:
                with open(history_file, 'r', encoding='utf-8') as f:
                    history_list = json.load(f)
            except:
                history_list = []
        else:
            history_list = []
        
        # Append new entry
        history_list.append(entry)
        
        # Write back to file
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(history_list, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Saved to history.json: {entry.get('filename', 'Unknown')}")
        return True
    except Exception as e:
        print(f"✗ Error saving to history.json: {e}")
        return False


def save_analysis(analysis_result, paper_text, filename=None):
    """
    Save analysis results to the database.
    
    Args:
        analysis_result (dict): The analysis result dictionary
        paper_text (str): The original paper text
        filename (str): Optional filename for the uploaded file
    """
    try:
        filename = filename or 'Text Input'
        
        # Save to SQLite database
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO analysis_history 
            (filename, total_questions, easy_count, medium_count, hard_count, 
             easy_percentage, medium_percentage, hard_percentage, 
             overall_difficulty, paper_text)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            filename,
            analysis_result['total_questions'],
            analysis_result['easy_count'],
            analysis_result['medium_count'],
            analysis_result['hard_count'],
            analysis_result['easy_percentage'],
            analysis_result['medium_percentage'],
            analysis_result['hard_percentage'],
            analysis_result['overall_difficulty'],
            paper_text
        ))
        
        conn.commit()
        conn.close()
        
        print(f"✓ Saved analysis to database: {filename}")
        return True
    except Exception as e:
        print(f"Error saving analysis: {e}")
        return False


# Authentication Decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


# Routes

@app.route('/register', methods=['GET', 'POST'])
def register():
    if "user_id" in session:
        return redirect(url_for('home'))
        
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        school = request.form.get('school')
        mobile = request.form.get('mobile')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if not all([name, email, school, mobile, password]):
            return render_template('register.html', error="All fields are required.")
            
        if not re.match(r'^\d{10}$', mobile):
            return render_template('register.html', error="Mobile number must be exactly 10 digits.")
            
        if password != confirm_password:
            return render_template('register.html', error="Passwords do not match.")
            
        hashed_password = generate_password_hash(password)
        
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (name, email, school, mobile, password) VALUES (?, ?, ?, ?, ?)', 
                         (name, email, school, mobile, hashed_password))
            conn.commit()
            conn.close()
            return redirect(url_for('login', success="Account created successfully! Please login."))
        except sqlite3.IntegrityError:
            return render_template('register.html', error="Email already exists.")
        except Exception as e:
            return render_template('register.html', error=f"An error occurred: {str(e)}")
            
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if "user_id" in session:
        return redirect(url_for('home'))
        
    success_msg = request.args.get('success')
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        conn.close()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            return redirect(url_for('staff_details'))
        else:
            return render_template('login.html', error="Invalid email or password.")
            
    return render_template('login.html', success=success_msg)


@app.route('/staff-details', methods=['GET', 'POST'])
@login_required
def staff_details():
    if request.method == 'POST':
        staff_name = request.form.get('staff_name')
        subject = request.form.get('subject')
        subject_code = request.form.get('subject_code')
        syllabus = request.form.get('syllabus')
        
        if not all([staff_name, subject, subject_code, syllabus]):
            return render_template('staff_details.html', error="All fields are required.")
            
        session['staff_name'] = staff_name
        session['subject'] = subject
        session['subject_code'] = subject_code
        session['syllabus'] = syllabus
        
        return redirect(url_for('home'))
        
    return render_template('staff_details.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/')
@login_required
def home():
    """Render the home page."""
    if 'staff_name' not in session:
        return redirect(url_for('staff_details'))
    return render_template('index.html', 
                          staff_name=session.get('staff_name'),
                          subject=session.get('subject'),
                          subject_code=session.get('subject_code'),
                          syllabus=session.get('syllabus', ''))


@app.route('/analyze', methods=['POST'])
@login_required
def analyze():
    """
    Handle paper analysis request with robust validation.
    Accepts:
    1. JSON: { "questions": [...], "syllabus": [...], "filename": "..." }
    2. File: Multipart form-data with 'file' key
    """
    try:
        paper_text = None
        filename = None
        
        # 1. Handle File Upload (Multipart Form Data)
        if 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                return jsonify({'error': 'No file selected.'}), 400
            
            if not allowed_file(file.filename):
                return jsonify({'error': f'File type not supported. Allowed: {", ".join(ALLOWED_EXTENSIONS)}'}), 400
            
            try:
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                
                # Extract text
                paper_text = extract_text(file_path)
                
                # Cleanup
                try:
                    os.remove(file_path)
                except:
                    pass
                
                # Analyze paper text
                analysis_result = analyze_paper(paper_text)
                
            except Exception as e:
                return jsonify({'error': f'File processing failed: {str(e)}'}), 400
        
        # 2. Handle JSON Request
        elif request.is_json:
            data = request.get_json()
            
            # MANDATORY DEBUG PRINT
            print("\n" + "="*50)
            print("Received JSON:", data)
            print("="*50 + "\n")
            
            if not data:
                return jsonify({'error': 'Request body is empty.'}), 400
                
            questions_list = data.get('questions')
            syllabus_list = data.get('syllabus')
            filename = data.get('filename', 'API Input')
            
            # STRICT VALIDATION
            if questions_list is None:
                return jsonify({'error': 'Missing "questions" key in request.'}), 400
            
            if not isinstance(questions_list, list) or len(questions_list) == 0:
                return jsonify({'error': '"questions" must be a non-empty list.'}), 400
                
            if syllabus_list is None:
                # Fallback to session if syllabus is missing but questions exist
                syllabus_val = session.get('syllabus', '')
                syllabus_list = [s.strip() for s in syllabus_val.split(',') if s.strip()]
            
            # Execute AI Analysis
            analysis_result = analyze_with_ai(questions_list, syllabus_list)
            
            # Handle AI errors (Bad Request / AI Hallucination)
            if 'error' in analysis_result:
                # If it's an API error or parsing error, treat as 400 or 500 accordingly
                status_code = 400
                err_msg = analysis_result.get('error') or ""
                if "parse" in err_msg.lower():
                    status_code = 500
                return jsonify(analysis_result), status_code
            
            # Create paper_text mock for database
            paper_text = "\n".join(questions_list)
        
        else:
            return jsonify({'error': 'Unsupported Request Type. Use JSON or File upload.'}), 400

        # 3. Finalize and Save (Common for both types)
        if not analysis_result or 'error' in analysis_result:
             return jsonify({'error': 'Analysis failed to produce results.'}), 500

        # Build history entry
        history_entry = {
            'filename': filename or 'Analysis',
            'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'level': analysis_result.get('overall_difficulty', 'N/A'),
            'easy_count': analysis_result.get('easy_count', 0),
            'easy': analysis_result.get('easy_percentage', 0),
            'medium_count': analysis_result.get('moderate_count', analysis_result.get('medium_count', 0)),
            'medium': analysis_result.get('medium_percentage', 0),
            'hard_count': analysis_result.get('hard_count', 0),
            'hard': analysis_result.get('hard_percentage', 0),
            'total_questions': analysis_result.get('total_questions', 0)
        }
        
        # Save to history file and DB
        save_to_history(history_entry)
        save_analysis(analysis_result, paper_text, filename)
        
        return jsonify(analysis_result), 200
        
    except Exception as e:
        print(f"CRITICAL ERROR in /analyze: {traceback.format_exc()}")
        return jsonify({
            'error': f'Server Error: {str(e)}'
        }), 500


@app.route('/history')
@login_required
def history():
    """
    Render the analysis history page.
    Loads history from history.json and displays in reverse order (newest first).
    """
    try:
        history_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'history.json')
        history_data = []
        
        if os.path.exists(history_file):
            with open(history_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Reverse to show newest first
                history_data = data[::-1] if data else []
        
        return render_template('history.html', history=history_data)
    except Exception as e:
        print(f"Error loading history: {e}")
        return render_template('history.html', history=[])


@app.route('/clear_all_history', methods=['GET', 'POST'])
def clear_all_history():
    """
    Clear all history entries - completely wipe the history.json file.
    """
    try:
        history_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'history.json')
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump([], f)
        print("✓ Cleared all history entries")
    except Exception as e:
        print(f"✗ Error clearing history: {e}")
    
    from flask import redirect  # type: ignore[import]
    return redirect('/history')


@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large error."""
    return jsonify({
        'error': f'File is too large. Maximum file size is {MAX_FILE_SIZE // (1024*1024)}MB.'
    }), 413


if __name__ == '__main__':
    # Initialize the database
    init_db()
    
    # Run the Flask app
    app.run(debug=True, host='127.0.0.1', port=5000)
