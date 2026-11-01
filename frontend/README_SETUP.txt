CAREERLY AI FRONTEND SETUP

1. Back up your existing frontend folder.
2. Copy this bundle's files into your project's frontend folder, replacing matching frontend files.
3. Open terminal in the frontend folder and run:
   npm install
   npm run dev
4. Keep the FastAPI backend running at http://127.0.0.1:8000.
5. Optional: create frontend/.env with:
   VITE_API_URL=http://127.0.0.1:8000
   Restart Vite after changing .env.

Pages:
  /              Home
  /analyze       Upload CV and view analysis
  /how-it-works  Process explanation
  /about         Project and technology info

API expects POST /api/analyze with multipart field "file".
The sample portraits are loaded from Unsplash, so internet access is needed for them.
If your API uses different JSON field names, adjust the mapping in the Analyze component in src/App.jsx.
Decorative home-page bars are sample visuals, not real model predictions.
