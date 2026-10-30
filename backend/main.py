
from pathlib import Path
import re

import numpy as np
import pandas as pd

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# --------------------------------------------------
# 1. APPLICATION CONFIGURATION
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

CSV_PATH = BASE_DIR / "jobs_processed.csv"
EMBEDDINGS_PATH = BASE_DIR / "job_embeddings.npy"

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB
TOP_N = 5

app = FastAPI(
    title="CV Analyzer and Job Matching API",
    description="Analyze CVs and find relevant job opportunities.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# --------------------------------------------------
# 2. SKILL DICTIONARY
# --------------------------------------------------

SKILLS = [
    "python",
    "java",
    "javascript",
    "c++",
    "sql",
    "mysql",
    "mongodb",
    "html",
    "css",
    "react",
    "node.js",
    "express",
    "php",
    "laravel",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "data science",
    "data analysis",
    "data visualization",
    "power bi",
    "tableau",
    "excel",
    "statistics",
    "pandas",
    "numpy",
    "scikit-learn",
    "tensorflow",
    "pytorch",
    "nlp",
    "natural language processing",
    "computer vision",
    "git",
    "github",
    "docker",
    "aws",
    "azure",
    "communication",
    "teamwork",
    "leadership",
    "problem solving",
    "project management"
]


# --------------------------------------------------
# 3. LOAD JOB DATA
# --------------------------------------------------

if not CSV_PATH.exists():
    raise FileNotFoundError(
        f"Missing job data file: {CSV_PATH}"
    )

if not EMBEDDINGS_PATH.exists():
    raise FileNotFoundError(
        f"Missing embeddings file: {EMBEDDINGS_PATH}"
    )

job_df = pd.read_csv(CSV_PATH)

required_columns = [
    "job_title",
    "job_description",
    "clean_job"
]

missing_columns = [
    col for col in required_columns
    if col not in job_df.columns
]

if missing_columns:
    raise ValueError(
        f"Missing CSV columns: {missing_columns}"
    )

for col in required_columns:
    job_df[col] = job_df[col].fillna("").astype(str)

job_embeddings = np.load(EMBEDDINGS_PATH)

if job_embeddings.ndim != 2:
    raise ValueError("Job embeddings must be a 2D array.")

if len(job_df) != len(job_embeddings):
    raise ValueError(
        "The number of job rows does not match "
        "the number of embedding rows."
    )


# --------------------------------------------------
# 4. LOAD SENTENCE TRANSFORMER
# --------------------------------------------------

model = SentenceTransformer(MODEL_NAME)

if job_embeddings.shape[1] != model.get_sentence_embedding_dimension():
    raise ValueError(
        "Embedding dimension mismatch. "
        "Regenerate job_embeddings.npy using the configured model."
    )

print("Job data loaded:", len(job_df))
print("Embedding shape:", job_embeddings.shape)
print("Sentence Transformer loaded successfully.")


# --------------------------------------------------
# 5. SKILL EXTRACTION
# --------------------------------------------------

def extract_skills(text):

    text = text.lower()

    detected = []

    for skill in SKILLS:

        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

        if re.search(pattern, text):
            detected.append(skill)

    return sorted(set(detected))


# --------------------------------------------------
# 6. EXTRACT TEXT FROM PDF
# --------------------------------------------------

def extract_pdf_text(file_bytes):

    try:
        import io

        reader = PdfReader(io.BytesIO(file_bytes))

        if reader.is_encrypted:
            raise HTTPException(
                status_code=400,
                detail="Encrypted PDFs are not supported."
            )

        text_parts = []

        for page in reader.pages:
            text_parts.append(page.extract_text() or "")

        text = "\n".join(text_parts).strip()

        if not text:
            raise HTTPException(
                status_code=400,
                detail="No readable text found in the PDF."
            )

        return text

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Could not read the uploaded PDF."
        )


# --------------------------------------------------
# 7. JOB MATCHING
# --------------------------------------------------

def find_job_matches(cv_text):

    cv_embedding = model.encode(
        [cv_text],
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    scores = cosine_similarity(
        cv_embedding,
        job_embeddings
    )[0]

    top_indices = np.argsort(scores)[::-1][:TOP_N]

    cv_skills = extract_skills(cv_text)

    matches = []

    for index in top_indices:

        job = job_df.iloc[index]

        job_text = (
            job["job_title"] + " " +
            job["job_description"] + " " +
            job["clean_job"]
        )

        job_skills = extract_skills(job_text)

        matched_skills = sorted(
            set(cv_skills).intersection(job_skills)
        )

        missing_skills = sorted(
            set(job_skills).difference(cv_skills)
        )

        matches.append({
            "job_title": job["job_title"],
            "job_description": job["job_description"][:500],
            "similarity_score": round(
                float(scores[index]) * 100, 2
            ),
            "matched_skills": matched_skills,
            "missing_skills": missing_skills
        })

    return cv_skills, matches


# --------------------------------------------------
# 8. API ROUTES
# --------------------------------------------------

@app.get("/")
def home():

    return {
        "message": "CV Analyzer API is running",
        "status": "success"
    }


@app.get("/api/health")
def health():

    return {
        "status": "healthy",
        "total_jobs": len(job_df),
        "model": MODEL_NAME
    }


@app.post("/api/analyze")
async def analyze_cv(file: UploadFile = File(...)):

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Please upload a PDF file."
        )

    file_bytes = await file.read()

    if len(file_bytes) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File size must be 5 MB or less."
        )

    if not file_bytes:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is empty."
        )

    cv_text = extract_pdf_text(file_bytes)

    detected_skills, matches = find_job_matches(cv_text)

    return {
        "status": "success",
        "filename": file.filename,
        "detected_skills": detected_skills,
        "total_skills_detected": len(detected_skills),
        "total_jobs_checked": len(job_df),
        "matches": matches
    }
