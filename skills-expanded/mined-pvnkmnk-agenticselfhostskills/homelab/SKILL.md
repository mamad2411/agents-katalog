---
name: docker-app-deployer
description: Encodes safe Docker Compose deployment, env var management, update strategies, and rollback patterns.
category: homelab
tags: [homelab, docker, deployment, compose, containers]
agents: [opencode, freebuff, antigravity, codex]
---

# docker-app-deployer

## Purpose

Guides safe, repeatable Docker Compose deployments for homelab services.

## Invocation

**OpenCode / Codex:** `Invoke docker-app-deployer`
**Freebuff:** `/skill docker-app-deployer`

## Deployment Workflow

1. **Review compose file** — confirm images, volumes, networks, and env vars before deploying.
2. **Check .env file** — ensure all required variables are set; no secrets in compose.yml.
3. **Pull images first** — `docker compose pull` before `up` to avoid partial updates.
4. **Deploy** — `docker compose up -d` with `--remove-orphans` to clean stale containers.
5. **Verify** — check logs with `docker compose logs -f <service>`, confirm service is healthy.
6. **Log the change** — record in `homelab-logbook`.

## Update Strategy

- Use Watchtower in **notify-only** mode for production services; apply updates manually after reviewing changelogs.
- For non-critical services, scheduled Watchtower pulls are acceptable.
- Always `docker compose pull && docker compose up -d` rather than `docker pull` alone.

## Rollback

- Pin image tags in `compose.yml` (e.g., `image: navidrome/navidrome:0.52.0`) for rollback-safe deployments.
- Use `docker compose down && docker compose up -d` with the previous tag if a rollback is needed.
- Never use `latest` for production services.

## Safety Rules

- Never run `docker system prune` without explicit user confirmation.
- Never remove named volumes without user confirmation.
- Always check `docker compose ps` after deployment to confirm all services are `Up`.

## Companion Skills

- `homelab-safe-ops` — always active
- `media-stack-builder` — compose design patterns
- `reverse-proxy-and-tunnel` — networking for deployed services
- `homelab-logbook` — log every deployment
