---
name: docker-best-practices
description: Follow container best practices for secure, efficient Docker images.
---

# Docker best practices

Root-running, bloated, or cache-unfriendly images widen the attack surface, slow every build and pull, and turn a container escape into host compromise. These constraints are checkable in a Dockerfile linter (e.g. `hadolint`) — wire it into CI.

## Rules

- Use multi-stage builds to keep final images small.
- Run as a non-root user in the final stage.
- Pin base image versions (avoid `latest` tag in production).
- Copy dependency manifests and install before copying source (layer caching).
- Include a `.dockerignore` that excludes `node_modules`, `.git`, `.env`, and build artifacts.
- Use `HEALTHCHECK` instructions for production services.
- Prefer `COPY` over `ADD` unless extracting archives.

## Examples

```dockerfile
# BAD — single stage, runs as root, copies everything before installing deps
FROM node:latest
COPY . .
RUN npm install
CMD ["node", "dist/index.js"]

# GOOD — multi-stage, non-root user, layer-cache-friendly dep install
FROM node:20.15.0-alpine3.20 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --omit=dev
COPY . .
RUN npm run build

FROM node:20.15.0-alpine3.20
WORKDIR /app
RUN addgroup -S app && adduser -S app -G app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
USER app
HEALTHCHECK CMD wget -qO- http://localhost:3000/health || exit 1
CMD ["node", "dist/index.js"]
```
