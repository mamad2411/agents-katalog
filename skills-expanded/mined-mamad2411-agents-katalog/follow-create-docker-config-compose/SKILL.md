---
name: follow-create-docker-config-compose
description: Create docker-compose for multi-service — networks, volumes, healthchecks, profiles
argument-hint: "[services]"
related:
  - follow-create-docker
  - follow-secret-manager
  - ask-me
---

## Goal

Create a `docker-compose.yml` for a multi-service stack — with correct networks, volumes, healthcheck dependencies, and env wiring

## Scope

- Covers compose for dev and production profiles
- Each service's Dockerfile → `workflows/setup-dockerfile`

## Execute

### 1. Inventory Services

> Goal: know all services and their dependencies

1. List services from the architecture — app, db, cache, queue, proxy
2. Define depends_on with `condition: service_healthy`
3. Split dev vs prod profiles (`profiles:`)

### 2. Write Compose

> Goal: a complete and reproducible compose file

1. Split networks into frontend/backend per the boundary
2. Named volumes for stateful services
3. Env via `env_file` or `${VAR}` — never hardcode secrets
4. Healthcheck every long-running service

### 3. Verify

> Goal: the full stack comes up

1. `docker compose config` validation passes
2. After `docker compose up -d`, every service is healthy

## Rules

- Secrets must come from env/`/follow-secret-manager` — never commit real values
- Pin image versions — never `latest`

## Expected Outcome

- `docker-compose.yml` + env example ready for dev/prod use
