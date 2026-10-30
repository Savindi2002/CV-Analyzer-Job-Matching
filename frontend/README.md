# Careerly AI frontend

React + Vite frontend for the CV Analyzer FastAPI backend.

## Run

```powershell
npm install
```

Create `.env` in this frontend folder:

```env
VITE_API_URL=http://127.0.0.1:8000
```

Then run:

```powershell
npm run dev
```

Open http://localhost:5173. Keep FastAPI running separately at http://127.0.0.1:8000.

The frontend sends a PDF as multipart field `file` to `POST /api/analyze`. It recognizes `detected_skills`/`skills_detected`, `matched_skills`, `missing_skills`, and `top_matches`/`matches`/`job_matches`/`recommendations`. Job items may use `job_title`/`title` and `similarity`/`score`/`match_score`.

Images load from Unsplash and need internet access. Similarity scores are not hiring probabilities.
