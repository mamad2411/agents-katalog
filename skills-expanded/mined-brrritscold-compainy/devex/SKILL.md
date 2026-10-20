---
name: devex
description: Builds a fast, reproducible local development loop. Invoked when the user says "docker-compose for local dev", "set up local infra", "make the dev loop faster", "one-command setup", "bootstrap script", "task runner", "Makefile", "justfile", "pre-commit", "lint setup", "seed data", "dev environment", or "developer experience". Produces docker-compose for service dependencies, a task runner, env/config scaffolding, seed/fixture scripts, and pre-commit/lint so a new contributor is productive in one command.
---

# Developer Experience Skill

Optimize the **inner loop** — the seconds-to-minutes cycle of run → change → test that a developer repeats hundreds of times a day. The goal: a fresh clone is productive with **one command**, dependencies run **locally and reproducibly**, and feedback (tests, lint, types) is **fast**. Keep it simple — the simplest setup that works beats a clever one (`principles-dry-kiss`, `YAGNI`).

## What "good" looks like

- `git clone` → one bootstrap command → app runs against real local dependencies.
- Dependencies (DB, cache, queue, object store) run in containers, versions pinned, no host installs.
- A task runner exposes the handful of verbs everyone needs (`up`, `down`, `test`, `lint`, `seed`, `migrate`).
- Config is `.env`-driven with a committed `.env.example`; secrets never committed.
- Pre-commit catches format/lint/type errors before they reach CI.

## Process

### 1. docker-compose for dependencies

Run every external dependency the service needs as a pinned container. Do **not** require host installs of databases or brokers.

```yaml
# docker-compose.yml — local dev dependencies (not production)
services:
  postgres:
    image: postgres:16
    environment: { POSTGRES_PASSWORD: dev, POSTGRES_DB: app }
    ports: ["5432:5432"]
    volumes: ["pgdata:/var/lib/postgresql/data"]
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 3s
      retries: 10
  redis:
    image: redis:7
    ports: ["6379:6379"]
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 3s
      retries: 10
volumes: { pgdata: {} }
```

- **Pin image tags** (`postgres:16`, not `latest`) — reproducibility over freshness. A major-only tag still floats across minors; for full reproducibility pin a fuller version or digest (`postgres:16.4`, or `@sha256:…`), with major-only as the pragmatic floor.
- Add a **healthcheck** to every dependency so the app/tests wait for readiness instead of racing it.
- Match the **versions to production** (and to what `data-modeling` / `cloud-infra` provision) so local behavior mirrors prod.
- Name volumes so data survives `down` but is wipeable (`down -v`).

### 2. Task runner — the verbs everyone uses

Expose a small, discoverable set of commands. Use a `Makefile`, `justfile`, or `Taskfile` — pick one per repo and stay consistent (`principles-dry-kiss`).

```makefile
# Makefile
.PHONY: up down test lint seed migrate bootstrap
bootstrap: ## one-command setup for a fresh clone
	cp -n .env.example .env || true
	docker compose up -d --wait
	$(MAKE) migrate seed
up:      ; docker compose up -d --wait
down:    ; docker compose down
test:    ; <project test command>
lint:    ; <format + lint + typecheck>
seed:    ; <run seed script>
migrate: ; <run migrations>
```

Keep verbs identical across services in a monorepo so muscle memory transfers.

### 3. Env & config scaffolding

- Commit a `.env.example` listing every variable with safe local defaults; load `.env` in the app for local only.
- Never commit real secrets. Document where production secrets come from (the `cloud-infra` secrets mechanism), don't duplicate them locally.
- One source of truth for config shape — don't redefine the same vars in compose, app, and CI separately; reference.

### 4. Seed & fixtures

Provide a deterministic seed script that loads a realistic-but-small dataset so the app is usable immediately and integration tests have known state. Keep seed data in version control; make it idempotent (safe to re-run).

### 5. Pre-commit & lint

Wire format + lint + typecheck (and fast unit tests when cheap) into a pre-commit hook so errors are caught before CI — the same checks `ci-cd` runs, so local and CI agree.

```yaml
# .pre-commit-config.yaml (or a husky/lefthook equivalent)
repos:
  - repo: local
    hooks:
      - id: lint
        name: lint
        entry: make lint
        language: system
        pass_filenames: false
```

Local pre-commit and the CI gate must run the **same** checks — divergence means "passes locally, fails in CI" (`principles-dry-kiss`: one definition of "clean").

### 6. Document the one path in

A short `README` / `CONTRIBUTING` section: prerequisites (just Docker + the task runner), the single bootstrap command, and the verb list. If setup takes more than one command and a paragraph to explain, simplify it.

## Boundaries

- **Local only.** This skill owns the dev loop, not production. Production provisioning, managed equivalents of these dependencies, and runtime config live in `cloud-infra`. Keep local versions matched to what `cloud-infra` provisions so local mirrors prod.
- **Test tiers** are defined by `principles-tdd`; this skill makes the dependencies those tiers need (Docker-backed integration/e2e) available locally and in CI — it does not redefine the tiers.
