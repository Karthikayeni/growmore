from flask import Flask, request, jsonify
import PyPDF2
import spacy

# Load spaCy's English NLP model
nlp = spacy.load("en_core_web_sm")

app = Flask(__name__)

# Define a set of sample skills and corresponding interview questions
SKILL_QUESTIONS = {
    "python": "Can you explain a project where you used Python extensively?",
    "machine learning": "What machine learning algorithms are you familiar with?",
    "data analysis": "How do you approach data analysis and which tools do you use?",
    "flutter": "Can you describe an app you built using Flutter?",
    "firebase": "How have you used Firebase in your projects?",
    "sql": "What experience do you have writing SQL queries?"
}

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in range(len(reader.pages)):
            text += reader.pages[page].extract_text()
    return text

def extract_skills_from_resume(resume_text):
    """Uses spaCy to extract possible skills from resume text."""
    doc = nlp(resume_text.lower())
    skills_found = []
    
    for token in doc:
        # Check if the token is a noun and a potential skill
        if token.pos_ in ["NOUN", "PROPN"]:
            if token.text in SKILL_QUESTIONS:
                skills_found.append(token.text)
    
    return list(set(skills_found))  # Return unique skills

@app.route('/upload_resume', methods=['POST'])
def upload_resume():
    file = request.files['resume']
    resume_text = extract_text_from_pdf(file)
    skills = extract_skills_from_resume(resume_text)
    
    if skills:
        questions = [SKILL_QUESTIONS[skill] for skill in skills]
        return jsonify({"skills": skills, "questions": questions})
    else:
        return jsonify({"message": "No skills found in the resume."})

if __name__ == "__main__":
    app.run(debug=True)
