import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Load .env file if it exists (for local development)
env_path = Path(__file__).parent.parent.parent / ".env"
if env_path.exists():
    load_dotenv(env_path)

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL environment variable is not set. "
        "Please set it in docker-compose.yml or your environment."
    )

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True, # ensures connections are alive before using them
    echo=False  # Set to True to see SQL queries in logs
)

# autocommit=False: transactions must be explicitly committed
# autoflush=False: changes aren't automatically flushed to DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
