from fastapi import FastAPI
from sqlalchemy import create_engine, text
import os

app = FastAPI(title="Project Zebra")

# Database connection check
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://zebra:zebra_dev_password@localhost:5432/zebra")


@app.get("/")
def root():
    """Root endpoint."""
    return {"message": "Project Zebra", "status": "running"}


@app.get("/health")
def health():
    """Health check with database connectivity test."""
    try:
        # Test database connection
        engine = create_engine(DATABASE_URL)
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
