---
name: docker-and-compose
description: Production containerization patterns, multi-stage Dockerfiles, Docker Compose orchestrations, non-root security hardening, and cache optimization.
aliases:
  - docker
  - dockerfile
  - docker-compose
  - containerization
category: "03 - Database & Migrations"
tags:
  - agent-skill
  - docker
  - containers
  - devops
  - stage-3
---

# Docker & Docker Compose Production Craft

Production-grade containerization standards for modern web applications, microservices, and databases. Designed for minimal image sizes, rapid layer caching, non-root security, and deterministic local development.

---

## 🛡️ Core Rules & Anti-Patterns

1. **Always Use Multi-Stage Builds**:
   - Separate build-time dependencies (compilers, devDependencies, header files) from runtime artifacts.
   - Use minimal runtime base images (`alpine`, `distroless`, or `-slim`).
2. **Never Run as Root**:
   - Explicitly create and switch to a non-privileged user (`USER appuser` or `USER node` / `USER nonroot`).
3. **Optimize Docker Layer Caching**:
   - Copy dependency manifests (`package.json`, `pnpm-lock.yaml`, `requirements.txt`, `go.mod`) and install dependencies *before* copying application source code.
4. **Always Provide a `.dockerignore`**:
   - Exclude `.git`, `node_modules`, `.env*`, `__pycache__`, build artifacts, and test coverage reports.
5. **Always Configure Health Checks**:
   - Add native `HEALTHCHECK` directives in Dockerfile and Compose services to enable zero-downtime restarts.

---

## 📦 Reference Architectures

### 1. Production Node.js / Next.js Multi-Stage Dockerfile

```dockerfile
# Stage 1: Base setup
FROM node:20-alpine AS base
RUN apk add --no-cache libc6-compat
WORKDIR /app

# Stage 2: Install dependencies
FROM base AS deps
COPY package.json pnpm-lock.yaml* ./
RUN corepack enable pnpm && pnpm install --frozen-lockfile

# Stage 3: Build application
FROM base AS builder
COPY --from=deps /app/node_modules ./node_modules
COPY . .
ENV NEXT_TELEMETRY_DISABLED=1
RUN corepack enable pnpm && pnpm build

# Stage 4: Production runner
FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
ENV PORT=3000

# Security: non-root user
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs
EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3000/api/health || exit 1

CMD ["node", "server.js"]
```

### 2. Production Python / FastAPI Dockerfile

```dockerfile
FROM python:3.11-slim AS builder
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.11-slim AS runner
WORKDIR /app
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH=/home/appuser/.local/bin:$PATH

RUN useradd -m -u 1001 appuser
COPY --from=builder --chown=appuser:appuser /root/.local /home/appuser/.local
COPY --chown=appuser:appuser . .

USER appuser
EXPOSE 8000

HEALTHCHECK --interval=15s --timeout=3s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
```

### 3. Local Development `docker-compose.yml`

```yaml
services:
  app:
    build:
      context: .
      dockerfile: Dockerfile.dev
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgres://postgres:postgres@db:5432/app_dev
    volumes:
      - .:/app
      - /app/node_modules
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: app_dev
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  pgdata:
```

---

## 🔗 Connected Skills (ทักษะที่เกี่ยวข้อง)
- [[Skills/database-migrations/SKILL|database-migrations]] — รัน Migration เชื่อมต่อกับ Database Container แบบปลอดภัย
- [[Skills/deploy-with-vercel/SKILL|deploy-with-vercel]] — ทางเลือกในการ Deploy Web Application สู่ Cloud
- [[Skills/systematic-debugging/SKILL|systematic-debugging]] — วินิจฉัยข้อผิดพลาดในการบิลด์และรัน Container

<!-- v1.1.0 synchronized: 2026-09-29 -->
