# NDPA Compliance Checker

An AI-driven web application that automatically checks
software documents against the Nigeria Data Protection
Act (NDPA) 2023 using Natural Language Processing.

## Artificial Intelligence Project
Department of Computer Science

---

## What It Does

This system allows Nigerian software developers and
organisations to upload their software documents and
automatically check them against the NDPA 2023.
It uses the MiniLM sentence transformer model to
compare document sentences against 35 extracted
NDPA rules and generates a detailed compliance report.

---

## Technology Stack

- Backend: Python Flask
- Database: SQLite with SQLAlchemy
- AI Model: all-MiniLM-L6-v2 (Sentence Transformers)
- PDF Processing: PyPDF2
- Report Generation: ReportLab
- Frontend: HTML, CSS, Bootstrap 5
- Authentication: Flask-Login with bcrypt

---

## How To Run Locally

### Step 1: Clone the repository
git clone https://github.com/yourusername/ndpa-compliance-checker.git
cd ndpa-compliance-checker

### Step 2: Create virtual environment
python -m venv venv
venv\Scripts\activate

### Step 3: Install dependencies
pip install -r requirements.txt

### Step 4: Run the application
python app.py

### Step 5: Open in browser
http://127.0.0.1:5000

---

## Default Admin Account

Email: admin@ndpa.com
Password: admin123

---

## Sample Test Documents

Located in tests/sample_documents/

- compliant_srs.txt: Well-designed compliant software
- non_compliant_srs.txt: Poorly designed non-compliant software
- mixed_srs.txt: Mixed compliance health system

---

## System Features

- User registration and login
- Secure password hashing
- Document upload (PDF and TXT)
- AI-powered compliance checking
- 35 NDPA 2023 rules pre-loaded
- Detailed compliance reports
- PDF report download
- Compliance history tracking
- Admin panel for user management
- Professional responsive UI

---

## Compliance Score Interpretation

- Above 70%: Compliant
- 40% to 70%: Partially Compliant
- Below 40%: Non-Compliant

---

## Project Structure

ndpa-compliance-checker/
    app.py
    config.py
    models/
    routes/
    services/
    templates/
    static/
        css/
        js/
    data/
    tests/
    requirements.txt
    README.md