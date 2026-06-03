import os
import re
from typing import Dict, List

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
import logging
import os
from dateutil import parser as date_parser

try:
    from google.cloud import aiplatform
except Exception:
    aiplatform = None

# Expanded skill keyword set — add or edit as needed.
SKILL_KEYWORDS = [
    "python",
    "java",
    "c++",
    "c#",
    "machine learning",
    "deep learning",
    "tensorflow",
    "keras",
    "pytorch",
    "nlp",
    "natural language processing",
    "computer vision",
    "opencv",
    "docker",
    "kubernetes",
    "aws",
    "azure",
    "gcp",
    "sql",
    "nosql",
    "mongodb",
    "postgresql",
    "scikit-learn",
    "pandas",
    "numpy",
    "spark",
    "hadoop",
    "react",
    "node",
]


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").strip().lower())


def _extract_skills(text: str) -> List[str]:
    t = _normalize(text)
    found = []
    for kw in SKILL_KEYWORDS:
        if kw in t:
            found.append(kw)
    return found


def _tfidf_cosine_score(a: str, b: str) -> float:
    vec = TfidfVectorizer(stop_words="english")
    try:
        X = vec.fit_transform([a or "", b or ""] )
        score = float(cosine_similarity(X[0:1], X[1:2])[0][0])
        return round(score * 100.0, 2)
    except Exception:
        return 0.0


def analyze_job(resume: str, job_description: str) -> Dict:
    """Analyze resume vs job description.

    Returns dict with `match_score` (skills overlap %), `ats_score` (TF-IDF similarity 0-100),
    and `missing_skills` (list).
    Uses local deterministic analysis. If you want LLM enhancement, wire Gemini calls in the
    `call_gemini()` stub and enrich outputs.
    """

    resume_t = _normalize(resume)
    jd_t = _normalize(job_description)

    resume_skills = set(_extract_skills(resume_t))
    jd_skills = set(_extract_skills(jd_t))
    overlap = resume_skills & jd_skills

    match_score = 0.0
    if jd_skills:
        match_score = round(100.0 * len(overlap) / len(jd_skills), 2)

    ats_score = _tfidf_cosine_score(resume_t, jd_t)

    missing_skills = sorted(list(jd_skills - resume_skills))

    # If Gemini (Vertex AI) credentials are available, call the model to enrich analysis
    if os.getenv("GOOGLE_APPLICATION_CREDENTIALS") and os.getenv("GCP_PROJECT") and os.getenv("GEMINI_MODEL") and aiplatform:
        try:
            prompt = (
                "You are an assistant that analyzes resumes against job descriptions. "
                "Given the resume and job description, output a JSON object with keys: match_score (0-100 float), "
                "ats_score (0-100 float), missing_skills (array of strings), notes (string).\n\n"
                f"Resume:\n{resume}\n\nJob Description:\n{job_description}\n\nRespond with JSON only."
            )
            g_resp = call_gemini(prompt)
            # Expecting JSON from Gemini; try to parse
            parsed = json.loads(g_resp)
            # merge deterministic fields where available
            result = {
                "match_score": parsed.get("match_score", match_score),
                "ats_score": parsed.get("ats_score", ats_score),
                "missing_skills": parsed.get("missing_skills", missing_skills),
            }
            return result
        except Exception as e:
            logging.exception("Gemini call failed, falling back to local analyzer: %s", e)

    return {"match_score": match_score, "ats_score": ats_score, "missing_skills": missing_skills}


def generate_referral(company: str, role: str, resume: str, recipient_name: str = "") -> str:
    """Generate a professional referral message. For higher quality, replace with Gemini-generated text.
    """
    greeting = f"Hi {recipient_name}," if recipient_name else "Hello," 
    body = (
        f"{greeting}\n\nI hope you are well. I'm writing to express my interest in the {role} role at {company}. "
        "My background includes relevant experience (see attached resume). I would greatly appreciate any advice or referral you can provide.\n\n"
    )
    closing = "Thanks for your time and help.\n\nBest regards,\n[Your Name]"
    return body + closing


def suggest_skills(resume: str, job_description: str) -> List[str]:
    analysis = analyze_job(resume, job_description)
    return analysis.get("missing_skills", [])


def call_gemini(prompt: str) -> str:
    """Stub for Gemini / Google Cloud Generative integration.

    Replace this with a safe, authenticated call to your Google Cloud project.
    Options:
      - Use `google.cloud.aiplatform` client when running on GCP with a service account.
      - Use REST with `GOOGLE_API_KEY` for short tests. Ensure you follow Google's API docs.

    This stub currently returns the prompt for debugging.
    """
    # If aiplatform is available and credentials are set, call Vertex AI Generative model
    if aiplatform and os.getenv("GCP_PROJECT") and os.getenv("GCP_LOCATION") and os.getenv("GEMINI_MODEL"):
        project = os.getenv("GCP_PROJECT")
        location = os.getenv("GCP_LOCATION")
        model_name = os.getenv("GEMINI_MODEL")
        aiplatform.init(project=project, location=location)
        try:
            model = aiplatform.TextGenerationModel.from_pretrained(model_name)
            response = model.predict(prompt, max_output_tokens=512)
            # response may be plain text
            return str(response)
        except Exception as e:
            logging.exception("Vertex AI call failed: %s", e)
            raise

    # Fallback: return a simple JSON suggestion string when no credentials are present
    fallback = json.dumps({
        "match_score": None,
        "ats_score": None,
        "missing_skills": [],
        "notes": "Gemini not configured — provide GOOGLE_APPLICATION_CREDENTIALS, GCP_PROJECT, GCP_LOCATION, GEMINI_MODEL to enable."
    })
    return fallback

