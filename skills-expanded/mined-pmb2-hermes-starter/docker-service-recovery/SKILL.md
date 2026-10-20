---

name: docker-service-recovery
description: "Techniques for recreating/replacing a single docker-compose service container while keeping the rest of the stack running, with Windows/Git-Bash-specific path fixes."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [docker, compose, recovery, container, traefik, windows, troubleshooting]
    triggers: [docker compose up fails, container recreation, single-service replace, broken docker service, docker run instead of compose, docker entrypoint override, MSYS path translation, docker network not found, traefik routing not working]
    related_skills: [vps-application-deployment, infrastructure-self-healing-pulse]
---
# Docker Service Recovery

## When to Use

When a `docker compose up -d <service>` fails due to dependency chain issues (missing env vars, service-not-found, depends-on failures) and you need to replace just one service while keeping the rest of the stack intact.

## Core Pattern

Stop → Remove → Recreate with `docker run`, replicating the compose service's networks, volumes, labels, and env vars:

```bash
docker stop <name>
docker rm <name>
export MSYS_NO_PATHCONV=1   # REQUIRED on Windows Git Bash
docker run -d \
  --name <name> \
  --network <compose-network-1> \
  --network <proxy-network> \
  --restart unless-stopped \
  --entrypoint /bin/sh \
  -v "host/path:/container/path:ro" \
  -l "com.docker.compose.project=<project>" \
  -l "com.docker.compose.service=<service>" \
  -l "traefik.enable=true" \
  -l "traefik.docker.network=<traefik-network>" \
  -l "traefik.http.routers.<name>.rule=Host(\`<domain>\`)" \
  -l "traefik.http.routers.<name>.tls=true" \
  -l "traefik.http.routers.<name>.tls.certresolver=<resolver>" \
  -l "traefik.http.services.<name>.loadbalancer.server.port=<port>" \
  -e "KEY=VALUE" \
  --network-alias <hostname> \
  <image> \
  <entrypoint-script> <command>
```

## Step-by-Step

### 1. Inspect the Existing Container
Capture all the config you need to replicate:

```bash
# Environment variables
docker inspect <name> --format '{{range .Config.Env}}{{println .}}{{end}}'

# Networks
docker inspect <name> --format '{{range $net, $conf := .NetworkSettings.Networks}}{{$net}} {{end}}'

# Labels (especially Traefik routing labels)
docker inspect <name> --format '{{range $k, $v := .Config.Labels}}{{$k}}={{$v}}{{"\n"}}{{end}}'

# Volume mounts
docker inspect <name> --format '{{json .Mounts}}'
```

### 2. Find the Correct Networks
The container must be on the SAME network as the reverse proxy (Traefik):

```bash
# What networks is Traefik on?
docker inspect traefik --format '{{range $net, $conf := .NetworkSettings.Networks}}{{$net}} {{end}}'

# What networks are other running services from the same compose on?
docker inspect <sibling-service> --format '{{range $net, $conf := .NetworkSettings.Networks}}{{$net}} {{end}}'
```

**Key insight:** The container needs to be on BOTH:
- The compose internal network (for DB/Redis access)
- The proxy network (so Traefik can route to it)

Attach to both with multiple `--network` flags. Each flag attaches in addition to the previous ones.

### 3. Handle the Entrypoint
Docker images have a built-in `ENTRYPOINT`. The compose file may override it. To replicate the compose's entrypoint:

```bash
# If compose has only command (no entrypoint override):
--entrypoint /bin/sh
<image>
<entrypoint-script> <cmd>

# The entrypoint script receives the command via "$@" and executes it
```

**Finding the compose entrypoint/command:** Look in the compose.yaml for the service definition:
```yaml
entrypoint:
  - /bin/sh
  - /opt/custom-entrypoint.sh
command:
  - node
  - dist/main
```

This becomes: `docker run --entrypoint /bin/sh ... image /opt/custom-entrypoint.sh node dist/main`

### 4. Verify
```bash
sleep 20 && docker logs --tail=10 <name>
docker logs <name> 2>&1 | grep -iE "error|WARN|invalid|exception" | head -10
curl -sk https://<domain>/healthz
```

## Windows / Git-Bash Specifics

### MSYS_NO_PATHCONV (Critical)
Git Bash translates Unix paths like `/bin/sh` to Windows paths (`C:/Program Files/Git/usr/bin/sh`), which don't exist in the Linux container. This causes:

```
exec: "C:/Program Files/Git/usr/bin/sh": stat C:/Program Files/Git/usr/bin/sh: no such file or directory
```

**Fix:** Export before any `docker run` with Unix paths:
```bash
export MSYS_NO_PATHCONV=1
```

### Volume Paths on Windows
```bash
-v "E:/Path/to/file:/container/path:ro"     # Quoted forward-slash — works
-v /e/Path/to/file:/container/path:ro       # MSYS path — works but MSYS_NO_PATHCONV still needed
```

### Container Name Conflicts
If a partial `docker run` fails, the container might still exist with error status. Remove it before retrying:
```bash
docker rm <container-id>   # by ID since same name is blocked
```

## Pitfalls

- **Entrypoint vs Command confusion**: `--entrypoint` replaces the image's ENTRYPOINT. Positional args after the image name become CMD. If the image ENTRYPOINT runs a script that calls `"$@"`, your positional args become that script's arguments.
- **Missing volume mounts**: If the compose mounts scripts/configs not in the image, you MUST mount them or the container won't have them.
- **Network aliases**: If other services resolve this container by hostname (e.g. `postgres`, `redis`), use `--network-alias <name>`.
- **Labels don't persist**: Traefik labels MUST be passed on `docker run`. The old container's labels don't carry over.
- **Health endpoint unreachable**: If the health check works inside the container but not from outside, check Traefik network attachment and label correctness.
- **Docker compose --force-recreate limitations**: When `docker compose up -d <service>` fails on dependency resolution (`depends_on` pointing to undefined services), you can't use compose at all — `docker run` is the only path.

## Detection: Post-Restart Silent Exit Pattern

**Containers can silently exit (137) after a Docker daemon restart and stay dead until discovered by a pulse check.** This is NOT covered by `docker compose` recovery — the container ran standalone, died during daemon restart, and Docker's recovery-thaw missed it.

**Fix:** After any known or suspected Docker restart, run:

```bash
docker ps -a --filter "status=exited" \
  --format "{{.Names}}\t{{.Status}}" | grep -E "137"
```

If found, `docker start <name>` recovers the container with its original config intact — lowest-risk recovery path.

See `references/docker-post-restart-exit-detection.md` for exit code semantics, full census pattern, and the concrete plane-mcp case study.
