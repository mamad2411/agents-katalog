# Docker Skill

You are working with Docker. Apply these conventions.

## Dockerfile Best Practices

- Use official minimal base images: `node:22-alpine`, `python:3.12-slim`, `golang:1.23-alpine`.
- Use multi-stage builds to keep the final image small:
  ```dockerfile
  FROM node:22-alpine AS builder
  WORKDIR /app
  COPY package*.json ./
  RUN npm ci
  COPY . .
  RUN npm run build

  FROM node:22-alpine AS runner
  WORKDIR /app
  ENV NODE_ENV=production
  COPY --from=builder /app/dist ./dist
  COPY --from=builder /app/node_modules ./node_modules
  CMD ["node", "dist/index.js"]
  ```
- Copy `package.json` and lock file before source code so Docker layer caching isn't invalidated by source changes.
- Run as a non-root user: `RUN addgroup -S app && adduser -S app -G app && USER app`.
- Use `CMD` (JSON array form) with explicit entry points — avoid shell form to prevent PID 1 signal issues.

## .dockerignore

Always include a `.dockerignore`:
```
node_modules
dist
.git
*.md
.env
coverage
```

## Compose

- Use `docker-compose.yml` for local development; `docker-compose.override.yml` for dev-only overrides.
- Use named volumes for persistent data (databases); use bind mounts for source code in dev.
- Define `depends_on` with `condition: service_healthy` to wait for database readiness.
- Use `healthcheck` on database services so dependent services wait for them.

## Security

- Scan images with `docker scout cves` or `trivy` in CI.
- Never store secrets in image layers; use Docker secrets or runtime environment injection.
- Pin base image digests in production: `node:22-alpine@sha256:…`.
- Use `--read-only` flag and `--cap-drop ALL` for distroless production containers when possible.

## Layer Optimization

- Order Dockerfile instructions from least to most frequently changed.
- Use `RUN --mount=type=cache` (BuildKit) to cache package manager caches between builds.
- Combine `RUN` commands with `&&` to minimize layers.
