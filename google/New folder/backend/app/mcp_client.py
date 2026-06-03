"""Minimal MCP client adapter for MongoDB usage in this project.
This acts as the 'partner MCP' integration (MongoDB) for storing traces, resumes, and application records.
"""
from typing import Any, Dict
from .db import get_collection


class MCPClient:
    def __init__(self):
        # collections: resumes, analyses, applications, traces
        self.resumes = get_collection("resumes")
        self.analyses = get_collection("analyses")
        self.applications = get_collection("applications")
        self.traces = get_collection("traces")

    def save_resume(self, doc: Dict[str, Any]):
        return self.resumes.insert_one(doc)

    def save_analysis(self, doc: Dict[str, Any]):
        return self.analyses.insert_one(doc)

    def save_application(self, doc: Dict[str, Any]):
        return self.applications.insert_one(doc)

    def save_trace(self, doc: Dict[str, Any]):
        return self.traces.insert_one(doc)
