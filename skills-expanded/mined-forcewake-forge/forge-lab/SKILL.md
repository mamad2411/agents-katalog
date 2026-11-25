---
name: forge-lab
description: Bring up or restart the local forge lab stack (postgres, redis, litellm, app, worker) in podman, rebuild the image after code changes, and verify health. Use for integration testing against a real GitLab CE.
---

# forge-lab: podman lab stack

Prerequisites: podman; a `.env` in the repo root with `GITLAB_URL`,
`GITLAB_TOKEN`, `GITLAB_WEBHOOK_SECRET`, `FORGE_BOT_USERNAME`,
`FORGE_BOT_TOKEN`, `FORGE_APPROVERS`, `FORGE_IMPLEMENTER_BACKEND`,
`FORGE_HARNESS_MODEL`, `ZAI_API_KEY`; a `litellm-config.yaml` (tiers
fast/strong/code against the model provider).

## Services (idempotent)

```bash
podman run -d --name forge-postgres -p 127.0.0.1:5433:5432 \
  -e POSTGRES_USER=forge -e POSTGRES_PASSWORD=forge -e POSTGRES_DB=forge \
  docker.io/library/postgres:17-alpine
podman run -d --name forge-redis -p 6379:6379 docker.io/library/redis:7-alpine
podman run -d --name forge-litellm -p 127.0.0.1:4000:4000 --env-file .env \
  -v "$PWD/litellm-config.yaml:/app/config.yaml:Z" \
  docker.io/litellm/litellm:main-stable --config /app/config.yaml --port 4000
```

## Rebuild image after code changes

```bash
printf 'FROM localhost/forge:dev\nCOPY --chown=forge:forge src /app/src\n' > /tmp/f.Containerfile
podman build -t localhost/forge:dev -f /tmp/f.Containerfile .
```

## App + worker (recreate with explicit -e; never --env-file — URLs differ)

Containers reach host-published services via `host.containers.internal`, so:
`DATABASE_URL=postgresql+asyncpg://forge:forge@host.containers.internal:5433/forge`,
`REDIS_URL=redis://host.containers.internal:6379/0`,
`LITELLM_URL=http://host.containers.internal:4000`. Pass every `FORGE_*`
and `GITLAB*` variable from `.env` with explicit `-e` flags (see git history
for the exact working command). App: `-p 8420:8420 -v "$PWD/data:/app/data"`
running `uv run uvicorn forge.main:app --host 0.0.0.0 --port 8420`; worker:
`python -m forge.worker` (the image CMD is the WEB APP — a worker container
created without the command override silently becomes a second useless web
server; LIVE-found 2026-09-17). **The worker MUST mount
`-v "$PWD/.secrets:/app/.secrets"`** — `FORGE_GITHUB_PRIVATE_KEY` is a PATH
to the GitHub App PEM; without the mount every GitHub call dies with
`InvalidKeyError: Could not parse the provided public key` and steps go
dead (LIVE-found 2026-09-17). The app mounts data (webhook captures) and
.secrets too.

## Verify

- `curl -s localhost:8420/metrics` → `workers_active >= 1`, `queue_depth`.
- `podman exec forge-worker uv run python -m forge.doctor` → exit 0.
  (Rebuild the image first or the container lacks new modules.)
- E2E: comment `/implement` on a lab issue as an approver → forge posts a
  plan → reply `@forge /go <run-id>` → watch the run reach
  `ready_for_human`.

## Notes

- podman machine: host.containers.internal = the Mac host; published ports
  are LAN-reachable (macOS firewall blocks direct Python listeners, not
  podman publishes).
- Do not use docker; do not run the docker executor inside podman (dead
  end). CI jobs run on the user's GitLab runner (unraid docker executor).
