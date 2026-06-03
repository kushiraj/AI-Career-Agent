"""Example runner for the deterministic analyzer.

Run from repository root:
    python backend/examples/run_analysis.py

This prints JSON output for sample resume/JD pairs using `analyze_job()`.
"""
import json
import sys
from pathlib import Path

# Ensure the backend package is importable when running the script directly
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "backend"))

from app.ai_client import analyze_job


samples = [
    {
        "name": "NVIDIA AI Engineer",
        "resume": "Experienced ML engineer with PyTorch and TensorFlow, python, deep learning, computer vision, CUDA.",
        "jd": "We are hiring an AI Engineer with experience in deep learning, PyTorch, TensorFlow, computer vision, and Docker.",
    },
    {
        "name": "Data Scientist - Google",
        "resume": "Data scientist skilled in Python, pandas, scikit-learn, SQL, machine learning, model deployment with Docker.",
        "jd": "Experienced Data Scientist required: SQL, machine learning, TensorFlow or PyTorch, data pipelines, cloud (GCP/AWS).",
    },
    {
        "name": "Backend Role",
        "resume": "Backend developer with Node, React, SQL, Docker, Kubernetes.",
        "jd": "Senior Backend Engineer: Go, Kubernetes, Docker, microservices, SQL, distributed systems.",
    },
]


def main():
    results = []
    for s in samples:
        out = analyze_job(s["resume"], s["jd"])
        results.append({"name": s["name"], "analysis": out})

    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
