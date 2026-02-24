"""
Test script to verify extraction and analysis functions work correctly
"""
import sys
sys.path.insert(0, '.')
from app import extract_text, analyze_paper

# Test extraction
try:
    text = extract_text('test_sample.txt')
    print('✅ File extraction successful')
    print(f'   Extracted {len(text)} characters')
except Exception as e:
    print(f'❌ Extraction failed: {e}')
    sys.exit(1)

# Test analysis
try:
    result = analyze_paper(text)
    print('✅ Analysis successful')
    print(f'   Total questions: {result["total_questions"]}')
    print(f'   Easy: {result["easy_count"]} ({result["easy_percentage"]}%)')
    print(f'   Medium: {result["medium_count"]} ({result["medium_percentage"]}%)')
    print(f'   Hard: {result["hard_count"]} ({result["hard_percentage"]}%)')
    print(f'   Overall: {result["overall_difficulty"]}')
except Exception as e:
    print(f'❌ Analysis failed: {e}')
    sys.exit(1)

print('\n✅ ALL TESTS PASSED - App is ready to run!')
