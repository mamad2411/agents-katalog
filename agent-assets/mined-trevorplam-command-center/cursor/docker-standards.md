---
description: Run Docker and Container Standards Check
globs: ["Dockerfile*", "docker-compose*.yml", ".dockerignore"]
---
# Infrastructure: Docker & Container Standards

<audit_rules>
- You MUST use specific version tags for base images (e.g., `node:18.17.1-alpine`) and NOT use `latest` or floating tags.
- You MUST create a non-root user with minimal permissions to run the application inside containers.
- You MUST implement multi-stage builds to minimize final image size and exclude build dependencies.
- You MUST set appropriate health checks in Docker Compose and Dockerfiles to monitor container status.
- You MUST ensure sensitive data is injected via environment variables or secrets, NOT hardcoded in images.
- You MUST use .dockerignore to exclude unnecessary files and directories from the build context.
- You MUST limit container resources (memory, CPU) in docker-compose.yml to prevent resource exhaustion.
</audit_rules>

<example_good>
```dockerfile
# Dockerfile
# Stage 1: Build
FROM node:18.17.1-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production && npm cache clean --force
COPY . .
RUN npm run build

# Stage 2: Runtime
FROM node:18.17.1-alpine AS runtime
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nextjs -u 1001
WORKDIR /app

# Copy built application
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static
COPY --from=builder --chown=nextjs:nodejs /app/public ./public

USER nextjs

EXPOSE 3000
ENV NODE_ENV=production
ENV PORT=3000

CMD ["node", "server.js"]

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:3000/api/health || exit 1
```

```yaml
# docker-compose.yml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - DATABASE_URL=${DATABASE_URL}
    restart: unless-stopped
    # Resource limits
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '0.5'
        reservations:
          memory: 256M
          cpus: '0.25'
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

```dockerignore
# .dockerignore
node_modules
.git
.gitignore
README.md
.env
.env.local
.env.development.local
.env.test.local
.env.production.local
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.next
coverage
.nyc_output
```
</example_good>

<example_bad>
```dockerfile
# BAD: Using latest tag, running as root, single stage
FROM node:latest
WORKDIR /app
COPY . .
RUN npm install
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
```

```yaml
# BAD: No resource limits, no health checks
version: '3.8'
services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgres://user:pass@localhost:5432/db # BAD: Hardcoded credentials
```
</example_bad>

