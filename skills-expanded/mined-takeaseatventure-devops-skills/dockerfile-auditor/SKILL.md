---
name: dockerfile-auditor
description: Audit Dockerfiles for layer bloat, cache-busting patterns, security smells, and best-practice violations. Use when a user writes or reviews a Dockerfile, when a Docker image is too large, when builds are slow, or when hardening a container for production. Pro skill — requires a takeaseat All-Access license.
license: pro
---

# dockerfile-auditor

> **Pro skill.** This skill is part of the takeaseat Pro tier. It provides deeper
> analysis than the free skills. To unlock, get an
> [All-Access license](https://takeaseatventure.com/pro).

## When to use this skill

- A user writes a Dockerfile or asks you to review one.
- A Docker image is too large (>500MB for a typical app).
- Docker builds are slow or fail to cache effectively.
- A container needs hardening for production deployment.
- A user asks "is this Dockerfile production-ready?"

## The 12 Dockerfile audit checks

Run every check against the Dockerfile. Report each as PASS / WARN / FAIL with a
specific, actionable recommendation.

### 1. Base image specificity

**FAIL** if the base image uses `:latest` tag — it's non-reproducible.
**WARN** if using a full OS image (`ubuntu`, `debian`) when a slim/alpine variant exists.
**PASS** if pinned to a specific version: `node:20.11-alpine3.19`.

```dockerfile
# ❌ Bad — non-reproducible, large
FROM node:latest

# ✅ Good — pinned, small
FROM node:20.11-alpine3.19
```

### 2. Layer ordering (cache efficiency)

Docker caches layers top-to-bottom. If a layer changes, all layers below it are
rebuilt. **Put the least-frequently-changing instructions first.**

**FAIL** if `COPY . .` appears before `RUN npm install` — every code change busts the
dependency cache.

```dockerfile
# ❌ Bad — any code change reinstalls all deps
COPY . .
RUN npm install

# ✅ Good — deps cached unless package.json changes
COPY package*.json ./
RUN npm ci --omit=dev
COPY . .
```

### 3. Multi-stage builds

**WARN** if the Dockerfile has no build stage and the final image contains build tools
compilers, or dev dependencies. The final image should contain only runtime artifacts.

```dockerfile
# Build stage
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Runtime stage — minimal
FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
USER node
CMD ["node", "dist/index.js"]
```

### 4. Root user

**FAIL** if the container runs as root (no `USER` directive). Containers should run as
a non-root user.

```dockerfile
# ❌ Bad — runs as root
CMD ["node", "index.js"]

# ✅ Good — dedicated user
RUN addgroup -S app && adduser -S app -G app
USER app
CMD ["node", "index.js"]
```

### 5. Secrets in layers

**FAIL** (critical) if secrets are baked into layers via `ENV`, `ARG`, or `COPY`:
```dockerfile
# ❌ CRITICAL — secret in image layer, recoverable from image history
ENV DATABASE_PASSWORD=s3cr3t
ARG API_KEY=sk_live_abc123
```

Secrets must come from runtime injection (Docker secrets, env vars at `docker run`,
Kubernetes secrets), never baked into the image.

### 6. .dockerignore

**WARN** if there's no `.dockerignore` file. Without it, `COPY . .` includes
`node_modules`, `.git`, `.env`, test files, and build artifacts — bloating the image
and potentially leaking secrets.

Essential `.dockerignore`:
```
node_modules
.git
.env*
*.md
test/
tests/
__pycache__/
*.pyc
.venv/
coverage/
.nyc_output/
Dockerfile*
docker-compose*
```

### 7. HEALTHCHECK

**WARN** if no `HEALTHCHECK` directive. Without it, orchestrators can't detect a
hung process.

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD wget -qO- http://localhost:3000/health || exit 1
```

### 8. APK/APT cache cleanup

**WARN** if `apk add` or `apt-get install` doesn't clean the package cache in the
same layer:

```dockerfile
# ❌ Bad — cache stays in the layer (~40MB wasted)
RUN apk add curl

# ✅ Good — cache removed in same layer
RUN apk add --no-cache curl
```

### 9. Explicit CMD/ENTRYPOINT form

**WARN** if `CMD` uses shell form instead of exec form. Shell form (`CMD npm start`)
starts via `/bin/sh -c`, which doesn't forward signals properly — `SIGTERM` won't
reach your app, causing slow container shutdowns.

```dockerfile
# ❌ Bad — shell form, no signal handling
CMD npm start

# ✅ Good — exec form, direct process
CMD ["node", "index.js"]
```

### 10. EXPOSE documentation

**INFO** if no `EXPOSE` directive. While not required (docker `-p` overrides), it
documents which ports the container listens on.

### 11. WORKDIR cleanliness

**WARN** if using `WORKDIR /` or no WORKDIR (files scattered in root). Always use a
dedicated directory: `WORKDIR /app`.

### 12. Image size estimation

Estimate the final image size based on the base image + installed packages. Flag if
over thresholds:
- **OK**: <200MB (typical Alpine-based app)
- **WARN**: 200-500MB
- **FAIL**: >500MB (unless justified — ML models, etc.)

## Output format

Present the audit as a table:

```
Dockerfile audit: ./Dockerfile
Base image: node:20.11-alpine3.19 (~45MB)

 # | Check                | Status | Detail
---|----------------------|--------|------------------------------------------
 1 | Base image pinned    |  PASS  | node:20.11-alpine3.19 ✓
 2 | Layer ordering       |  FAIL  | COPY . . before npm ci — cache busted on every change
 3 | Multi-stage build    |  WARN  | Single stage; devDeps in final image (~120MB)
 4 | Non-root user        |  FAIL  | No USER directive — runs as root
 5 | No secrets in layers |  PASS  | No ENV/ARG secrets detected
 6 | .dockerignore        |  WARN  | File missing — node_modules/.git included
 7 | HEALTHCHECK          |  WARN  | No health check defined
 8 | Cache cleanup        |  PASS  | --no-cache used
 9 | Exec form CMD        |  PASS  | ["node", "dist/index.js"]
10 | EXPOSE documented    |  PASS  | 3000/tcp
11 | WORKDIR              |  PASS  | /app
12 | Image size estimate  |  WARN  | ~350MB (single-stage + devDeps)

Score: 6/12. See recommendations above.
Estimated savings with fixes: ~180MB (52% reduction).
```

## Always provide the fixed Dockerfile

After the audit, provide a corrected Dockerfile that fixes all FAIL/WARN items. This
is the most valuable part — the user gets a drop-in replacement.
