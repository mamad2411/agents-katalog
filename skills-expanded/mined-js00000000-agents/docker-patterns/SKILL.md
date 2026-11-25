---
name: docker-patterns
description: Docker and Docker Compose best practices for local development, multi-stage builds, and container orchestration.
---

# Docker & Docker Compose Patterns

Best practices for containerized development and deployment, tailored for the Fusion Labs infrastructure.

## When to Activate

- Working with Docker or Docker Compose
- Setting up local development infrastructure
- Creating Dockerfiles for Go or Node.js applications
- Configuring service networking
- Working in `system/infra/`

## Fusion Labs Infrastructure

The shared development services are in `system/infra/`:

```yaml
# system/infra/docker-compose.yml
version: '3.8'

services:
  postgres:
    image: postgres:16-alpine
    container_name: fusion-postgres
    restart: unless-stopped
    ports:
      - "5432:5432"
    environment:
      POSTGRES_USER: devuser
      POSTGRES_PASSWORD: devpassword
      POSTGRES_DB: devdb
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U devuser -d devdb"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    container_name: fusion-redis
    restart: unless-stopped
    ports:
      - "6379:6379"
    command: redis-server --requirepass devpassword
    volumes:
      - redis_data:/var/lib/redis/data
    healthcheck:
      test: ["CMD", "redis-cli", "-a", "devpassword", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
  redis_data:
```

## Dockerfile Patterns

### Go Multi-Stage Build

```dockerfile
# Stage 1: Build
FROM golang:1.22-alpine AS builder

WORKDIR /app

# Cache dependencies
COPY go.mod go.sum ./
RUN go mod download

# Build
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-s -w" -o /app/server ./cmd/server

# Stage 2: Runtime
FROM alpine:3.19

RUN apk --no-cache add ca-certificates tzdata

WORKDIR /app

COPY --from=builder /app/server .

# Non-root user
RUN adduser -D -g '' appuser
USER appuser

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s \
  CMD wget --no-verbose --tries=1 --spider http://localhost:8080/health || exit 1

ENTRYPOINT ["./server"]
```

### Node.js / React + Vite Multi-Stage Build

```dockerfile
# Stage 1: Dependencies
FROM node:20-alpine AS deps

WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --production=false

# Stage 2: Build
FROM node:20-alpine AS builder

WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

# Stage 3: Serve with nginx
FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

## Docker Compose Patterns

### Full Application Stack

```yaml
version: '3.8'

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8080:8080"
    environment:
      - DATABASE_URL=postgresql://devuser:devpassword@postgres:5432/devdb?sslmode=disable
      - REDIS_URL=redis://:devpassword@redis:6379/0
      - JWT_SECRET=dev-jwt-secret-change-in-production
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    restart: unless-stopped

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:80"
    depends_on:
      - backend

  postgres:
    image: postgres:16-alpine
    ports:
      - "5432:5432"
    environment:
      POSTGRES_USER: devuser
      POSTGRES_PASSWORD: devpassword
      POSTGRES_DB: devdb
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U devuser -d devdb"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    command: redis-server --requirepass devpassword
    healthcheck:
      test: ["CMD", "redis-cli", "-a", "devpassword", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
  redis_data:
```

### Development Overrides

```yaml
# docker-compose.override.yml (auto-loaded in dev)
version: '3.8'

services:
  backend:
    volumes:
      - ./backend:/app          # Live reload
    environment:
      - GIN_MODE=debug
    command: ["air", "-c", ".air.toml"]  # Hot reload with Air

  frontend:
    volumes:
      - ./frontend/src:/app/src  # Hot module replacement
    command: ["npm", "run", "dev"]
    ports:
      - "5173:5173"              # Vite dev server
```

## Best Practices

### 1. Layer Ordering

Order Dockerfile instructions from least to most frequently changed:

```dockerfile
# 1. Base image (rarely changes)
FROM golang:1.22-alpine

# 2. System dependencies (rarely changes)
RUN apk add --no-cache git

# 3. App dependencies (changes occasionally)
COPY go.mod go.sum ./
RUN go mod download

# 4. Source code (changes frequently)
COPY . .

# 5. Build step
RUN go build -o /app/server ./cmd/server
```

### 2. .dockerignore

```text
# .dockerignore
.git
.gitignore
node_modules
*.md
.env*
.vscode
.idea
tmp/
dist/
coverage/
```

### 3. Health Checks

Always include health checks for production services:

```yaml
healthcheck:
  test: ["CMD-SHELL", "curl -f http://localhost:8080/health || exit 1"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

### 4. Named Volumes for Persistence

```yaml
volumes:
  postgres_data:
    driver: local
  redis_data:
    driver: local
```

### 5. Security

```dockerfile
# Don't run as root
RUN adduser -D -g '' appuser
USER appuser

# Don't store secrets in images
# Use environment variables or Docker secrets instead

# Use specific image tags, not :latest
FROM postgres:16.2-alpine  # Specific version
```

## Useful Commands

```bash
# Start infrastructure
cd system/infra && docker-compose up -d

# View logs
docker-compose logs -f postgres
docker-compose logs -f redis

# Stop & clean up
docker-compose down
docker-compose down -v  # Also remove volumes

# Rebuild specific service
docker-compose build --no-cache backend

# Execute command in running container
docker-compose exec postgres psql -U devuser -d devdb

# View resource usage
docker stats

# Prune unused resources
docker system prune -a
docker volume prune
```

## Networking

```yaml
# Custom network for isolation
networks:
  fusion-net:
    driver: bridge

services:
  backend:
    networks:
      - fusion-net
  postgres:
    networks:
      - fusion-net
```

Services on the same network can reach each other by service name (e.g., `postgres:5432` from the backend container).

---

**Remember**: Containers should be ephemeral — able to be stopped, destroyed, and rebuilt with minimal effort. Keep images small, layers cached, and configurations external.
