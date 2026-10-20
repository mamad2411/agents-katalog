---
name: compose-test-runner-container
description: Set up a dedicated test-runner container in Docker Compose that spans all networks for cross-service integration testing, with volume-mounted tests, common library only, and sleep-infinity for docker exec pytest access.
version: 1
created: 2026-05-18
updated: 2026-05-18
---
# Cross-Network Test-Runner Container for Docker Compose

Set up a dedicated test container that spans all network segments, volume-mounts test files, installs only the shared/common library (not service-specific code), and runs `sleep infinity` for `docker exec`-based integration testing.

## When to Use

- You have a Docker Compose microservice stack with **multiple isolated networks** (e.g., internet/DMZ/settlement) and need to run tests that cross those boundaries
- You want to **volume-mount test files** rather than bake them into service images (faster iteration, no rebuild for test changes)
- You need a **multi-homed container** that can reach any service in any network segment by hostname
- You want to run `pytest` or other test suites via `docker exec` without adding test tooling to every service container

**Do NOT use** when:
- Your services are all on the same network (use a simple `depends_on` + `command` pattern)
- You need tests baked into the image (CI/CD with pre-built images) — use a multi-stage build instead
- Your project is single-service (use pytest directly in the service container)
- You don't have a shared/common library (the test-runner needs it for models/schemas/types)

## Procedure

### Step 1: Create the test-runner Dockerfile

Create `test-runner/Dockerfile`:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install test tooling
RUN pip install --no-cache-dir pytest httpx pytest-asyncio

# Install the shared/common library only (not service-specific code)
COPY common/pyproject.toml /app/common/
COPY common/src/ /app/common/src/
RUN pip install --no-cache-dir /app/common/.

# Sleep infinitely so docker exec can access this container on demand
CMD ["sleep", "infinity"]
```

**Key decisions:**
- Install **only the shared library** — not service-specific code. Tests import models, schemas, and clients from common, then call services over HTTP.
- `sleep infinity` as CMD — the container starts and sits idle, waiting for `docker exec` commands. This is the key pattern for `docker exec`-based testing.
- No ENTRYPOINT override — the CMD runs directly.

### Step 2: Add the test-runner service to docker-compose.yml

```yaml
services:
  # ... your existing services ...

  # ── Test runner (cross-network integration testing) ──
  test-runner:
    build:
      context: .
      dockerfile: test-runner/Dockerfile
    networks:
      - internet
      - facilitator-dmz
      - settlement-net
    environment:
      - X402_NETWORK_SEGMENT=test
      - X402_OTLP_ENDPOINT=http://jaeger:4317  # if using tracing
    volumes:
      - ./tests:/tests:ro
    depends_on:
      - seller
      - verification
      - gateway
      # depends_on all services you test against
```

**Key decisions:**
- **Multi-homed networking**: put on ALL network segments. This is the whole point — the test-runner can resolve and reach any service by its compose service name (`http://seller:8000`, `http://verifier:8000`).
- **Volume-mount tests**: `./tests:/tests:ro` — test files live on the host and are mounted at runtime. Change a test, no rebuild needed.
- **Read-only mount**: `:ro` prevents accidental test file modification from inside the container.
- **`depends_on`**: List all services under test so the test-runner starts after they're healthy (if using health checks + condition).

### Step 3: Create pytest config for async tests

Create `test-runner/pytest.ini` (or at a test directory root):

```ini
[pytest]
asyncio_mode = auto
testpaths = /tests
asyncio_default_fixture_loop_scope = function
```

`asyncio_mode = auto` is critical — it allows async test functions (`async def test_...`) without `@pytest.mark.asyncio` on every test.

### Step 4: Write tests using direct service URLs

Tests in `./tests/` reference services by their Docker Compose service name:

```python
"""End-to-end tests that run inside the test-runner container.

All services are reachable by hostname because the test-runner
spans all network segments in the compose topology.
"""
import pytest
import httpx


@pytest.fixture
def seller_client():
    with httpx.Client(base_url="http://seller:8000", timeout=15.0) as c:
        yield c


class TestHappyPath:
    def test_payment_request_returns_402(self, seller_client):
        """Standard 402 payment flow."""
        resp = seller_client.get("/translate?text=hello")
        assert resp.status_code == 402

    def test_authorize_endpoint(self):
        """Direct call to a service on a different network segment."""
        resp = httpx.post("http://verifier:8000/authorize", json={
            "payment_id": "pay-001",
            "amount": "49.99",
            "currency": "USD",
            "merchant_id": "merchant-1",
        }, timeout=10.0)
        assert resp.status_code == 200
        data = resp.json()
        assert data["authorized"] is True

    def test_settle_endpoint_cross_network(self):
        """Call a service on the settlement network."""
        resp = httpx.post("http://offramp:8000/settle", json={
            "payment_id": "pay-001",
            "tx_hash": "0xabc123",
            "amount": "49.99",
        }, timeout=10.0)
        assert resp.status_code == 200
        data = resp.json()
        assert data["settled"] is True
```

**Test design rules:**
- Each test file creates its own clients (not a monolithic conftest.py) — keeps tests independent and self-documenting
- Set explicit `timeout` values — no-default-timeout means tests hang forever if a service is down
- Test across network boundaries by using different service hostnames

### Step 5: Run tests via docker exec

From the host (or DinD host):

```bash
# Discover the test-runner container (name varies by compose project prefix)
TEST_RUNNER=$(docker ps --format '{{.Names}}' | grep test-runner | head -1)

# Run all tests
docker exec "$TEST_RUNNER" python3 -m pytest /tests/ -v

# Run specific test file
docker exec "$TEST_RUNNER" python3 -m pytest /tests/test_happy_path.py -v

# Run with coverage
docker exec "$TEST_RUNNER" python3 -m pytest /tests/ -v --cov=/app/common/src/
```

If running inside a Docker-in-Docker container:

```bash
DIND_NAME="my-dind-container"
TEST_RUNNER=$(docker exec "$DIND_NAME" docker ps --format '{{.Names}}' | grep test-runner | head -1)
docker exec "$DIND_NAME" docker exec "$TEST_RUNNER" python3 -m pytest /tests/ -v
```

### Step 6: (Optional) Add a convenience shell script

Create `run-tests.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail

# In DinD: discover test-runner by pattern
if docker info >/dev/null 2>&1; then
    TEST_RUNNER=$(docker ps --format '{{.Names}}' | grep test-runner | head -1)
else
    echo "Docker not running."
    exit 1
fi

if [ -z "$TEST_RUNNER" ]; then
    echo "Test-runner container not found. Is the stack up?"
    exit 1
fi

TARGET="${*:-/tests/}"
docker exec "$TEST_RUNNER" python3 -m pytest "$TARGET" -v -s
```

Usage:
```bash
./run-tests.sh                      # Run all tests
./run-tests.sh /tests/test_happy_path.py -x  # Single file, stop-on-first-fail
```

## Pitfalls

- **`docker exec` two-hop shell quoting**: When running through DinD, complex commands with quotes need careful escaping. Prefer passing test file paths as arguments, not inline shell scripts.
- **sleep infinity not installed**: Some minimal images (Alpine) don't have `sleep infinity`. Use `sleep 2147483647` or `tail -f /dev/null` as alternatives.
- **Volume-mount path mismatch**: The `./tests` path in docker-compose.yml is relative to the compose file's directory. Use absolute paths if the compose file is not at the project root.
- **Stale common library**: If the shared library changes, the test-runner must be rebuilt (`docker compose build test-runner`). The volume-mounted tests update immediately.
- **Service DNS resolution**: The test-runner resolves service names via Docker's embedded DNS (127.0.0.11). This only works for services on the same Docker Compose network. If the test-runner spans multiple custom networks, DNS resolves correctly for all.
- **pytest-asyncio version compatibility**: `asyncio_mode = auto` requires pytest-asyncio >= 0.21. Check your installed version. Older versions need `@pytest.mark.asyncio` on each test.
- **Module-level HTTP clients in tests**: If you create `httpx.Client` at module level in test files, they may be shared across test functions (depending on pytest's scope). Prefer fixtures or function-local clients.
- **Container name varies**: Docker Compose prefixes container names with the project name (directory name or `--project-name` flag). Use `docker ps --format '{{.Names}}' | grep test-runner | head -1` to discover it dynamically instead of hardcoding.

## Verification

1. **Test-runner starts and sleeps**: Run `docker compose up test-runner` — verify it starts and shows status "Up" without crashing. Run `docker exec <test-runner> echo "alive"` — should return "alive".
2. **Volume mount works**: Create a temp test file `tests/test_volume.py` with `def test_volume(): assert True`. Run `docker exec <test-runner> python3 -m pytest /tests/test_volume.py -v` — should pass. Delete the file afterward.
3. **Cross-network reachability**: From inside the test-runner, run `python3 -c "import httpx; r = httpx.get('http://seller:8000/health'); print(r.status_code)"` — should return 200. Repeat for services on other network segments.
4. **Test suite passes**: Run the full test suite — all async and sync tests pass. Tests on one network reach services on other networks.
5. **No service-specific code in test-runner**: Verify with `docker exec <test-runner> python3 -c "import verifier.main" 2>&1` — should raise `ModuleNotFoundError` (only common library is installed).
6. **Async tests work without decorators**: Verify with `docker exec <test-runner> python3 -m pytest /tests/ -v --co` — async tests run without `@pytest.mark.asyncio`.