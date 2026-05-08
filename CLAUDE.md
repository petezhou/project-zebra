# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Full-stack authentication system with FastAPI backend, React frontend, and PostgreSQL database. Monorepo structure with separate backend/frontend directories.

## Architecture

**Backend (FastAPI):**
- `app/api/` - API route handlers (e.g., auth.py for /auth/register, /auth/login)
- `app/core/` - Security (password hashing with Argon2, JWT tokens), dependencies (get_db)
- `app/models/` - SQLAlchemy ORM models (User)
- `app/schemas/` - Pydantic schemas for request/response validation
- `app/db/` - Database session management, Base declarative class
- `alembic/` - Database migrations

**Frontend (React + Vite):**
- `src/components/` - React components (Register.jsx)
- Vite dev server on port 5173

**Key architectural patterns:**
- Dependency injection via FastAPI's `Depends(get_db)` for database sessions
- Pydantic schemas separate from SQLAlchemy models (schemas for validation, models for ORM)
- Password hashing with Argon2 (not bcrypt)
- CORS only enabled in development via `ENVIRONMENT=development` env var (production uses reverse proxy)
- Tests use in-memory SQLite with `StaticPool` to share DB across connections

## Development Commands

**Docker (primary development workflow):**
```bash
# Start all services (backend, frontend, db)
docker-compose up -d

# View logs
docker-compose logs -f [backend|frontend|db]

# Restart a service after code changes
docker-compose restart backend

# Stop everything
docker-compose down
```

**Backend (local development with venv):**
```bash
cd backend

# Activate venv (must do this every time)
source venv/bin/activate

# Install dependencies
pip install -e .[test,dev]

# Run tests (all)
pytest

# Run tests (verbose)
pytest -v

# Run specific test
pytest tests/test_auth.py::test_register_user

# Lint
ruff check .

# Format
ruff check . --fix && ruff format .
```

**Frontend (local development):**
```bash
cd frontend

# Install dependencies
npm install

# Start dev server (outside Docker)
npm run dev

# Build for production
npm run build
```

**Database:**
```bash
# Connect to PostgreSQL
docker-compose exec db psql -U zebra -d zebra

# Check users table
docker-compose exec db psql -U zebra -d zebra -c "SELECT id, email, full_name, created_at FROM users;"

# Run migrations
docker-compose exec backend alembic upgrade head

# Create new migration
docker-compose exec backend alembic revision --autogenerate -m "description"
```

## Configuration

All config via environment variables in `.env` (never commit this file):
- `ENVIRONMENT=development` - Enables CORS for local frontend
- `DATABASE_URL` - PostgreSQL connection string (postgres:// in Docker, sqlite:// for local tests)
- `SECRET_KEY` - JWT signing key (generate with `openssl rand -hex 32`)

## Testing

Tests use in-memory SQLite (no artifacts). The `conftest.py` uses `StaticPool` to ensure all test connections share the same in-memory database instance. Each test gets a fresh database via function-scoped fixtures.

API routes do not have `/api` prefix in code (e.g., `/auth/register` not `/api/auth/register`). Production reverse proxy adds `/api` prefix for routing.

## Ports

- Backend: http://localhost:8000
- Frontend: http://localhost:5173
- PostgreSQL: localhost:5432
- API Docs: http://localhost:8000/docs
