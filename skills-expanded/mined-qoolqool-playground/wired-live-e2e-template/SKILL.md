---
name: wired-live-e2e-template
description: "Template for creating wired live E2E tests against real Docker infrastructure (no mocks). Follows the 13-step + summary pattern with SoftAssert, step-based output, and infrastructure-first validation. Use when adding new E2E scenarios to a Docker Compose microservices testbed."
---

# Wired Live E2E Test Template

Template for creating end-to-end tests that run against real Docker Compose infrastructure with no mocking. Tests follow a 13-step + summary pattern with soft assertions, step-based output markers (`[OK]`/`[FAIL]`/`[INFO]`/`[WARN]`), and infrastructure-first validation.

## When to Use

Use this skill when:

- Creating a new wired E2E test for a Docker Compose microservices testbed
- Adding a new scenario to an existing E2E suite (e.g., `wired_02_iso_translation.py`, `wired_03_programmable_payment.py`)
- Converting a mock-based test to a live infrastructure test
- The test must validate real container-to-container communication (no mocks except the backend under test)

**Do NOT use** when: writing unit tests, integration tests with mocks, or tests that need to run outside Docker (CI-only tests without infrastructure).

## Reference Files

| File | Description |
|------|-------------|
| `/workspace/sample/wired_01_happy_flow.py` | Original 13-step pattern (Fabric CBDC system) |
| `/workspace/tests/e2e/test_wired_01_happy_flow.py` | Adapted for QUIC Edge Ingress proxy infrastructure |
| `/workspace/tests/e2e/conftest.py` | Shared fixtures (service URLs, expected containers) |

## Procedure

### 1. Create the test file

Create a new file at `tests/e2e/test_wired_XX_scenario_name.py` following the 13-step + summary pattern.

### 2. Write the docstring header

The docstring must describe:

- What the test validates (full lifecycle)
- What the test-runner can reach (service URLs, protocols)
- All participants (containers) in the testbed
- The 13-step flow (numbered 0–12 + 100 for summary)
- Key patterns used
- Prerequisites and run commands

### 3. Set up imports and constants

```python
import asyncio
import json
import os
import sys
import uuid

import httpx
import pytest
import pytest_asyncio

HTTP_TIMEOUT = 30.0
```

Define service URLs as environment variables with defaults:

```python
SERVICE_A = os.environ.get("SERVICE_A", "http://service-a:8000")
SERVICE_B = os.environ.get("SERVICE_B", "http://service-b:9901")
```

### 4. Add demo output helpers

```python
def step(n: int, msg: str):
    print(f"\n{'=' * 60}", file=sys.stderr)
    print(f"  STEP {n}: {msg}", file=sys.stderr)
    print(f"{'=' * 60}", file=sys.stderr)

def ok(msg: str):
    print(f"  [OK] {msg}", file=sys.stderr)

def info(msg: str):
    print(f"  [INFO] {msg}", file=sys.stderr)

def warn(msg: str):
    print(f"  [WARN] {msg}", file=sys.stderr)
```

### 5. Add the SoftAssert class

```python
class SoftAssert:
    """Collect assertions and report all failures at once."""
    def __init__(self):
        self._errors = []

    def check(self, condition: bool, msg: str):
        if condition:
            ok(msg)
        else:
            print(f"  [FAIL] {msg}", file=sys.stderr)
            self._errors.append(msg)

    def assert_empty(self):
        if self._errors:
            raise AssertionError(
                f"Soft assertions failed:\n  - "
                + "\n  - ".join(self._errors)
            )
```

### 6. Define async fixtures

Use `pytest_asyncio.fixture` for HTTP clients to each service:

```python
@pytest_asyncio.fixture
async def svc_a():
    async with httpx.AsyncClient(base_url=SERVICE_A, timeout=HTTP_TIMEOUT) as c:
        yield c

@pytest_asyncio.fixture
async def svc_b():
    async with httpx.AsyncClient(base_url=SERVICE_B, timeout=HTTP_TIMEOUT) as c:
        yield c
```

Add a `run_id` fixture for idempotency:

```python
@pytest.fixture
def run_id():
    return f"e2e-{uuid.uuid4().hex[:8]}"
```

### 7. Write the 13-step test function

The test function follows this structure:

```python
@pytest.mark.asyncio
async def test_scenario_happy_flow_live(svc_a, svc_b, run_id):
    soft = SoftAssert()

    # STEP 0: Infrastructure Check
    #   Verify all core services are reachable via HTTP.
    #   Use asyncio.wait_for with short timeout for each.
    #   Mark netem/tc-only containers as [INFO] (no HTTP server).

    # STEP 1: Health Check
    #   /health on each service, /ready on Envoy admin.
    #   Verify response status and body content.

    # STEP 2: Register Test Data
    #   Seed baseline data (payments, banks, tokens, etc.).
    #   Use run_id for idempotent keys.

    # STEP 3: Snapshot Initial State
    #   Record initial counts, balances, metrics.
    #   Query Prometheus targets if available.

    # STEP 4: Primary Proxy Verification (if applicable)
    #   Verify proxy is LIVE, check cluster health, listener config.
    #   Note companion commands for H2C/H3 tests.

    # STEP 5: Core CRUD via Direct API
    #   Create, list, retrieve (bypassing proxy).
    #   Validate response fields match.

    # STEP 6: Secondary Proxy Verification (if applicable)
    #   Verify alternative proxy (Caddy, etc.).

    # STEP 7: Cross-Protocol Consistency
    #   Verify data created via different paths is consistent.
    #   Reconcile all created records.

    # STEP 8: Detailed Infrastructure Health
    #   Cluster membership, healthy hosts, server info/version.

    # STEP 9: End-to-End Chain Validation
    #   Verify full chain: proxy → backend → cache → metrics.
    #   Note companion commands for protocol-specific tests.

    # STEP 10: Security / Anti-Replay (if applicable)
    #   Token caching, duplicate detection, idempotency keys.

    # STEP 11: Observability
    #   Prometheus targets and metrics, OTEL collector, Grafana.

    # STEP 12: Reconciliation
    #   Final count/balance check, verify all records exist.
    #   Verify proxy still healthy after all operations.

    # STEP 100: Summary
    #   Print final state of all services.
    #   Print companion commands for protocol-specific tests.
```

### 8. Create the conftest.py

Create `tests/e2e/conftest.py` with shared fixtures:

```python
import pytest
import pytest_asyncio
import httpx

@pytest.fixture
def service_urls():
    return {
        "envoy_h2": "http://quic-edge-proxy:8443",
        "envoy_admin": "http://quic-edge-proxy:9901",
        "caddy_h2": "http://caddy:8444",
        "caddy_health": "http://caddy:8080",
        "mock_api": "http://mock-payment-api:8000",
        "anti_replay": "http://anti-replay-cache:6380",
        "prometheus": "http://prometheus:9090",
        "otel": "http://otel-collector:13133",
        "grafana": "http://grafana:3000",
    }

@pytest.fixture
def expected_containers():
    return [
        "quic-edge-proxy", "caddy", "mock-payment-api",
        "quic-client", "test-runner", "netem-router",
        "cert-gen", "anti-replay-cache", "prometheus",
        "otel-collector", "grafana",
    ]
```

### 9. Run the test

```bash
cd /workspace/deploy/compose && docker compose up -d
docker compose exec test-runner python -m pytest tests/e2e/test_wired_XX_scenario_name.py -v -s
```

## Step Numbering Convention

| Step | Purpose | When to Include |
|------|---------|-----------------|
| 0 | Infrastructure Check — verify all services reachable | Always |
| 1 | Health Check — detailed health endpoint validation | Always |
| 2 | Register Test Data — seed baseline data | Always |
| 3 | Snapshot Initial State — record starting state | Always |
| 4 | Primary Proxy Verification | If proxy is in the architecture |
| 5 | Core CRUD via Direct API | Always |
| 6 | Secondary Proxy Verification | If multiple proxies |
| 7 | Cross-Protocol Consistency | If multiple paths exist |
| 8 | Detailed Infrastructure Health | Always |
| 9 | End-to-End Chain Validation | Always |
| 10 | Security / Anti-Replay | If security features exist |
| 11 | Observability | If observability stack exists |
| 12 | Reconciliation | Always |
| 100 | Summary | Always |

## Pitfalls

- **No Docker socket in test-runner:** The test-runner container typically has no Docker CLI or socket. All checks must use HTTP. Do not use `docker` Python SDK or `subprocess` for Docker commands.
- **H2C vs H2:** Envoy's H2 listener may use cleartext HTTP/2 (H2C). Standard `httpx` cannot speak H2C — use `curl --http2-prior-knowledge` from a companion container.
- **H3 requires quic-client:** HTTP/3 tests need a QUIC-capable curl (quiche build). Delegate to the `quic-client` container via companion commands.
- **TLS self-signed certs:** Caddy's `tls internal` generates self-signed certs. Use `--insecure` or `-sk` with curl, but TLS handshake may still fail if the client doesn't trust the CA.
- **Upstream protocol mismatch:** If Envoy's upstream cluster is configured for H2C but the backend speaks HTTP/1.1, the proxy returns 502. Document this as a known limitation.
- **netem-router has no HTTP server:** tc/netem containers with `NET_ADMIN` capability typically have no HTTP server. Mark as `[INFO]` in infrastructure checks.
- **OTEL collector may be unreachable:** The OTEL collector health endpoint may not be exposed. Use `[WARN]` instead of `[FAIL]` for optional services.
- **SoftAssert ordering:** Each `soft.assert_empty()` call is a gate. Place them after logical groups so failures are caught early but don't cascade unnecessarily.
- **Run ID for idempotency:** Always use a `run_id` fixture (UUID hex prefix) for test data keys to prevent collisions across test runs.
- **Prometheus targets may be empty:** On first startup, Prometheus may have 0 targets. Use `[INFO]` for target counts, not `[FAIL]`.

## Verification

- [ ] Test passes with `pytest -v -s` from the test-runner container
- [ ] All 13 steps produce `[OK]` or `[INFO]` output (no `[FAIL]`)
- [ ] SoftAssert reports no errors at the end
- [ ] Companion commands (H2C, H3) are documented in the summary
- [ ] Service URLs are configurable via environment variables
- [ ] `run_id` prevents data collision across runs
- [ ] Conftest.py provides shared fixtures for all E2E tests
- [ ] Test file passes `python -c "import ast; ast.parse(open('test_file.py').read())"` for syntax validity
