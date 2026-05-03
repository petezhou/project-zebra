from sqlalchemy.ext.declarative import declarative_base

# Base class for all SQLAlchemy models
# All models will inherit from this
Base = declarative_base()

# Import all models here so Alembic can detect them for migrations
from app.models.user import User  # noqa: F401, E402
