# Resume Analyzer & Interview Question Generator 🎯

An AI-powered Flask application that analyzes resumes using OpenAI's GPT models and generates relevant interview questions based on a provided job description.

## 🔍 Features

- Extracts and analyzes resume content from uploaded PDF files.
- Matches resume content with a job description using GPT.
- Generates relevant interview questions.
- Provides feedback on candidate responses with follow-up questions.

## 🛠️ Tech Stack

- **Backend:** Flask
- **AI:** OpenAI GPT (via `openai` API)
- **PDF Processing:** PyPDF2
- **Environment Management:** python-dotenv
- **Deployment:** Render

---

## 📁 Project Structure

```
.
├── app.py               # Main Flask application
├── requirements.txt     # Python dependencies
├── Procfile             # For Render deployment
├── .env                 # Environment variables (local only)
└── README.md            # Project documentation
```

---

## 🧪 Local Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/resume-analyzer.git
cd resume-analyzer
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your OpenAI API key to a `.env` file

```ini
OPENAI_API_KEY=your_openai_key_here
```

### 5. Run the Flask App

```bash
python app.py
```

The app will run on `http://127.0.0.1:5000`

---

## 🚀 Deployment on Render

### 1. Push to GitHub

Make sure your code is in a GitHub repository.

### 2. Create a Web Service on [Render](https://render.com/)

- Select **Flask** app from your GitHub repo.
- Set `Build Command:` (leave empty or use `pip install -r requirements.txt`)
- Set `Start Command:` to:

  ```
  gunicorn app:app
  ```

- Add environment variable:

  ```
  Key: OPENAI_API_KEY
  Value: your-openai-key-here
  ```

### 3. Auto Deploy

Enable **automatic deploys** for smoother updates from GitHub.

---

## 📬 API Endpoints

### `POST /analyze-and-interview`

**Form Data:**
- `resume`: PDF file
- `jd`: Job description text

**Response:**
```json
{
  "analysis": "Brief summary of resume and key skills...",
  "questions": "1. Question one...\n2. Question two..."
}
```

---

### `POST /interview-response`

**JSON Body:**
```json
{
  "question": "What are your strengths?",
  "answer": "I am very detail-oriented...",
  "jd": "Looking for a software engineer with Python skills..."
}
```

**Response:**
```json
{
  "analysis": "The candidate's response shows... Follow-up question: ..."
}
```

---

## ✅ To-Do

- [ ] Frontend Integration (e.g., React or Streamlit)
- [ ] Authentication (optional)
- [ ] Logging and Monitoring

---

## 📄 License

MIT License. Feel free to use, modify, and deploy.

---

## 🙋‍♀️ Author

Made by [Your Name](https://github.com/your-username) 💙