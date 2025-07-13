import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import PyPDF2 as pdf
from dotenv import load_dotenv
from openai import OpenAI  # NEW import

# Load environment variables
load_dotenv()

# Initialize OpenAI client with API key
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Flask app setup
app = Flask(__name__)
CORS(app)

# Input prompt template for resume analysis
resume_analysis_prompt = '''
As an ATS specialist, analyze this resume for a tech, software, or data science position. Provide a brief summary and identify key skills and experiences.

Resume:
{text}

Job Description:
{jd}
'''

# Function to get response from OpenAI's ChatGPT API (New SDK)
def get_chatgpt_response(prompt, model="gpt-3.5-turbo"):
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": prompt}]
    )
    return response.choices[0].message.content

# Function to extract text from uploaded PDF
def text_in_uploaded_pdf(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ''
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return text

# API route to handle resume analysis and question generation
@app.route('/analyze-and-interview', methods=['POST'])
def analyze_and_interview():
    try:
        resume_file = request.files.get('resume')
        job_description = request.form.get('jd')

        if not resume_file or not job_description:
            return jsonify({'error': 'Missing resume or job description'}), 400

        resume_text = text_in_uploaded_pdf(resume_file)

        # Analyze resume
        analysis_prompt = resume_analysis_prompt.format(text=resume_text, jd=job_description)
        analysis_result = get_chatgpt_response(analysis_prompt)

        # Generate interview questions
        questions_prompt = f"Based on this resume analysis and job description, generate 5 relevant interview questions:\n\nAnalysis: {analysis_result}\n\nJob Description: {job_description}"
        interview_questions = get_chatgpt_response(questions_prompt)

        return jsonify({
            'analysis': analysis_result,
            'questions': interview_questions
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API route to handle interview response analysis
@app.route('/interview-response', methods=['POST'])
def interview_response():
    try:
        data = request.json
        question = data.get('question')
        answer = data.get('answer')
        job_description = data.get('jd')
        
        if not question or not answer or not job_description:
            return jsonify({'error': 'Missing question, answer, or job description'}), 400

        analysis_prompt = f'''
        Analyze this interview response for a tech job. Provide feedback and a follow-up question.

        Job Description: {job_description}

        Question: {question}

        Candidate's Answer: {answer}

        Please provide:
        1. Brief analysis of the answer (2-3 sentences)
        2. One relevant follow-up question
        '''

        response_analysis = get_chatgpt_response(analysis_prompt)

        return jsonify({'analysis': response_analysis}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Optional route to show API is live
@app.route('/', methods=['GET'])
def home():
    return "✅ Resume Analyzer API is running!", 200

# Run locally
if __name__ == "__main__":
    app.run(debug=True)
