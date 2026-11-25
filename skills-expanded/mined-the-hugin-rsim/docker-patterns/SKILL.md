---
name: docker-patterns
description: Docker and Docker Compose patterns for local development, container security, networking, volume strategies, and multi-stage builds.
origin: ECC
group: domain
triggers:
  - "Dockerfile"
  - "docker compose паттерн"
  - "контейнер безопасность"
  - "multi-stage build"
output: "secure, production-ready Dockerfiles and docker-compose.yml configurations"
calls: []
---

# Docker Patterns

Docker and Docker Compose best practices for containerized development.

## When to Activate

- Setting up Docker Compose for local development
- Designing multi-container architectures
- Reviewing Dockerfiles for security and size
- Troubleshooting container networking or volume issues

## Standard Web App Stack

```yaml
# docker-compose.yml
services:
  app:
    build:
      context: .
      target: dev
    ports:
      - "3000:3000"
    volumes:
      - .:/app                     # Bind mount for hot reload
      - /app/node_modules          # Anonymous volume — preserves container deps
    environment:
      - DATABASE_URL=postgres://postgres:postgres@db:5432/app_dev
      - NODE_ENV=development
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: app_dev
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 3s
      retries: 5

  redis:
    image: redis:7-alpine
    volumes:
      - redisdata:/data

volumes:
  pgdata:
  redisdata:
```

## Multi-Stage Dockerfile

```dockerfile
# deps stage
FROM node:22-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci

# dev stage (hot reload)
FROM node:22-alpine AS dev
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
EXPOSE 3000
CMD ["npm", "run", "dev"]

# build stage
FROM node:22-alpine AS build
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build && npm prune --production

# production stage (minimal, non-root)
FROM node:22-alpine AS production
WORKDIR /app
RUN addgroup -g 1001 -S appgroup && adduser -S appuser -u 1001
USER appuser
COPY --from=build --chown=appuser:appgroup /app/dist ./dist
COPY --from=build --chown=appuser:appgroup /app/node_modules ./node_modules
ENV NODE_ENV=production
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=3s CMD wget -qO- http://localhost:3000/health || exit 1
CMD ["node", "dist/server.js"]
```

## Override Files

```yaml
# docker-compose.override.yml (dev-only, auto-loaded)
services:
  app:
    environment:
      - DEBUG=app:*
      - LOG_LEVEL=debug

# docker-compose.prod.yml (explicit for production)
services:
  app:
    build:
      target: production
    restart: always
    deploy:
      resources:
        limits:
          cpus: "1.0"
          memory: 512M
```

```bash
# Development (auto-loads override)
docker compose up

# Production
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## Networking

```yaml
# Service discovery: services resolve by name
# From "app" container:
# postgres://postgres:postgres@db:5432/app_dev  ← "db" resolves automatically

# Custom networks for isolation
services:
  frontend:
    networks: [frontend-net]
  api:
    networks: [frontend-net, backend-net]
  db:
    networks: [backend-net]     # Only reachable from api

networks:
  frontend-net:
  backend-net:
```

## Volume Strategies

| Type | Usage | Example |
|---|---|---|
| Named volume | Persist data across restarts | `pgdata:/var/lib/postgresql/data` |
| Bind mount | Hot reload in dev | `.:/app` |
| Anonymous volume | Protect container paths from bind mount | `/app/node_modules` |

## Container Security

```dockerfile
# 1. Pin specific image versions (never :latest)
FROM node:22.12-alpine3.20

# 2. Run as non-root user
RUN addgroup -g 1001 -S app && adduser -S app -u 1001
USER app
```

```yaml
# Compose hardening
services:
  app:
    security_opt:
      - no-new-privileges:true
    read_only: true
    tmpfs:
      - /tmp
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE   # only if binding ports < 1024
```

## Secret Management

```yaml
# GOOD: env_file (never commit .env to git)
services:
  app:
    env_file: .env

# BAD: hardcoded in image
# ENV API_KEY=sk-proj-xxxxx   ← NEVER
```

## .dockerignore

```
node_modules
.git
.env
.env.*
dist
coverage
*.log
.next
.cache
```

## Debugging Commands

```bash
# Logs
docker compose logs -f app
docker compose logs --tail=50 db

# Shell into container
docker compose exec app sh
docker compose exec db psql -U postgres

# Status
docker compose ps
docker stats

# Rebuild
docker compose up --build
docker compose build --no-cache app

# Cleanup
docker compose down           # stop containers
docker compose down -v        # + remove volumes (DESTRUCTIVE)
docker system prune           # remove unused images
```

## Multi-Compose Caddy Proxying

When adding a new service from a separate docker-compose to an existing Caddy instance:

```bash
# 1. Find the actual network Caddy lives in (NOT always "projectname_default")
docker ps --format "table {{.Names}}\t{{.Networks}}"

# 2. Connect new container to that network
docker network connect <caddy-network> <new-container>

# 3. Reload Caddy
docker exec caddy caddy reload --config /etc/caddy/Caddyfile
```

```
# Caddyfile: use container name as upstream — NOT localhost
new-subdomain.example.com {
    reverse_proxy new-container-name:PORT
}
```

> ⚠️ `localhost:PORT` inside Caddy container = the Caddy container itself, not the host.
> Network name = `<compose-folder-name>_<network-name>` — verify before connecting.

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|---|---|---|
| `:latest` tag | Non-reproducible builds | Pin to `node:22.12-alpine3.20` |
| Running as root | Security risk | Create non-root user |
| Data in container | Lost on restart | Use named volumes |
| Secrets in compose.yml | Exposed in git | Use `.env` (gitignored) |
| One giant container | Hard to scale/debug | One process per container |
