---
name: docker-patterns
description: "Docker patterns: production docker-compose files, optimized Dockerfiles for Python, Go (distroless), and Java (Spring Boot), BuildKit caching, Docker networks, resource limits and OOM protection, and container debugging. Use when writing Dockerfiles or compose files or debugging containers."
---

# Docker Patterns

Multi-stage Dockerfiles, docker-compose with health checks, BuildKit caching, and container security patterns.

## Production docker-compose.yml

```yaml
# docker-compose.yml
version: "3.9"

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
      target: runtime           # Build only to runtime stage
      cache_from:
        - type=registry,ref=myregistry/myapp:buildcache
      args:
        BUILDKIT_INLINE_CACHE: "1"
    image: myregistry/myapp:${IMAGE_TAG:-latest}
    restart: unless-stopped
    ports:
      - "3000:3000"
    environment:
      NODE_ENV: production
      PORT: "3000"
    env_file:
      - .env.prod               # Non-secret config
    secrets:
      - database_url            # Docker secrets (or external: true for Swarm)
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:3000/health || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    security_opt:
      - no-new-privileges:true
    read_only: true
    tmpfs:
      - /tmp:noexec,nosuid,size=100m
    cap_drop:
      - ALL
    mem_limit: 512m
    cpus: '1.0'
    networks:
      - frontend
      - backend
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"

  db:
    image: postgres:16-alpine
    restart: unless-stopped
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: myapp
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
    secrets:
      - db_password
    volumes:
      - db_data:/var/lib/postgresql/data
      - ./db/init:/docker-entrypoint-initdb.d:ro
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U myapp -d myapp"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s
    networks:
      - backend
    mem_limit: 1g

  redis:
    image: redis:7-alpine
    restart: unless-stopped
    command: redis-server --maxmemory 256mb --maxmemory-policy allkeys-lru --requirepass ${REDIS_PASSWORD}
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "-a", "${REDIS_PASSWORD}", "ping"]
      interval: 5s
      timeout: 3s
      retries: 5
    networks:
      - backend
    mem_limit: 256m

  nginx:
    image: nginx:1.25-alpine
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
    depends_on:
      - app
    networks:
      - frontend
    mem_limit: 64m

secrets:
  database_url:
    file: ./secrets/database_url.txt
  db_password:
    file: ./secrets/db_password.txt

volumes:
  db_data:
    driver: local
  redis_data:
    driver: local

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true   # No internet access from backend network
```

## Optimized Dockerfiles by Language

### Python (FastAPI/Flask)
```dockerfile
# syntax=docker/dockerfile:1.6
FROM python:3.12-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

FROM base AS deps
WORKDIR /app
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-deps -r requirements.txt

FROM base AS runtime
RUN groupadd -r -g 1001 appgroup && \
    useradd -r -u 1001 -g appgroup -m appuser
WORKDIR /app
COPY --from=deps /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=deps /usr/local/bin/uvicorn /usr/local/bin/uvicorn
COPY --chown=appuser:appgroup . .
USER appuser
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
```

### Go (Distroless)
```dockerfile
# syntax=docker/dockerfile:1.6
FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN --mount=type=cache,target=/go/pkg/mod \
    go mod download
COPY . .
RUN --mount=type=cache,target=/go/pkg/mod \
    --mount=type=cache,target=/root/.cache/go-build \
    CGO_ENABLED=0 GOOS=linux GOARCH=amd64 \
    go build -ldflags="-w -s" -o /bin/app .

# Distroless: no shell, no package manager, minimal attack surface
FROM gcr.io/distroless/static-debian12:nonroot AS runtime
COPY --from=builder /bin/app /app
EXPOSE 8080
ENTRYPOINT ["/app"]
```

### Java (Spring Boot)
```dockerfile
# syntax=docker/dockerfile:1.6
FROM eclipse-temurin:21-jdk-alpine AS builder
WORKDIR /app
COPY mvnw pom.xml ./
COPY .mvn .mvn
RUN --mount=type=cache,target=/root/.m2 \
    ./mvnw dependency:go-offline -q

COPY src ./src
RUN --mount=type=cache,target=/root/.m2 \
    ./mvnw package -q -DskipTests
# Extract layers for better Docker layer caching
RUN java -Djarmode=layertools -jar target/*.jar extract --destination target/extracted

FROM eclipse-temurin:21-jre-alpine AS runtime
RUN addgroup -S spring && adduser -S spring -G spring
WORKDIR /app
COPY --from=builder --chown=spring:spring /app/target/extracted/dependencies/ ./
COPY --from=builder --chown=spring:spring /app/target/extracted/spring-boot-loader/ ./
COPY --from=builder --chown=spring:spring /app/target/extracted/snapshot-dependencies/ ./
COPY --from=builder --chown=spring:spring /app/target/extracted/application/ ./
USER spring
EXPOSE 8080
# JVM flags for containers: respect cgroup memory limits
ENV JAVA_OPTS="-XX:+UseContainerSupport -XX:MaxRAMPercentage=75.0"
ENTRYPOINT ["java", "org.springframework.boot.loader.JarLauncher"]
```

## BuildKit Cache Optimization

```bash
# Enable BuildKit
export DOCKER_BUILDKIT=1

# Build with registry cache (best for CI)
docker buildx build \
  --cache-from type=registry,ref=myregistry/myapp:buildcache \
  --cache-to type=registry,ref=myregistry/myapp:buildcache,mode=max \
  --tag myregistry/myapp:latest \
  --push \
  .

# GitHub Actions cache (stores in Actions cache, free)
docker buildx build \
  --cache-from type=gha \
  --cache-to type=gha,mode=max \
  .

# Local cache (useful for development)
docker buildx build \
  --cache-from type=local,src=/tmp/docker-cache \
  --cache-to type=local,dest=/tmp/docker-cache,mode=max \
  .
```

## Docker Network Patterns

```yaml
# Isolated backend network: prevents direct internet access from DB containers
networks:
  frontend:
    driver: bridge      # App + nginx, can reach internet
  backend:
    driver: bridge
    internal: true      # DB + Redis: no outbound internet

# Result:
# nginx <-> app: both on frontend network
# app <-> db: both on backend network
# db: cannot initiate outbound connections (internal: true)
```

## Resource Limits and OOM Protection

```yaml
# docker-compose resource limits
services:
  app:
    mem_limit: 512m           # Hard OOM kill at 512MB
    mem_reservation: 256m     # Soft limit for scheduling
    memswap_limit: 512m       # Disable swap (== mem_limit): prevent swap thrashing
    cpus: '1.5'               # Max 1.5 CPU cores
    cpu_shares: 512           # Relative weight (default 1024)

# ulimits for app servers
    ulimits:
      nofile:
        soft: 65536
        hard: 65536
      nproc:
        soft: 4096
        hard: 4096
```

## Container Debugging Patterns

```bash
# Shell into running container
docker exec -it container_name sh    # Alpine
docker exec -it container_name bash  # Debian/Ubuntu

# Read-only or distroless: create debug sidecar
kubectl debug -it pod/myapp --image=busybox --target=myapp

# Inspect container without running
docker create --name debug myimage sh
docker cp debug:/etc/nginx/nginx.conf ./nginx.conf.extracted
docker rm debug

# Override entrypoint for debugging
docker run --rm -it --entrypoint sh myapp:latest

# View container logs
docker logs --follow --timestamps container_name
docker logs --tail 100 container_name

# Export container filesystem for inspection
docker export container_name | tar -tv | grep -E "(\.conf|\.env|\.key)"
```
