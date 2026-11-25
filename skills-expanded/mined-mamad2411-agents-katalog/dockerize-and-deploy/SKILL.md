---
name: dockerize-and-deploy
description: Dockerize a repository and produce production-grade deployment scripts, a docker-compose setup with properly configured volumes, and a pre-flight validation shell script. Use when the user wants to containerize an app, add Docker support, write a deployment pipeline, set up docker-compose, configure volumes, or deploy to production with Docker.
---

# Dockerize and Deploy

Containerize a repo and produce a production-ready deployment setup. Work in phases — never write everything at once.

## Quick Start

1. Audit the repo (language, services, DB, existing Docker files).
2. Confirm phases with the user.
3. Execute one phase at a time, verifying after each.

## Workflow

### 1. Audit the repo

Read the codebase to identify:

- **Runtime**: Node.js, Python, Go, Java, etc. and version
- **Services**: web server, background workers, scheduled jobs
- **Datastores**: PostgreSQL, MySQL, Redis, MongoDB, S3-compatible storage
- **Build step**: bundler, compiler, static assets
- **Existing Docker files**: `Dockerfile`, `docker-compose.yml`, `.dockerignore`
- **Secrets/env vars**: `.env.example`, config files, hardcoded values

Summarize findings and propose phases before writing anything.

### 2. Confirm phases

Standard phases — adjust based on what the repo needs:

1. **Dockerfile** — multi-stage build for the app
2. **docker-compose** — local dev stack with all services
3. **Production compose** — `docker-compose.prod.yml` with volumes, restart policies, resource limits
4. **Pre-flight script** — `scripts/preflight.sh` validates environment before deploy
5. **Deploy script** — `scripts/deploy.sh` orchestrates the full deployment

Present to the user as a numbered list. Merge or skip phases if the repo is simple.

### 3. Write the Dockerfile (Phase 1)

Use a multi-stage build:
- **Stage 1 (builder)**: install deps, compile/bundle
- **Stage 2 (runtime)**: copy only built artifacts, run as non-root user

Pin the base image to a specific minor version (e.g. `node:20.11-alpine`). Add a `.dockerignore` that excludes `node_modules`, `.env`, `.git`, build artifacts.

### 4. Write docker-compose files (Phases 2–3)

Dev compose: mounts source for hot reload, exposes debug ports, uses named volumes for DB data.

Prod compose: no source mounts, `restart: unless-stopped`, healthchecks on every service, explicit volume declarations, resource limits (`mem_limit`, `cpus`). See [REFERENCE.md](REFERENCE.md) for volume and healthcheck patterns.

### 5. Write pre-flight script (Phase 4)

Copy `scripts/preflight.sh` from this skill's `scripts/` directory into the project. It validates:
- Required env vars are set and non-empty
- Docker and docker-compose are installed and reachable
- No port conflicts on required ports
- DB connection string is reachable (optional ping)
- Image builds successfully (dry run)

Run it: `bash scripts/preflight.sh` — exits non-zero on any failure.

### 6. Write deploy script (Phase 5)

`scripts/deploy.sh` flow:
1. Run `preflight.sh` — abort if it fails
2. Pull latest images / build new image
3. Run DB migrations (if applicable)
4. Rolling restart: bring up new containers before stopping old ones
5. Health-check the running stack
6. Print service URLs and status

### 7. Verify after each phase

```bash
docker build -t app:test .           # Dockerfile compiles
docker compose config                # compose files are valid YAML
docker compose up -d && docker compose ps  # services start healthy
bash scripts/preflight.sh            # pre-flight passes
```

## Guardrails

- Never embed secrets in Dockerfiles or compose files — use env files or secrets mounts.
- Always run containers as a non-root user.
- Do not use `latest` image tags in production — pin versions.
- Volumes for DB data must use named volumes, never bind mounts to host paths.
- If the repo has no `.env.example`, create one before writing any Docker config.

## References

- [REFERENCE.md](REFERENCE.md) — volume patterns, healthcheck templates, resource limits, multi-stage examples by runtime, rolling deploy strategies.
