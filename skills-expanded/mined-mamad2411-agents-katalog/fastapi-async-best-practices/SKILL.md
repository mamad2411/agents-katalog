---
name: fastapi-async-best-practices
description: >
  Build correct FastAPI async services: non-blocking I/O, threadpool offload for
  sync libraries, lifespan resources, connection pools, and concurrency
  pitfalls. Use when async def routes, Starlette concurrency, or reviewing
  blocking calls under uvicorn workers.
---

# FastAPI Async Best Practices

## Scope And Authorization

- **In scope:** FastAPI services you own.
- **Out of scope:** Load-testing third-party APIs without permission.
- Blocking I/O in `async def` stalls the event loop for the worker—treat as a reliability bug.
- Pair with `fastapi-dependency-auth`, `fastapi-security-patterns`, and `code-quality-standards`.

## When To Use

- Writing or reviewing `async def` endpoints and dependencies.
- Integrating sync ORM/SDK clients into async apps.
- Configuring lifespan for pools (DB, HTTP, Redis).
- Diagnosing latency spikes under concurrency.
- Choosing `def` vs `async def` for routes.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Auth dependencies | `fastapi-dependency-auth` |
| Security headers/CORS/JWT patterns | `fastapi-security-patterns` |
| Generic Python style | `python-style-and-typing` |
| Implementation quality baseline | `code-quality-standards` |
| Load test methodology | performance skills |

## Domain Focus

| Area | Guidance |
| --- | --- |
| async def | Only when awaits are non-blocking |
| def routes | Run in threadpool automatically—OK for sync libs |
| Offload | `asyncio.to_thread` / `run_in_executor` for blocking |
| Pools | Async engines (asyncpg, httpx.AsyncClient) |
| Lifespan | Create/shutdown clients once |
| Timeouts | Always on outbound HTTP/DB |

## Workflow

### 1. Confirm scope and success criteria

1. Endpoints, worker model (uvicorn workers), expected concurrency.
2. Success: no blocking in async paths; p95 stable under concurrent load test in stage.

### 2. Inventory async usage

```bash
rg -n "async def|def " app -g'*.py' | head
rg -n "requests\\.|time\\.sleep|psycopg2|boto3|open\\(" app -g'*.py'
```

1. Flag `requests` / sync boto3 / `time.sleep` inside `async def`.
2. Note global clients created per request (anti-pattern).

### 3. Baseline

1. Capture event-loop lag metrics if available.
2. Reproduce stall with concurrent requests to suspect endpoint.

### 4. Apply patterns

```python
from contextlib import asynccontextmanager
import httpx
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.http = httpx.AsyncClient(timeout=httpx.Timeout(5.0))
    yield
    await app.state.http.aclose()

app = FastAPI(lifespan=lifespan)

@app.get("/upstream")
async def upstream():
    r = await app.state.http.get("https://example.internal/health")
    r.raise_for_status()
    return r.json()

# Sync library: either use def route...
@app.get("/report")
def report_sync():
    return blocking_report()

# ...or offload inside async
@app.get("/report2")
async def report_async():
    return await asyncio.to_thread(blocking_report)
```

1. SQLAlchemy: prefer async session for async routes; don’t mix carelessly.
2. Avoid CPU-bound heavy work on the event loop—separate worker queue.
3. Size connection pools for workers × concurrency.

### 5. Dependencies and timeouts

1. Yield dependencies must not block on exit without timeout.
2. Cancel-safe cleanup where possible.
3. Set explicit timeouts on all external calls.

### 6. Verify with evidence

```bash
pytest -q
ruff check app
# Stage: concurrent load on fixed endpoint
# hey -n 1000 -c 50 https://stage/api/upstream
```

1. Confirm thread offload paths under load don’t collapse throughput.
2. Watch worker CPU and latency histograms.

### 7. Hand off

1. Document which routes are async and why.
2. Standard client factories in lifespan.
3. Link security skills for auth middleware.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| HTTP | httpx.AsyncClient shared | `requests.get` in async def |
| Sleep | `await asyncio.sleep` | `time.sleep` in async |
| Clients | lifespan singleton | New client per request |
| Sync ORM | `def` route or to_thread | Blocking session in async |
| Timeouts | Always set | Hang forever on dependency |

## Output Checklist

- [ ] Blocking calls in async paths removed or offloaded
- [ ] Shared async clients via lifespan
- [ ] Timeouts on outbound I/O
- [ ] Pool sizing considered
- [ ] Load evidence on stage
- [ ] Tests green
- [ ] Residual risk noted

## Rules

- `async def` means non-blocking awaits only.
- Prefer one pattern per codebase for sync libs.
- Don’t hide blocking behind “temporary” code.
- Auth concerns → dependency-auth skill.
- Security baseline → fastapi-security-patterns.
