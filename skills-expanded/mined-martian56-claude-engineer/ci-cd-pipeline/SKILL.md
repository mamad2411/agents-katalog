---
name: ci-cd-pipeline
description: Use near the end of a project to generate CI and make the app deploy-ready. Produces a polyglot GitHub Actions workflow (lint, typecheck, test, build) and multi-stage Dockerfiles. The finish line is CI-green and container-ready, not an actual deploy.
---

# CI/CD Pipeline

**Announce at start:** "I'm using claude-engineer:ci-cd-pipeline to generate CI and containerization."

## Finish line
**CI-green + container-ready. No actual deploy.** (Deploy targets/credentials are out of scope for v1.)

## What to generate
1. **GitHub Actions** - a polyglot workflow that, on PR and main:
   - installs both toolchains (uv for Python, pnpm/Bun for JS) with caching;
   - **lint** (`ruff` + `eslint`/`prettier --check`);
   - **typecheck** (`mypy`/`pyright` + `tsc --noEmit`);
   - **test** (`pytest` + `vitest run --coverage`) using **service containers** (Postgres/Redis) for integration tests;
   - **build** (frontend build + backend image build);
   - run the **four quality gates** (`claude-engineer:testing-and-quality`) as the merge condition.
2. **Multi-stage Dockerfiles** - FastAPI (uv builder → slim runtime) and the frontend (Next `output: standalone` or static build) + `.dockerignore`. These prove the app is container-ready.

## Non-negotiables
1. CI enforces the **same four gates** the local commit gate enforces - no weaker checks in CI.
2. Caching for both toolchains (don't reinstall the world each run).
3. Pin action versions and base images.

**Full detail (the complete Actions workflow, service-container config, the multi-stage Dockerfiles, prod compose notes):**
read `references/ci-and-containers.md` on demand.

## Red flags - STOP
- CI that skips a gate the local gate enforces.
- A Dockerfile that copies `.env`/secrets or `node_modules`/`.venv` (use `.dockerignore`).
- Unpinned `latest` actions or base images.
