from typing import Dict, Any
from .ai_client import analyze_job, generate_referral, suggest_skills, call_gemini
from .parsers import parse_resume
from .mcp_client import MCPClient
import os


class CareerAgent:
    def __init__(self):
        self.mcp = MCPClient()

    def run_apply_flow(self, resume: str, job_description: str, company: str = "", role: str = "") -> Dict[str, Any]:
        """Multi-step agent flow:
        1. Save resume
        2. Analyze JD vs resume
        3. Generate suggested skills & roadmap
        4. Generate referral message
        5. Save analysis, application, and trace to MCP
        """
        # Step 1: persist resume (structured)
        parsed = parse_resume(resume)
        resume_doc = {"resume": resume, "parsed": parsed}
        self.mcp.save_resume(resume_doc)

        # Step 2: analysis
        analysis = analyze_job(resume, job_description)
        analysis_doc = {"resume": resume, "job_description": job_description, "analysis": analysis}
        self.mcp.save_analysis(analysis_doc)

        # Step 3: suggested skills and simple roadmap
        missing = analysis.get("missing_skills", [])
        roadmap = [{"skill": s, "link": f"https://www.google.com/search?q=learn+{s.replace(' ', '+')}", "weeks": 1} for s in missing]

        # Step 4: referral via Gemini stub or local
        if os.getenv("GOOGLE_API_KEY") or os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
            prompt = f"Write a referral message for {role} at {company} given this resume: {resume[:800]}"
            referral = call_gemini(prompt)
        else:
            referral = generate_referral(company, role, resume)

        # Step 5: Save application and trace
        app_doc = {"company": company, "role": role, "status": "candidate_generated", "notes": "Created by agent"}
        self.mcp.save_application(app_doc)

        trace = {"steps": [
            {"step": "save_resume"},
            {"step": "analysis", "result": analysis},
            {"step": "roadmap", "result": roadmap},
            {"step": "referral", "result": referral},
            {"step": "save_application", "result": app_doc}
        ]}
        self.mcp.save_trace(trace)

        return {"analysis": analysis, "roadmap": roadmap, "referral": referral}
