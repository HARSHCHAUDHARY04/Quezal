# app.py - IQBattle: AI-Powered Quiz Battleground
from flask import Flask, request, render_template, jsonify, send_file, session, abort
from flask_cors import CORS
import os
import json
from datetime import datetime
import PyPDF2
from dotenv import load_dotenv
import requests
import sqlite3
import hashlib
import secrets
from io import BytesIO

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Secret for sessions
app.secret_key = os.getenv("FLASK_SECRET_KEY") or secrets.token_hex(16)

# Configure battle arsenal folders
UPLOAD_FOLDER = 'battle_uploads'
RESULTS_FOLDER = 'battle_results'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max arsenal size

# === Database Setup ===
DB_PATH = os.path.join(os.path.dirname(__file__), 'quezal.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True) if os.path.dirname(DB_PATH) else None
    conn = get_db_connection()
    cur = conn.cursor()
    # Users table
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            name TEXT,
            password_hash TEXT NOT NULL,
            user_type TEXT DEFAULT 'student',
            created_at TEXT NOT NULL
        );
        """
    )
    # Quizzes table
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS quizzes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            result_filename TEXT NOT NULL,
            original_filename TEXT,
            num_questions INTEGER,
            difficulty TEXT,
            mode TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
        """
    )
    conn.commit()
    conn.close()

def hash_password(password: str) -> str:
    salt = os.getenv('PASSWORD_SALT', 'quezal_salt')
    return hashlib.sha256((salt + password).encode('utf-8')).hexdigest()

def get_current_user_id():
    return session.get('user_id')

def get_current_user_type():
    return session.get('user_type', 'student')

def extract_generated_text(result):
    """Safely extract text from Gemini AI battle response"""
    try:
        candidates = result.get('candidates', [])
        if not candidates or not isinstance(candidates, list):
            raise ValueError('No AI battle candidates found')
        
        content = candidates[0].get('content')
        if isinstance(content, list) and len(content) > 0:
            content = content[0]
        
        parts = content.get('parts')
        if not parts or not isinstance(parts, list):
            raise ValueError('No battle intelligence parts found')
        
        text = parts[0].get('text')
        if not text:
            raise ValueError('No battle text generated')
        
        return text
    except Exception as e:
        print(f"❌ Battle intelligence extraction failed: {e}")
        print(f"🔍 Full AI response: {result}")
        return None

def extract_text_from_pdf(pdf_path):
    """Extract battle intelligence from PDF documents"""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            
            # Extract intelligence from all pages
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text() + "\n"
                
            return text.strip()
    except Exception as e:
        print(f"❌ PDF intelligence extraction failed: {e}")
        return None

def generate_battle_questions(pdf_text, num_questions=8, difficulty="Medium", question_types="mixed"):
    """Generate IQBattle questions using AI battle intelligence"""
    
    # Get AI battle credentials
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        print("❌ No AI battle credentials found! Check your .env battle config")
        return None
        
    print(f"✅ AI Battle Commander authenticated: {api_key[:10]}...")
    print(f"⚔️ Battle mode: {question_types}")
    print(f"🎯 Difficulty protocol: {difficulty}")
    
    # Validate input
    if not pdf_text or len(pdf_text.strip()) < 100:
        print("❌ Insufficient PDF text for question generation")
        return None
    
    # AI Battle Command Center endpoint
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    
    # Battle mode configurations
    battle_modes = {
        "mcq": {
            "name": "MCQ Assault Mode",
            "instruction": "Deploy ONLY multiple choice battle questions with exactly 4 tactical options (A, B, C, D).",
            "example": """
            {
                "question": "What is the primary objective in database normalization?",
                "type": "mcq",
                "options": ["A) Increase storage space", "B) Eliminate data redundancy", "C) Slow down queries", "D) Increase complexity"],
                "correct_answer": "B",
                "explanation": "Database normalization eliminates redundancy and ensures data integrity"
            }"""
        },
        "true_false": {
            "name": "Binary Strike Mode",
            "instruction": "Execute ONLY true/false binary battle decisions.",
            "example": """
            {
                "question": "Database locks are always necessary for maintaining consistency.",
                "type": "true_false",
                "options": ["True", "False"],
                "correct_answer": "False",
                "explanation": "While locks help, there are lock-free methods like optimistic concurrency control"
            }"""
        },
        "fill_blank": {
            "name": "Stealth Mission Mode",
            "instruction": "Launch ONLY fill-in-the-blank stealth operations using _______ for tactical blanks.",
            "example": """
            {
                "question": "The _______ protocol ensures that database transactions appear to execute in _______ order.",
                "type": "fill_blank",
                "options": [],
                "correct_answer": "two-phase locking; serial",
                "explanation": "Two-phase locking protocol ensures serializability by controlling transaction execution order"
            }"""
        },
        "essay": {
            "name": "Intelligence Report Mode",
            "instruction": "Generate ONLY comprehensive intelligence report questions requiring detailed analysis.",
            "example": """
            {
                "question": "Analyze the importance of ACID properties in database management systems and their real-world applications.",
                "type": "essay",
                "options": [],
                "correct_answer": "A complete analysis should cover: 1) Atomicity - all-or-nothing transactions 2) Consistency - data integrity rules 3) Isolation - concurrent transaction handling 4) Durability - permanent data storage 5) Real-world examples in banking, e-commerce, etc.",
                "explanation": "Students should demonstrate understanding of each ACID property and provide practical examples"
            }"""
        }
    }
    
    # Select battle configuration
    if question_types in battle_modes:
        mode_config = battle_modes[question_types]
        battle_instruction = mode_config["instruction"]
        battle_example = mode_config["example"]
        print(f"🎮 Deploying {mode_config['name']}")
    else:
        battle_instruction = "Deploy a STRATEGIC MIX of all battle question types: MCQ Assault, Binary Strike, Stealth Mission, and Intelligence Report."
        battle_example = "Mix of mcq, true_false, fill_blank, and essay questions"
        print(f"🎮 Deploying Mixed Battle Formation")
    
    # AI Battle Command Prompt
    battle_prompt = f"""
    IQBATTLE MISSION BRIEFING
    ========================
    
    Battle Intelligence Source:
    {pdf_text[:3500]}
    
    MISSION PARAMETERS:
    - Deploy exactly {num_questions} battle questions
    - Difficulty Protocol: {difficulty}
    - Battle Mode: {battle_instruction}
    
    TACTICAL REQUIREMENTS:
    - Questions must test intellectual combat skills, not just memory recall
    - Each question needs strategic explanation for battle debriefing
    - Ensure questions are battlefield-ready and unambiguous
    - Base all intelligence strictly on provided battle document
    
    BATTLE FORMATION (JSON ONLY):
    {{
        "questions": [
            {battle_example}
        ]
    }}
    
    DEPLOY BATTLE QUESTIONS NOW - JSON RESPONSE ONLY, NO ADDITIONAL COMMUNICATION
    """
    
    # Battle payload for AI Command Center
    payload = {
        "contents": [{
            "parts": [{
                "text": battle_prompt
            }]
        }]
    }
    
    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": api_key
    }
    
    try:
        print(f"🤖 AI Battle Commander generating {num_questions} {question_types} questions...")
        print("⚔️ Engaging AI battle systems...")
        
        response = requests.post(url, json=payload, headers=headers)
        print(f"📡 Battle Command Response: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            
            # Extract battle intelligence
            generated_text = extract_generated_text(result)
            if not generated_text:
                print("❌ AI Battle Commander failed to generate intelligence")
                return None
            
            print("✅ Battle intelligence successfully extracted")
            
            # Clean battle response
            generated_text = generated_text.strip()
            if generated_text.startswith("```"):
                generated_text = generated_text[7:]
            if generated_text.endswith("```"):
                generated_text = generated_text[:-3]
            
            # Parse battle data
            try:
                battle_data = json.loads(generated_text)
                
                # Validate battle questions
                if 'questions' in battle_data:
                    question_types_found = [q.get('type', 'mcq') for q in battle_data['questions']]
                    print(f"✅ Battle questions deployed: {question_types_found}")
                    
                    # Count battle formation
                    formation_count = {}
                    for qtype in question_types_found:
                        formation_count[qtype] = formation_count.get(qtype, 0) + 1
                    print(f"📊 Battle formation: {formation_count}")
                
                return battle_data
            except json.JSONDecodeError as e:
                print(f"❌ Battle data parsing failed: {e}")
                print(f"🔍 Raw battle response (first 500 chars): {generated_text[:500]}")
                return None
                
        else:
            print(f"❌ AI Battle Command Error: {response.status_code}")
            print(f"💥 Battle failure details: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Battle system failure: {e}")
        return None

@app.route('/')
def battle_arena():
    """Main IQBattle Arena"""
    return render_template('index.html')

@app.route('/user')
def user_dashboard_page():
    """User dashboard page (requires login)"""
    if not get_current_user_id():
        # Render index and open modal on load via query param could be an option; keep simple: redirect to home
        return render_template('index.html')
    return render_template('user.html')

# === Auth APIs ===
@app.route('/api/signup', methods=['POST'])
def api_signup():
    try:
        data = request.get_json(silent=True) or {}
        email = (data.get('email') or '').strip().lower()
        password = (data.get('password') or '').strip()
        name = (data.get('name') or '').strip() or None
        user_type = (data.get('user_type') or 'student').strip().lower()
        
        # Validate user type
        if user_type not in ['teacher', 'student']:
            return jsonify({'success': False, 'error': 'Invalid user type. Must be teacher or student'}), 400
        
        if not email or not password:
            return jsonify({'success': False, 'error': 'Email and password are required'}), 400
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                'INSERT INTO users (email, name, password_hash, user_type, created_at) VALUES (?, ?, ?, ?, ?)',
                (email, name, hash_password(password), user_type, datetime.now().isoformat())
            )
            conn.commit()
            user_id = cur.lastrowid
        except sqlite3.IntegrityError:
            conn.close()
            return jsonify({'success': False, 'error': 'Email already in use'}), 409
        conn.close()
        session['user_id'] = user_id
        session['user_type'] = user_type
        return jsonify({'success': True, 'user': {'id': user_id, 'email': email, 'name': name, 'user_type': user_type}})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/login', methods=['POST'])
def api_login():
    try:
        data = request.get_json(silent=True) or {}
        email = (data.get('email') or '').strip().lower()
        password = (data.get('password') or '').strip()
        if not email or not password:
            return jsonify({'success': False, 'error': 'Email and password are required'}), 400
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT id, password_hash, name, user_type FROM users WHERE email = ?', (email,))
        row = cur.fetchone()
        conn.close()
        if not row or row['password_hash'] != hash_password(password):
            return jsonify({'success': False, 'error': 'Invalid credentials'}), 401
        session['user_id'] = row['id']
        session['user_type'] = row['user_type']
        return jsonify({'success': True, 'user': {'id': row['id'], 'email': email, 'name': row['name'], 'user_type': row['user_type']}})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/logout', methods=['POST'])
def api_logout():
    session.pop('user_id', None)
    return jsonify({'success': True})

@app.route('/api/me')
def api_me():
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({'authenticated': False})
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, email, name, user_type FROM users WHERE id = ?', (user_id,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return jsonify({'authenticated': False})
    return jsonify({'authenticated': True, 'user': {'id': row['id'], 'email': row['email'], 'name': row['name'], 'user_type': row['user_type']}})

@app.route('/upload', methods=['POST'])
def deploy_battle():
    """Deploy PDF battle document and generate IQBattle"""
    try:
        # Check if user is authenticated
        user_id = get_current_user_id()
        user_type = get_current_user_type()
        
        if not user_id:
            return jsonify({'error': 'Authentication required'}), 401
        
        # Both teachers and students can create quizzes now
        
        # Battle intelligence gathering
        print('=== IQBATTLE DEPLOYMENT INITIATED ===')
        print(f'🎯 Battle request method: {request.method}')
        print(f'📁 Uploaded arsenal: {list(request.files.keys())}')
        print(f'⚙️ Battle parameters: {list(request.form.keys())}')
        
        # Validate battle document upload
        if 'pdf_file' not in request.files:
            print('❌ No battle document detected')
            return jsonify({'error': 'No PDF battle document uploaded'}), 400
        
        battle_file = request.files['pdf_file']
        print(f'📄 Battle document: {battle_file}')
        print(f'📝 Document name: {battle_file.filename}')
        
        if battle_file.filename == '':
            print('❌ Empty battle document name')
            return jsonify({'error': 'No battle document selected'}), 400
        
        # Extract battle parameters
        num_questions = int(request.form.get('num_questions', 8))
        difficulty = request.form.get('difficulty', 'Medium')
        question_types = request.form.get('question_types', 'mixed')
        
        # Validate battle configuration
        if num_questions < 4:
            print(f"❌ Insufficient battle questions ({num_questions}) for effective combat")
            return jsonify({'error': 'Minimum 4 questions required for IQBattle deployment'}), 400
        
        print(f"🎮 Battle Configuration:")
        print(f"   📊 Questions: {num_questions}")
        print(f"   🎯 Difficulty: {difficulty}")
        print(f"   ⚔️ Battle Mode: {question_types}")
        
        # Secure battle document
        battle_filename = f"battle_document_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        battle_path = os.path.join(app.config['UPLOAD_FOLDER'], battle_filename)
        battle_file.save(battle_path)
        
        print(f"🔒 Battle document secured: {battle_filename}")
        
        # Extract battle intelligence
        battle_intelligence = extract_text_from_pdf(battle_path)
        if not battle_intelligence:
            return jsonify({'error': 'Failed to extract battle intelligence from PDF'}), 400
        
        print(f"🧠 Battle intelligence extracted: {len(battle_intelligence)} characters")
        
        # Generate IQBattle questions
        battle_questions = generate_battle_questions(battle_intelligence, num_questions, difficulty, question_types)
        if not battle_questions:
            return jsonify({'error': 'AI Battle Commander failed to generate questions. Please check your PDF content and try again.'}), 500
        
        # Validate generated questions
        if 'questions' not in battle_questions or not battle_questions['questions']:
            return jsonify({'error': 'Generated questions are invalid. Please try again.'}), 500
        
        # Ensure all questions have required fields
        for i, q in enumerate(battle_questions['questions']):
            if not q.get('question') or not q.get('correct_answer'):
                print(f"⚠️ Question {i+1} missing required fields: {q}")
                return jsonify({'error': f'Question {i+1} is incomplete. Please try again.'}), 500
        
        print("✅ IQBattle questions successfully generated")
        
        # Store battle results
        battle_result_filename = f"iqbattle_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        battle_result_path = os.path.join(RESULTS_FOLDER, battle_result_filename)
        
        # Count question types for battle statistics
        question_formation = {}
        if 'questions' in battle_questions:
            for q in battle_questions['questions']:
                qtype = q.get('type', 'mcq')
                question_formation[qtype] = question_formation.get(qtype, 0) + 1
        
        # Battle result archive
        battle_archive = {
            'battle_document': battle_filename,
            'deployment_timestamp': datetime.now().isoformat(),
            'battle_parameters': {
                'num_questions': num_questions,
                'difficulty_protocol': difficulty,
                'battle_mode': question_types,
                'question_formation': question_formation
            },
            'battle_system': 'IQBattle_v2.0_AI_Enhanced',
            'battle_commander': 'Google_AI_Gemini_1.5_Flash',
            'battle_data': battle_questions
        }
        
        with open(battle_result_path, 'w') as f:
            json.dump(battle_archive, f, indent=2)
        
        # Clean up battle document (optional - keep for debugging)
        # os.remove(battle_path)
        
        print("🏆 IQBattle deployment successful!")

        # Persist quiz metadata if user is logged in
        user_id = get_current_user_id()
        if user_id:
            try:
                conn = get_db_connection()
                cur = conn.cursor()
                cur.execute(
                    'INSERT INTO quizzes (user_id, result_filename, original_filename, num_questions, difficulty, mode, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)',
                    (
                        user_id,
                        battle_result_filename,
                        battle_file.filename,
                        num_questions,
                        difficulty,
                        question_types,
                        datetime.now().isoformat()
                    )
                )
                conn.commit()
                conn.close()
            except Exception as e:
                print(f"⚠️ Failed to persist quiz metadata: {e}")
        
        return jsonify({
            'success': True,
            'battle_status': 'VICTORY_ACHIEVED',
            'quiz_data': battle_questions,
            'question_types': question_formation,
            'result_file': battle_result_filename,
            'battle_stats': {
                'total_questions': sum(question_formation.values()),
                'battle_mode': question_types,
                'difficulty_protocol': difficulty,
                'deployment_time': datetime.now().strftime('%H:%M:%S')
            },
            'message': f'IQBattle deployed: {sum(question_formation.values())} questions ready for intellectual combat!'
        })
        
    except Exception as e:
        print(f"💥 IQBATTLE SYSTEM FAILURE: {e}")
        return jsonify({
            'error': f'Battle system failure: {str(e)}',
            'battle_status': 'MISSION_FAILED'
        }), 500

@app.route('/download/<filename>')
def download_battle_results(filename):
    """Download IQBattle results archive"""
    try:
        fmt = request.args.get('format', 'json')
        battle_file_path = os.path.join(RESULTS_FOLDER, filename)
        if not os.path.exists(battle_file_path):
            abort(404)
        if fmt == 'pdf':
            # Render PDF from stored JSON
            with open(battle_file_path, 'r') as f:
                data = json.load(f)
            pdf_bytes = generate_quiz_pdf(data)
            return send_file(BytesIO(pdf_bytes), as_attachment=True, download_name=filename.replace('.json', '.pdf'), mimetype='application/pdf')
        return send_file(battle_file_path, as_attachment=True, download_name=filename)
    except Exception as e:
        return jsonify({
            'error': f'Battle archive retrieval failed: {str(e)}',
            'battle_status': 'ARCHIVE_NOT_FOUND'
        }), 404

def generate_quiz_pdf(archive: dict) -> bytes:
    try:
        # Lazy import to avoid hard dependency if not installed
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        from reportlab.lib.units import inch
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
        from reportlab.lib import colors

        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, leftMargin=0.75*inch, rightMargin=0.75*inch, topMargin=0.75*inch, bottomMargin=0.75*inch)
        styles = getSampleStyleSheet()
        story = []

        title = archive.get('battle_document', 'Quezal Quiz')
        story.append(Paragraph(f"<b>Quezal Quiz</b>", styles['Title']))
        story.append(Spacer(1, 0.2*inch))

        battle_data = archive.get('battle_data', {})
        questions = battle_data.get('questions', [])
        for idx, q in enumerate(questions, start=1):
            story.append(Paragraph(f"<b>Q{idx}.</b> {q.get('question','')}", styles['Heading4']))
            qtype = q.get('type', 'mcq')
            opts = q.get('options') or []
            if opts:
                for opt in opts:
                    story.append(Paragraph(f"- {opt}", styles['Normal']))
            story.append(Spacer(1, 0.1*inch))
            story.append(Paragraph(f"<b>Answer:</b> {q.get('correct_answer','')}", styles['Normal']))
            story.append(Paragraph(f"<b>Explanation:</b> {q.get('explanation','')}", styles['Normal']))
            story.append(Spacer(1, 0.2*inch))

        doc.build(story)
        pdf = buffer.getvalue()
        buffer.close()
        return pdf
    except Exception as e:
        # Fallback: return a tiny PDF with error
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.pdfgen import canvas
            buf = BytesIO()
            c = canvas.Canvas(buf, pagesize=letter)
            c.drawString(72, 750, "Quezal Quiz")
            c.drawString(72, 730, f"Error generating PDF: {e}")
            c.save()
            return buf.getvalue()
        except Exception:
            return b""

@app.route('/api/my-quizzes')
def api_my_quizzes():
    user_id = get_current_user_id()
    user_type = get_current_user_type()
    if not user_id:
        return jsonify({'success': False, 'error': 'Not authenticated'}), 401
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # All users see their own created quizzes
        cur.execute(
            'SELECT id, result_filename, original_filename, num_questions, difficulty, mode, created_at FROM quizzes WHERE user_id = ? ORDER BY id DESC',
            (user_id,)
        )
        
        rows = cur.fetchall()
        conn.close()
        quizzes = [dict(row) for row in rows]
        return jsonify({'success': True, 'quizzes': quizzes, 'user_type': user_type})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/my-quizzes/<int:quiz_id>', methods=['DELETE'])
def api_delete_my_quiz(quiz_id: int):
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({'success': False, 'error': 'Not authenticated'}), 401
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        # Verify ownership and fetch filename to optionally delete file
        cur.execute('SELECT result_filename FROM quizzes WHERE id = ? AND user_id = ?', (quiz_id, user_id))
        row = cur.fetchone()
        if not row:
            conn.close()
            return jsonify({'success': False, 'error': 'Quiz not found'}), 404
        result_filename = row['result_filename']
        cur.execute('DELETE FROM quizzes WHERE id = ? AND user_id = ?', (quiz_id, user_id))
        conn.commit()
        conn.close()
        # Do not delete the file on disk to preserve archives; uncomment to remove
        # try:
        #     os.remove(os.path.join(RESULTS_FOLDER, result_filename))
        # except Exception:
        #     pass
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# === Profile APIs ===
@app.route('/api/profile', methods=['GET', 'PUT'])
def api_profile():
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({'success': False, 'error': 'Not authenticated'}), 401
    if request.method == 'GET':
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT id, email, name, created_at FROM users WHERE id = ?', (user_id,))
        row = cur.fetchone()
        conn.close()
        if not row:
            return jsonify({'success': False, 'error': 'User not found'}), 404
        return jsonify({'success': True, 'profile': dict(row)})
    else:
        data = request.get_json(silent=True) or {}
        name = (data.get('name') or '').strip() or None
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('UPDATE users SET name = ? WHERE id = ?', (name, user_id))
        conn.commit()
        conn.close()
        return jsonify({'success': True})

@app.route('/api/change-password', methods=['POST'])
def api_change_password():
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({'success': False, 'error': 'Not authenticated'}), 401
    data = request.get_json(silent=True) or {}
    current_password = (data.get('current_password') or '').strip()
    new_password = (data.get('new_password') or '').strip()
    if not current_password or not new_password:
        return jsonify({'success': False, 'error': 'Both current and new password required'}), 400
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT password_hash FROM users WHERE id = ?', (user_id,))
    row = cur.fetchone()
    if not row or row['password_hash'] != hash_password(current_password):
        conn.close()
        return jsonify({'success': False, 'error': 'Current password incorrect'}), 400
    cur.execute('UPDATE users SET password_hash = ? WHERE id = ?', (hash_password(new_password), user_id))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/api/battle-stats')
def get_battle_statistics():
    """Get IQBattle deployment statistics"""
    try:
        battle_stats = {
            'total_battles': 0,
            'battle_formations': {},
            'difficulty_protocols': {},
            'recent_battles': [],
            'battle_system_status': 'OPERATIONAL'
        }
        
        # Analyze battle archives
        if os.path.exists(RESULTS_FOLDER):
            battle_files = [f for f in os.listdir(RESULTS_FOLDER) if f.endswith('.json')]
            battle_stats['total_battles'] = len(battle_files)
            
            # Analyze recent battle data
            for battle_file in sorted(battle_files)[-10:]:  # Last 10 battles
                battle_path = os.path.join(RESULTS_FOLDER, battle_file)
                try:
                    with open(battle_path, 'r') as f:
                        battle_data = json.load(f)
                    
                    # Count formations
                    if 'battle_parameters' in battle_data and 'question_formation' in battle_data['battle_parameters']:
                        formations = battle_data['battle_parameters']['question_formation']
                        for formation, count in formations.items():
                            battle_stats['battle_formations'][formation] = battle_stats['battle_formations'].get(formation, 0) + count
                    
                    # Count difficulty protocols
                    if 'battle_parameters' in battle_data:
                        difficulty = battle_data['battle_parameters'].get('difficulty_protocol', 'Medium')
                        battle_stats['difficulty_protocols'][difficulty] = battle_stats['difficulty_protocols'].get(difficulty, 0) + 1
                    
                    # Add to recent battles
                    battle_stats['recent_battles'].append({
                        'battle_id': battle_file,
                        'deployment_time': battle_data.get('deployment_timestamp'),
                        'questions_deployed': battle_data['battle_parameters'].get('num_questions', 0),
                        'battle_mode': battle_data['battle_parameters'].get('battle_mode', 'mixed'),
                        'difficulty': battle_data['battle_parameters'].get('difficulty_protocol', 'Medium')
                    })
                except:
                    continue
        
        return jsonify(battle_stats)
    except Exception as e:
        return jsonify({
            'error': f'Battle statistics retrieval failed: {str(e)}',
            'battle_system_status': 'STATISTICS_ERROR'
        }), 500

@app.route('/api/take-quiz/<int:quiz_id>')
def api_take_quiz(quiz_id):
    """Get quiz data for students to take"""
    user_id = get_current_user_id()
    user_type = get_current_user_type()
    
    if not user_id:
        return jsonify({'success': False, 'error': 'Authentication required'}), 401
    
    if user_type != 'student':
        return jsonify({'success': False, 'error': 'Only students can take quizzes'}), 403
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Get quiz data
        cur.execute('''
            SELECT q.result_filename, q.original_filename, q.num_questions, q.difficulty, q.mode, q.created_at,
                   u.name as creator_name
            FROM quizzes q
            JOIN users u ON q.user_id = u.id
            WHERE q.id = ?
        ''', (quiz_id,))
        
        row = cur.fetchone()
        conn.close()
        
        if not row:
            return jsonify({'success': False, 'error': 'Quiz not found'}), 404
        
        # Load quiz data from file
        quiz_file_path = os.path.join(RESULTS_FOLDER, row['result_filename'])
        if not os.path.exists(quiz_file_path):
            return jsonify({'success': False, 'error': 'Quiz file not found'}), 404
        
        with open(quiz_file_path, 'r', encoding='utf-8') as f:
            quiz_data = json.load(f)
        
        return jsonify({
            'success': True,
            'quiz': {
                'id': quiz_id,
                'filename': row['result_filename'],
                'original_filename': row['original_filename'],
                'num_questions': row['num_questions'],
                'difficulty': row['difficulty'],
                'mode': row['mode'],
                'created_at': row['created_at'],
                'creator_name': row['creator_name'],
                'questions': quiz_data.get('battle_data', {}).get('questions', [])
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/battle-health')
def battle_system_health():
    """IQBattle system health check"""
    try:
        health_status = {
            'battle_system': 'IQBattle_v2.0',
            'ai_commander': 'Google_AI_Gemini_1.5_Flash',
            'system_status': 'OPERATIONAL',
            'battle_arsenal_ready': os.path.exists(UPLOAD_FOLDER),
            'battle_archives_ready': os.path.exists(RESULTS_FOLDER),
            'ai_credentials_loaded': bool(os.getenv("GOOGLE_API_KEY")),
            'max_arsenal_size': '16MB',
            'supported_battle_modes': ['mixed', 'mcq', 'true_false', 'fill_blank', 'essay'],
            'last_system_check': datetime.now().isoformat()
        }
        
        # Overall system status
        if all([
            health_status['battle_arsenal_ready'],
            health_status['battle_archives_ready'],
            health_status['ai_credentials_loaded']
        ]):
            health_status['overall_status'] = 'READY_FOR_BATTLE'
        else:
            health_status['overall_status'] = 'SYSTEM_COMPROMISED'
        
        return jsonify(health_status)
    except Exception as e:
        return jsonify({
            'battle_system': 'IQBattle_v2.0',
            'system_status': 'CRITICAL_FAILURE',
            'error': str(e),
            'last_system_check': datetime.now().isoformat()
        }), 500

if __name__ == '__main__':
    # Ensure DB exists
    try:
        init_db()
        print("🗄️ Database initialized at:", DB_PATH)
    except Exception as e:
        print("⚠️ Failed to init DB:", e)
    print("=" * 50)
    print("🚀 QUIZGO PROFESSIONAL SYSTEM")
    print("=" * 50)
    print("⚔️ AI-Powered Quiz Generation Starting...")
    print("🧠 AI Engine: Google AI Gemini 1.5 Flash")
    print("🎮 Quiz Modes: MCQ | True/False | Fill-Blank")
    print("🏆 Mission: Transform Education Through AI")
    print("=" * 50)
    
    # Production configuration
    port = int(os.getenv('PORT', 5000))
    debug_mode = os.getenv('FLASK_ENV') != 'production'
    
    if debug_mode:
        print("🌐 Local Development: http://localhost:5000")
        print("🔧 Debug Mode: ENABLED")
    else:
        print("🌍 Production Deployment: ACTIVE")
        print("🔧 Debug Mode: DISABLED")
    
    print("=" * 50)
    print("⚡ QuizGo System: READY FOR DEPLOYMENT")
    print("=" * 50)
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug_mode
    )
