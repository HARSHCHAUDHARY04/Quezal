# 🧠 Quezal - AI-Powered Quiz Generation Platform

<div align="center">
  <img src="https://img.shields.io/badge/Version-2.0-purple?style=for-the-badge" alt="Version">
  <img src="https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Flask-2.3.3-green?style=for-the-badge&logo=flask" alt="Flask">
  <img src="https://img.shields.io/badge/Google%20AI-Gemini%201.5-orange?style=for-the-badge&logo=google" alt="Google AI">
  <img src="https://img.shields.io/badge/License-MIT-red?style=for-the-badge" alt="License">
</div>

## 📖 Overview

**Quezal** is a modern, AI-powered web application that transforms PDF documents into interactive quizzes using Google's Gemini AI. Built with Flask and featuring a beautiful, responsive UI, Quezal empowers educators and learners to create engaging assessments effortlessly.

### ✨ Key Features

- 🤖 **AI-Powered Generation**: Uses Google Gemini 1.5 Flash for intelligent quiz creation
- 👨‍🏫 **Dual User System**: Teacher and Student roles with different capabilities
- 📱 **Modern UI/UX**: Beautiful, responsive design with glassmorphism effects
- 👤 **Role-Based Authentication**: Secure signup/login with user type selection
- 📊 **User Dashboard**: Personal statistics and quiz management
- 📄 **PDF Processing**: Extracts text from uploaded PDF documents
- 🎯 **Multiple Question Types**: MCQ, True/False, Fill-in-the-blanks, Essay questions
- 💾 **Data Persistence**: SQLite database for user data and quiz history
- 🔒 **Role-Based Access Control**: Teachers create, Students practice
- 📱 **Responsive Design**: Works seamlessly on desktop, tablet, and mobile

## 🏗️ Architecture & Tech Stack

### **Backend Stack**
- **Framework**: Flask 2.3.3 (Python web framework)
- **Database**: SQLite with SQL Alchemy integration
- **AI Integration**: Google Generative AI (Gemini 1.5 Flash)
- **PDF Processing**: PyPDF2 for text extraction
- **Authentication**: Session-based with password hashing
- **CORS**: Flask-CORS for cross-origin requests
- **Environment**: python-dotenv for configuration management

### **Frontend Stack**
- **Languages**: HTML5, CSS3, Vanilla JavaScript
- **Design**: Modern CSS with CSS Variables and Flexbox/Grid
- **Fonts**: Inter & Plus Jakarta Sans from Google Fonts
- **Icons**: Font Awesome 6.4.0
- **Animations**: CSS animations and transitions
- **Responsive**: Mobile-first responsive design

### **External APIs**
- **Google Generative AI**: Gemini 1.5 Flash model for quiz generation
- **Endpoint**: `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent`

## 📁 Project Structure

```
sumitquiz/
├── 📄 app.py                      # Main Flask application
├── 📄 quiz_generator.py           # Standalone quiz generator script
├── 📄 requirements.txt            # Python dependencies
├── 📄 quezal.db                   # SQLite database
├── 📄 update_users.py             # Database migration script
├── 📄 .env                        # Environment variables (not in repo)
├── 📁 templates/                  # HTML templates
│   ├── 📄 index.html             # Main landing page with role-based UI
│   ├── 📄 user.html              # User dashboard
│   └── 📄 index_new.html         # Alternative homepage
├── 📁 battle_uploads/            # Uploaded PDF files storage
├── 📁 battle_results/            # Generated quiz JSON files
├── 📁 uploads/                   # Legacy upload folder
├── 📁 results/                   # Legacy results folder
├── 📁 venv/                      # Python virtual environment
├── 📁 tests/                     # Test files
│   ├── 📄 test_packages.py
│   ├── 📄 test_pdf_extraction.py
│   ├── 📄 test_quiz_debug.py
│   └── 📄 test_token.py
└── 📁 documentation/             # Project documentation
    ├── 📄 FIXES_APPLIED.md
    ├── 📄 UI_IMPROVEMENTS.md
    ├── 📄 README.md
    └── 📄 gamma_ai_prompt_short.md # Gamma.ai presentation prompt
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

**Users Table**:
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    name TEXT,
    password_hash TEXT NOT NULL,
    user_type TEXT DEFAULT 'student',
    created_at TEXT NOT NULL
);
```

**Quizzes Table**:
```sql
CREATE TABLE quizzes (
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
```

### **Role-Based System**

#### **👨‍🏫 Teacher Role**
- **Purpose**: Create and manage educational content
- **Capabilities**:
  - Upload PDF documents for quiz generation
  - Create AI-powered quizzes from content
  - Manage personal quiz library
  - Download quiz files in various formats
  - Delete own quizzes
  - View quiz creation statistics
- **Interface Features**:
  - Upload zone with teacher icon
  - "My Created Quizzes" section
  - Quiz management tools
  - Creation statistics dashboard

#### **👨‍🎓 Student Role**
- **Purpose**: Practice and learn with generated quizzes
- **Capabilities**:
  - View all available quizzes
  - Take quizzes interactively
  - Practice with different topics
  - Track learning progress
  - Download quiz files for offline study
  - See quiz creator information
- **Interface Features**:
  - "Available Quizzes" section
  - Quiz taking interface
  - Progress tracking
  - Practice history

#### **🔐 Role-Based Access Control**
- **Authentication**: User type selection during signup
- **Permissions**: Server-side validation of user capabilities
- **Security**: Role-based API endpoint protection
- **Session Management**: User type stored securely in session

### **Test Files**

#### `test_packages.py`
- **Purpose**: Verify Python package installations
- **Tests**: Import tests for all required dependencies

#### `test_pdf_extraction.py`
- **Purpose**: Test PDF text extraction functionality
- **Tests**: PyPDF2 functionality and error handling

#### `test_quiz_debug.py`
- **Purpose**: Debug quiz generation and answer checking
- **Tests**: Answer validation logic and quiz data structure

#### `test_token.py`
- **Purpose**: Test Google AI API integration
- **Tests**: API connectivity and authentication

## 🚀 Installation & Setup

### **Prerequisites**
- Python 3.8 or higher
- Google AI Studio API key
- Modern web browser

### **1. Clone the Repository**
```bash
git clone <repository-url>
cd sumitquiz
```

### **2. Create Virtual Environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4. Environment Configuration**
Create a `.env` file in the project root:
```env
GOOGLE_API_KEY=your_google_ai_api_key_here
FLASK_SECRET_KEY=your_secret_key_here
FLASK_ENV=development
```

### **5. Initialize Database**
```bash
python -c "from app import init_db; init_db()"
```

### **6. Update Existing Users (Optional)**
If you have existing users, run the migration script to add user types:
```bash
python update_users.py
```

### **7. Run the Application**
```bash
# Development
python app.py

# Production
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### **8. Access the Application**
- **Local Development**: http://localhost:5000
- **Dashboard**: http://localhost:5000/user (requires login)

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

## 🎨 UI/UX Features

### **Design System**
- **Primary Color**: Purple (#7c3aed)
- **Secondary Color**: Cyan (#06b6d4)
- **Accent Color**: Amber (#f59e0b)
- **Typography**: Inter (body), Plus Jakarta Sans (headings)

### **Interactive Elements**
- **Hover Effects**: Smooth transitions and scaling
- **Loading States**: Spinners and progress indicators
- **Animations**: Floating particles and smooth transitions
- **Responsive**: Mobile-first design with breakpoints

### **User Experience**
- **Signup Requirement**: Overlay prompts for authentication
- **File Upload**: Enhanced drag & drop with visual feedback
- **Real-time Validation**: Instant form validation
- **Error Handling**: User-friendly error messages
- **Success Feedback**: Celebratory animations and messages

## 🔍 API Integration Details

### **Google Generative AI (Gemini)**
- **Model**: gemini-1.5-flash-latest
- **Endpoint**: `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent`
- **Authentication**: API key in URL parameter
- **Request Format**:
```json
{
  "contents": [{
    "parts": [{
      "text": "prompt_text"
    }]
  }]
}
```

### **Quiz Generation Prompt Structure**
```javascript
Battle Mode Configurations:
- MCQ Assault Mode: Multiple choice with 4 options
- Binary Strike Mode: True/False questions
- Stealth Mission Mode: Fill-in-the-blank questions
- Intelligence Report Mode: Essay questions
- Mixed Battle Formation: Combination of all types
```

## 🎯 Use Cases & Applications

### **👨‍🏫 For Teachers**
- **University Professors**: Create course assessments and practice materials
- **Corporate Trainers**: Generate training quizzes for employee development
- **Content Creators**: Build interactive educational content
- **Online Educators**: Create engaging assessments for remote learning
- **Subject Matter Experts**: Develop specialized quiz content

### **👨‍🎓 For Students**
- **University Students**: Practice with course materials and prepare for exams
- **Corporate Learners**: Complete training assessments and track progress
- **Self-Learners**: Practice with various topics and subjects
- **Test Preparers**: Use AI-generated questions for exam preparation
- **Skill Developers**: Practice specific skills through targeted quizzes

### **🏢 For Organizations**
- **Educational Institutions**: Streamline quiz creation and assessment processes
- **Training Companies**: Deliver scalable training programs
- **HR Departments**: Create employee assessment and evaluation tools
- **Content Platforms**: Provide interactive learning experiences
- **Research Teams**: Generate survey instruments and assessment tools

## 🧪 Testing

### **Run All Tests**
```bash
python test_packages.py      # Package installation verification
python test_pdf_extraction.py # PDF processing tests
python test_quiz_debug.py    # Quiz logic debugging
python test_token.py         # API connectivity tests
```

### **Debug Quiz Generation**
```bash
python test_quiz_debug.py
```
This script:
- Tests answer checking logic
- Analyzes existing quiz files
- Provides debugging information
- Validates quiz data structure

## 🚢 Deployment

### **Development Deployment**
```bash
python app.py
```

### **Production Deployment**
```bash
# Using Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Using Docker (create Dockerfile)
docker build -t quezal .
docker run -p 5000:5000 quezal
```

### **Environment Variables for Production**
```env
FLASK_ENV=production
GOOGLE_API_KEY=your_production_api_key
FLASK_SECRET_KEY=secure_random_key
PORT=5000
```

## 🔒 Security Features

### **Authentication**
- Password hashing with SHA-256 and salt
- Session-based authentication
- Secure session management
- CSRF protection through session tokens

### **File Security**
- File type validation (PDF only)
- File size limits (16MB maximum)
- Secure file storage with timestamp naming
- Input sanitization for file uploads

### **Data Protection**
- SQL injection prevention
- XSS protection through proper escaping
- Secure error handling
- Environment variable protection

## 📊 Performance Optimizations

### **Frontend**
- CSS minification and optimization
- Efficient DOM manipulation
- Debounced event handlers
- Optimized animations with hardware acceleration

### **Backend**
- Efficient database queries
- File caching strategies
- Asynchronous operations where possible
- Memory management for large files

### **AI Integration**
- Request timeout handling
- Error recovery mechanisms
- Efficient prompt optimization
- Response parsing optimization

## 🤝 Contributing

### **Development Setup**
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Submit a pull request

### **Code Style**
- Follow PEP 8 for Python code
- Use meaningful variable names
- Add docstrings for functions
- Comment complex logic

## 🐛 Troubleshooting

### **Common Issues**

**1. Google AI API Errors**
```bash
# Check API key
echo $GOOGLE_API_KEY

# Test API connectivity
python test_token.py
```

**2. PDF Upload Issues**
```bash
# Check file permissions
python test_pdf_extraction.py

# Verify file size and type
```

**3. Database Issues**
```bash
# Reinitialize database
python -c "from app import init_db; init_db()"
```

**4. Authentication Problems**
```bash
# Clear browser cache and cookies
# Check session configuration
```

**5. Role-Based System Issues**
```bash
# Check user type in database
python update_users.py

# Verify role-based permissions
# Ensure teachers can create, students can take quizzes
```

## 📈 Future Enhancements

### **Planned Features**
- **Advanced Analytics**: Detailed quiz performance metrics
- **Collaboration Tools**: Team quiz creation and sharing
- **Question Bank**: Reusable question repository
- **Export Options**: Multiple format exports (Word, PowerPoint)
- **Integration APIs**: LMS integration capabilities
- **Advanced AI**: Custom AI model training

### **Technical Improvements**
- **Caching Layer**: Redis for improved performance
- **Database Migration**: PostgreSQL for production
- **Microservices**: Service-oriented architecture
- **API Documentation**: OpenAPI/Swagger documentation

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google AI**: Gemini 1.5 Flash for intelligent quiz generation
- **Flask Community**: Excellent web framework and documentation
- **Font Awesome**: Beautiful icons for UI enhancement
- **Google Fonts**: Typography (Inter & Plus Jakarta Sans)

## 📞 Support

For support, please:
1. Check the troubleshooting section
2. Review existing issues
3. Create a new issue with detailed description
4. Include error logs and environment details

---

<div align="center">
  <p><strong>Built with ❤️ for educators and learners worldwide</strong></p>
  <p><em>Transforming education through AI-powered quiz generation</em></p>
</div>
