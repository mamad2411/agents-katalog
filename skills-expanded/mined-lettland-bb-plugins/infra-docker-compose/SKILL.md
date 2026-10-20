---
name: infra-docker-compose
description: Use when defining multi-container apps with Docker Compose — services, healthchecks, restart policies, secrets, override files.
metadata:
  added: 2026-05-18
  last_reviewed: 2026-05-18
  type: domain
  status: active
  invokes_shell: false
  shell_reviewed: "valksor 2026-05-17"
  related: [infra-docker-swarm, ci-github-actions, observability-essentials]
  keywords: [production, prod, deploy, deployment]
---

# Infra Docker Compose

**Iron Law: NEVER `image: foo:latest` in prod. Every service has a healthcheck. Every service has a restart policy. Secrets via Docker secrets / a manager / `.env` (gitignored), NEVER inline in `environment:` — non-secret config in `environment:` is fine.**

**Base image default:** Debian (`*-slim`, `*-trixie-slim`, `distroless-debian`). Alpine only when image size dominates and you've verified musl-libc compat (cgo, glibc-only wheels, DNS resolver edge cases). Long-form rationale: `Skill(infra-docker-images)`.

## What Compose is (and isn't)

Compose is for: dev environments, small-fleet single-host deployments, integration testing. **Not for**: multi-host orchestration (use Swarm or k8s), zero-downtime deploys without effort, autoscaling.

## Skeleton (compose spec, no version key)

```yaml
# docker-compose.yml — the modern Compose spec drops the top-level `version:`
services:
  api:
    image: ghcr.io/me/api:v1.4.2 # NEVER :latest in prod
    restart: unless-stopped
    depends_on:
      db:
        condition: service_healthy # wait for healthcheck to pass
    environment:
      - LOG_LEVEL=info
    env_file: [.env] # gitignored
    secrets: [db_password]
    # /healthz MUST gate on app readiness, not just TCP listener-up. Minimum pattern in the handler:
    #   try: db.execute("SELECT 1"); assert migrations.current() == migrations.head(); return 200
    #   except: return 503
    # Otherwise dependents launch against a half-initialised app. For distroless images (no curl/wget),
    # add a `--healthcheck` flag to your binary and probe that instead, or move probes to the orchestrator.
    healthcheck:
      test: ["CMD", "curl", "-fsS", "http://localhost:8080/healthz"] # OK on non-distroless images that ship curl
      interval: 10s
      timeout: 3s
      retries: 3
      start_period: 20s
    networks: [appnet]
    ports: ["127.0.0.1:8080:8080"] # bind explicit interface, not 0.0.0.0
    deploy:
      resources:
        limits: { cpus: "1.0", memory: 512M }

  db:
    image: postgres:17 # Debian variant; -alpine only after musl/cgo audit
    restart: unless-stopped
    environment:
      POSTGRES_USER: app
      POSTGRES_DB: app
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
    secrets: [db_password]
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app -d app"]
      interval: 10s
      timeout: 5s
      retries: 5
    volumes:
      - dbdata:/var/lib/postgresql/data # named volume — survives recreation
    networks: [appnet]

volumes:
  dbdata:

networks:
  appnet:
    driver: bridge

secrets:
  db_password:
    file: ./secrets/db_password.txt # mode 0400, gitignored, mounted at /run/secrets/db_password
```

## Restart policy decision

| Policy           | When                                                                                 |
| ---------------- | ------------------------------------------------------------------------------------ |
| `no` (default)   | one-shot jobs, batch tasks                                                           |
| `on-failure[:N]` | recoverable errors only; bounded retries                                             |
| `always`         | restarts even after manual `docker stop` — usually wrong                             |
| `unless-stopped` | **default for long-lived services** — restarts on crash + boot, respects manual stop |

## Healthchecks — required

Every long-lived service needs one. Without it `depends_on: service_healthy` doesn't work, restart loops thrash, and orchestrators can't tell "starting" from "broken".

| Service     | Test                                                    |
| ----------- | ------------------------------------------------------- |
| HTTP app    | `curl -fsS http://localhost:PORT/healthz`               |
| Postgres    | `pg_isready -U user -d db`                              |
| Redis       | `redis-cli ping`                                        |
| Kafka       | `kafka-topics --bootstrap-server localhost:9092 --list` |
| Generic TCP | `nc -z localhost PORT`                                  |

Tune `start_period` for slow boots (Java apps, DB init) — failures during start_period don't count.

## Volumes — named, not bind, in prod

| Type                                   | Use                                                   |
| -------------------------------------- | ----------------------------------------------------- |
| **Named volume** (`dbdata:`)           | prod state — managed by Docker, survives `down`/`up`  |
| **Bind mount** (`./src:/app`)          | dev hot-reload only — host-path-coupled, breaks in CI |
| **tmpfs** (`type: tmpfs`)              | scratch, secret-ish in-memory data                    |
| **External volume** (`external: true`) | volume managed outside this Compose file              |

`docker compose down -v` deletes named volumes — destructive, gate it.

## Secrets — never `environment:`

Compose v2 reads `secrets:` entries and mounts them at `/run/secrets/<name>` as files (mode 0400). Your app reads from file, not env. For real production move to AWS Secrets Manager / Vault / SOPS; for dev a gitignored `./secrets/` directory is fine.

`environment: { DB_PASSWORD: xyz }` leaks to `docker inspect`, container env, child processes, and crash logs. Use secrets or `env_file:` with a gitignored file.

## Multi-file overrides

```bash
# Base + prod overlay
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

```yaml
# docker-compose.prod.yml — overrides + additions only
services:
  api:
    image: ghcr.io/me/api:v1.4.2
    deploy:
      { replicas: 3 } # NOTE: `deploy.replicas` is honored ONLY by Swarm (docker stack deploy),
      # silently ignored by plain `docker compose up`. For single-host Compose,
      # use `docker compose up --scale api=3` from CLI instead.
    logging: { driver: json-file, options: { max-size: "10m", max-file: "5" } }
```

Compose auto-merges. Common split: `compose.yml` (base) + `compose.override.yml` (dev, auto-loaded) + `compose.prod.yml` (explicit `-f`).

## Profiles — env-conditional services

```yaml
services:
  worker:
    profiles: [worker] # only starts with --profile worker
  mailhog:
    profiles: [dev]
```

`docker compose --profile dev up` brings up dev-only services (mailhog, minio, otel-collector); prod compose call omits the profile.

## depends_on conditions

```yaml
depends_on:
  db: { condition: service_healthy }
  cache: { condition: service_started }
  migrate: { condition: service_completed_successfully } # one-shot job
```

Without `condition:`, `depends_on` only waits for the container to _start_, not for the app inside it to be ready. Always use healthchecks.

## Anti-patterns

- `image: foo:latest` in any non-local file — non-reproducible; pin to digest in highest-stakes envs
- Missing healthcheck — restart loops thrash, dependents start too early
- Secrets in `environment:` — leak via `docker inspect`, logs, child procs
- `ports: ["8080:8080"]` bound to `0.0.0.0` on a server with public IPs — exposed without firewall
- `restart: always` everywhere — masks crash loops; you wanted `unless-stopped`
- `depends_on: [db]` without `condition:` — race condition on startup
- Bind-mounting source dirs in prod — host path coupling, perms drift
- No resource limits — one runaway service starves the host
- One `compose.yml` doing dev + prod via env-var ifs — split with override files
- Forgetting `--remove-orphans` — leftover containers from removed services

## Red flags

| Thought                                       | Reality                                                                            |
| --------------------------------------------- | ---------------------------------------------------------------------------------- |
| "It works locally"                            | Local has bind mounts + `:latest`; prod doesn't — test the prod compose explicitly |
| "We'll add healthchecks later"                | First flaky deploy = retrofit in the middle of an incident                         |
| "Just put the password in env, it's internal" | `docker inspect` exposes env to anyone with daemon access                          |
| "Compose is fine for our 10-host fleet"       | At 3+ hosts: Swarm. At 10+: k8s or Nomad.                                          |

## Hand-off

For multi-host orchestration (overlay networks, secrets, replicas): `Skill(infra-docker-swarm)`. For metrics/logging/tracing on these services: `Skill(observability-essentials)`. For CI building + pushing images: `Skill(ci-github-actions)`.
