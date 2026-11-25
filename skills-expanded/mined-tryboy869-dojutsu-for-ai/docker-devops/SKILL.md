---
name: docker-devops
description: "Apply when writing Dockerfiles, docker-compose files, or container orchestration. Covers: multi-stage builds, layer caching, security hardening, compose patterns, health checks. Trigger for: Docker, container, Dockerfile, docker-compose, k8s."
---

# DOCKER & DEVOPS — Production Container Patterns

## Dockerfile — Multi-stage (MANDATORY for production)
```dockerfile
# Stage 1: Build
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime (no build tools)
FROM python:3.12-slim AS runtime
WORKDIR /app

# Security: non-root user
RUN addgroup --system app && adduser --system --group app
USER app

# Copy only what's needed
COPY --from=builder /root/.local /home/app/.local
COPY --chown=app:app src/ ./src/

ENV PATH=/home/app/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Layer Caching — Order matters
```dockerfile
# ✅ Correct order (rarely changed → frequently changed)
COPY requirements.txt .      # 1. deps (cached until requirements change)
RUN pip install ...           # 2. install
COPY src/ .                   # 3. code (changes most often)

# ❌ Wrong — invalidates cache on every code change
COPY . .
RUN pip install ...
```

## .dockerignore (always)
```
.git
.env
__pycache__
*.pyc
*.egg-info
dist/
node_modules/
.pytest_cache/
```

## docker-compose — Development
```yaml
version: "3.9"
services:
  api:
    build: { context: ., target: runtime }
    ports: ["8000:8000"]
    env_file: .env
    depends_on:
      db: { condition: service_healthy }
      redis: { condition: service_healthy }
    volumes:
      - ./src:/app/src  # hot reload in dev only

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: ${DB_NAME}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      retries: 5
    volumes:
      - pgdata:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]

volumes:
  pgdata:
```

## Security Rules
- Never run as root in production
- Never `COPY . .` without `.dockerignore`
- No secrets in Dockerfile — use `--secret` or env vars at runtime
- Pin base image versions (not `latest`)
- Scan images: `docker scout cves myimage`

## Forbidden
❌ `FROM ubuntu` (use distroless or slim)
❌ Secrets in ENV or ARG (visible in image layers)
❌ `CMD ["bash"]` in production
❌ Root user
❌ No healthcheck
