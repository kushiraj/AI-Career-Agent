"""Seed script to insert sample application records into MongoDB.
Run with: python backend/seed.py
"""
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("MONGO_DB", "ai_career_agent")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
apps = db["applications"]

sample = [
    {"company": "NVIDIA", "role": "AI Engineer", "status": "applied", "applied_on": "2026-05-01", "notes": "Referral via LinkedIn"},
    {"company": "Google", "role": "Research Scientist", "status": "interview", "applied_on": "2026-04-15", "notes": "Campus placement"},
    {"company": "OpenAI", "role": "ML Engineer", "status": "applied", "applied_on": "2026-03-20", "notes": "Submitted via website"},
    {"company": "Meta", "role": "Applied Scientist", "status": "offer", "applied_on": "2026-02-10", "notes": "Onsite completed"},
    {"company": "Amazon", "role": "Data Scientist", "status": "rejected", "applied_on": "2026-01-05", "notes": "No response"},
    {"company": "Microsoft", "role": "AI Researcher", "status": "applied", "applied_on": "2026-04-01", "notes": "Referred"},
    {"company": "Apple", "role": "ML Infrastructure", "status": "applied", "applied_on": "2026-03-11", "notes": "Resume updated"},
    {"company": "DeepMind", "role": "Research Engineer", "status": "interview", "applied_on": "2026-05-12", "notes": "Coding round scheduled"},
    {"company": "Anthropic", "role": "Safety Engineer", "status": "applied", "applied_on": "2026-02-25", "notes": "Referral"},
    {"company": "Waymo", "role": "Robotics Engineer", "status": "applied", "applied_on": "2026-01-30", "notes": "Submitted"},
]

if __name__ == "__main__":
    apps.delete_many({})
    res = apps.insert_many(sample)
    print(f"Inserted {len(res.inserted_ids)} sample applications into {DB_NAME}.")
