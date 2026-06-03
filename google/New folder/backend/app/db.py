import os
from pymongo import MongoClient

from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("MONGO_DB", "ai_career_agent")

_client = MongoClient(MONGO_URI)
_db = _client[DB_NAME]


def get_applications_collection():
    return _db["applications"]


def get_collection(name: str):
    return _db[name]
