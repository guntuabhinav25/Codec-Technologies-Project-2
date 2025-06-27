import os
import re
import pdfplumber
import spacy
from flask import request
from werkzeug.utils import secure_filename
from app import app

# Load spaCy NLP model
nlp = spacy.load("en_core_web_sm")

@app.route('/')
def index():
    return '''
        <h2>Resume Upload</h2>
        <form action="/upload" method="post" enctype="multipart/form-data">
            <input type="file" name="resume" required>
            <input type="submit" value="Upload">
        </form>
    '''

@app.route('/upload', methods=['POST'])
def upload_resume():
    if 'resume' not in request.files:
        return "No file part"
    file = request.files['resume']
    if file.filename == '':
        return "No selected file"
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Parse PDF with PDFPlumber
        text = ""
        if filepath.lower().endswith(".pdf"):
            with pdfplumber.open(filepath) as pdf:
                for page in pdf.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + "\n"
        else:
            return "Only PDF files are currently supported for parsing."

        # Run spaCy NLP on the text
        doc = nlp(text)

        # Improved name extraction
        names = list({ent.text.strip() for ent in doc.ents if ent.label_ == "PERSON" and len(ent.text.split()) <= 3})
        names = names[:2] if names else ["Not found"]

        # Email extraction
        emails = list({token.text for token in doc if token.like_email})
        if not emails:
            emails = ["Not found"]

        # Improved phone extraction using regex
        phones = re.findall(r'\+?\d[\d\s().-]{7,}\d', text)
        phones = list(set([p.strip() for p in phones]))
        if not phones:
            phones = ["Not found"]

        result_html = f"<h3>Parsed Results</h3><ul>"
        result_html += f"<li><strong>Name(s):</strong> {', '.join(names)}</li>"
        result_html += f"<li><strong>Email(s):</strong> {', '.join(emails)}</li>"
        result_html += f"<li><strong>Phone(s):</strong> {', '.join(phones)}</li>"
        result_html += "</ul>"

        return result_html
