# 🚀 AI-Powered CV Analyzer & Job Matching System

An AI-powered web application that analyzes uploaded CVs, extracts relevant skills, and recommends suitable job opportunities using Natural Language Processing (NLP) and semantic similarity.

## 📌 Project Overview

Finding suitable job opportunities can be challenging when candidates need to compare their qualifications with many job descriptions.

This project aims to simplify that process by allowing users to upload their CVs in PDF format and receive relevant job-matching results based on the information extracted from their resumes.

## ✨ Key Features

- 📄 **CV Upload:** Upload CVs in PDF format.
- 🔍 **Text Extraction:** Extract textual information from uploaded CVs.
- 🧠 **NLP-Based Processing:** Process CV content and job descriptions.
- 🎯 **Job Matching:** Identify relevant job opportunities using semantic similarity.
- 📊 **Similarity Scores:** Display how closely a CV matches available job descriptions.
- 💡 **Skill Analysis:** Identify relevant skills and potential skill gaps.

## 🛠️ Technology Stack

| Component | Technologies |
|---|---|
| Frontend | React.js, Vite |
| Backend | Python, FastAPI |
| NLP Model | Sentence Transformers |
| Embedding Model | all-MiniLM-L6-v2 |
| Matching Algorithm | Cosine Similarity |
| PDF Processing | PyPDF |
| Data Processing | Pandas, NumPy |

## ⚙️ How It Works

1. User uploads a CV in PDF format.
2. The backend extracts text from the uploaded document.
3. The extracted text is processed.
4. Sentence Transformers generates numerical text embeddings.
5. Cosine similarity compares the CV embedding with job-description embeddings.
6. The system ranks relevant job opportunities.
7. Matching results are displayed through the web interface.

## 📂 Project Structure

```text
CV-Analyzer-Job-Matching/
│
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── jobs_processed.csv
│   └── job_embeddings.npy
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.js
│
├── .gitignore
└── README.md
```

## 💻 Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Savindi2002/CV-Analyzer-Job-Matching.git
```

```bash
cd CV-Analyzer-Job-Matching
```

### 2. Set Up the Backend

```bash
cd backend
```

Create a virtual environment:

```bash
py -m venv .venv
```

Activate it on Windows:

```bash
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

Backend URL:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

### 3. Set Up the Frontend

Open a second terminal:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

Frontend URL:

```text
http://localhost:5173
```

Keep both servers running while using the application.

## 📊 Matching Methodology

The application uses the Sentence Transformer model `all-MiniLM-L6-v2` to convert text into numerical embeddings.

Cosine similarity is then used to measure the similarity between the CV and job descriptions.

A higher similarity score indicates greater textual relevance.

**Note:** Similarity scores are not hiring probabilities or guarantees of employment.

## ⚠️ Limitations

- The system currently supports PDF CV uploads.
- Skill extraction depends on the available skill vocabulary and extraction logic.
- Scanned PDFs may require OCR support.
- Matching results depend on the quality of the CV and job descriptions.
- The system is intended as a decision-support tool, not a replacement for human recruitment decisions.

## 🚀 Future Improvements

- Support additional document formats.
- Improve skill extraction using advanced NLP techniques.
- Expand the job dataset.
- Add personalized career recommendations.
- Improve skill-gap analysis.
- Deploy the application for public access.

## 👩‍💻 Author

**Savindi Hewage**

Data Science Undergraduate  
Sabaragamuwa University of Sri Lanka

- GitHub: [Savindi2002](https://github.com/Savindi2002)
- LinkedIn: [Savindi Hewage](https://www.linkedin.com/in/savindi-hewage-506790326/)

---

⭐ If you find this project interesting, feel free to explore the repository and share your feedback!

**Building with AI. Learning through projects. Creating meaningful solutions.**
