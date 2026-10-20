---
name: dind-discover-containers-by-pattern
description: Discover Docker containers by name pattern inside a Docker-in-Docker environment instead of hardcoding names. Handles Docker Compose project name prefixes that vary based on directory name or --project-name flag.
version: 1
created: 2026-05-18
updated: 2026-05-18
---
## When to Use

When running shell scripts or CLI tools that need to `docker exec` into specific containers inside a Docker-in-Dinner (DinD) setup. Container names in Docker Compose are unpredictable because Compose prefixes them with the project name (derived from the compose file's parent directory or `--project-name` flag), so hardcoding container names like `test-runner` or `x402_test-runner_1` is fragile.

## Procedure

### 1. List containers by name pattern inside DinD

Use `docker ps --format '{{.Names}}'` piped through `grep` to find the container by a substring of its name:

```bash
DIND_NAME="my-dind-container"
TEST_RUNNER=$(docker exec "$DIND_NAME" docker ps --format '{{.Names}}' | grep test-runner | head -1)
```

### 2. Fail early if container not found

```bash
if [ -z "$TEST_RUNNER" ]; then
    echo "Test runner not found. Available containers:"
    docker exec "$DIND_NAME" docker ps --format '{{.Names}}'
    exit 1
fi
```

### 3. Use the discovered name for docker exec

```bash
docker exec "$DIND_NAME" docker exec "$TEST_RUNNER" python -m pytest /tests/ -v
```

### 4. Full script template

```bash
#!/usr/bin/env bash
set -euo pipefail

DIND_NAME="${DIND_NAME:-tooling-dind}"

# Verify DinD is running
if ! docker exec "$DIND_NAME" docker info >/dev/null 2>&1; then
    echo "DinD not running."
    exit 1
fi

# Discover container by pattern
CONTAINER_PATTERN="${1:-service-name}"
TARGET_CONTAINER=$(docker exec "$DIND_NAME" docker ps --format '{{.Names}}' | grep "$CONTAINER_PATTERN" | head -1)

if [ -z "$TARGET_CONTAINER" ]; then
    echo "No container matching '$CONTAINER_PATTERN' found."
    docker exec "$DIND_NAME" docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}'
    exit 1
fi

echo "Found container: $TARGET_CONTAINER"
docker exec "$DIND_NAME" docker exec "$TARGET_CONTAINER" "$@"
```

## Pitfalls

- **Multiple matches:** `grep pattern | head -1` selects the first match. If you have multiple containers matching (e.g., `test-runner-1` and `test-runner-2`), use a more specific pattern or add logic to handle multiple matches.
- **Compose project name prefix:** Docker Compose prefixes container names with the project name. For a compose file at `/project/x402-poc/docker-compose.yml`, containers will be named like `x402-poc_<service>_1` (Linux) or `x402-poc-<service>-1` (Docker Compose v2). The directory name or `--project-name` flag controls the prefix.
- **`container_name` in compose overrides the prefix.** If `container_name: test-runner` is set in docker-compose.yml, the container name is exactly `test-runner` with no prefix. In that case, grep still works but the prefix issue is avoided entirely.
- **Container might not be running.** `docker ps` only shows running containers. Use `docker ps -a` if you need to find stopped containers too.
- **`docker exec` shell quoting:** When passing complex commands through two layers of `docker exec`, be careful with shell quoting. Prefer passing arguments as the test target rather than inline commands.

## Verification

1. Run the script — verify it finds the correct container
2. Run with a non-matching pattern — verify the early-exit error message shows available containers
3. Verify that the discovered container name is used successfully by `docker exec` to run commands