from backend.app.ai_client import analyze_job, generate_referral


def test_analyze_job_returns_required_fields():
    resume = "Experienced ML engineer with PyTorch and TensorFlow, python, deep learning, computer vision, CUDA."
    jd = "We are hiring an AI Engineer with experience in deep learning, PyTorch, TensorFlow, computer vision, and Docker."
    result = analyze_job(resume, jd)

    assert isinstance(result, dict)
    assert "match_score" in result
    assert "ats_score" in result
    assert "missing_skills" in result
    assert result["match_score"] >= 0
    assert isinstance(result["missing_skills"], list)
    assert "docker" in result["missing_skills"]


def test_generate_referral_contains_company_and_role():
    referral_text = generate_referral("NVIDIA", "AI Engineer", "resume text", "Recruiter")
    assert "NVIDIA" in referral_text
    assert "AI Engineer" in referral_text
    assert "Hello" in referral_text or "Hi Recruiter" in referral_text
