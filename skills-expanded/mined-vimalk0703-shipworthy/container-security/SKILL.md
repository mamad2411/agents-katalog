---
name: container-security
description: Dockerfile best practices, secure base images, no secrets in build context, multi-stage builds, non-root execution, and image scanning guidance.
invoke_when: Use when writing or reviewing Dockerfiles, docker-compose files, container build pipelines, or discussing container deployment and image security.
---

# Container Security

## Base Image Rules

1. **Use official or verified images only** -- `node:22-slim`, `python:3.12-slim`, `alpine:3.20`.
2. **Pin by digest, not just tag** -- tags are mutable.
3. **Prefer `-slim` or `-alpine` variants** -- smaller attack surface.
4. **Never use `latest`** -- builds must be reproducible.

```dockerfile
# BAD
FROM node:latest

# GOOD -- pinned tag + slim variant
FROM node:22.12-slim
```

## No Secrets in the Dockerfile

Secrets in the build context end up in image layers. Layers are permanent and extractable.

```dockerfile
# BAD -- secret baked into the image
ENV DATABASE_URL=postgres://user:password@host/db
COPY .env /app/.env

# GOOD -- inject at runtime via docker run -e or --env-file
# For build-time secrets, use BuildKit secret mounts:
RUN --mount=type=secret,id=npmrc,target=/root/.npmrc npm ci
```

## Multi-Stage Builds

Keep build tools out of the final image:

```dockerfile
FROM node:22.12-slim AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:22.12-slim
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
USER node
CMD ["node", "dist/server.js"]
```

## Non-Root User

Always run as a non-root user. Most official images ship one (e.g., `node`).

```dockerfile
RUN addgroup --system app && adduser --system --ingroup app app
USER app
```

## .dockerignore Is Required

Every project with a Dockerfile must have a `.dockerignore`:

```
.git
.env*
node_modules
*.md
.github
tests
coverage
```

## Image Scanning

Scan images in CI before pushing to a registry. **Tools:** Trivy (free, fast), Snyk Container, Docker Scout.

**Policy:** No CRITICAL vulnerabilities in production images. HIGH must be triaged within 7 days.

```yaml
- name: Scan image
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: myapp:${{ github.sha }}
    severity: CRITICAL,HIGH
    exit-code: 1
```

## Dockerfile Review Checklist

- [ ] Base image is official/verified, pinned to a specific version
- [ ] No `ENV` or `COPY` of secrets -- runtime injection only
- [ ] Multi-stage build separates build tools from production image
- [ ] Final stage runs as non-root user
- [ ] `.dockerignore` exists and excludes `.env*`, `.git`, `node_modules`
- [ ] Image is scanned in CI with a fail-on-critical policy
