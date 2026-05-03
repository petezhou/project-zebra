from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL environment variable is not set. "
        "Please set it in docker-compose.yml or your environment."
    )

# Create engine
# pool_pre_ping=True ensures connections are alive before using them
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    echo=False  # Set to True to see SQL queries in logs
)

# Session factory
# autocommit=False: transactions must be explicitly committed
# autoflush=False: changes aren't automatically flushed to DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
