"""
Configuration settings for Question Paper Difficulty Analyzer
Customize these settings without modifying app.py
"""

# Flask Configuration
DEBUG_MODE = True
HOST = '127.0.0.1'
PORT = 5000

# Database Configuration
DATABASE_PATH = 'database.db'

# UI Settings
APP_TITLE = 'Question Paper Difficulty Analyzer'
APP_SUBTITLE = 'Analyze your exam papers and understand their difficulty distribution'

# Difficulty Classification Keywords
# You can customize these based on your requirements
DIFFICULTY_KEYWORDS = {
    'easy': [
        'define',      # Definition questions
        'list',        # Listing items
        'identify',    # Identification questions
        'name',        # Naming questions
        'what',        # What is questions
        'state',       # State/Write questions
        'write'        # Writing questions
    ],
    'medium': [
        'explain',     # Explanation questions
        'describe',    # Description questions
        'summarize',   # Summarization questions
        'discuss',     # Discussion questions
        'illustrate',  # Illustration questions
        'outline',     # Outline questions
        'distinguish'  # Distinction questions
    ],
    'hard': [
        'analyze',     # Analysis questions
        'evaluate',    # Evaluation questions
        'justify',     # Justification questions
        'compare',     # Comparison questions
        'criticize',   # Criticism questions
        'synthesis',   # Synthesis questions
        'create'       # Creation questions
    ]
}

# Paper Difficulty Classification Thresholds
# Adjust these percentages to change how papers are classified
EASY_PAPER_THRESHOLD = 50        # % of easy questions for "Easy Paper"
HARD_PAPER_THRESHOLD = 50        # % of hard questions for "Tough Paper"
# If neither threshold is met, it's classified as "Moderate Paper"

# Results Display Settings
SHOW_HISTORY_LIMIT = 100         # Maximum number of histories to show per page
RESULTS_CHART_HEIGHT = '400px'   # Chart container height

# Export Settings (for future enhancements)
ENABLE_PDF_EXPORT = False
ENABLE_CSV_EXPORT = False
ENABLE_JSON_EXPORT = False

# Security Settings
MAX_FILE_SIZE_MB = 10            # Maximum file upload size in MB
ALLOWED_FILE_EXTENSIONS = ['txt'] # Allowed file types for upload
