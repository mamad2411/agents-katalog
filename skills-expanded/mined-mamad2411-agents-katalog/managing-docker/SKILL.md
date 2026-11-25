---
name: managing-docker
description: |
  Use when working with Docker — docker container lifecycle and image
  management. Covers container operations, image builds, volume/network
  inspection, Docker Compose orchestration, resource usage monitoring, and
  registry management. Use when managing containers, debugging container issues,
  inspecting images, or orchestrating multi-container applications.
connection_type: docker
preload: false
---

# Docker Management Skill

Manage Docker containers, images, volumes, networks, and Compose stacks.

## Core Helper Functions

```bash
#!/bin/bash

# Docker command wrapper with error handling
docker_cmd() {
    docker "$@" 2>/dev/null || echo "ERROR: docker $1 failed"
}

# Format docker output as compact JSON
docker_json() {
    docker "$@" --format '{{json .}}' 2>/dev/null | jq -s '.'
}

# Docker API helper (for remote Docker hosts)
docker_api() {
    local endpoint="$1"
    curl -s --unix-socket /var/run/docker.sock "http://localhost${endpoint}"
}
```

## MANDATORY: Discovery-First Pattern

**Always inspect host and running containers before performing operations.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Docker Host Info ==="
docker info --format '{{json .}}' 2>/dev/null | jq '{
    server_version: .ServerVersion,
    os: .OperatingSystem,
    arch: .Architecture,
    cpus: .NCPU,
    memory_gb: (.MemTotal / 1073741824 | floor),
    containers: {total: .Containers, running: .ContainersRunning, stopped: .ContainersStopped},
    images: .Images,
    storage_driver: .Driver
}'

echo ""
echo "=== Running Containers ==="
docker ps --format '{{.ID}}\t{{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}' | column -t | head -30

echo ""
echo "=== Disk Usage Summary ==="
docker system df --format 'table {{.Type}}\t{{.TotalCount}}\t{{.Size}}\t{{.Reclaimable}}' 2>/dev/null
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Use `--format` with Go templates or `--format '{{json .}}'` with jq
- Never dump full `docker inspect` output -- extract key fields

## Common Operations

### Container Lifecycle Dashboard

```bash
#!/bin/bash
echo "=== All Containers (running + stopped) ==="
docker ps -a --format '{{json .}}' | jq -s '
    {
        total: length,
        running: [.[] | select(.State == "running")] | length,
        exited: [.[] | select(.State == "exited")] | length,
        restarting: [.[] | select(.State == "restarting")] | length
    }'

echo ""
echo "=== Resource Usage (running containers) ==="
docker stats --no-stream --format '{{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}\t{{.BlockIO}}' \
    | column -t | head -20

echo ""
echo "=== Containers With Restart Issues ==="
docker ps -a --filter "status=restarting" --format '{{.Names}}\t{{.Image}}\t{{.Status}}' | column -t
docker ps -a --format '{{json .}}' | jq -r 'select(.Status | test("Restarting|Exited \\(1")) | "\(.Names)\t\(.Image)\t\(.Status)"' | head -10
```

### Container Inspection & Debugging

```bash
#!/bin/bash
CONTAINER="${1:?Container name or ID required}"

echo "=== Container Details: $CONTAINER ==="
docker inspect "$CONTAINER" | jq '.[0] | {
    id: .Id[0:12],
    name: .Name,
    image: .Config.Image,
    state: .State.Status,
    started_at: .State.StartedAt,
    restart_count: .RestartCount,
    pid: .State.Pid,
    ports: .NetworkSettings.Ports,
    env_count: (.Config.Env | length),
    mounts: [.Mounts[] | {source: .Source, destination: .Destination, rw: .RW}],
    networks: [.NetworkSettings.Networks | keys[]]
}'

echo ""
echo "=== Recent Logs (last 50 lines) ==="
docker logs "$CONTAINER" --tail 50 --timestamps 2>&1 | tail -20

echo ""
echo "=== Health Check Status ==="
docker inspect "$CONTAINER" | jq '.[0].State.Health // "No health check configured"'
```

### Image Management

```bash
#!/bin/bash
echo "=== Local Images (sorted by size) ==="
docker images --format '{{.Repository}}:{{.Tag}}\t{{.Size}}\t{{.ID}}\t{{.CreatedSince}}' \
    | sort -k2 -h -r | column -t | head -20

echo ""
echo "=== Dangling Images ==="
docker images -f "dangling=true" --format '{{.ID}}\t{{.Size}}\t{{.CreatedSince}}' | column -t

echo ""
echo "=== Image Layer Analysis ==="
IMAGE="${1:-}"
if [ -n "$IMAGE" ]; then
    docker history "$IMAGE" --format '{{.CreatedBy}}\t{{.Size}}' --no-trunc | head -15
fi
```

### Volume & Network Inspection

```bash
#!/bin/bash
echo "=== Volumes ==="
docker volume ls --format '{{.Name}}\t{{.Driver}}\t{{.Mountpoint}}' | column -t | head -20

echo ""
echo "=== Unused Volumes ==="
docker volume ls -f "dangling=true" --format '{{.Name}}\t{{.Driver}}' | column -t

echo ""
echo "=== Networks ==="
docker network ls --format '{{.Name}}\t{{.Driver}}\t{{.Scope}}\t{{.ID}}' | column -t

echo ""
echo "=== Network Details ==="
for net in $(docker network ls --format '{{.Name}}' | grep -v "bridge\|host\|none"); do
    echo "--- $net ---"
    docker network inspect "$net" | jq '.[0] | {
        name: .Name,
        driver: .Driver,
        subnet: .IPAM.Config[0].Subnet,
        containers: [.Containers | to_entries[] | .value.Name]
    }'
done
```

### Docker Compose Operations

```bash
#!/bin/bash
COMPOSE_DIR="${1:-.}"

echo "=== Compose Services Status ==="
docker compose -f "${COMPOSE_DIR}/docker-compose.yml" ps --format json 2>/dev/null \
    | jq -s '.[] | "\(.Name)\t\(.State)\t\(.Health)\t\(.Ports)"' | column -t

echo ""
echo "=== Compose Config Validation ==="
docker compose -f "${COMPOSE_DIR}/docker-compose.yml" config --quiet 2>&1 \
    && echo "Config: VALID" || echo "Config: INVALID"

echo ""
echo "=== Service Dependencies ==="
docker compose -f "${COMPOSE_DIR}/docker-compose.yml" config --format json 2>/dev/null \
    | jq '.services | to_entries[] | {name: .key, depends_on: (.value.depends_on // {} | keys), ports: .value.ports}'

echo ""
echo "=== Compose Logs (last errors) ==="
docker compose -f "${COMPOSE_DIR}/docker-compose.yml" logs --tail 20 --no-color 2>/dev/null \
    | grep -i "error\|fatal\|exception\|fail" | tail -15
```

## Safety Rules
- **Read-only by default**: Only use `docker inspect`, `docker ps`, `docker logs`, `docker stats`
- **Never run** `docker rm`, `docker rmi`, `docker system prune` without explicit user confirmation
- **Never expose** environment variables containing secrets from `docker inspect`
- **Log limits**: Always use `--tail` to prevent unbounded log output

## Output Format

Present results as a structured report:
```
Managing Docker Report
══════════════════════
Resources discovered: [count]

Resource       Status    Key Metric    Issues
──────────────────────────────────────────────
[name]         [ok/warn] [value]       [findings]

Summary: [total] resources | [ok] healthy | [warn] warnings | [crit] critical
Action Items: [list of prioritized findings]
```

Target ≤50 lines of output. Use tables for multi-resource comparisons.

## Anti-Hallucination Rules

1. **NEVER assume resource names** — always discover via CLI/API in Phase 1 before referencing in Phase 2.
2. **NEVER fabricate metric names or dimensions** — verify against the service documentation or `--help` output.
3. **NEVER mix CLI commands between service versions** — confirm which version/API you are targeting.
4. **ALWAYS use the discovery → verify → analyze chain** — every resource referenced must have been discovered first.
5. **ALWAYS handle empty results gracefully** — an empty response is valid data, not an error to retry.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |

## Common Pitfalls
- **Dangling images accumulate**: Use `docker image prune` periodically but confirm first
- **Volume data loss**: `docker rm -v` deletes anonymous volumes -- warn before removing containers
- **Network DNS**: Containers on custom networks resolve by name; default bridge does not
- **Compose v1 vs v2**: `docker-compose` (v1) vs `docker compose` (v2) -- check which is installed
- **Build cache bloat**: Multi-stage builds leave intermediate layers -- use `--squash` or BuildKit
