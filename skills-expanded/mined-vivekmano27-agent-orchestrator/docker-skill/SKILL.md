---
name: docker-skill
description: Create optimized Dockerfiles, multi-stage builds, docker-compose configs, health checks, and container security. Use when the user says "Dockerize", "Docker compose", "container", "Dockerfile", or needs to containerize their application.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Docker Skill

Production-grade containerization.

## Multi-Stage Dockerfile (Node.js)
```dockerfile
# Stage 1: Dependencies
FROM node:20-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --only=production

# Stage 2: Build
FROM node:20-alpine AS builder
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 3: Production
FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
RUN addgroup -g 1001 -S nodejs && adduser -S nextjs -u 1001
COPY --from=deps /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package.json ./
USER nextjs
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=3s CMD wget -qO- http://localhost:3000/health || exit 1
CMD ["node", "dist/main.js"]
```

## Multi-Stage Dockerfile (Python)
```dockerfile
# Stage 1: Build
FROM python:3.12-slim-bookworm AS builder
WORKDIR /app
RUN pip install --no-cache-dir --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2: Production
FROM python:3.12-slim-bookworm AS runner
WORKDIR /app
RUN groupadd -g 1001 appgroup && useradd -u 1001 -g appgroup -s /bin/false appuser
COPY --from=builder /install /usr/local
COPY . .
RUN chown -R appuser:appgroup /app
USER appuser
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1
CMD ["gunicorn", "main:app", "--bind", "0.0.0.0:8000", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker"]
```

## Multi-Stage Dockerfile (Go)
```dockerfile
# Stage 1: Build
FROM golang:1.22-alpine AS builder
WORKDIR /src
RUN apk add --no-cache git ca-certificates
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-s -w" -o /app/server ./cmd/server

# Stage 2: Production
FROM gcr.io/distroless/static-debian12:nonroot AS runner
COPY --from=builder /app/server /server
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s CMD ["/server", "healthcheck"]
USER nonroot:nonroot
ENTRYPOINT ["/server"]
```

## Multi-Stage Dockerfile (Flutter Web)
```dockerfile
# Stage 1: Build
FROM ghcr.io/cirruslabs/flutter:stable AS builder
WORKDIR /app
COPY pubspec.yaml pubspec.lock ./
RUN flutter pub get
COPY . .
RUN flutter build web --release --tree-shake-icons

# Stage 2: Production
FROM nginx:1.25-alpine AS runner
RUN addgroup -g 1001 -S appgroup && adduser -S appuser -u 1001 -G appgroup
COPY --from=builder /app/build/web /usr/share/nginx/html
COPY <<'NGINX' /etc/nginx/conf.d/default.conf
server {
    listen 80;
    root /usr/share/nginx/html;
    index index.html;
    location / {
        try_files $uri $uri/ /index.html;
    }
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff2?)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
NGINX
EXPOSE 80
HEALTHCHECK --interval=30s --timeout=3s CMD wget -qO- http://localhost:80/ || exit 1
USER appuser
CMD ["nginx", "-g", "daemon off;"]
```

## Dockerfile Best Practices

### Non-Root User
```dockerfile
# Debian-based
RUN groupadd -g 1001 appgroup && useradd -u 1001 -g appgroup -s /bin/false appuser
USER appuser

# Alpine-based
RUN addgroup -g 1001 -S appgroup && adduser -S appuser -u 1001 -G appgroup
USER appuser

# Distroless (built-in)
USER nonroot:nonroot
```

### .dockerignore
```
node_modules
.git
.env
*.md
dist
build
__pycache__
*.pyc
.venv
.idea
.vscode
Dockerfile
docker-compose*.yml
```

### Layer Caching
```dockerfile
# GOOD: copy dependency manifests first, install, then copy source
COPY package.json package-lock.json ./
RUN npm ci
COPY . .

# BAD: invalidates cache on every source change
COPY . .
RUN npm ci
```

### Health Checks
```dockerfile
# HTTP health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD wget -qO- http://localhost:3000/health || exit 1

# TCP health check
HEALTHCHECK --interval=30s --timeout=3s \
  CMD nc -z localhost 8080 || exit 1

# Custom binary health check (Go)
HEALTHCHECK --interval=30s --timeout=3s \
  CMD ["/server", "healthcheck"]
```

### Security Scanning
```bash
# Scan image for vulnerabilities
docker scout cves myimage:latest

# Trivy scan
trivy image --severity HIGH,CRITICAL myimage:latest

# Lint Dockerfile
hadolint Dockerfile
```

## Docker Compose
```yaml
version: '3.8'
services:
  app:
    build: .
    ports: ['3000:3000']
    environment:
      DATABASE_URL: postgresql://postgres:postgres@db:5432/app
      REDIS_URL: redis://redis:6379
    depends_on:
      db: { condition: service_healthy }
      redis: { condition: service_healthy }
  
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: app
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    volumes: ['postgres_data:/var/lib/postgresql/data']
    healthcheck:
      test: ['CMD-SHELL', 'pg_isready -U postgres']
      interval: 5s
      timeout: 5s
      retries: 5
  
  redis:
    image: redis:7-alpine
    healthcheck:
      test: ['CMD', 'redis-cli', 'ping']
      interval: 5s

volumes:
  postgres_data:
```

## Anti-Patterns

- **Running as root** — containers running as root user; always use a non-root USER in the Dockerfile
- **No .dockerignore** — copying node_modules, .git, and .env into the image; always create a .dockerignore
- **Using :latest tag** — non-deterministic builds; pin base images to specific versions or SHAs
- **Single-stage builds** — including build tools (compilers, dev dependencies) in the production image; use multi-stage builds
- **No health checks** — containers without HEALTHCHECK; orchestrators can't detect unhealthy containers
- **Hardcoded config** — baking environment-specific config into the image; use environment variables

## Checklist

- [ ] Multi-stage build separating build and runtime
- [ ] Base image pinned to specific version
- [ ] .dockerignore excludes node_modules, .git, .env, build artifacts
- [ ] Non-root USER directive in Dockerfile
- [ ] HEALTHCHECK instruction defined
- [ ] Environment variables for all configuration
- [ ] docker-compose.yml for local development with all services
- [ ] Health checks on all service dependencies (DB, Redis, etc.)
