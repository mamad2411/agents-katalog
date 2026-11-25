---
name: docker-compose
description: Create production-ready Docker Compose configurations for multi-container applications. Outputs service definitions, networking, volumes, and environment management.
argument-hint: [application architecture, services needed]
allowed-tools: Read, Write, Bash
---

# Docker Compose Configuration

Design a complete Docker Compose setup for local development and staging environments. Not just "docker-compose up" — proper networking, volume management, health checks, secrets, and environment-specific overrides.

## Process

1. **Identify services.** Web app, database, cache, queue, workers — what needs to run?
2. **Define service images.** Official images vs custom Dockerfiles.
3. **Configure networking.** Bridge networks for isolation, service discovery by name.
4. **Plan volumes.** Persistent data (database), bind mounts (code for dev), named volumes.
5. **Set environment variables.** Dev vs staging configs, secrets management.
6. **Add health checks.** Ensure dependencies start in correct order.
7. **Configure resource limits.** Memory, CPU constraints.
8. **Create override files.** `docker-compose.override.yml` for local dev tweaks.

## Output Format

### Docker Compose Setup: [Application Name]

**Environment:** Development + Staging  
**Total Services:** 6  
**Networks:** 2 (frontend, backend)  
**Volumes:** 4 (postgres_data, redis_data, uploads, logs)  

---

## Base Configuration (docker-compose.yml)

```yaml
version: '3.8'

services:
  # Web Application (Django/Flask/Node)
  web:
    build:
      context: .
      dockerfile: Dockerfile
      target: development  # Multi-stage build
    image: myapp-web:latest
    container_name: myapp_web
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/myapp
      - REDIS_URL=redis://redis:6379/0
      - DJANGO_SETTINGS_MODULE=myapp.settings.development
      - DEBUG=true
    volumes:
      - .:/app  # Bind mount for hot reload
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    networks:
      - frontend
      - backend
    restart: unless-stopped
    command: python manage.py runserver 0.0.0.0:8000
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health/"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  # PostgreSQL Database
  db:
    image: postgres:15-alpine
    container_name: myapp_db
    environment:
      - POSTGRES_DB=myapp
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
      - PGDATA=/var/lib/postgresql/data/pgdata
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql  # Init script
    ports:
      - "5432:5432"  # Expose for local tools (pgAdmin)
    networks:
      - backend
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: '1.0'

  # Redis Cache
  redis:
    image: redis:7-alpine
    container_name: myapp_redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    networks:
      - backend
    restart: unless-stopped
    command: redis-server --appendonly yes --maxmemory 256mb --maxmemory-policy allkeys-lru
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 3

  # Celery Worker (Background Tasks)
  celery_worker:
    build:
      context: .
      dockerfile: Dockerfile
      target: development
    image: myapp-web:latest
    container_name: myapp_celery
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/myapp
      - REDIS_URL=redis://redis:6379/0
      - CELERY_BROKER_URL=redis://redis:6379/1
      - CELERY_RESULT_BACKEND=redis://redis:6379/2
    volumes:
      - .:/app
      - media_volume:/app/media
    depends_on:
      - db
      - redis
    networks:
      - backend
    restart: unless-stopped
    command: celery -A myapp worker -l info --concurrency=4
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '0.5'

  # Celery Beat (Scheduled Tasks)
  celery_beat:
    build:
      context: .
      dockerfile: Dockerfile
      target: development
    image: myapp-web:latest
    container_name: myapp_celery_beat
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/myapp
      - REDIS_URL=redis://redis:6379/0
      - CELERY_BROKER_URL=redis://redis:6379/1
    volumes:
      - .:/app
    depends_on:
      - db
      - redis
    networks:
      - backend
    restart: unless-stopped
    command: celery -A myapp beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler

  # Nginx (Reverse Proxy + Static Files)
  nginx:
    image: nginx:1.25-alpine
    container_name: myapp_nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - static_volume:/var/www/static:ro
      - media_volume:/var/www/media:ro
      - ./ssl:/etc/nginx/ssl:ro  # SSL certificates
    depends_on:
      - web
    networks:
      - frontend
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost/health/"]
      interval: 30s
      timeout: 10s
      retries: 3

# Networks
networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge

# Volumes
volumes:
  postgres_data:
    driver: local
  redis_data:
    driver: local
  static_volume:
    driver: local
  media_volume:
    driver: local
```

---

## Development Overrides (docker-compose.override.yml)

This file is automatically merged with `docker-compose.yml` for local development.

```yaml
version: '3.8'

services:
  web:
    build:
      target: development
    environment:
      - DEBUG=true
      - DJANGO_SETTINGS_MODULE=myapp.settings.development
    volumes:
      - .:/app:cached  # Cached for Mac performance
    command: python manage.py runserver 0.0.0.0:8000 --noreload

  db:
    ports:
      - "5432:5432"  # Expose for local DB clients

  redis:
    ports:
      - "6379:6379"  # Expose for redis-cli

  # Add debugging tools
  adminer:
    image: adminer:latest
    container_name: myapp_adminer
    ports:
      - "8080:8080"
    networks:
      - backend
    environment:
      - ADMINER_DEFAULT_SERVER=db
```

---

## Staging Configuration (docker-compose.staging.yml)

```yaml
version: '3.8'

services:
  web:
    build:
      target: production
    environment:
      - DEBUG=false
      - DJANGO_SETTINGS_MODULE=myapp.settings.staging
      - DATABASE_URL=${DATABASE_URL}  # From .env file
      - REDIS_URL=${REDIS_URL}
      - SECRET_KEY=${SECRET_KEY}
    volumes:
      - static_volume:/app/staticfiles:ro  # Read-only
      - media_volume:/app/media
    command: gunicorn myapp.wsgi:application --bind 0.0.0.0:8000 --workers 4

  db:
    environment:
      - POSTGRES_PASSWORD=${DB_PASSWORD}  # Secrets from .env
    ports: []  # Don't expose externally

  redis:
    ports: []  # Don't expose externally
    command: redis-server --requirepass ${REDIS_PASSWORD}

  celery_worker:
    command: celery -A myapp worker -l warning --concurrency=8

  nginx:
    volumes:
      - ./nginx.staging.conf:/etc/nginx/nginx.conf:ro
```

**Usage:**
```bash
# Start staging environment
docker-compose -f docker-compose.yml -f docker-compose.staging.yml up -d
```

---

## Multi-Stage Dockerfile

```dockerfile
# Stage 1: Base
FROM python:3.11-slim as base
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Stage 2: Development
FROM base as development
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir debugpy ipdb  # Dev tools
COPY . .
EXPOSE 8000

# Stage 3: Production
FROM base as production
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN python manage.py collectstatic --noinput
EXPOSE 8000
CMD ["gunicorn", "myapp.wsgi:application", "--bind", "0.0.0.0:8000"]
```

---

## Environment Files

### .env.example
```bash
# Database
DATABASE_URL=postgresql://postgres:password@db:5432/myapp
DB_PASSWORD=change_me_in_production

# Redis
REDIS_URL=redis://redis:6379/0
REDIS_PASSWORD=change_me_in_production

# Application
SECRET_KEY=change_me_in_production
DEBUG=false
ALLOWED_HOSTS=localhost,127.0.0.1,staging.example.com

# AWS (if needed)
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_STORAGE_BUCKET_NAME=

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
```

### .env (gitignored)
```bash
# Copy from .env.example and fill in real values
SECRET_KEY=actual_secret_key_here
DB_PASSWORD=actual_db_password
```

---

## Nginx Configuration (nginx.conf)

```nginx
events {
    worker_connections 1024;
}

http {
    upstream web {
        server web:8000;
    }

    server {
        listen 80;
        server_name localhost;

        client_max_body_size 100M;

        # Static files
        location /static/ {
            alias /var/www/static/;
            expires 30d;
            add_header Cache-Control "public, immutable";
        }

        # Media files
        location /media/ {
            alias /var/www/media/;
            expires 7d;
        }

        # Health check
        location /health/ {
            access_log off;
            return 200 "OK\n";
            add_header Content-Type text/plain;
        }

        # Proxy to Django
        location / {
            proxy_pass http://web;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            
            proxy_connect_timeout 60s;
            proxy_send_timeout 60s;
            proxy_read_timeout 60s;
        }
    }
}
```

---

## Database Initialization (init.sql)

```sql
-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";  -- For text search

-- Create read-only user for analytics
CREATE USER analytics_reader WITH PASSWORD 'analytics_password';
GRANT CONNECT ON DATABASE myapp TO analytics_reader;
GRANT USAGE ON SCHEMA public TO analytics_reader;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO analytics_reader;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO analytics_reader;
```

---

## Common Commands

### Start Services
```bash
# Development (uses docker-compose.override.yml automatically)
docker-compose up -d

# Staging
docker-compose -f docker-compose.yml -f docker-compose.staging.yml up -d

# View logs
docker-compose logs -f web

# View logs for all services
docker-compose logs -f
```

### Database Operations
```bash
# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Backup database
docker-compose exec db pg_dump -U postgres myapp > backup.sql

# Restore database
docker-compose exec -T db psql -U postgres myapp < backup.sql

# Access PostgreSQL shell
docker-compose exec db psql -U postgres myapp
```

### Celery Operations
```bash
# View active tasks
docker-compose exec celery_worker celery -A myapp inspect active

# Purge all tasks
docker-compose exec celery_worker celery -A myapp purge

# Monitor tasks in real-time
docker-compose exec celery_worker celery -A myapp events
```

### Cleanup
```bash
# Stop services
docker-compose down

# Stop and remove volumes (DELETES DATA)
docker-compose down -v

# Rebuild images
docker-compose build --no-cache

# Remove dangling images
docker image prune -f
```

---

## Secrets Management

### Using Docker Secrets (Swarm Mode)
```yaml
services:
  web:
    secrets:
      - db_password
      - secret_key
    environment:
      - DB_PASSWORD_FILE=/run/secrets/db_password
      - SECRET_KEY_FILE=/run/secrets/secret_key

secrets:
  db_password:
    file: ./secrets/db_password.txt
  secret_key:
    file: ./secrets/secret_key.txt
```

### Using .env Files (Development)
```yaml
services:
  web:
    env_file:
      - .env
      - .env.local  # Overrides .env
```

---

## Resource Limits

### Development (Generous)
```yaml
services:
  web:
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: '1.0'
        reservations:
          memory: 512M
          cpus: '0.5'
```

### Production (Strict)
```yaml
services:
  web:
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '0.5'
        reservations:
          memory: 256M
          cpus: '0.25'
```

---

## Health Checks Best Practices

### Web Application
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health/"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s  # Grace period for startup
```

### Database
```yaml
healthcheck:
  test: ["CMD-SHELL", "pg_isready -U postgres"]
  interval: 10s
  timeout: 5s
  retries: 5
```

### Redis
```yaml
healthcheck:
  test: ["CMD", "redis-cli", "ping"]
  interval: 10s
  timeout: 5s
  retries: 3
```

---

## Troubleshooting

### Container Won't Start
```bash
# Check logs
docker-compose logs web

# Inspect container
docker-compose ps
docker inspect myapp_web

# Check resource usage
docker stats
```

### Database Connection Issues
```bash
# Verify database is healthy
docker-compose exec db pg_isready -U postgres

# Check network connectivity
docker-compose exec web ping db

# Verify environment variables
docker-compose exec web env | grep DATABASE
```

### Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000
# Or
netstat -tuln | grep 8000

# Kill process or change port mapping
```

---

## CI/CD Integration

### GitHub Actions
```yaml
name: Docker Build

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Build and test
        run: |
          docker-compose -f docker-compose.yml -f docker-compose.test.yml build
          docker-compose -f docker-compose.yml -f docker-compose.test.yml run web pytest
      
      - name: Push to registry
        run: |
          docker-compose build web
          docker tag myapp-web:latest registry.example.com/myapp-web:${{ github.sha }}
          docker push registry.example.com/myapp-web:${{ github.sha }}
```

## Rules

- Every service must have a health check — dependencies use `depends_on: condition: service_healthy`.
- Secrets must never be hardcoded — use .env files (dev) or Docker secrets (prod).
- Database data must use named volumes, not bind mounts — prevents data loss.
- Always specify image versions (`:15-alpine` not `:latest`) for reproducibility.
- Development uses bind mounts for hot reload, production uses COPY in Dockerfile.
- Resource limits are mandatory for production to prevent memory leaks from crashing host.
- Networks should isolate frontend (public) from backend (internal) services.
- Restart policy should be `unless-stopped` for persistence across host reboots.
- Port exposure should be minimized in production — only nginx needs public ports.
- Use multi-stage Dockerfiles to keep production images small (exclude dev dependencies).
