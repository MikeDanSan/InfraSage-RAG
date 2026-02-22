"""
FastAPI application entry point.

Responsibilities:
- Define the FastAPI app instance
- POST /ingest endpoint: accepts a PDF, runs the ingestion pipeline
- POST /query endpoint: accepts a question, runs the query pipeline
- Wire together ingestion, embeddings, retrieval, and llm modules
"""
