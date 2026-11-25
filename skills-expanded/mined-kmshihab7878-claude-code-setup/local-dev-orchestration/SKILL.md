---
name: local-dev-orchestration
description: Local development environment orchestration with Docker Compose, Tilt, and mise for multi-service Python/TS stacks
triggers:
  - local dev
  - docker compose
  - development environment
  - tilt
  - mise
  - devbox
---

# Local Development Orchestration

Orchestrate local development environments for multi-service architectures. Covers Docker Compose, Tilt, mise, and service dependency management tailored for Python/TypeScript stacks on macOS ARM64.

## Core Principles

1. **Fast feedback loops** -- hot-reload everything, minimize container rebuilds
2. **Production parity** -- local env should mirror production as closely as possible
3. **One-command startup** -- `just up` or `tilt up` should bring everything online
4. **Isolated dependencies** -- each service owns its runtime version via mise

## Docker Compose Patterns

### Multi-stage development compose

```yaml
# docker/docker-compose.yml
services:
  api:
    build:
      context: ..
      dockerfile: docker/Dockerfile
      target: development
    volumes:
      - ../src:/app/src:cached
      - ../tests:/app/tests:cached
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://coremind:coremind@db:5432/coremind
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    command: uvicorn coremind.api.main:app --reload --host 0.0.0.0

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: coremind
      POSTGRES_USER: coremind
      POSTGRES_PASSWORD: coremind
    volumes:
      - pgdata:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U coremind"]
      interval: 5s
      timeout: 3s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  pgdata:
```

### Dockerfile with multi-stage build

```dockerfile
# Base stage
FROM python:3.10-slim AS base
WORKDIR /app
RUN pip install --no-cache-dir uv

# Development stage (includes dev deps, hot reload)
FROM base AS development
COPY pyproject.toml requirements*.txt ./
RUN uv pip install --system -r requirements.txt -r requirements-dev.txt
COPY src/ ./src/
COPY tests/ ./tests/

# Production stage (minimal, no dev deps)
FROM base AS production
COPY pyproject.toml requirements.txt ./
RUN uv pip install --system -r requirements.txt --no-dev
COPY src/ ./src/
RUN useradd --create-home appuser
USER appuser
CMD ["uvicorn", "coremind.api.main:app", "--host", "0.0.0.0"]
```

## mise Integration

```toml
# .mise.toml at project root
[tools]
python = "3.10"
node = "22"
terraform = "1.10"

[env]
PYTHONDONTWRITEBYTECODE = "1"
DATABASE_URL = "postgresql://coremind:coremind@localhost:5432/coremind"
REDIS_URL = "redis://localhost:6379/0"
```

Run `mise install` to set up all runtimes. Run `mise trust` in a new project.

## Service Health Checks

Always verify services before running tests or starting dependent services:

```bash
# justfile recipe
wait-for-services:
    @echo "Waiting for PostgreSQL..."
    @until pg_isready -h localhost -p 5432 -U coremind 2>/dev/null; do sleep 1; done
    @echo "Waiting for Redis..."
    @until redis-cli -h localhost ping 2>/dev/null | grep -q PONG; do sleep 1; done
    @echo "All services ready."
```

## Debugging in Containers

For Python services, enable remote debugging:

```python
# In development, add to entrypoint
import debugpy
debugpy.listen(("0.0.0.0", 5678))
```

Expose port 5678 in compose and attach VS Code debugger.

## Performance Tips for macOS

- Use `:cached` volume mounts for source code
- Use named volumes (not bind mounts) for database data
- Consider Colima instead of Docker Desktop for lower memory usage
- Use `COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1` for faster builds
