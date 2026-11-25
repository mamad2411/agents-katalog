---
name: tpl-devops-docker-compose-dev
description: Template do pack (devops/04-docker-compose-dev.md). Orienta o agente em infra, deploy, CI/CD e operacao alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: devops/04-docker-compose-dev.md
  generated_by: install_pack_templates_as_claude_skills
---

# PROJECT: Docker Compose Multi-Service Dev Environment

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `devops/04-docker-compose-dev.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

## STACK
- **Docker Compose:** v3.9 (Compose Specification)
- **Services:** Node.js app + PostgreSQL 16 + Redis 7 + Nginx
- **Hot Reload:** Nodemon / Vite HMR via bind mounts
- **Environment:** .env file (dotenv)
- **Networking:** Custom bridge network with DNS service discovery
- **Profiles:** dev (all services) / test (app + db only) / prod (override)

---

## FILE STRUCTURE
```
project/
├── docker-compose.yml          # Base config (shared across envs)
├── docker-compose.override.yml # Dev overrides (auto-loaded)
├── docker-compose.prod.yml     # Prod overrides (explicit)
├── docker-compose.test.yml     # Test overrides
├── .env                        # Local env vars (gitignored)
├── .env.example                # Committed template
├── Dockerfile                  # Multi-stage (dev + prod)
└── nginx/
    ├── nginx.conf
    └── conf.d/
        └── default.conf
```

---

## ARCHITECTURE RULES
1. **`.env` is gitignored** — `.env.example` is committed with all keys (values redacted).
2. **Volumes for data, binds for code** — named volumes for DB/Redis data; bind mounts for app source.
3. **`depends_on` with `condition: service_healthy`** — app never starts before DB is truly ready.
4. **Services talk by service name** — `postgres://postgres:5432/mydb`, not `localhost`.
5. **No hardcoded ports in app code** — always use `process.env.REDIS_HOST`, `process.env.DB_HOST`.
6. **Dev Dockerfile stage has devDependencies** — prod stage does NOT (`npm ci --omit=dev`).
7. **Health checks on every stateful service** — postgres, redis, nginx must have `healthcheck`.
8. **Resource limits on prod override** — do not run unbounded containers in any environment.

---

## BASE COMPOSE FILE

```yaml
# docker-compose.yml
version: "3.9"

x-common-env: &common-env
  NODE_ENV: ${NODE_ENV:-development}
  LOG_LEVEL: ${LOG_LEVEL:-debug}

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
      target: ${BUILD_TARGET:-dev}     # dev | prod
    ports:
      - "${APP_PORT:-3000}:3000"
    environment:
      <<: *common-env
      DATABASE_URL: postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@postgres:5432/${POSTGRES_DB}
      REDIS_URL: redis://redis:6379
      PORT: 3000
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - app-network
    restart: unless-stopped

  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER:     ${POSTGRES_USER:-appuser}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-changeme}
      POSTGRES_DB:       ${POSTGRES_DB:-appdb}
    volumes:
      - postgres-data:/var/lib/postgresql/data
      - ./db/init:/docker-entrypoint-initdb.d:ro   # Init SQL scripts
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER:-appuser} -d ${POSTGRES_DB:-appdb}"]
      interval: 5s
      timeout: 5s
      retries: 10
      start_period: 10s
    networks:
      - app-network
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    command: >
      redis-server
      --requirepass ${REDIS_PASSWORD:-changeme}
      --maxmemory 256mb
      --maxmemory-policy allkeys-lru
    volumes:
      - redis-data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "-a", "${REDIS_PASSWORD:-changeme}", "ping"]
      interval: 5s
      timeout: 3s
      retries: 5
    networks:
      - app-network
    restart: unless-stopped

  nginx:
    image: nginx:1.25-alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/conf.d:/etc/nginx/conf.d:ro
      - nginx-cache:/var/cache/nginx
    depends_on:
      app:
        condition: service_started
    healthcheck:
      test: ["CMD", "nginx", "-t"]
      interval: 30s
      timeout: 5s
      retries: 3
    networks:
      - app-network
    restart: unless-stopped

networks:
  app-network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16

volumes:
  postgres-data:
    driver: local
  redis-data:
    driver: local
  nginx-cache:
    driver: local
```

---

## DEV OVERRIDE (auto-loaded)

```yaml
# docker-compose.override.yml
services:
  app:
    build:
      target: dev
    volumes:
      # Hot reload: bind-mount source into container
      - ./src:/app/src:delegated
      - ./package.json:/app/package.json:ro
      - ./tsconfig.json:/app/tsconfig.json:ro
      # Preserve container's node_modules (NOT bind-mounted)
      - app-node-modules:/app/node_modules
    command: npm run dev          # nodemon or ts-node-dev
    environment:
      CHOKIDAR_USEPOLLING: "true"    # Needed on Windows/WSL2
      WATCHPACK_POLLING: "true"      # For webpack/vite in WSL2

  postgres:
    ports:
      - "5432:5432"   # Expose in dev for DBeaver/psql access

  redis:
    ports:
      - "6379:6379"   # Expose in dev for Redis Insight

volumes:
  app-node-modules:
```

---

## PRODUCTION OVERRIDE

```yaml
# docker-compose.prod.yml
# Usage: docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
services:
  app:
    build:
      target: prod
    restart: always
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  postgres:
    # Do NOT expose ports in production
    deploy:
      resources:
        limits:
          memory: 1G

  redis:
    deploy:
      resources:
        limits:
          memory: 512M
```

---

## MULTI-STAGE DOCKERFILE

```dockerfile
# Dockerfile
FROM node:20-alpine AS base
WORKDIR /app
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# --- Dependencies stage ---
FROM base AS deps
COPY package*.json ./
RUN npm ci

# --- Development stage ---
FROM deps AS dev
ENV NODE_ENV=development
COPY . .
USER appuser
CMD ["npm", "run", "dev"]

# --- Build stage ---
FROM deps AS builder
COPY . .
RUN npm run build

# --- Production stage ---
FROM base AS prod
ENV NODE_ENV=production
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package*.json ./
RUN npm ci --omit=dev && npm cache clean --force
USER appuser
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD wget -qO- http://localhost:3000/healthz || exit 1
CMD ["node", "dist/server.js"]
```

---

## .ENV.EXAMPLE

```bash
# .env.example — commit this, NOT .env
NODE_ENV=development
APP_PORT=3000

POSTGRES_USER=appuser
POSTGRES_PASSWORD=changeme_dev
POSTGRES_DB=appdb

REDIS_PASSWORD=changeme_dev

LOG_LEVEL=debug

# JWT_SECRET=         ← fill in .env
# OPENAI_API_KEY=     ← fill in .env
```

---

## COMMON COMMANDS

```bash
# Start all services (dev)
docker compose up -d

# Tail logs
docker compose logs -f app

# Exec into running container
docker compose exec app sh

# Run one-off command (migrations)
docker compose run --rm app npm run db:migrate

# Rebuild after Dockerfile changes
docker compose up -d --build

# Production deployment
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build

# Full teardown (keeps volumes)
docker compose down

# Nuke everything including volumes (danger)
docker compose down -v
```

---

## NGINX REVERSE PROXY CONFIG

```nginx
# nginx/conf.d/default.conf
upstream app_backend {
    server app:3000;
    keepalive 32;
}

server {
    listen 80;
    server_name _;

    location /healthz {
        proxy_pass http://app_backend;
        access_log off;
    }

    location / {
        proxy_pass http://app_backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_cache_bypass $http_upgrade;
        client_max_body_size 10M;
    }
}
```
