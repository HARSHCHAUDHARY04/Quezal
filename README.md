# 🧠 Quezal - AI-Powered Quiz Generation Platform

<div align="center">
  <img src="https://img.shields.io/badge/Version-3.0-purple?style=for-the-badge" alt="Version">
  <img src="https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Django-5.0-green?style=for-the-badge&logo=django" alt="Django">
  <img src="https://img.shields.io/badge/Google%20AI-Gemini%201.5-orange?style=for-the-badge&logo=google" alt="Google AI">
  <img src="https://img.shields.io/badge/Vercel-Frontend-black?style=for-the-badge&logo=vercel" alt="Vercel">
  <img src="https://img.shields.io/badge/Render-Backend-lightgray?style=for-the-badge&logo=render" alt="Render">
</div>

---

## 📖 Table of Contents
1. [Overview](#-overview)
2. [Architecture](#-architecture)
3. [Core Features](#-core-features)
4. [Tech Stack](#-tech-stack)
5. [In-Depth Workflows](#-in-depth-workflows)
6. [API Documentation](#-api-documentation)
7. [Database Schema](#-database-schema)
8. [Installation & Setup](#-installation--setup)
9. [Deployment Strategy](#-deployment-strategy)
10. [Design Philosophy](#-design-philosophy)

---

## 📖 Overview

**Quezal** is an enterprise-grade, AI-powered educational platform designed to bridge the gap between static content and active learning. By leveraging the advanced reasoning capabilities of **Google Gemini 1.5 Flash**, Quezal enables educators to transform complex PDF documents into high-quality, pedagogical assessments in seconds.

The platform is built on a **modern decoupled architecture**, ensuring high performance, global scalability, and a seamless user experience across all devices.

---

## 🏗️ Architecture

Quezal follows a **Decoupled Single Page Application (SPA)** architecture:

*   **Backend (The Intelligence Layer)**: A robust Django 5.0 REST API hosted on **Render**. It handles intensive tasks like PDF parsing, AI orchestration, and secure data management.
*   **Frontend (The Interaction Layer)**: A high-fidelity, glassmorphic UI built with Vanilla JS and HSL-based CSS tokens, hosted on **Vercel's Edge Network**.
*   **Database (The Persistence Layer)**: A distributed PostgreSQL instance managed by **Neon.tech**, providing low-latency data access and automated backups.

---

## ✨ Core Features

### 🤖 Intelligent Generation
*   **Context-Aware AI**: Uses deep-context parsing to ensure questions are accurate and relevant to the source material.
*   **Multi-Mode Assessment**: Supports MCQ, True/False, Fill-in-the-blanks, and Essay formats.
*   **Dynamic Difficulty**: AI-driven scaling (Easy, Medium, Hard) to match learner proficiency.

### 👨‍🏫 Teacher Ecosystem
*   **Bulk Upload**: Drag-and-drop PDF processing (up to 16MB).
*   **Quiz Library**: A personal repository for managing and archiving generated assessments.
*   **Analytics Preview**: Real-time stats on questions generated and content coverage.

### 👨‍🎓 Student Experience
*   **Interactive Testing**: A distraction-free, animated quiz interface.
*   **Instant Feedback**: Detailed explanations for every answer, powered by AI.
*   **Universal Access**: Global quiz library for discovering content created by educators.

---

## 🏗️ Tech Stack

### **Backend (Django Core)**
- **Framework**: Django 5.0 + Django REST Framework (DRF)
- **AI Orchestration**: Google Generative AI SDK
- **Static Assets**: WhiteNoise (Optimized for production serving)
- **Security**: Django-CORS-Headers, Argon2 Password Hashing
- **File Processing**: PyPDF2 (Binary stream extraction)

### **Frontend (Modern Vanilla)**
- **Styling**: HSL Color Tokens, Flexbox/Grid Layouts, Glassmorphism design system.
- **Interactions**: Async Fetch API with `{ credentials: 'include' }` for cross-domain sessions.
- **Animations**: CSS Variables + Web Animations API for 60fps micro-interactions.

---

## 🎯 In-Depth Workflows

### **1. AI Generation Pipeline**
1.  **Ingestion**: User uploads a PDF. The frontend sends it as `multipart/form-data` to `/upload`.
2.  **Extraction**: The Django backend extracts raw text streams from the PDF buffers.
3.  **Prompt Engineering**: A multi-layered prompt is constructed, defining JSON schemas and pedagogical constraints for Gemini.
4.  **Synthesis**: Gemini 1.5 Flash processes the text and generates a structured JSON payload.
5.  **Refinement**: The backend validates the JSON structure and commits metadata to PostgreSQL.

### **2. Cross-Domain Authentication**
*   **Strategy**: Token-less, secure cookie-based auth.
*   **Implementation**: Vercel frontend communicates with Render backend using `CORS_ALLOW_CREDENTIALS` and `SameSite='None'`.
*   **Security**: CSRF protection is handled via custom headers to prevent malicious cross-site requests.

---

## 🔍 API Documentation

| Endpoint | Method | Role | Description |
| :--- | :--- | :--- | :--- |
| `/api/signup` | `POST` | Public | Register as Teacher or Student. |
| `/api/login` | `POST` | Public | Secure authentication and session start. |
| `/upload` | `POST` | Teacher | Process PDF and generate AI quiz. |
| `/api/my-quizzes` | `GET` | Both | Fetch user-specific quiz history. |
| `/api/me` | `GET` | Both | Retrieve current session user data. |
| `/api/profile` | `PUT` | Both | Update user name and profile data. |

---

## 🐘 Database Schema

### **User Table**
- `id`: Unique Identifier
- `email`: Authenticated Email
- `user_type`: 'teacher' | 'student'
- `password_hash`: Secure Argon2 Hash

### **Quiz Table**
- `id`: Unique Identifier
- `user_id`: Reference to Creator
- `result_filename`: Path to AI-generated JSON
- `difficulty`: Easy/Medium/Hard
- `mode`: mcq/binary/mixed

---

## 🚀 Installation & Setup

### **Local Development**
1.  **Clone**: `git clone <repo-url>`
2.  **Backend Setup**:
    ```bash
    cd Quezal
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    python manage.py migrate
    python manage.py runserver
    ```
3.  **Frontend Setup**:
    *   Navigate to `Quezal/frontend`.
    *   Set `API_BASE_URL` in `index.html` to `http://127.0.0.1:8000`.

---

## 🚢 Deployment Strategy

### **Backend (Render)**
*   **Root Directory**: `.`
*   **Build**: `./build.sh`
*   **Environment Variables**:
    *   `DATABASE_URL`: Your Neon PostgreSQL string.
    *   `GOOGLE_API_KEY`: Your Gemini key.

### **Frontend (Vercel)**
*   **Root Directory**: `Quezal/frontend`
*   **Build Command**: `npm run build`
*   **Environment Variables**:
    *   `BACKEND_URL`: Your live Render URL.

---

## 🎨 Design Philosophy

Quezal follows the **"Vanguard Modern"** design system:
*   **Visual Hierarchy**: Uses deep shadows and Z-index layering to separate content.
*   **Micro-Animations**: Hover states use subtle `scale(1.02)` and `backdrop-filter: blur()` for a premium feel.
*   **Color Palette**: 
    - `Primary`: Purple HSL(262, 83%, 58%)
    - `Accent`: Cyan HSL(189, 94%, 43%)
    - `Dark Mode`: Slate HSL(222, 47%, 11%)

---

<div align="center">
  <p><strong>Built with ❤️ by the Quezal Engineering Team</strong></p>
  <p><em>Empowering the next generation of educators.</em></p>
</div>
