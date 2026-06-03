from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_analyze_endpoint():
    response = client.post(
        "/analyze",
        json={
            "resume": "Python developer with machine learning experience.",
            "job_description": "Looking for Python engineer with ML and TensorFlow knowledge.",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "match_score" in data
    assert "ats_score" in data
    assert "missing_skills" in data


def test_generate_referral_endpoint():
    response = client.post(
        "/generate_referral",
        json={
            "company": "NVIDIA",
            "role": "AI Engineer",
            "resume": "Resume content.",
            "recipient_name": "Alex",
        },
    )
    assert response.status_code == 200
    assert "message" in response.json()
