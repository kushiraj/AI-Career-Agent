from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

from .db import get_applications_collection
from .ai_client import analyze_job, generate_referral, suggest_skills
from .agent import CareerAgent

app = FastAPI(title="AI Career Agent")


class AnalyzeRequest(BaseModel):
    resume: str
    job_description: str


class AnalyzeResponse(BaseModel):
    match_score: float
    ats_score: float
    missing_skills: List[str]


class ReferralRequest(BaseModel):
    company: str
    role: str
    resume: str
    recipient_name: str = ""


class ApplicationIn(BaseModel):
    company: str
    role: str
    status: str
    applied_on: str = ""
    notes: str = ""


class AnalyzeFullRequest(BaseModel):
    resume: str
    job_description: str


class AgentRunRequest(BaseModel):
    resume: str
    job_description: str
    company: str = ""
    role: str = ""


agent = CareerAgent()


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(req: AnalyzeRequest):
    try:
        result = analyze_job(req.resume, req.job_description)
        return AnalyzeResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate_referral")
def referral(req: ReferralRequest):
    try:
        msg = generate_referral(req.company, req.role, req.resume, req.recipient_name)
        return {"message": msg}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/applications")
def track_application(app_in: ApplicationIn):
    col = get_applications_collection()
    doc = app_in.dict()
    res = col.insert_one(doc)
    return {"inserted_id": str(res.inserted_id)}


@app.get("/applications")
def list_applications():
    col = get_applications_collection()
    docs = list(col.find().limit(100))
    for d in docs:
        d["_id"] = str(d["_id"])
    return docs


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/analyze_full")
def analyze_full(req: AnalyzeFullRequest):
    try:
        analysis = analyze_job(req.resume, req.job_description)
        # enrich with suggested learning links and short roadmap
        missing = analysis.get("missing_skills", [])
        resources = {s: f"https://www.google.com/search?q=learn+{s.replace(' ', '+')}" for s in missing}
        roadmap = [{"skill": s, "action": "Complete tutorials and build small projects", "link": resources[s], "duration_days": 7} for s in missing]
        return {"analysis": analysis, "resources": resources, "roadmap": roadmap}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/agent/run")
def run_agent(req: AgentRunRequest):
    try:
        res = agent.run_apply_flow(req.resume, req.job_description, req.company, req.role)
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
