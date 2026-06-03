import re
from typing import Dict, Any
from dateutil import parser as date_parser


EMAIL_RE = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
PHONE_RE = re.compile(r"(\+\d{1,3}[- ]?)?\d{10}|\(\d{3}\)\s*\d{3}[- ]?\d{4}")


SKILL_KEYWORDS = [
    "python",
    "tensorflow",
    "pytorch",
    "scikit-learn",
    "sql",
    "docker",
    "kubernetes",
    "aws",
    "gcp",
    "linux",
]


def extract_contacts(text: str) -> Dict[str, Any]:
    emails = EMAIL_RE.findall(text or "")
    phones = PHONE_RE.findall(text or "")
    return {"emails": emails, "phones": phones}


def extract_skills(text: str):
    t = (text or "").lower()
    found = [k for k in SKILL_KEYWORDS if k in t]
    return found


def extract_dates(text: str):
    results = []
    # simple approach: look for years and parse
    years = re.findall(r"(19|20)\d{2}", text or "")
    for y in years:
        try:
            results.append(int(y))
        except Exception:
            pass
    return results


def parse_resume(text: str) -> Dict[str, Any]:
    return {
        "contacts": extract_contacts(text),
        "skills": extract_skills(text),
        "dates": extract_dates(text),
    }
