import streamlit as st
import requests
import requests.exceptions
import os
from typing import List

BACKEND = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(page_title="AI Career Agent", layout="wide")
st.title("AI Career Agent — Resume & Job Match")
st.markdown(
    "Use this page to analyze your resume against a job description, generate referral messages, "
    "track applications, and view structured outputs." 
)

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = {}
if "referral_text" not in st.session_state:
    st.session_state.referral_text = ""
if "apps" not in st.session_state:
    st.session_state.apps = []
if "backend_online" not in st.session_state:
    st.session_state.backend_online = False


def check_backend() -> bool:
    try:
        resp = requests.get(f"{BACKEND}/health", timeout=3)
        return resp.status_code == 200 and resp.json().get("status") == "ok"
    except requests.exceptions.RequestException:
        return False


def local_analysis(resume: str, jd: str) -> dict:
    keywords = [
        "python",
        "machine learning",
        "deep learning",
        "tensorflow",
        "pytorch",
        "nlp",
        "computer vision",
        "docker",
        "kubernetes",
        "sql",
        "nosql",
        "scikit-learn",
    ]
    resume_skills = {k for k in keywords if k in resume.lower()}
    jd_skills = {k for k in keywords if k in jd.lower()}
    overlap = resume_skills & jd_skills
    match_score = round(100.0 * len(overlap) / max(1, len(jd_skills)), 2)
    ats_score = round(min(100.0, (len(overlap) / max(1, len(jd_skills))) * 100.0), 2)
    return {
        "match_score": match_score,
        "ats_score": ats_score,
        "missing_skills": sorted(list(jd_skills - resume_skills)),
        "source": "local_fallback",
    }


def analyze_resume(resume: str, jd: str) -> dict:
    if not resume or not jd:
        return {}
    if st.session_state.backend_online:
        try:
            resp = requests.post(f"{BACKEND}/analyze_full", json={"resume": resume, "job_description": jd}, timeout=8)
            resp.raise_for_status()
            result = resp.json()
            result["source"] = "backend"
            return result
        except requests.exceptions.RequestException:
            return local_analysis(resume, jd)
    return local_analysis(resume, jd)


def generate_referral(company: str, role: str, resume: str, recipient: str) -> str:
    if not company or not role:
        return ""
    if st.session_state.backend_online:
        try:
            resp = requests.post(
                f"{BACKEND}/generate_referral",
                json={"company": company, "role": role, "resume": resume, "recipient_name": recipient},
                timeout=8,
            )
            resp.raise_for_status()
            return resp.json().get("message", "")
        except requests.exceptions.RequestException:
            pass
    greeting = f"Hi {recipient}," if recipient else "Hello,"
    body = (
        f"{greeting}\n\nI hope you are well. I wanted to share my interest in the {role} role at {company}. "
        "My background includes experience relevant to the position (see attached resume). I would greatly appreciate any advice or referral you can provide.\n\n"
    )
    closing = "Thanks for your time and help.\n\nBest regards,\n[Your Name]"
    return body + closing


def save_application(payload: dict) -> str:
    if st.session_state.backend_online:
        try:
            resp = requests.post(f"{BACKEND}/applications", json=payload, timeout=8)
            resp.raise_for_status()
            return f"Saved to backend: {resp.json().get('inserted_id')}"
        except requests.exceptions.RequestException:
            pass
    st.session_state.apps.append(payload)
    return "Saved locally in session"


def list_applications() -> list:
    if st.session_state.backend_online:
        try:
            resp = requests.get(f"{BACKEND}/applications", timeout=8)
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.RequestException:
            pass
    return st.session_state.apps


# Check backend status
st.session_state.backend_online = check_backend()
status_text = "Online" if st.session_state.backend_online else "Offline"
status_color = "green" if st.session_state.backend_online else "red"
st.markdown(f"**Backend status:** <span style='color:{status_color}'>{status_text}</span>", unsafe_allow_html=True)

with st.expander("Backend URL and instructions", expanded=False):
    st.write(BACKEND)
    if not st.session_state.backend_online:
        st.info("Start the FastAPI backend with `uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000`.")

with st.container():
    st.subheader("1. Resume + Job Description Analysis")
    resume = st.text_area("Resume text", height=180, key="resume_text")
    jd = st.text_area("Job description", height=180, key="jd_text")
    if st.button("Analyze resume and job match", key="analyze_btn"):
        if not resume or not jd:
            st.warning("Please provide both resume text and job description.")
        else:
            st.session_state.analysis_result = analyze_resume(resume, jd)

    if st.session_state.analysis_result:
        analysis = st.session_state.analysis_result.get("analysis", st.session_state.analysis_result)
        resources = st.session_state.analysis_result.get("resources", {})
        roadmap = st.session_state.analysis_result.get("roadmap", [])

        col1, col2, col3 = st.columns(3)
        col1.metric("Match Score", f"{analysis.get('match_score', 0)}%")
        col2.metric("ATS Score", f"{analysis.get('ats_score', 0)}%")
        col3.metric("Skills Missing", len(analysis.get("missing_skills", [])))

        st.markdown("**Missing Skills**")
        st.write(analysis.get("missing_skills", []))

        if resources:
            st.markdown("**Learning Resources**")
            for skill, link in resources.items():
                st.markdown(f"- **{skill}**: [{link}]({link})")

        if roadmap:
            st.markdown("**Roadmap**")
            st.table(roadmap)

with st.container():
    st.subheader("2. Generate Referral Message")
    company = st.text_input("Company", key="company_text")
    role = st.text_input("Role", key="role_text")
    recipient = st.text_input("Recipient name (optional)", key="recipient_text")
    if st.button("Generate referral message", key="referral_btn"):
        if not company or not role:
            st.warning("Enter both company and role to generate a referral.")
        else:
            st.session_state.referral_text = generate_referral(company, role, st.session_state.get("resume_text", ""), recipient)
    if st.session_state.referral_text:
        st.text_area("Referral message", value=st.session_state.referral_text, height=220)

with st.container():
    st.subheader("3. Track Application")
    with st.form("application_form"):
        company_name = st.text_input("Company name", key="app_company")
        role_name = st.text_input("Role", key="app_role")
        status = st.selectbox("Status", ["applied", "interview", "offer", "rejected", "withdrawn"], key="app_status")
        notes = st.text_area("Notes", key="app_notes")
        submitted = st.form_submit_button("Save application")
        if submitted:
            payload = {
                "company": company_name,
                "role": role_name,
                "status": status,
                "notes": notes,
            }
            message = save_application(payload)
            st.success(message)

with st.container():
    st.subheader("4. View tracked applications")
    if st.button("Refresh application list", key="refresh_apps"):
        st.session_state.apps = list_applications()
    apps = st.session_state.apps
    if apps:
        st.table(apps)
    else:
        st.info("No applications saved yet.")

