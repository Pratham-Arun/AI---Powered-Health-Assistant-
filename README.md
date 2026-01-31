# 🩺 AI-Powered Health Assistant

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://aiphagg.streamlit.app/)

A comprehensive health assistant chatbot built with Streamlit and a custom Medical Engine, providing intelligent health insights, progress tracking, and professional health reports.

## Problem Statement
Seeking reliable health info and tracking tools shouldn't be complicated. This assistant solves the need for an easy, accessible platform that offers:
- Trustworthy health information and symptom guidance.
- Daily health tracking (Weight, Water, Meds).
- Professional documentation of health consultations.

## Features

### 🤖 Intelligent Health Chat
- **Medical Knowledge Base**: Detailed info on common symptoms (Headaches, Fever, etc.) and diagnostic tests.
- **Smart Conversational Logic**: Provides a clear "thought process" and redirects to related health topics.
- **Safety First**: Integrated emergency detection and mandatory medical disclaimers.

### 📊 Health Tracking Tools
- **BMI Calculator**: Immediate weight-to-height analysis with health status indicators.
- **Water Tracker**: Daily intake goal monitoring to ensure proper hydration.
- **Medicine Checklist**: Interactive daily to-do list to track your medication schedule.

### 📄 Professional Health Reports
- **PDF Export**: Generate a clean, structured PDF report of your chat summary, BMI, and daily goals.
- **Consultation History**: Automatically includes recent chat context for your records.

## Technologies / Tools Used

- **Frontend**: Streamlit (Web Framework), Custom CSS/HTML for Premium UI.
- **Backend & Logic**: Python 3.8+, Custom `MedicalEngine` logic.
- **AI/ML**: Hugging Face Transformers, PyTorch.
- **Reporting**: `fpdf2` for professional PDF generation.

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Step-by-Step Installation

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd AI---Powered-Health-Assistant-
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   # Windows: venv\Scripts\activate
   # macOS/Linux: source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**
   ```bash
   python -m streamlit run streamlit_app.py
   ```

## Usage
- **Chat**: Ask about symptoms or general health topics.
- **Tools**: Switch to the "Health Tools" tab to calculate BMI or check off medications.
- **Report**: Click "Download My Health Report" at the bottom of the chat to get your PDF.

---

⚠️ **Important Medical Disclaimer**: This AI assistant provides general health information only. It is not a substitute for professional medical advice, diagnosis, or treatment. Always consult with qualified healthcare professionals for medical concerns. In case of emergency, call your local emergency services immediately.

---
*Note: This project was built with the assistance of advanced AI tools to accelerate development and ensure high-quality code implementation.*
