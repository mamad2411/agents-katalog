---
name: docker-smoke-test-loop
description: Run a one-shot docker container, tail its logs for a readiness sentinel, then fire an integration test against the exposed port - with layered fallbacks when the CLI is unavailable.
category: devops
version: 1.0.0
version_origin: extracted
tags: [docker, smoke-test, ci, readiness-probe]
confidence: medium
source_type: extracted-from-git
source_url: https://github.com/lukilabs/craft-agents-oss.git
source_ref: main
source_commit: 61f7d48a5b4fd0a8094f002c9e3aea5f3824dcfb
source_project: craft-agents-oss
source_path: scripts/docker-smoke-test.sh
imported_at: 2026-04-18T00:00:00Z
---

# Docker smoke-test loop

## When to use
- CI needs to verify a freshly built image actually boots and accepts connections.
- You have a sentinel line your server prints on ready (e.g. `CRAFT_SERVER_URL=...`).
- Want cleanup guaranteed even on failure.
- Different CI environments have different tooling (sometimes no CLI, no node, no nc).

## How it works
1. **Deterministic container name + token**: `CONTAINER_NAME="craft-smoke-$$"` (PID of the script, avoids collisions when tests run in parallel), `TOKEN="smoke-test-$(openssl rand -hex 16)"`.
2. **Cleanup trap before anything else**:
   ```sh
   cleanup() { docker logs "$CONTAINER_NAME" 2>/dev/null || true; docker rm -f "$CONTAINER_NAME" 2>/dev/null || true; }
   trap cleanup EXIT
   ```
   Guarantees logs flush to CI output and container is removed even if the script exits abnormally. The `|| true` swallows errors when the container never got created.
3. **Run the container detached**: `docker run -d --name ... -p PORT:9100 -e TOKEN ...`.
4. **Readiness loop** polls two conditions each second:
   - Still running? `docker inspect -f '{{.State.Running}}' "$CONTAINER_NAME"` - if no, dump logs and exit 1 immediately.
   - Ready? `docker logs "$CONTAINER_NAME" 2>&1 | grep -q "CRAFT_SERVER_URL="` - match the server's own stdout signal.
   Timeout defaults to 30s via `SMOKE_TEST_TIMEOUT` env.
5. **Layered test invocation**:
   - If `bun` + `apps/cli/src/index.ts` exist, run the real CLI validator.
   - Else try a tiny node-based WebSocket ping: `new WebSocket(url, { headers: { 'x-craft-token': TOKEN }})`.
   - Else just `nc -z 127.0.0.1 $PORT` to confirm the port is listening.
   - Else warn but don't fail - container-is-running counts as a weak smoke signal.

## Example
```bash
#!/usr/bin/env bash
set -euo pipefail
IMAGE="${1:?Usage: smoke.sh <image>}"
CONTAINER="smoke-$$"
TOKEN="$(openssl rand -hex 16)"
trap 'docker logs "$CONTAINER" 2>/dev/null || true; docker rm -f "$CONTAINER" 2>/dev/null || true' EXIT

docker run -d --name "$CONTAINER" -p 9100:9100 -e "TOKEN=$TOKEN" "$IMAGE"

for _ in $(seq 30); do
  docker inspect -f '{{.State.Running}}' "$CONTAINER" | grep -q true || { docker logs "$CONTAINER"; exit 1; }
  docker logs "$CONTAINER" 2>&1 | grep -q "SERVER_URL=" && break
  sleep 1
done

nc -z 127.0.0.1 9100 && echo OK
```

## Gotchas
- `docker logs | grep` is cheap but re-reads the whole log each iteration. Fine for small outputs, not for logs-per-second servers.
- The readiness sentinel must be on **stdout** or **stderr** and flushed promptly - buffered output breaks the probe.
- `trap ... EXIT` fires on normal exit AND signals; combined with `set -e` it's the cleanest cleanup pattern.
- Use `$$` not `$RANDOM` for the container name in CI - deterministic per test-runner PID makes debugging easier.
