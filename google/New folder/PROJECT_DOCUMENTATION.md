# AI Career Agent Project Documentation

## 1. Project Purpose
This project builds an AI-powered career agent that helps users analyze job descriptions against resumes, generate referral messages, track applications, and store results in MongoDB.

It is designed for a hackathon-style challenge that requires:
- moving beyond a simple chatbot,
- integrating Gemini/Google Cloud Agent Builder logic,
- using MongoDB as the partner MCP server,
- executing multi-step tasks and saving results,
- providing a production-level, reusable backend.

## 2. Requirements
The project fulfills these requirements:
1. **Resume and Job Description Analysis**
   - Compare a resume to a job description.
   - Calculate a match score (`match_score`).
   - Calculate an ATS-style similarity score (`ats_score`).
   - Identify missing skills.
2. **Referral Message Generation**
   - Produce a professional referral message for a target company and role.
3. **Application Tracking**
   - Save company, role, status, and notes.
   - Persist application data in MongoDB.
4. **MongoDB MCP Integration**
   - Use MongoDB collections to save resumes, analyses, applications, and traces.
5. **Agent Workflow / Multi-Step Execution**
   - Implement a multi-step agent flow.
   - Store agent execution traces in MongoDB.
6. **Gemini / Vertex AI Integration**
   - Support real LLM calls when Google Cloud credentials are configured.
   - Provide a safe local fallback when credentials are not available.
7. **Production-Level Behavior**
   - Structured resume parsing.
   - Clean UI and backend health status.
   - Clear documentation and run instructions.

## 3. What This Project Does
The project provides:
- a **Streamlit user interface** for interaction,
- a **FastAPI backend** offering analysis and agent endpoints,
- a **MongoDB persistence layer** for applications and traces,
- a **Gemini-ready integration path** using Google Cloud Vertex AI,
- a **local fallback analyzer** for offline use.

### Core features
- **Analyze resume vs JD**: returns `match_score`, `ats_score`, `missing_skills`, learning resources, and a short roadmap.
- **Generate referral message**: provides a referral letter based on company, role, and resume.
- **Track applications**: stores application data in MongoDB, with local session fallback if backend is offline.
- **Run agent workflow**: executes a multi-step agent flow and persists results.

## 4. Architecture
### Components
- **Streamlit frontend**: `streamlit_app.py`
  - Provides user inputs, status checks, and result display.
- **FastAPI backend**: `backend/app/main.py`
  - Exposes endpoints for analysis, referrals, tracking, and agent execution.
- **AI client**: `backend/app/ai_client.py`
  - Computes local analysis with TF-IDF and skill matching.
  - Integrates with Google Cloud Vertex AI when configured.
- **MCP adapter**: `backend/app/mcp_client.py`
  - Saves data to MongoDB collections.
- **Agent orchestrator**: `backend/app/agent.py`
  - Runs a multi-step workflow and saves traces.
- **Resume parsers**: `backend/app/parsers.py`
  - Extracts contacts, skills, and dates from resumes.

### Data storage
MongoDB collections used:
- `resumes`
- `analyses`
- `applications`
- `traces`

## 5. Key Files
- `streamlit_app.py` — frontend UI
- `backend/app/main.py` — API routes
- `backend/app/ai_client.py` — analysis and Gemini integration
- `backend/app/agent.py` — agent logic / workflow
- `backend/app/mcp_client.py` — MongoDB MCP adapter
- `backend/app/parsers.py` — resume parsing
- `backend/seed.py` — seed sample data
- `agent_builder.yaml` — Google Cloud Agent Builder template
- `requirements.txt` — dependencies
- `PROJECT_DOCUMENTATION.md` — this documentation

## 6. Backend Endpoints
- `GET /health` — returns backend status.
- `POST /analyze` — simple analysis endpoint.
- `POST /analyze_full` — enriched analysis with learning resources and roadmap.
- `POST /generate_referral` — generates a referral message.
- `POST /applications` — stores a tracked application.
- `GET /applications` — retrieves stored applications.
- `POST /agent/run` — executes the multi-step agent workflow.

## 7. Example Output
### `POST /analyze_full`
Response example:
```json
{
  "analysis": {
    "match_score": 80.0,
    "ats_score": 76.5,
    "missing_skills": ["docker"]
  },
  "resources": {
    "docker": "https://www.google.com/search?q=learn+docker"
  },
  "roadmap": [
    {
      "skill": "docker",
      "action": "Complete tutorials and build small projects",
      "link": "https://www.google.com/search?q=learn+docker",
      "duration_days": 7
    }
  ]
}
```

### `POST /agent/run`
Response example:
```json
{
  "analysis": { ... },
  "roadmap": [ ... ],
  "referral": "Hi, ... Best regards, [Your Name]"
}
```

## 8. How to Run
1. Create `.env` from `.env.example`.
2. Install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\Activate.ps1 on Windows
pip install -r requirements.txt
```
3. Start MongoDB (optional but required for persistence):
```bash
docker run -d --name mongo -p 27017:27017 -v mongo_data:/data/db mongo:6.0
```
4. Seed sample data:
```bash
python backend/seed.py
```
5. Run backend:
```bash
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```
6. Run frontend:
```bash
python -m streamlit run streamlit_app.py
```

## 9. Gemini / Vertex AI Integration
To enable real Gemini output, set these environment variables:
- `GOOGLE_APPLICATION_CREDENTIALS`
- `GCP_PROJECT`
- `GCP_LOCATION`
- `GEMINI_MODEL`

The code will call Vertex AI if these are present and the Google Cloud SDK is installed.

## 10. Notes
- The system works with or without a backend.
- Local analysis fallback is available when the backend is offline.
- MongoDB persistence is used for applications and audit traces.
- The project is ready for a hackathon submission in the MongoDB partner track.
