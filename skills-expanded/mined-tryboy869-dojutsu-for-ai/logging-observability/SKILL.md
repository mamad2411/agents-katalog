---
name: logging-observability
description: "Apply when setting up logging, metrics, tracing, or monitoring for any application. Covers: structured logging with structlog, OpenTelemetry, health endpoints, alerting patterns. Trigger for: logging, monitoring, observability, metrics, traces, health check, structlog."
---

# LOGGING & OBSERVABILITY — Production Standards

## Structured Logging (structlog)
```python
import structlog

# Configure once at startup
structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),  # machine-readable
    ],
)

log = structlog.get_logger()

# Usage — always with context
log.info("job.submitted",
    job_id=str(job_id),
    job_type=job_type,
    user_id=str(user_id),
    payload_size=len(str(payload))
)

log.error("job.failed",
    job_id=str(job_id),
    error=str(exc),
    attempt=attempt,
    will_retry=attempt < max_retries,
)
```

## Request Context (per-request trace ID)
```python
import uuid
from structlog.contextvars import bind_contextvars, clear_contextvars

@app.middleware("http")
async def request_context(request: Request, call_next):
    clear_contextvars()
    bind_contextvars(
        request_id=str(uuid.uuid4()),
        method=request.method,
        path=request.url.path,
    )
    response = await call_next(request)
    return response
# All log calls in this request automatically include request_id
```

## Health Endpoints
```python
@app.get("/health")           # Load balancer check (fast)
async def health():
    return {"status": "ok"}

@app.get("/health/ready")     # K8s readiness — check dependencies
async def readiness():
    checks = {
        "database": await check_db(),
        "redis":    await check_redis(),
    }
    status = "ok" if all(checks.values()) else "degraded"
    code = 200 if status == "ok" else 503
    return JSONResponse({"status": status, "checks": checks}, status_code=code)
```

## Key Metrics to Track
```python
# Business metrics (most important)
# - jobs submitted per minute
# - job success rate (target: > 99%)
# - job p95 duration
# - queue depth (alert if > 1000)

# Technical metrics
# - HTTP request duration (p50, p95, p99)
# - Database query duration
# - Cache hit rate (target: > 80%)
# - Error rate per endpoint
```

## Forbidden
❌ `print()` for logging (use structlog)
❌ Logging passwords, tokens, PII
❌ One giant log string ("User 123 did thing X") — use structured fields
❌ No log levels (everything at INFO)
❌ No health endpoints
❌ Logging inside tight loops (performance hit)
