#!/usr/bin/env python3
"""
Quiz Debug Test Script
This script helps debug quiz generation and answer checking issues
"""

import json
import os
from datetime import datetime

def test_answer_checking():
    """Test the answer checking logic"""
    print("🧪 Testing Answer Checking Logic")
    print("=" * 50)
    
    # Sample quiz data
    test_questions = [
        {
            "question": "What is the capital of France?",
            "type": "mcq",
            "options": ["A) London", "B) Paris", "C) Berlin", "D) Madrid"],
            "correct_answer": "B",
            "explanation": "Paris is the capital of France"
        },
        {
            "question": "Which planet is closest to the Sun?",
            "type": "mcq", 
            "options": ["A) Venus", "B) Earth", "C) Mercury", "D) Mars"],
            "correct_answer": "C",
            "explanation": "Mercury is the closest planet to the Sun"
        },
        {
            "question": "Is the Earth round?",
            "type": "true_false",
            "options": ["True", "False"],
            "correct_answer": "True",
            "explanation": "The Earth is approximately spherical"
        }
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n📝 Question {i}: {question['question']}")
        print(f"🎯 Correct Answer: '{question['correct_answer']}'")
        print(f"📋 Options:")
        
        for j, option in enumerate(question['options']):
            # Test the same logic as the frontend
            selected_text = option.strip()
            correct_answer = question['correct_answer'].strip()
            
            is_correct = False
            
            # Direct comparison
            if selected_text == correct_answer:
                is_correct = True
            # Check if selected text starts with the correct answer (for MCQ with letter prefixes)
            elif (selected_text.startswith(correct_answer + ')') or 
                  selected_text.startswith(correct_answer + '.') or 
                  selected_text.startswith(correct_answer + '-')):
                is_correct = True
            # Check if correct answer contains the selected text (for partial matches)
            elif correct_answer.find(selected_text) != -1 and len(selected_text) > 3:
                is_correct = True
            # For MCQ with A), B), C), D) format
            elif selected_text.startswith(correct_answer + ')') or selected_text.startswith(correct_answer + ')'):
                is_correct = True
            # For MCQ with A. B. C. D. format
            elif selected_text.startswith(correct_answer + '.') or selected_text.startswith(correct_answer + '.'):
                is_correct = True
            # For MCQ with A- B- C- D- format
            elif selected_text.startswith(correct_answer + '-') or selected_text.startswith(correct_answer + '-'):
                is_correct = True
            
            status = "✅ CORRECT" if is_correct else "❌ INCORRECT"
            print(f"   {j+1}. '{option}' -> {status}")
        
        print(f"🔍 Debug Info:")
        print(f"   - Question Type: {question['type']}")
        print(f"   - Correct Answer: '{question['correct_answer']}'")
        print(f"   - Options: {[opt.strip() for opt in question['options']]}")

def check_existing_quizzes():
    """Check existing quiz files for potential issues"""
    print("\n🔍 Checking Existing Quiz Files")
    print("=" * 50)
    
    results_folder = 'battle_results'
    if not os.path.exists(results_folder):
        print("❌ No results folder found")
        return
    
    quiz_files = [f for f in os.listdir(results_folder) if f.endswith('.json')]
    
    if not quiz_files:
        print("❌ No quiz files found")
        return
    
    print(f"📁 Found {len(quiz_files)} quiz files")
    
    for quiz_file in quiz_files[-3:]:  # Check last 3 files
        print(f"\n📄 Analyzing: {quiz_file}")
        try:
            with open(os.path.join(results_folder, quiz_file), 'r') as f:
                data = json.load(f)
            
            if 'battle_data' in data and 'questions' in data['battle_data']:
                questions = data['battle_data']['questions']
                print(f"   📊 Questions: {len(questions)}")
                
                for i, q in enumerate(questions[:2]):  # Check first 2 questions
                    print(f"   Q{i+1}: {q.get('question', 'NO QUESTION')[:50]}...")
                    print(f"      Type: {q.get('type', 'UNKNOWN')}")
                    print(f"      Correct: '{q.get('correct_answer', 'NO ANSWER')}'")
                    print(f"      Options: {len(q.get('options', []))}")
                    
                    # Check for potential issues
                    if not q.get('question'):
                        print(f"      ⚠️  Missing question text")
                    if not q.get('correct_answer'):
                        print(f"      ⚠️  Missing correct answer")
                    if not q.get('options') and q.get('type') in ['mcq', 'true_false']:
                        print(f"      ⚠️  Missing options for {q.get('type')} question")
                    
            else:
                print("   ❌ Invalid quiz format")
                
        except Exception as e:
            print(f"   ❌ Error reading file: {e}")

def main():
    """Main function"""
    print("🚀 Quiz Debug Test Script")
    print("=" * 50)
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    test_answer_checking()
    check_existing_quizzes()
    
    print("\n✅ Debug test completed!")
    print("\n💡 Tips for fixing issues:")
    print("1. Check browser console for debug logs")
    print("2. Use the 'Debug Answer' button to see question details")
    print("3. Ensure PDF content is readable and substantial")
    print("4. Check that Google API key is properly configured")

if __name__ == "__main__":
    main()
