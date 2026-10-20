---
name: dind-compose-setup
description: Set up Docker-in-Docker (on Podman or Docker) with docker-compose.yml orchestration, CA cert injection, docker cp source seeding, tiered rebuild strategy, and test-runner infrastructure. Consolidates dind-on-podman + docker-dind-compose-setup.
version: 1
created: 2026-05-20
updated: 2026-05-20
---
# Docker-in-Docker Compose Setup

## When to Use
When building a Docker Compose microservices environment that runs inside a DinD container, where the host may use Podman or Docker. Covers the full setup: DinD container management, source code seeding, CA certificate injection, compose orchestration, and test infrastructure.

## Procedure

### 1. Start DinD as a sibling container

Start with no port mapping (Podman already uses port 2375). Access DinD via `docker exec`, not TCP:

```bash
docker run -d --name myproject-dind --privileged \
  -p 16686:16686 -p 3000:3000 -p 8080:8080 \
  -e DOCKER_TLS_CERTDIR="" \
  docker:dind
```

**Do NOT use `-p 2375:2375`** — Podman already binds port 2375 on the host. Even on Docker hosts, avoid exposing the Docker API socket directly.

**Port forwarding**: Expose only the ports needed from the host (Jaeger 16686, Grafana 3000, demo UI 8080). Internal service-to-service communication stays within the compose network. See `dind-port-forwarding` for the full 3-layer pattern.

### 2. Inject CA certificates before pulling images

If behind a corporate proxy or WARP, install CA certs BEFORE any `docker compose build`:

```bash
docker cp /path/to/cert.pem myproject-dind:/usr/local/share/ca-certificates/custom-ca.crt
docker exec myproject-dind update-ca-certificates
```

Make this idempotent — check if the cert already exists before copying:

```bash
_inject_ca() {
  local cert_name="custom-ca.crt"
  if ! docker exec "$DIND_NAME" test -f "/usr/local/share/ca-certificates/$cert_name" 2>/dev/null; then
    docker cp "$CERT_PATH" "$DIND_NAME:/usr/local/share/ca-certificates/$cert_name"
    docker exec "$DIND_NAME" update-ca-certificates
  fi
}
```

**Why before build**: If images pull base layers from a registry behind a MITM proxy, they need the CA cert at pull time. Rebaking images after CA install requires `docker compose down` + `docker compose up --build` to invalidate cached layers.

### 3. Seed source code via docker cp (not volume mounts)

Podman can't resolve virtiofs paths from inside the tooling container. Always use `docker cp`:

```bash
# CRITICAL: trailing /. copies CONTENTS flattened, not nested
docker cp "$PROJECT_DIR/." myproject-dind:/workspace/
# Result: /workspace/docker-compose.yml (NOT /workspace/myproject/...)

# Without trailing /., it nests:
docker cp "$PROJECT_DIR" myproject-dind:/workspace/
# Result: /workspace/myproject/docker-compose.yml
```

**Volume mounts** (Docker host only, not Podman): If your host runs native Docker, you CAN use bind mounts in compose. Use `./path` (relative to the compose file), NOT `../path`. DinD resolves volumes relative to the mounted `/workspace` directory.

### 4. Run compose inside DinD

All compose commands run via docker exec targeting the inner daemon:

```bash
docker exec myproject-dind docker compose -f /workspace/docker-compose.yml up -d --build
```

**Dockerfile COPY paths**: Build context is `.` = `/workspace/` (the compose directory). Use:
```dockerfile
COPY common/pyproject.toml /app/common/
COPY services/my-service/ /app/
```

Shell variables do NOT expand in Dockerfile COPY — hardcode service names per Dockerfile.

**Static IP allocation**: Docker assigns `.1` as the gateway on each bridge network. Never use `.1` as a static container IP. Use `.10+` for static assignments.

### 5. Pre-install dependencies

Add all shared Python packages to the tooling Dockerfile's pip install line. Services inside DinD have their own Dockerfiles with per-service pip installs. This ensures container rebuilds don't lose packages.

### 6. Set up test-runner and infra services

**Test runner**: A dedicated container inside the compose network that spans all network segments. Runs tests via `docker exec test-runner pytest`. See `compose-test-runner-container` for full setup.

**Infra setup service**: If using a Python script for dynamic infra config (Toxiproxy, etc.), create a dedicated Dockerfile that pip-installs dependencies before COPYing the script.

### 7. Tiered rebuild strategy

Structure your bootstrap script with three distinct command depths (see `compose-bootstrap-cli` for full implementation):

| Command  | DinD Check | CA Certs | Source Copy | Image Build | Verify Gate | Use Case |
|----------|-----------|----------|-------------|-------------|-------------|----------|
| `up`     | ✅ create  | ✅ yes   | ✅ yes      | ✅ yes      | ✅ yes      | First run, DinD recreated |
| `rebuild`| ✅ ensure  | ❌ skip  | ✅ yes      | ✅ yes      | ✅ yes      | Code/Dockerfile changes |
| `restart`| ✅ ensure  | ❌ skip  | ❌ skip     | ❌ skip     | ❌ skip     | Config/env var changes only |

### 8. Clean stale networks between restarts

```bash
docker exec myproject-dind docker network prune -f
```

Stale IP allocations cause "address already in use" errors on restart.

## Pitfalls
- **`docker cp` trailing slash**: `docker cp src/. dind:/workspace/` copies contents flat into /workspace/. Without `/.`, it creates a subdirectory. This is the #1 gotcha.
- **Port 2375 conflict**: Podman already uses 2375 for its own daemon. Never expose DinD on this port.
- **CA cert timing**: Must be injected BEFORE pulling images from ghcr.io or other registries behind MITM proxies.
- **Shell variables in Dockerfile**: COPY doesn't expand `${VAR}`. Use hardcoded service names per Dockerfile.
- **Compose `version` key is obsolete**: Remove `version: "3.8"` to avoid deprecation warnings in Compose v2+.
- **Stale networks**: Always prune networks between compose restarts. Static IP allocations persist across `docker compose down`.
- **No volume mounts in Podman**: Podman can't resolve virtiofs paths from inside a tooling container. Always `docker cp`.

## Verification
1. `docker exec dind docker info` — DinD daemon is healthy
2. `docker exec dind docker compose -f /workspace/docker-compose.yml config` — compose validates
3. `docker exec dind docker compose -f /workspace/docker-compose.yml ps` — all services running
4. `docker exec dind docker compose -f /workspace/docker-compose.yml up -d --build` — builds succeed