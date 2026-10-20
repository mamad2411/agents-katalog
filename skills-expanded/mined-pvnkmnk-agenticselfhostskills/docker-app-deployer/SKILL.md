---
name: docker-app-deployer
description: Deploys Docker and Docker Compose applications to homelab hosts with configuration management and health verification.
---

# docker-app-deployer

Handles the end-to-end deployment of Docker and Docker Compose applications to homelab hosts. Manages image pulls, environment variable injection, volume mapping, network attachment, and post-deploy health checks. Always operates within `homelab-safe-ops` constraints.

## Invocation

**OpenCode / Codex:** `Invoke docker-app-deployer`
**Freebuff:** `/skill docker-app-deployer`

## Workflow Steps

1. **Pre-flight:** Run `homelab-safe-ops` check; confirm target host and disk space.
2. **Prepare:** Create or validate docker-compose.yml / Dockerfile.
3. **Configure:** Set environment variables from `.env` or secret manager (never hardcode).
4. **Pull:** `docker pull` or `docker compose pull` image(s).
5. **Deploy:** `docker compose up -d` or equivalent.
6. **Health check:** Verify container is running; check logs for errors.
7. **Expose:** If needed, invoke `reverse-proxy-and-tunnel` to configure access.
8. **Log:** Record deployment in `homelab-logbook`.

## Safety

- Never hardcode credentials in compose files.
- Always map named volumes; never use anonymous volumes for persistent data.
- Do not expose ports directly to the internet; use reverse proxy or tunnel.
- Confirm backup exists before replacing a running container with persistent state.

## Companion Skills

- `homelab-safe-ops` — safety gate
- `reverse-proxy-and-tunnel` — configure access
- `homelab-logbook` — log deployments
- `homelab-monitoring-analyst` — monitor after deploy

## References

- Docker Compose docs: https://docs.docker.com/compose/
- Portainer: https://docs.portainer.io/
