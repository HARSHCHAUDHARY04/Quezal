# 🧠 Quezal - AI-Powered Quiz Generation Platform

<div align="center">
  <a href="https://quezal-ai.onrender.com" target="_blank"><img src="https://img.shields.io/badge/Live%20Demo-Quezal-brightgreen?style=for-the-badge" alt="Live Demo"></a>
  <img src="https://img.shields.io/badge/Version-2.0-purple?style=for-the-badge" alt="Version">
  <img src="https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Flask-2.3.3-green?style=for-the-badge&logo=flask" alt="Flask">
  <img src="https://img.shields.io/badge/Google%20AI-Gemini%202.0-orange?style=for-the-badge&logo=google" alt="Google AI">
  <img src="https://img.shields.io/badge/License-MIT-red?style=for-the-badge" alt="License">
</div>

## 📖 Overview

**Quezal** transforms PDF documents into interactive quizzes using Google's Gemini AI. Built with Flask and featuring a responsive UI, it empowers educators and learners to create engaging assessments.

### ✨ Key Features

- 🤖 **AI-Powered**: Google Gemini 2.0 Flash for quiz creation
- 👨‍🏫 **Dual Roles**: Teacher (create) and Student (practice) capabilities
- 📱 **Modern UI**: Responsive design with glassmorphism effects
- 👤 **Role-Based Auth**: Secure signup/login with user type selection
- 📊 **Dashboard**: Personal statistics and quiz management
- 📄 **PDF Processing**: Text extraction from documents
- 🎯 **Question Types**: MCQ, True/False, Fill-in-blanks, Essay

## 🏗️ Architecture & Tech Stack

### **Backend Stack**
- **Framework**: Flask 2.3.3 (Python web framework)
- **Database**: SQLite with direct connection
- **AI**: Google Generative AI (Gemini 2.0 Flash)
- **PDF Processing**: PyPDF2 for text extraction
- **Authentication**: Session-based with password hashing

### **Frontend Stack**
- **Languages**: HTML5, CSS3, JavaScript
- **Design**: Modern CSS with Flexbox/Grid
- **Fonts**: Inter & Plus Jakarta Sans
- **Responsive**: Mobile-first design

### **External APIs**
- **Google AI**: Gemini 2.0 Flash for quiz generation
- **Endpoint**: `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent`

## 📁 Project Structure

```
quiz/
├── 📄 app.py                      # Main Flask application
├── 📄 quiz_generator.py           # Standalone quiz generator script
├── 📄 requirements.txt            # Python dependencies
├── 📄 quezal.db                   # SQLite database
├── 📄 update_users.py             # Database migration script
├── 📄 .env                        # Environment variables (not in repo)
├── 📄 gamma_ai_prompt_short.md    # AI prompt documentation
├── 📁 templates/                  # HTML templates
│   ├── 📄 index.html             # Main landing page with role-based UI
│   └── 📄 user.html              # User dashboard
├── 📁 battle_uploads/            # Uploaded PDF files storage
├── 📁 battle_results/            # Generated quiz JSON files
├── 📁 .venv/                     # Python virtual environment
├── 📄 test_packages.py           # Test file for package verification
├── 📄 test_pdf_extraction.py     # Test file for PDF extraction
├── 📄 test_quiz_debug.py         # Test file for quiz debugging
└── 📄 test_token.py              # Test file for token verification
```

## 📂 Detailed File & Folder Descriptions

### **Core Application Files**

#### `app.py` - Main Flask Application
- **Purpose**: Core web application server
- **Features**:
  - Role-based user authentication (teacher/student signup, login, logout)
  - PDF upload and processing (teachers only)
  - Quiz generation using Google AI
  - User dashboard and profile management
  - Database operations (users, quizzes)
  - File download functionality
  - Session management with user type
  - Role-based access control
- **Routes**:
  - `GET /` - Main homepage
  - `GET /user` - User dashboard
  - `POST /upload` - PDF upload and quiz generation (teachers only)
  - `POST /api/signup` - User registration with role selection
  - `POST /api/login` - User authentication
  - `GET /api/me` - User profile information
  - `GET /api/my-quizzes` - User's quiz history (role-based)
  - `GET /api/take-quiz/<id>` - Take quiz (students only)
  - `DELETE /api/my-quizzes/<id>` - Delete quiz (teachers only)
  - `GET /download/<filename>` - Download quiz files

#### `quiz_generator.py` - Standalone Quiz Generator
- **Purpose**: Command-line quiz generation script
- **Features**:
  - PDF text extraction
  - Google AI integration
  - Backup quiz generation
  - Educational content focus
- **Use Case**: Testing and standalone quiz generation

#### `requirements.txt` - Python Dependencies
```python
Flask==2.3.3              # Web framework
flask-cors==4.0.0          # Cross-origin resource sharing
PyPDF2==3.0.1             # PDF text extraction
google-generativeai==0.8.3 # Google AI integration
python-dotenv==1.0.0       # Environment variable management
gunicorn==21.2.0           # Production WSGI server
werkzeug==2.3.7           # WSGI utilities
reportlab==4.2.2          # PDF generation
```

### **Template Files**

#### `templates/index.html` - Main Homepage
- **Purpose**: Primary user interface with role-based views
- **Features**:
  - Modern responsive design
  - Role-based authentication modal (teacher/student selection)
  - Dynamic interface based on user type
  - File upload with drag & drop (teachers only)
  - Quiz taking interface (students only)
  - Interactive quiz display
  - User statistics
  - Signup requirement overlay
- **Design Elements**:
  - Purple-cyan gradient theme
  - Glassmorphism effects
  - Floating particles animation
  - Smooth transitions and hover effects
  - User type selector with icons and descriptions

#### `templates/user.html` - User Dashboard
- **Purpose**: User management interface with role-based features
- **Features**:
  - Personal statistics (role-based)
  - Profile management
  - Password change functionality
  - Quiz history and management (role-based)
  - Responsive dashboard layout
- **Teacher Statistics**:
  - Total quizzes created
  - Total questions generated
  - Monthly activity
  - Quiz metadata (difficulty, type, date)
- **Student Statistics**:
  - Total quizzes taken
  - Practice history
  - Performance tracking
  - Available quizzes count

### **Storage Directories**

#### `battle_uploads/` - PDF File Storage
- **Purpose**: Stores uploaded PDF documents
- **Naming Convention**: `battle_document_YYYYMMDD_HHMMSS.pdf`
- **File Management**: Automatic cleanup and organization
- **Security**: File type validation and size limits (16MB max)

#### `battle_results/` - Quiz Data Storage
- **Purpose**: Stores generated quiz data in JSON format
- **Naming Convention**: `iqbattle_result_YYYYMMDD_HHMMSS.json`
- **Content Structure**:
```json
{
  "battle_document": "filename.pdf",
  "deployment_timestamp": "2024-01-01T12:00:00",
  "battle_parameters": {
    "num_questions": 8,
    "difficulty_protocol": "Medium",
    "battle_mode": "mcq",
    "question_formation": {"mcq": 8}
  },
  "battle_system": "IQBattle_v2.0_AI_Enhanced",
  "battle_commander": "Google_AI_Gemini_1.5_Flash",
  "battle_data": {
    "questions": [...]
  }
}
```

#### `venv/` - Python Virtual Environment
- **Purpose**: Isolated Python environment
- **Contents**:
  - `Scripts/` - Python executables and activation scripts
  - `Lib/site-packages/` - Installed Python packages
  - `pyvenv.cfg` - Virtual environment configuration

### **Database**

#### `quezal.db` - SQLite Database
- **Purpose**: User data and quiz metadata storage with role-based system
- **Tables**:

**Database Schema**:
- **Users**: ID, email, name, password_hash, user_type, created_at
- **Quizzes**: ID, user_id, filenames, question details, created_at

### **Role-Based System**

#### **👨‍🏫 Teacher Role**
- Upload PDFs and create AI quizzes
- Manage quiz library and view statistics

#### **👨‍🎓 Student Role**
- Take quizzes interactively
- Track progress and download for offline study

### **Test Files**
- `test_packages.py`: Verify dependencies
- `test_pdf_extraction.py`: Test PDF extraction
- `test_quiz_debug.py`: Debug quiz generation
- `test_token.py`: Test Google AI integration

## 🚀 Installation & Setup

### **Prerequisites**
- Python 3.8+
- Google AI API key
- Web browser

### **Quick Setup**
```bash
# Clone and navigate
git clone <repository-url>
cd quiz

# Setup environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Install and configure
pip install -r requirements.txt
# Create .env with GOOGLE_API_KEY=your_key

# Run application
python app.py  # Development
gunicorn app:app  # Production
```

Access at: http://localhost:5000

## 🔧 Configuration

### **Environment Variables**
- `GOOGLE_API_KEY`: Google AI Studio API key for Gemini access
- `FLASK_SECRET_KEY`: Secret key for session security
- `FLASK_ENV`: Environment mode (development/production)
- `PORT`: Application port (default: 5000)
- `PASSWORD_SALT`: Salt for password hashing (optional)

### **Application Settings**
- **Max File Size**: 16MB for PDF uploads
- **Supported Formats**: PDF only
- **Question Types**: MCQ, True/False, Fill-in-blanks, Essay
- **Difficulty Levels**: Easy, Medium, Hard
- **Question Range**: 4-20 questions per quiz

## 🎯 How It Works

### **1. Role-Based User Registration/Login**
1. User clicks "Sign Up" or "Login"
2. **Role Selection**: Choose between Teacher or Student
3. Form validation (email format, password strength)
4. Password hashing with salt
5. User data stored in SQLite database with role
6. Session creation with user type

### **2. Teacher Workflow (Content Creation)**
1. **PDF Upload**: Teacher uploads PDF (drag & drop or click)
2. File validation (type, size, content)
3. File saved to `battle_uploads/` directory
4. Text extraction using PyPDF2
5. Content validation and preprocessing
6. **AI Quiz Generation**: Extracted text sent to Google Gemini AI
7. Structured prompt with quiz parameters
8. AI generates questions in JSON format
9. Response parsing and validation
10. Quiz data saved to `battle_results/`
11. **Quiz Management**: Teacher can manage, download, or delete quizzes

### **3. Student Workflow (Content Consumption)**
1. **Quiz Discovery**: Student views available quizzes
2. **Quiz Selection**: Choose quiz to take
3. **Interactive Taking**: Questions rendered with interactive UI
4. Answer selection with visual feedback
5. Real-time answer validation
6. Score calculation and explanation display
7. **Practice History**: Track progress and performance

### **4. Role-Based Dashboard**
1. **Teacher Dashboard**: Statistics calculation (total quizzes created, questions generated)
2. **Student Dashboard**: Statistics calculation (total quizzes taken, practice history)
3. Quiz history with metadata (role-based)
4. Profile management capabilities
5. Role-specific actions (create vs. take quizzes)

## 🎨 UI Features
- Modern design with purple-cyan theme
- Responsive layout for all devices
- Interactive elements with smooth transitions

## 🔍 API Integration
- **Model**: Google Gemini 2.0 Flash
- **Endpoint**: `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent`
- **Authentication**: API key in URL parameter
- **Question Types**: MCQ, True/False, Fill-in-blank, Essay

## 🎯 Use Cases

### **👨‍🏫 For Teachers**
- **University Professors**: Create course assessments and practice materials
- **Corporate Trainers**: Generate training quizzes for employee development
- **Content Creators**: Build interactive educational content

### **👨‍🎓 For Students**
- **University Students**: Practice with course materials and prepare for exams
- **Self-Learners**: Practice with various topics and subjects
- **Test Preparers**: Use AI-generated questions for exam preparation

### **🏢 For Organizations**
- **Educational Institutions**: Streamline quiz creation and assessment processes
- **Training Companies**: Deliver scalable training programs
- **HR Departments**: Create employee assessment and evaluation tools

## 🧪 Testing
```bash
python test_packages.py      # Package installation verification
python test_pdf_extraction.py # PDF processing tests
python test_quiz_debug.py    # Quiz logic debugging
python test_token.py         # API connectivity tests
```

## 🚢 Deployment
```bash
# Development
python app.py

# Production with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 🔒 Security
- Password hashing with SHA-256 and salt
- Session-based authentication with CSRF protection
- File validation (PDF only, 16MB max)
- SQL injection prevention and XSS protection

## 📊 Performance
- Optimized frontend with efficient DOM manipulation
- Efficient database queries and file caching
- AI request optimization and error handling

## 🤝 Contributing
- Fork, create branch, make changes, add tests, submit PR
- Follow PEP 8 for Python code
- Add docstrings and comment complex logic

## 🐛 Troubleshooting

**Common Issues**
- Google AI API: Check key with `python test_token.py`
- PDF Upload: Verify with `python test_pdf_extraction.py`
- Database: Reinitialize with `python -c "from app import init_db; init_db()"`
- Authentication: Clear cache and check session configuration
- Role-Based System: Check user types with `python update_users.py`

## 📈 Future Plans
- Advanced analytics and collaboration tools
- Question bank and additional export formats
- LMS integration and enhanced AI capabilities
- Performance improvements with caching and database optimization

## 📜 License
MIT License

## 🙏 Acknowledgments
Google AI, Flask, Font Awesome, Google Fonts

---

<div align="center">
  <p><strong>Built with ❤️ for educators and learners</strong></p>
</div>
