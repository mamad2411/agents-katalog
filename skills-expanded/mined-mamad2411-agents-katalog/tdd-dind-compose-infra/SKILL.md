---
name: tdd-dind-compose-infra
description: "TDD Red-Green-Refactor cycle for adding infrastructure (observability, databases, message queues) to a Docker-in-Docker Compose environment: write failing integration tests against absent infrastructure, add compose services + code, wire verification gates, then refactor."
version: 1
created: 2026-05-16
updated: 2026-05-16
---
# TDD Red-Green-Refactor for DinD Compose Infrastructure

Add new infrastructure (Jaeger, databases, message queues, etc.) to a Docker-in-Docker Compose environment using strict TDD: write failing integration tests first, then add infrastructure + code to make them pass, then refactor with verification gates.

## When to Use

- Adding a new infrastructure service (Jaeger, Redis, Postgres, RabbitMQ) to a Docker Compose stack running inside DinD
- Adding observability (tracing, metrics, logging) to existing containerized microservices
- Any change where the "unit under test" is cross-container infrastructure, not just code
- When you need proof that infrastructure is reachable and wired correctly before shipping

## Why This Pattern Matters

Standard TDD assumes tests and code run in the same environment. In DinD Compose, tests run inside a container, code runs in other containers, and infrastructure sits in yet another container. The rebuild cycle is slow (minutes, not seconds). Writing tests first prevents you from building infrastructure that nobody can reach or that doesn't produce the right signals.

## Procedure

### Phase 1: Red — Write Failing Tests

Write integration tests that assert the infrastructure AND the wire-up both work. These tests should fail for the right reason: the infrastructure doesn't exist yet (connection refused, import error, missing config).

**Test categories to write:**

| Category | What It Tests | Failure Mode |
|----------|--------------|--------------|
| Infrastructure health | New service/container is reachable | Connection refused |
| Signal emission | Services emit the right data (traces, metrics, messages) | 404 / empty response from query API |
| Cross-service propagation | Data propagates across service boundaries | Missing headers, missing span attributes |
| Environment attributes | Each service reports correct metadata (segment, role) | Missing env vars, wrong values |

**Example (adding Jaeger tracing):**
```python
# tests/test_observability.py — ALL FAIL until Phase 2

def test_jaeger_healthy():
    """Jaeger UI returns 200 and OTLP collector is reachable on 4317."""
    r = httpx.get("http://jaeger:16686/", timeout=5.0)
    assert r.status_code == 200  # FAILS: jaeger DNS doesn't resolve

def test_traces_emitted():
    """After a payment flow, Jaeger API returns traces from the buyer service."""
    r = httpx.get("http://jaeger:16686/api/traces", params={"service": "buyer"})
    data = r.json()
    assert len(data.get("data", [])) > 0  # FAILS: no traces yet

def test_payment_id_propagation():
    """Same payment ID appears on spans across services."""
    # FAILS: PaymentIdMiddleware doesn't exist yet

def test_network_segment_attribute():
    """x402.network_segment matches each service's expected context."""
    # FAILS: no network_segment resource attribute
```

**Key rules for Red phase tests:**
1. Tests must run from a container that can reach the target infrastructure (check network assignments)
2. Tests should test the REAL infrastructure, not mocks — the point is to verify the compose wire-up
3. Each test should fail for ONE clear reason (don't bundle health + signal + propagation in one test)
4. Name test files descriptively: `test_observability.py`, `test_redis_connectivity.py`

**Verification:** Run tests inside DinD. Expect ALL to fail with clear errors (connection refused, import error).

```bash
docker exec x402-dind docker exec workspace-test-runner-1 python3 -m pytest tests/test_observability.py -v
# Expect: 4 failed, 0 passed
```

### Phase 2: Green — Add Infrastructure + Wire Code

This is the most complex phase. It involves changes at 3 levels simultaneously:

**Level 1: Compose configuration**
- Add the new service to `docker-compose.yml`
- Add network assignments (which segments need access?)
- Add environment variables to ALL services that will use the infrastructure
- Add port mappings if host access is needed (see Phase 3)

**Level 2: Shared library / common code**
- Add config fields (`network_segment`, `otlp_endpoint`, `redis_url`, etc.) to shared config
- Rewrite or extend the wiring function (`instrument()` -> `setup_tracing()` pattern)
- Add cross-service propagation (contextvars, middleware, event hooks)
- Update `__init__.py` exports

**Level 3: Each service's main.py**
- Update import (old function -> new function)
- Update initialization call (add new params from config)
- MUST follow dependency order: `config = ServiceConfig()` BEFORE `setup_tracing(app, config.xxx)`

**Example wiring order (Jaeger):**
```
1. docker-compose.yml        — add jaeger service + env vars on all services
2. common/config.py          — add network_segment, otlp_endpoint fields
3. common/telemetry.py       — rewrite setup_tracing() with OTLP exporter
4. common/tracing.py (NEW)   — PaymentIdMiddleware + _payment_id_var
5. common/http.py            — add _propagate_payment_id event hook
6. common/__init__.py        — export setup_tracing instead of instrument
7. All service/main.py files — instrument(app) -> setup_tracing(app, config.xxx)
```

**Critical dependency rule:** Changes at Level 2 must be consistent before touching Level 3. If `telemetry.py` exports `setup_tracing` but `__init__.py` still exports `instrument`, every service crashes on import.

**Verification after Green phase:**
```bash
# Rebuild inside DinD:
bootstrap.sh rebuild

# Run the Red phase tests — they should now PASS:
docker exec x402-dind docker exec workspace-test-runner-1 python3 -m pytest tests/test_observability.py -v
# Expect: 4 passed (or at minimum, health + emission tests pass)
```

**If tests still fail after Green:**
- `ConnectionRefusedError`: Service not on the right network, or not started yet
- `ImportError`: Missing export in `__init__.py` or circular import
- `TimeoutError`: OTLP exporter can't reach target (check env var for endpoint URL)
- Empty trace data: `BatchSpanProcessor` delays — add `time.sleep(2)` or use `SimpleSpanProcessor` for test reliability

### Phase 3: Green (continued) — Port Forwarding for Host Access

If infrastructure has a UI or API that should be reachable from the host browser, add 3-layer port forwarding:

```
Host browser :PORT -> tooling container :PORT -> DinD container :PORT -> compose service :PORT
```

**Three files to update:**

1. **DinD `docker run`** (in `bootstrap.sh`): Add `-p PORT:PORT` for each port
2. **Compose service** (in `docker-compose.yml`): Already exposes the port in its own compose
3. **Outer `docker-compose.yml`** (tooling container): Add port mappings

**Verification:**
```bash
# From host:
curl -s http://localhost:16686/ | head -5
# Should return the service's HTML/JSON response
```

### Phase 4: Refactor — Wire Verification Gates + Cleanup

Now that the infrastructure works, wire it into the project's operational tooling:

1. **Add health check to verify gate** — The new infrastructure service must appear in `bootstrap.sh verify` output
2. **Add operational section to observe** — `bootstrap.sh observe` should show real data from the new infrastructure
3. **Run static verification** — When DinD isn't running, verify correctness without deploying:

**Static verification checklist (run without DinD):**

| Check | Method |
|-------|--------|
| All test files are valid Python | `python3 -c "import ast; ast.parse(open(f).read())"` |
| All service main.py are valid Python | Same |
| All shared library files are valid Python | Same |
| Compose YAML is valid | `python3 -c "import yaml; yaml.safe_load(open(f))"` |
| No circular imports | Trace import graph manually or with script |
| No stale function references | `grep -r "old_function_name" services/` |
| Config initialized before wiring | Check each main.py: config instantiation before setup call |
| All services have required env vars | Check compose env blocks |
| Port forwarding chain complete | Verify all 3 layers have matching ports |
| No sensitive values hardcoded in compose | Scan compose env blocks for secret patterns |
| Network isolation respected | Settlement services NOT on internet, etc. |
| New infra on correct networks | Jaeger bridges all nets; DB on right segment |

4. **Search and replace stale references:** `grep -r` for old function names, old env vars, old imports

**Verification after Refactor phase:**
```bash
bootstrap.sh verify    # Should include new infra in health checks
bootstrap.sh observe   # Should show live data from new infra
```

### Phase 5: Full Suite — Run All Tests

Run every test, not just the new ones, to catch regressions:

```bash
docker exec x402-dind docker exec workspace-test-runner-1 python3 -m pytest tests/ -v
# ALL tests must pass (existing + new)

bootstrap.sh review   # Static analysis gate
bootstrap.sh verify   # Health gate (should score >= 0.95)
bootstrap.sh profile  # Latency baseline (should show no regression)
```

## Commit Strategy

One commit per phase, with phase label in commit message:

```
test(project): add N failing <feature> tests (Red phase)
feat(project): add <feature> infrastructure (Green phase)
feat(project): add 3-layer port forwarding for <feature>
refactor(project): add <feature> health check to verify + data to observe
```

This makes the TDD cycle visible in git history and makes rollback precise (revert port forwarding without losing the infrastructure commit).

## Pitfalls

- **Don't test mocks, test the real wire-up.** The whole point of DinD is that services really run. Mocking observability infrastructure in a test that is supposed to verify the wire-up defeats the purpose.
- **Don't skip the static verification** when DinD isn't running. Syntax errors and missing imports will bite you on next deploy.
- **Don't forget the config-before-tracing dependency order.** Services crash on startup if `setup_tracing` is called before `ServiceConfig()` parses env vars.
- **Don't add port forwarding in Phase 2.** Keep Green focused on making tests pass. Forwarding is an independent concern (Phase 3).
- **BatchSpanProcessor delays traces.** If tests check observability infrastructure immediately after a request, data may not be flushed yet. Add a small sleep or use SimpleSpanProcessor for test runs.
- **Test-runner must be on the right network.** If new infra is only on `settlement-net` and test-runner is only on `internet`, the health test will fail even though the infra is running fine.
- **`docker cp` flattens directories.** When copying code into DinD, source ends up at `/workspace/`, not `/workspace/project/`. Test paths must match.

## Verification

After applying this skill, confirm:
1. Red phase: all new tests fail with clear error messages (not unrelated crashes)
2. Green phase: all new tests pass, all existing tests still pass
3. Refactor phase: verify gate and observe include the new infrastructure
4. Static verification: all checks pass without DinD running
5. Git history shows one commit per phase with phase labels