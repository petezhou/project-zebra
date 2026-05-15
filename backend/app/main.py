import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.api import auth
from app.db.session import engine

app = FastAPI(title="Project Zebra", version="0.1.0")

# CORS - only needed in development (local frontend on different port)
# Production uses reverse proxy (same origin, no CORS needed)
if os.getenv("ENVIRONMENT") == "development":
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],
        allow_credentials=True,  # Required for cookies (refresh token)
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Register routers
app.include_router(auth.router)


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
