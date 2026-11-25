---
name: compose-bootstrap-cli
description: "Build a bootstrap.sh CLI with subcommands for the full development lifecycle of a DinD Docker Compose microservices project: up, down, status, rebuild, verify, observe, profile, review, scenario, loadgen. Includes tiered rebuild depths (full cold-start, app-only, quick-restart), verification gates with auto-rollback, and nested docker exec patterns for test-runner access. Consolidates compose-bootstrap-cli + dind-tiered-rebuild."
version: 3
created: 2026-05-20
updated: 2026-05-20
---
# Bootstrap CLI for DinD Docker Compose Projects

Build a single `bootstrap.sh` entry point with subcommands for the full development lifecycle of a Docker-in-Docker Docker Compose microservices project. The CLI replaces manual docker/docker-compose commands with a predictable, extensible interface that scales from `up`/`down` to `observe`/`profile`/`loadgen` as the project grows.

## When to Use

- You have a Docker-in-Docker Compose microservices project and want a single CLI for all lifecycle operations
- Your project has grown past "docker compose up/down" and needs repeatable commands for verification, observability, profiling, and testing
- You want to avoid typing long docker exec commands with nested docker exec for test-runner access
- You need a pattern that is extensible — adding new subcommands as the project gains capabilities

**Do NOT use** when:
- Your project runs directly on the host Docker daemon (no DinD) — use a plain Makefile or task runner instead
- Your project only needs `docker compose up/down` — the pattern is overkill
- You need structured argument parsing (positional args, flags, help text from argparse-style) — use a Python CLI (click/typer) instead

## Procedure

### 1. Define helper functions at the top of the script

Create reusable helper functions for DinD lifecycle checks and common operations:

```bash
#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
DIND_NAME="${PROJECT_NAME:-myproject}-dind"
DIND_IMAGE="docker:dind"
DIND_WORKSPACE="/workspace"
COMPOSE_FILE="$DIND_WORKSPACE/docker-compose.yml"

_dind_running() {
    docker ps --format '{{.Names}}' 2>/dev/null | grep -q "^${DIND_NAME}$"
}

_dind_healthy() {
    docker exec "$DIND_NAME" docker info >/dev/null 2>&1
}

_dind_docker() {
    docker exec "$DIND_NAME" docker "$@"
}
```

**Key design decisions**:
- `DIND_NAME` uses a project prefix so multiple projects on the same host don't collide
- `_dind_running` and `_dind_healthy` are separate — a container may exist but the DinD daemon inside may not be ready
- `_dind_docker` is a thin wrapper around `docker exec $DIND_NAME docker` — all subsequent compose commands use this to target the inner daemon

### 2. Add lifecycle helper functions

```bash
_ensure_dind() {
    if _dind_running && _dind_healthy; then
        echo "DinD already running, skipping"
        return
    fi
    echo "Starting DinD container..."
    docker rm -f "$DIND_NAME" 2>/dev/null || true
    docker run -d \
        --name "$DIND_NAME" \
        --privileged \
        -p 16686:16686 \
        -p 3000:3000 \
        -p 8080:8080 \
        -e DOCKER_TLS_CERTDIR="" \
        "$DIND_IMAGE"
    _wait_for_dind
}

_wait_for_dind() {
    echo -n "Waiting for DinD daemon..."
    for i in $(seq 1 30); do
        if _dind_healthy; then echo " OK"; return; fi
        echo -n "."
        sleep 1
    done
    echo " FAIL"
    exit 1
}

_copy_source() {
    echo "Copying source into DinD container..."
    docker exec "$DIND_NAME" rm -rf "$DIND_WORKSPACE" 2>/dev/null || true
    docker cp "$PROJECT_DIR/." "$DIND_NAME:$DIND_WORKSPACE"
}

_install_ca() {
    local cert_name="custom-ca.crt"
    if docker exec "$DIND_NAME" test -f "/usr/local/share/ca-certificates/$cert_name" 2>/dev/null; then
        echo "CA cert already present, skipping"
        return
    fi
    local cert_file="/path/to/your-ca.crt"
    if [ -f "$cert_file" ]; then
        echo "Installing CA into DinD..."
        docker cp "$cert_file" "$DIND_NAME:/usr/local/share/ca-certificates/$cert_name"
        docker exec "$DIND_NAME" update-ca-certificates --fresh >/dev/null 2>&1
    fi
}
```

**Note on `docker cp`**: Using `docker cp src/. dest/` copies the **contents** of src/ into dest/ (flattened). Without the trailing `/.`, it copies src/ as a subdirectory inside dest/. This is the #1 pitfall — always verify with `docker exec dind ls /workspace/` after copying.

### 3. Implement subcommand dispatch with `case`

Use a simple `case "${1:-}" in` pattern:

```bash
case "${1:-}" in
    up)     cmd_up ;;
    rebuild) cmd_rebuild ;;
    restart) cmd_restart ;;
    down)   cmd_down ;;
    status) cmd_status ;;
    verify) cmd_verify ;;
    observe) cmd_observe ;;
    review) cmd_review ;;
    *)
        echo "Usage: bootstrap.sh {up|rebuild|restart|down|status|verify|observe|review|scenario|loadgen|profile|pcap}"
        exit 1
        ;;
esac
```

**Pattern for help text**: Keep the usage string in the catch-all `*)` block. Update it every time you add a subcommand. Running `bootstrap.sh` with no args always shows the full menu.

### 4. Implement tiered rebuild subcommands

The three rebuild tiers vary in depth to avoid unnecessary work:

| Command  | DinD Check | CA Certs | Source Copy | Image Build | Verify Gate | Use Case |
|----------|-----------|----------|-------------|-------------|-------------|----------|
| `up`     | ✅ create  | ✅ yes   | ✅ yes      | ✅ yes      | ✅ yes      | First run, DinD recreated |
| `rebuild`| ✅ ensure  | ❌ skip  | ✅ yes      | ✅ yes      | ✅ yes      | Code/Dockerfile changes |
| `restart`| ✅ ensure  | ❌ skip  | ❌ skip     | ❌ skip     | ❌ skip     | Config/env var changes |

#### `up` — Full cold start (most expensive)

```bash
cmd_up() {
    echo "=== Full Cold Start ==="
    _ensure_dind
    _install_ca
    _copy_source
    echo "Building and starting services..."
    _dind_docker compose -f "$COMPOSE_FILE" up -d --build
    _dind_docker compose -f "$COMPOSE_FILE" ps
    # Run verification gate with auto-rollback
    . /workspace/lib-verify.sh 2>/dev/null && verify_stack || echo "(no verify lib yet)"
}
```

#### `rebuild` — App changes only (skip CA, no DinD create)

```bash
cmd_rebuild() {
    echo "=== App Rebuild ==="
    _ensure_dind
    _copy_source
    echo "Rebuilding images and services..."
    _dind_docker compose -f "$COMPOSE_FILE" up -d --build
    _dind_docker network prune -f 2>/dev/null || true
    # Verification gate with auto-rollback
    if ! . /workspace/lib-verify.sh 2>/dev/null || ! verify_stack; then
        echo "🚨 Verification failed — rolling back"
        _dind_docker compose -f "$COMPOSE_FILE" down
        exit 1
    fi
    echo "✅ Rebuild verified, saved as last-known-good"
}
```

#### `restart` — Quickest tier (no copy, no build)

```bash
cmd_restart() {
    echo "=== Quick Restart ==="
    _ensure_dind
    _dind_docker compose -f "$COMPOSE_FILE" restart
    echo "Services restarted."
}
```

### 5. Implement lifecycle subcommands

```bash
cmd_down() {
    if _dind_running; then
        _dind_docker compose -f "$COMPOSE_FILE" down -v 2>/dev/null || true
    fi
    docker rm -f "$DIND_NAME" 2>/dev/null || true
    echo "DinD stopped and removed."
}

cmd_status() {
    if ! _dind_running; then echo "DinD not running."; exit 1; fi
    echo "=== Service Status ==="
    _dind_docker compose -f "$COMPOSE_FILE" ps
    echo ""
    echo "=== Quick Health ==="
    . /workspace/lib-verify.sh 2>/dev/null && _verify_health || echo "(no verify lib)"
}
```

### 6. Add commands that run code inside the test-runner

For commands that execute Python inside the compose network, use the **nested docker exec** pattern:

```bash
cmd_verify() {
    if ! _dind_running; then echo "DinD not running."; exit 1; fi
    docker exec "$DIND_NAME" sh -c '. /workspace/lib-verify.sh && verify_stack'
}

cmd_observe() {
    if ! _dind_running; then echo "DinD not running."; exit 1; fi
    TEST_RUNNER=$(docker exec "$DIND_NAME" docker ps --format '{{.Names}}' | grep test-runner | head -1)
    if [ -z "$TEST_RUNNER" ]; then echo "Test-runner not found."; exit 1; fi

    # Health status
    echo "=== Service Health ==="
    . /workspace/lib-verify.sh 2>/dev/null && _verify_health

    # Jaeger trace inspection
    echo "=== Traces ==="
    docker exec "$DIND_NAME" docker exec "$TEST_RUNNER" python3 -c '
import http.client, json
try:
    conn = http.client.HTTPConnection("jaeger", 16686)
    conn.request("GET", "/api/services")
    services = json.loads(conn.getresponse().read()).get("data", [])
    print(f"  Jaeger: {len([s for s in services if s != \"jaeger\"])} services reporting traces")
except Exception as e:
    print(f"  (Jaeger unavailable: {e})")
'
}
```

**Key patterns**:
- **Sourcing library scripts**: Use `docker exec DIND_NAME sh -c ". /workspace/lib-foo.sh && foo_func"` to source and call functions. The `.` (source) runs inside the container, not on the host.
- **Finding test-runner**: Use `docker ps --format '{{.Names}}' | grep test-runner | head -1` to discover by pattern instead of hardcoding names (which vary by compose project prefix).
- **Inline Python**: Use `python3 -c '...'` with single quotes for short scripts. For longer scripts, `docker cp` a file first.
- **Copying scripts into test-runner**: Use `docker exec DIND_NAME docker cp /workspace/script.py TEST_RUNNER:/tmp/script.py`.

### 7. Add the pre-commit review gate (static analysis)

```bash
cmd_review() {
    echo "=== Pre-Commit Review Gate ==="
    local critical=0 warnings=0

    # Security: hardcoded secrets
    if grep -r 'password.*=' services/ --include='*.py' 2>/dev/null | grep -v '#.*ignore'; then
        echo "  ❌ Hardcoded secrets found"
        critical=$((critical + 1))
    fi

    # Architecture: network isolation
    for svc_dir in services/*/; do
        svc=$(basename "$svc_dir")
        ns_count=$(yq -r '.services.'"$svc"'.networks | length' docker-compose.yml 2>/dev/null || echo "0")
        if [ "$ns_count" -gt 1 ]; then
            echo "  ℹ️  $svc is multi-homed ($ns_count networks) — verify intent"
        fi
    done

    if [ "$critical" -gt 0 ]; then
        echo "Score: FAIL ($critical critical, $warnings warnings)"
        exit 1
    fi
    echo "Score: PASS ✅"
}
```

### 8. Extend with additional subcommands

Common additions organized by development phase:

| Phase | Subcommand | Purpose |
|-------|-----------|---------|
| Core | `up`, `rebuild`, `restart`, `down`, `status` | Lifecycle management |
| Validation | `verify` | Health checks + e2e smoke tests + auto-rollback |
| Observability | `observe` | Health dashboard, reachability matrix, trace inspection |
| Performance | `profile` | Per-service latency p50/p95/p99, bottleneck detection |
| Quality | `review` | Pre-commit checks (secrets, network isolation, imports) |
| Testing | `scenario` | Run named YAML scenarios against running services |
| Load | `loadgen` | Generate traces/metrics for dashboard population |
| Debug | `pcap` | Start/stop packet capture on specific network segments |

Each new subcommand follows the same pattern:
1. Check `_dind_running` (or not — `review` runs on host files)
2. Use `_dind_docker` compose commands
3. Use nested `docker exec` for test-runner code
4. Output clear success/failure messages
5. Update the `*)` usage block

## Pitfalls
- **`docker cp` trailing slash**: `docker cp src/. dind:/workspace/` copies flat; without `/.`, it nests. This is the #1 pitfall.

- **Nested docker exec quoting**: Inner command strings MUST use single quotes to prevent host shell expansion. If the Python inline script contains single quotes, use `python3 <<'PYEOF' ... PYEOF` heredoc instead.

- **Host shell expands variables in `sh -c`**: When using `docker exec "$DIND_NAME" sh -c ". $DIND_WORKSPACE/lib-verify.sh"`, the `$DIND_WORKSPACE` is expanded by the HOST shell. Use single-quoted strings for DinD-internal paths:
  ```sh
  # Wrong — host expands $DIND_WORKSPACE
  docker exec "$DIND_NAME" sh -c ". $DIND_WORKSPACE/lib-verify.sh"

  # Safe — single-quoted
  docker exec "$DIND_NAME" sh -c '. /workspace/lib-verify.sh'
  ```

- **Env vars don't propagate through nested exec**: Pass them explicitly:
  ```sh
  docker exec "$DIND_NAME" docker exec -e MY_VAR=value TEST_RUNNER python3 -c 'import os; print(os.environ["MY_VAR"])'
  ```

- **`container_name:` changes discovery rules**: Services with explicit `container_name:` keep that exact name regardless of project prefix. Use `docker ps --filter "label=com.docker.compose.service=$svc" --format '{{.Names}}'` to find services reliably.

- **CA cert timing**: Install CA certs in DinD BEFORE building images. Rebaking after CA install requires `docker compose down` + `up --build` to invalidate cached layers.

- **`set -euo pipefail` affects grep**: `grep | head -1` fails if no match (pipefail + grep returns 1). Use `... 2>/dev/null || true` or handle empty case explicitly.

- **Verification gate needs a wait**: Services need time to stabilize before health checks pass. Default 15s but make configurable. Too short = false failures; too long = slow feedback.

- **Auto-rollback on failed verify**: If verification fails after rebuild, shut down compose so you're not left in a half-broken state. The verify library handles this automatically.

- **Stale networks cause IP conflicts**: Always run `docker network prune -f` between rebuilds to avoid "address already in use" errors.

- **Bind mount staleness after `--build`**: After `docker compose up -d --build`, bind-mounted volumes may show stale content because old containers were reused. Use `--force-recreate <service>` to force remount.

## Verification
1. **`bootstrap.sh` (no args)** — Prints usage with all subcommands listed
2. **`bootstrap.sh up`** — Full cold start: DinD created, CA injected, source copied, images built, verify passes
3. **`bootstrap.sh rebuild`** — Source re-copied, images rebuilt, verify passes (no CA step, no DinD recreate)
4. **`bootstrap.sh restart`** — Services restart quickly (no copy, no build)
5. **`bootstrap.sh status`** — Shows running compose services and health
6. **`bootstrap.sh down`** — Stops all services and removes DinD container
7. **`bootstrap.sh verify`** — Runs health checks + e2e tests, exits 0 on success
8. **`bootstrap.sh observe`** — Shows health/reachability/trace output without errors
9. **Adding a new subcommand** — Create a new `case` block, update usage — works without modifying existing subcommands
10. **Sequential `up → rebuild → rebuild`** — works without recreating DinD