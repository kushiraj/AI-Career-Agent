# AI Career Agent — Minimal Production Scaffold

This repository contains a minimal production-ready scaffold for the AI Career Agent described in the brief.

Components
- Backend: FastAPI (backend/app)
- Frontend: Streamlit demo (`streamlit_app.py`)
- Database: MongoDB (configured via `MONGO_URI`)
- Seed: `backend/seed.py` inserts 10 sample application records
- Containers: `docker-compose.yml` for backend and Streamlit

Quick start (local)

1. Create `.env` from `.env.example` and adjust `MONGO_URI`.

2. Install dependencies (recommended in virtualenv):

```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

3. Seed sample data:

```bash
python backend/seed.py
```

4. Run backend:

```bash
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

5. Run frontend (Streamlit):

```bash
streamlit run streamlit_app.py
```

Docker (optional)

```bash
docker-compose up --build
```

Run tests

```bash
pytest
```

Notes
- `backend/app/ai_client.py` contains a mock fallback for Gemini. Replace TODO sections with Google Cloud Generative API calls when you have credentials and the SDK set up.
- This scaffold focuses on the core features: analyze JD vs resume, generate referral message, track applications, and store data in MongoDB.

Local deterministic analyzer (improved)
- The project now includes a stronger local analyzer in `backend/app/ai_client.py` that:
	- Extracts skills using an expanded keyword list.
	- Calculates `match_score` as skills-overlap percentage.
	- Calculates `ats_score` using TF-IDF cosine similarity (0-100) for resume vs JD.
	- Returns `missing_skills` for actionable guidance.

Gemini / Vertex AI integration (template)
- A `call_gemini()` stub is present in `backend/app/ai_client.py` as a template. To enable real LLM-powered analysis, set these environment variables in your `.env` and implement the call using the Google Cloud SDK or REST API:
	- `GOOGLE_API_KEY` (optional) — for simple REST testing
	- `GOOGLE_APPLICATION_CREDENTIALS` — path to service account JSON (recommended)
	- `GCP_PROJECT`, `GCP_LOCATION`, `GEMINI_MODEL` — your project details and model name

Security note: Never paste service-account JSON or API keys into chat. Put secrets into your `.env` or your deployment secret manager.

If you want, I can implement the Gemini call using the Google Cloud Python client once you confirm your preferred authentication method (API key vs service account). 

Example: run the deterministic analyzer locally

```powershell
python backend\examples\run_analysis.py
```

Sample output (JSON) will show `match_score`, `ats_score`, and `missing_skills` for each pair.

New endpoints (backend)
- `POST /analyze_full` — returns enriched analysis: `analysis`, `resources`, and `roadmap`.
- `POST /agent/run` — runs the multi-step agent flow (save resume, analyze, suggest roadmap, generate referral, persist traces). Payload: `{ "resume":"...", "job_description":"...", "company":"...", "role":"..." }`

Agent Builder template
- See `agent_builder.yaml` for a starter Google Cloud Agent Builder template that shows how the agent can call the backend and the MongoDB MCP server. Replace environment placeholders before deploying.
