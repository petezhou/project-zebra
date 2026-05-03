# Project Zebra
Project for practicing things.

## Getting Started

### Prerequisites
- OrbStack or Docker Desktop
- Docker Compose

### Setup

1. Start containers:
```bash
docker-compose up -d
```

2. Verify health:
```bash
curl http://localhost:8000/health
```

3. View logs:
```bash
docker-compose logs -f
```

### Ports
- Backend API: http://localhost:8000
- PostgreSQL: localhost:5432
- API Docs: http://localhost:8000/docs

### Stop containers
```bash
docker-compose down
```
