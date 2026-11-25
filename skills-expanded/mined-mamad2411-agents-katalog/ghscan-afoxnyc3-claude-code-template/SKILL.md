# Production Readiness Skill

## Overview

This skill defines requirements for deploying code to production. Use this checklist before any production deployment.

**Persona**: You are an SRE who has been paged at 2 AM because:
- A service had no health check and sat broken for hours
- Logs said "error" with no context, making debugging impossible
- A deployment had no rollback plan and corrupted data
- A service had no graceful shutdown and dropped requests during deploys

You ensure every service can be operated safely in production.

---

## Pre-Production Checklist

### Health & Observability

- [ ] **Health endpoint**: `/health` or `/healthz` returns 200 when healthy
- [ ] **Readiness endpoint**: `/ready` returns 200 only when ready to serve traffic
- [ ] **Structured logging**: JSON format with correlation IDs
- [ ] **Metrics exposed**: Request count, latency, error rate (RED metrics)
- [ ] **Distributed tracing**: Trace IDs propagated through all calls

### Reliability

- [ ] **Graceful shutdown**: Handles SIGTERM, drains connections
- [ ] **Timeouts**: All external calls have explicit timeouts
- [ ] **Retries**: Transient failures retry with exponential backoff
- [ ] **Circuit breakers**: Fail fast when dependencies are down
- [ ] **Resource limits**: CPU/memory limits set in container config

### Configuration

- [ ] **Environment-based config**: No hardcoded URLs or credentials
- [ ] **Config validation**: Fails fast on startup if config invalid
- [ ] **Feature flags**: High-risk features can be disabled without deploy

### Deployment

- [ ] **Rollback plan**: Can revert to previous version in < 5 minutes
- [ ] **Zero-downtime deploy**: Rolling update with health checks
- [ ] **Database migrations**: Backward compatible, separate from app deploy

---

## Patterns

### Health Endpoints

```python
from fastapi import FastAPI, Response

app = FastAPI()

# Simple liveness - is the process running?
@app.get("/health")
def health():
    return {"status": "healthy"}

# Readiness - can we serve traffic?
@app.get("/ready")
async def ready():
    # Check dependencies
    checks = {
        "database": await check_database(),
        "cache": await check_cache(),
    }

    all_healthy = all(checks.values())

    return Response(
        content=json.dumps({"checks": checks}),
        status_code=200 if all_healthy else 503,
        media_type="application/json"
    )
```

### Graceful Shutdown

```python
import signal
import asyncio
from contextlib import asynccontextmanager

shutdown_event = asyncio.Event()

def handle_sigterm(signum, frame):
    shutdown_event.set()

signal.signal(signal.SIGTERM, handle_sigterm)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    yield
    # Shutdown - drain connections
    log.info("shutdown_initiated", reason="SIGTERM")
    # Give in-flight requests time to complete
    await asyncio.sleep(5)
    log.info("shutdown_complete")
```

### Timeouts and Retries

```python
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10)
)
async def call_external_api(url: str) -> dict:
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()
```

### Circuit Breaker

```python
from circuitbreaker import circuit

@circuit(failure_threshold=5, recovery_timeout=30)
async def call_flaky_service():
    # After 5 failures, circuit opens
    # Calls fail fast for 30 seconds
    # Then circuit half-opens and allows one test request
    return await make_request()
```

### Structured Logging

```python
import structlog

log = structlog.get_logger()

# Configure JSON output
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ]
)

# Usage - always include context
log.info(
    "request_completed",
    request_id=request_id,
    user_id=user_id,
    duration_ms=duration,
    status_code=200
)
```

### Kubernetes Probes

```yaml
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      containers:
      - name: app
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 500m
            memory: 512Mi
```

### ECS Task Definition

```json
{
  "containerDefinitions": [{
    "healthCheck": {
      "command": ["CMD-SHELL", "curl -f http://localhost:8080/health || exit 1"],
      "interval": 30,
      "timeout": 5,
      "retries": 3,
      "startPeriod": 60
    },
    "stopTimeout": 30,
    "ulimits": [{
      "name": "nofile",
      "softLimit": 65536,
      "hardLimit": 65536
    }]
  }]
}
```

---

## Production Readiness Review

Before deploying, verify:

```markdown
## Production Readiness Review

### Service: [name]
### Date: [date]
### Reviewer: [name]

### Health & Observability
- [ ] /health endpoint exists and returns 200
- [ ] /ready endpoint checks dependencies
- [ ] Logs are JSON with correlation IDs
- [ ] Metrics are exposed (Prometheus/CloudWatch)

### Reliability
- [ ] SIGTERM handled with graceful shutdown
- [ ] All HTTP calls have timeouts (< 30s)
- [ ] Retries use exponential backoff
- [ ] Resource limits set (CPU, memory)

### Configuration
- [ ] No hardcoded secrets or URLs
- [ ] Config validated at startup
- [ ] Environment variables documented

### Deployment
- [ ] Rollback tested and documented
- [ ] Health checks configured in orchestrator
- [ ] Runbook exists for common issues

### Sign-off
Ready for production: YES / NO
Blockers: [list any issues]
```

---

## References

- 12 Factor App: https://12factor.net/
- Google SRE Book: https://sre.google/sre-book/table-of-contents/
