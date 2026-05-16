import os
import json
from datetime import datetime
import hashlib
import secrets
from io import BytesIO
import PyPDF2
import requests
from dotenv import load_dotenv

from django.http import JsonResponse, FileResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.shortcuts import render
from .models import User, Quiz

# Load environment variables
load_dotenv()

# Configure battle arsenal folders
UPLOAD_FOLDER = os.path.join(settings.BASE_DIR, 'battle_uploads')
RESULTS_FOLDER = os.path.join(settings.BASE_DIR, 'battle_results')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

def hash_password(password: str) -> str:
    salt = os.getenv('PASSWORD_SALT', 'quezal_salt')
    return hashlib.sha256((salt + password).encode('utf-8')).hexdigest()

def get_current_user_id(request):
    return request.session.get('user_id')

def get_current_user_type(request):
    return request.session.get('user_type', 'student')

def extract_generated_text(result):
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
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text() + "\n"
            return text.strip()
    except Exception as e:
        print(f"❌ PDF intelligence extraction failed: {e}")
        return None

def generate_battle_questions(pdf_text, num_questions=8, difficulty="Medium", question_types="mixed"):
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ No AI battle credentials found! Check your .env battle config")
        return None
        
    print(f"✅ AI Battle Commander authenticated: {api_key[:10]}...")
    print(f"⚔️ Battle mode: {question_types}")
    print(f"🎯 Difficulty protocol: {difficulty}")
    
    if not pdf_text or len(pdf_text.strip()) < 100:
        print("❌ Insufficient PDF text for question generation")
        return None
    
    # AI Battle Command Center endpoint - Using Gemini Flash Latest for broader quota availability
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent"
    
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
    
    if question_types in battle_modes:
        mode_config = battle_modes[question_types]
        battle_instruction = mode_config["instruction"]
        battle_example = mode_config["example"]
    else:
        battle_instruction = "Deploy a STRATEGIC MIX of all battle question types: MCQ Assault, Binary Strike, Stealth Mission, and Intelligence Report."
        battle_example = "Mix of mcq, true_false, fill_blank, and essay questions"
    
    battle_prompt = f"""
    IQBATTLE MISSION BRIEFING
    ========================
    
    Battle Intelligence Source:
    {pdf_text[:15000]}
    
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
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            result = response.json()
            generated_text = extract_generated_text(result)
            if not generated_text:
                return {"error": "AI Battle Commander failed to generate intelligence"}
            
            generated_text = generated_text.strip()
            if generated_text.startswith("```"):
                if generated_text.startswith("```json"):
                    generated_text = generated_text[7:]
                else:
                    generated_text = generated_text[3:]
            if generated_text.endswith("```"):
                generated_text = generated_text[:-3]
            
            try:
                battle_data = json.loads(generated_text)
                return battle_data
            except json.JSONDecodeError as e:
                return {"error": "Battle data parsing failed. The AI response was not in a valid format."}
        elif response.status_code == 429:
            return {"error": "Google AI Quota Exceeded. Please wait 60 seconds and try again."}
        else:
            return {"error": f"AI Battle Command Error ({response.status_code}): {response.text[:200]}"}
            
    except Exception as e:
        return None

def generate_quiz_pdf(archive: dict) -> bytes:
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        from reportlab.lib.units import inch
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
        
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

@require_http_methods(["GET"])
def battle_arena(request):
    return render(request, 'index.html')

@require_http_methods(["GET"])
def user_dashboard_page(request):
    if not get_current_user_id(request):
        return render(request, 'index.html')
    return render(request, 'user.html')

@csrf_exempt
@require_http_methods(["POST"])
def api_signup(request):
    try:
        data = json.loads(request.body) if request.body else {}
        email = (data.get('email') or '').strip().lower()
        password = (data.get('password') or '').strip()
        name = (data.get('name') or '').strip() or None
        user_type = (data.get('user_type') or 'student').strip().lower()
        
        if user_type not in ['teacher', 'student']:
            return JsonResponse({'success': False, 'error': 'Invalid user type. Must be teacher or student'}, status=400)
        
        if not email or not password:
            return JsonResponse({'success': False, 'error': 'Email and password are required'}, status=400)
            
        if User.objects.filter(email=email).exists():
            return JsonResponse({'success': False, 'error': 'Email already in use'}, status=409)
            
        user = User.objects.create(
            email=email,
            name=name,
            password_hash=hash_password(password),
            user_type=user_type
        )
        
        request.session['user_id'] = user.id
        request.session['user_type'] = user.user_type
        request.session.modified = True
        
        return JsonResponse({'success': True, 'user': {'id': user.id, 'email': email, 'name': name, 'user_type': user_type}})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def api_login(request):
    try:
        data = json.loads(request.body) if request.body else {}
        email = (data.get('email') or '').strip().lower()
        password = (data.get('password') or '').strip()
        
        if not email or not password:
            return JsonResponse({'success': False, 'error': 'Email and password are required'}, status=400)
            
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Invalid credentials'}, status=401)
            
        if user.password_hash != hash_password(password):
            return JsonResponse({'success': False, 'error': 'Invalid credentials'}, status=401)
            
        request.session['user_id'] = user.id
        request.session['user_type'] = user.user_type
        request.session.modified = True
        
        return JsonResponse({'success': True, 'user': {'id': user.id, 'email': email, 'name': user.name, 'user_type': user.user_type}})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def api_logout(request):
    request.session.pop('user_id', None)
    request.session.pop('user_type', None)
    request.session.modified = True
    return JsonResponse({'success': True})

@require_http_methods(["GET"])
def api_me(request):
    user_id = get_current_user_id(request)
    if not user_id:
        return JsonResponse({'authenticated': False})
        
    try:
        user = User.objects.get(id=user_id)
        return JsonResponse({'authenticated': True, 'user': {'id': user.id, 'email': user.email, 'name': user.name, 'user_type': user.user_type}})
    except User.DoesNotExist:
        return JsonResponse({'authenticated': False})

@csrf_exempt
@require_http_methods(["POST"])
def deploy_battle(request):
    try:
        user_id = get_current_user_id(request)
        if not user_id:
            return JsonResponse({'error': 'Authentication required'}, status=401)
        
        if 'pdf_file' not in request.FILES:
            return JsonResponse({'error': 'No PDF battle document uploaded'}, status=400)
            
        battle_file = request.FILES['pdf_file']
        if battle_file.name == '':
            return JsonResponse({'error': 'No battle document selected'}, status=400)
            
        num_questions = int(request.POST.get('num_questions', 8))
        difficulty = request.POST.get('difficulty', 'Medium')
        question_types = request.POST.get('question_types', 'mixed')
        
        if num_questions < 4:
            return JsonResponse({'error': 'Minimum 4 questions required for IQBattle deployment'}, status=400)
            
        battle_filename = f"battle_document_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        battle_path = os.path.join(UPLOAD_FOLDER, battle_filename)
        
        with open(battle_path, 'wb+') as destination:
            for chunk in battle_file.chunks():
                destination.write(chunk)
                
        battle_intelligence = extract_text_from_pdf(battle_path)
        if not battle_intelligence:
            return JsonResponse({'error': 'Failed to extract battle intelligence from PDF'}, status=400)
            
        battle_questions = generate_battle_questions(battle_intelligence, num_questions, difficulty, question_types)
        
        if not battle_questions or (isinstance(battle_questions, dict) and 'error' in battle_questions):
            error_msg = battle_questions.get('error') if isinstance(battle_questions, dict) else "AI Battle Commander failed to generate questions."
            status_code = 429 if "Quota Exceeded" in error_msg else 500
            return JsonResponse({'error': error_msg}, status=status_code)
            
        if 'questions' not in battle_questions or not battle_questions['questions']:
            return JsonResponse({'error': 'Generated questions are invalid. Please try again.'}, status=500)
            
        for i, q in enumerate(battle_questions['questions']):
            if not q.get('question') or not q.get('correct_answer'):
                return JsonResponse({'error': f'Question {i+1} is incomplete. Please try again.'}, status=500)
                
        battle_result_filename = f"iqbattle_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        battle_result_path = os.path.join(RESULTS_FOLDER, battle_result_filename)
        
        question_formation = {}
        if 'questions' in battle_questions:
            for q in battle_questions['questions']:
                qtype = q.get('type', 'mcq')
                question_formation[qtype] = question_formation.get(qtype, 0) + 1
                
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
            
        try:
            user = User.objects.get(id=user_id)
            Quiz.objects.create(
                user=user,
                result_filename=battle_result_filename,
                original_filename=battle_file.name,
                num_questions=num_questions,
                difficulty=difficulty,
                mode=question_types
            )
        except Exception as e:
            print(f"⚠️ Failed to persist quiz metadata: {e}")
            
        return JsonResponse({
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
        return JsonResponse({
            'error': f'Battle system failure: {str(e)}',
            'battle_status': 'MISSION_FAILED'
        }, status=500)

@require_http_methods(["GET"])
def download_battle_results(request, filename):
    try:
        fmt = request.GET.get('format', 'json')
        battle_file_path = os.path.join(RESULTS_FOLDER, filename)
        if not os.path.exists(battle_file_path):
            raise Http404("Battle archive not found")
            
        if fmt == 'pdf':
            with open(battle_file_path, 'r') as f:
                data = json.load(f)
            pdf_bytes = generate_quiz_pdf(data)
            response = FileResponse(BytesIO(pdf_bytes), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{filename.replace(".json", ".pdf")}"'
            return response
            
        response = FileResponse(open(battle_file_path, 'rb'), content_type='application/json')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    except Http404:
        raise
    except Exception as e:
        return JsonResponse({
            'error': f'Battle archive retrieval failed: {str(e)}',
            'battle_status': 'ARCHIVE_NOT_FOUND'
        }, status=404)

@require_http_methods(["GET"])
def api_my_quizzes(request):
    user_id = get_current_user_id(request)
    user_type = get_current_user_type(request)
    if not user_id:
        return JsonResponse({'success': False, 'error': 'Not authenticated'}, status=401)
        
    try:
        quizzes = Quiz.objects.filter(user_id=user_id).order_by('-id')
        quizzes_list = [
            {
                'id': q.id,
                'result_filename': q.result_filename,
                'original_filename': q.original_filename,
                'num_questions': q.num_questions,
                'difficulty': q.difficulty,
                'mode': q.mode,
                'created_at': q.created_at.isoformat()
            } for q in quizzes
        ]
        return JsonResponse({'success': True, 'quizzes': quizzes_list, 'user_type': user_type})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["DELETE"])
def api_delete_my_quiz(request, quiz_id):
    user_id = get_current_user_id(request)
    if not user_id:
        return JsonResponse({'success': False, 'error': 'Not authenticated'}, status=401)
        
    try:
        quiz = Quiz.objects.get(id=quiz_id, user_id=user_id)
        quiz.delete()
        return JsonResponse({'success': True})
    except Quiz.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Quiz not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["GET", "PUT"])
def api_profile(request):
    user_id = get_current_user_id(request)
    if not user_id:
        return JsonResponse({'success': False, 'error': 'Not authenticated'}, status=401)
        
    try:
        user = User.objects.get(id=user_id)
        if request.method == 'GET':
            return JsonResponse({'success': True, 'profile': {
                'id': user.id, 'email': user.email, 'name': user.name, 'created_at': user.created_at.isoformat()
            }})
        else:
            data = json.loads(request.body) if request.body else {}
            name = (data.get('name') or '').strip() or None
            user.name = name
            user.save()
            return JsonResponse({'success': True})
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'User not found'}, status=404)

@csrf_exempt
@require_http_methods(["POST"])
def api_change_password(request):
    user_id = get_current_user_id(request)
    if not user_id:
        return JsonResponse({'success': False, 'error': 'Not authenticated'}, status=401)
        
    try:
        data = json.loads(request.body) if request.body else {}
        current_password = (data.get('current_password') or '').strip()
        new_password = (data.get('new_password') or '').strip()
        
        if not current_password or not new_password:
            return JsonResponse({'success': False, 'error': 'Both current and new password required'}, status=400)
            
        user = User.objects.get(id=user_id)
        if user.password_hash != hash_password(current_password):
            return JsonResponse({'success': False, 'error': 'Current password incorrect'}, status=400)
            
        user.password_hash = hash_password(new_password)
        user.save()
        return JsonResponse({'success': True})
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'User not found'}, status=404)

@require_http_methods(["GET"])
def get_battle_statistics(request):
    try:
        battle_stats = {
            'total_battles': 0,
            'battle_formations': {},
            'difficulty_protocols': {},
            'recent_battles': [],
            'battle_system_status': 'OPERATIONAL'
        }
        
        if os.path.exists(RESULTS_FOLDER):
            battle_files = [f for f in os.listdir(RESULTS_FOLDER) if f.endswith('.json')]
            battle_stats['total_battles'] = len(battle_files)
            
            for battle_file in sorted(battle_files)[-10:]:
                battle_path = os.path.join(RESULTS_FOLDER, battle_file)
                try:
                    with open(battle_path, 'r') as f:
                        battle_data = json.load(f)
                    
                    if 'battle_parameters' in battle_data and 'question_formation' in battle_data['battle_parameters']:
                        formations = battle_data['battle_parameters']['question_formation']
                        for formation, count in formations.items():
                            battle_stats['battle_formations'][formation] = battle_stats['battle_formations'].get(formation, 0) + count
                    
                    if 'battle_parameters' in battle_data:
                        difficulty = battle_data['battle_parameters'].get('difficulty_protocol', 'Medium')
                        battle_stats['difficulty_protocols'][difficulty] = battle_stats['difficulty_protocols'].get(difficulty, 0) + 1
                    
                    battle_stats['recent_battles'].append({
                        'battle_id': battle_file,
                        'deployment_time': battle_data.get('deployment_timestamp'),
                        'questions_deployed': battle_data['battle_parameters'].get('num_questions', 0),
                        'battle_mode': battle_data['battle_parameters'].get('battle_mode', 'mixed'),
                        'difficulty': battle_data['battle_parameters'].get('difficulty_protocol', 'Medium')
                    })
                except:
                    continue
        
        return JsonResponse(battle_stats)
    except Exception as e:
        return JsonResponse({
            'error': f'Battle statistics retrieval failed: {str(e)}',
            'battle_system_status': 'STATISTICS_ERROR'
        }, status=500)

@require_http_methods(["GET"])
def api_take_quiz(request, quiz_id):
    user_id = get_current_user_id(request)
    user_type = get_current_user_type(request)
    
    if not user_id:
        return JsonResponse({'success': False, 'error': 'Authentication required'}, status=401)
    
    if user_type != 'student':
        return JsonResponse({'success': False, 'error': 'Only students can take quizzes'}, status=403)
        
    try:
        quiz = Quiz.objects.select_related('user').get(id=quiz_id)
        quiz_file_path = os.path.join(RESULTS_FOLDER, quiz.result_filename)
        
        if not os.path.exists(quiz_file_path):
            return JsonResponse({'success': False, 'error': 'Quiz file not found'}, status=404)
            
        with open(quiz_file_path, 'r', encoding='utf-8') as f:
            quiz_data = json.load(f)
            
        return JsonResponse({
            'success': True,
            'quiz': {
                'id': quiz.id,
                'filename': quiz.result_filename,
                'original_filename': quiz.original_filename,
                'num_questions': quiz.num_questions,
                'difficulty': quiz.difficulty,
                'mode': quiz.mode,
                'created_at': quiz.created_at.isoformat(),
                'creator_name': quiz.user.name,
                'questions': quiz_data.get('battle_data', {}).get('questions', [])
            }
        })
    except Quiz.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Quiz not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@require_http_methods(["GET"])
def battle_system_health(request):
    try:
        health_status = {
            'battle_system': 'IQBattle_v2.0_Django',
            'ai_commander': 'Google_AI_Gemini_1.5_Flash',
            'system_status': 'OPERATIONAL',
            'battle_arsenal_ready': os.path.exists(UPLOAD_FOLDER),
            'battle_archives_ready': os.path.exists(RESULTS_FOLDER),
            'ai_credentials_loaded': bool(os.getenv("GOOGLE_API_KEY")),
            'max_arsenal_size': '16MB',
            'supported_battle_modes': ['mixed', 'mcq', 'true_false', 'fill_blank', 'essay'],
            'last_system_check': datetime.now().isoformat()
        }
        
        if all([
            health_status['battle_arsenal_ready'],
            health_status['battle_archives_ready'],
            health_status['ai_credentials_loaded']
        ]):
            health_status['overall_status'] = 'READY_FOR_BATTLE'
        else:
            health_status['overall_status'] = 'SYSTEM_COMPROMISED'
        
        return JsonResponse(health_status)
    except Exception as e:
        return JsonResponse({
            'battle_system': 'IQBattle_v2.0_Django',
            'system_status': 'CRITICAL_FAILURE',
            'error': str(e),
            'last_system_check': datetime.now().isoformat()
        }, status=500)
