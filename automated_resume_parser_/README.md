# Automated Resume Parser (Improved)

## Features
- Extracts name, email, and phone from uploaded resumes (PDF)
- Uses spaCy + PDFPlumber + regex
- Web interface to upload resumes

## How to Run

1. Install requirements:
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

2. Start app:
```bash
python run.py
```

3. Open [http://127.0.0.1:5000](http://127.0.0.1:5000) to upload resumes.
