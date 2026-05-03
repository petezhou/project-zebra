from fastapi import FastAPI
from sqlalchemy import text

from app.db.session import engine

app = FastAPI(title="Project Zebra")


@app.get("/")
def root():
    """Root endpoint."""
    return {"message": "Project Zebra", "status": "running"}


@app.get("/health")
def health():
    """Health check with database connectivity test."""
    try:
        # Test database connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            result.fetchone()

        return {
            "status": "healthy",
            "database": "connected"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }
