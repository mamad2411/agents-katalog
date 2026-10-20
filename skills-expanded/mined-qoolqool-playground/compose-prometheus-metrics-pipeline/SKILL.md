---
name: compose-prometheus-metrics-pipeline
description: "Add Prometheus metrics to every FastAPI service in a Docker Compose stack: shared library middleware with Counter/Histogram/Gauge, /metrics endpoint, Prometheus scraper config, Grafana datasource provisioning, and Prometheus-based Grafana dashboards with service label queries."
version: 3
created: 2026-05-18
updated: 2026-05-18
---
# Prometheus Metrics Pipeline for Docker Compose FastAPI Microservices

Add Prometheus metrics instrumentation to every FastAPI service in a Docker Compose stack using a shared library middleware, Prometheus scraper, Grafana datasource, and Prometheus-based Grafana dashboards.

## When to Use

- You have a Docker Compose stack of Python/FastAPI microservices and want Prometheus metrics (request count, duration, error rate, in-flight requests, service up/down)
- You want a **shared library** approach where one `MetricsMiddleware` + `/metrics` endpoint is added to every service via `create_app()` — no per-service boilerplate
- You want a Prometheus scraper targeting all services by Docker DNS name, with a Grafana Prometheus datasource
- You want Grafana dashboards that use Prometheus queries with service-level labels

**Do NOT use** when:
- You need only OTel/Jaeger tracing (use `jaeger-otel-distributed-tracing-compose` instead)
- Your services aren't FastAPI/Python
- You're using a managed Prometheus service (Grafana Cloud, etc.) — the compose-local Prometheus scraper isn't needed

## Procedure

### Step 1: Add prometheus_client to your shared library

```toml
# common/pyproject.toml
[project]
dependencies = [
    "prometheus-client>=0.19",
]
```

### Step 2: Create a shared metrics module

```python
# common/src/yourproject/metrics.py
"""Prometheus metrics instrumentation for FastAPI services."""
import time
from prometheus_client import Counter, Histogram, Gauge, generate_latest, REGISTRY, CONTENT_TYPE_LATEST
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

# Define metric families with service label
REQUEST_COUNT = Counter(
    "app_requests_total",
    "Total HTTP requests",
    labelnames=["service", "method", "endpoint", "status"],
)

REQUEST_DURATION = Histogram(
    "app_request_duration_seconds",
    "HTTP request duration in seconds",
    labelnames=["service", "method", "endpoint"],
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0),
)

IN_FLIGHT_REQUESTS = Gauge(
    "app_requests_in_flight",
    "Current number of in-flight requests",
    labelnames=["service"],
)

ERROR_COUNT = Counter(
    "app_errors_total",
    "Total HTTP error responses (4xx, 5xx)",
    labelnames=["service", "status"],
)

SERVICE_UP = Gauge(
    "app_service_up",
    "Service health status (1=up, 0=down)",
    labelnames=["service"],
)


class MetricsMiddleware(BaseHTTPMiddleware):
    """Middleware that records Prometheus metrics for each request."""

    def __init__(self, app, service_name: str):
        super().__init__(app)
        self.service_name = service_name

    async def dispatch(self, request: Request, call_next):
        method = request.method
        endpoint = request.url.path

        IN_FLIGHT_REQUESTS.labels(service=self.service_name).inc()
        start = time.monotonic()
        try:
            response = await call_next(request)
            return response
        finally:
            duration = time.monotonic() - start
            status = response.status_code if "response" in dir() else 500

            REQUEST_COUNT.labels(
                service=self.service_name, method=method,
                endpoint=endpoint, status=status,
            ).inc()

            REQUEST_DURATION.labels(
                service=self.service_name, method=method,
                endpoint=endpoint,
            ).observe(duration)

            if status >= 400:
                ERROR_COUNT.labels(
                    service=self.service_name, status=str(status),
                ).inc()

            IN_FLIGHT_REQUESTS.labels(service=self.service_name).dec()


def add_metrics_route(app, service_name: str):
    """Add /metrics endpoint and middleware to a FastAPI app."""
    app.add_middleware(MetricsMiddleware, service_name=service_name)
    SERVICE_UP.labels(service=service_name).set(1)

    @app.get("/metrics")
    async def metrics():
        return Response(
            content=generate_latest(REGISTRY).decode("utf-8"),
            media_type=CONTENT_TYPE_LATEST,
        )

    @app.on_event("shutdown")
    async def set_down():
        SERVICE_UP.labels(service=service_name).set(0)
```

### Step 3: Wire metrics into your shared `create_app()`

```python
# common/src/yourproject/mock_base.py
from fastapi import FastAPI
from yourproject.metrics import add_metrics_route


def create_app(title: str, version: str = "0.1.0") -> FastAPI:
    app = FastAPI(title=title, version=version)

    # Add Prometheus metrics (every service gets /metrics)
    add_metrics_route(app, service_name=title)

    @app.get("/health")
    async def health():
        return {"status": "healthy"}

    return app
```

**Key**: Every service that calls `create_app("my-service")` automatically gets:
- `/metrics` endpoint with Prometheus-formatted metrics
- Request count, duration, in-flight, error count, service up/down
- Consistent label schemas across all services

### Step 4: Create Prometheus scraper config

```yaml
# prometheus/prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'yourproject-services'
    static_configs:
      - targets:
        - 'service-a:8000'
        - 'service-b:8000'
        - 'service-c:8000'
        labels:
          stack: 'yourproject'
```

**Target names**: Use Docker Compose service DNS names (e.g., `seller:8000`, `gateway:8000`, `verifier:8000`). Each service must expose port 8000 (or the configured port).

### Step 5: Add Prometheus to docker-compose.yml

```yaml
services:
  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    networks: [your-network]  # must be on a network reachable by Grafana
    volumes:
      - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
    depends_on:
      - service-a
      - service-b
```

### Step 6: Add Grafana Prometheus datasource provisioning

```yaml
# grafana/provisioning/datasources/prometheus.yaml
apiVersion: 1
datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true  # or false — set one datasource as default
    editable: true
    uid: prometheus    # explicit UID prevents drift on container recreate
    jsonData:
      timeInterval: "15s"
```

**Important**: Set an explicit `uid` (not auto-generated). Auto-generated UIDs change every time the Grafana container is recreated, which breaks dashboard panel references. See `grafana-datasource-uid-integrity-test` skill.

### Step 7: Create Prometheus-based Grafana dashboards

Create JSON dashboard files that query Prometheus metrics:

```json
{
  "dashboard": {
    "title": "Service Overview",
    "panels": [
      {
        "title": "Request Rate",
        "type": "graph" or "timeseries",
        "datasource": { "type": "prometheus", "uid": "prometheus" },
        "targets": [{
          "expr": "sum(rate(app_requests_total[5m])) by (service)",
          "legendFormat": "{{service}}"
        }]
      },
      {
        "title": "Error Rate",
        "type": "graph",
        "datasource": { "type": "prometheus", "uid": "prometheus" },
        "targets": [{
          "expr": "sum(rate(app_errors_total[5m])) by (service)",
          "legendFormat": "{{service}} (errors)"
        }]
      },
      {
        "title": "Request Duration (P95)",
        "type": "graph",
        "datasource": { "type": "prometheus", "uid": "prometheus" },
        "targets": [{
          "expr": "histogram_quantile(0.95, sum(rate(app_request_duration_seconds_bucket[5m])) by (le, service))",
          "legendFormat": "{{service}}"
        }]
      },
      {
        "title": "In-Flight Requests",
        "type": "graph",
        "datasource": { "type": "prometheus", "uid": "prometheus" },
        "targets": [{
          "expr": "app_requests_in_flight",
          "legendFormat": "{{service}}"
        }]
      },
      {
        "title": "Service Health",
        "type": "stat",
        "datasource": { "type": "prometheus", "uid": "prometheus" },
        "targets": [{
          "expr": "app_service_up",
          "instant": true
        }]
      }
    ]
  }
}
```

**Dashboard panel query patterns**:
- Use `sum(rate(...[5m])) by (service)` for throughput
- Use `histogram_quantile(0.95, sum(rate(..._bucket[5m])) by (le, service))` for latency percentiles
- Use `{{service}}` in `legendFormat` to get per-service labels
- Service label values must match the `service_name` passed to `add_metrics_route()`

### Step 8: Add Grafana dashboard provisioning YAML

```yaml
# grafana/provisioning/dashboards/default.yaml
apiVersion: 1
providers:
  - name: 'x402 Dashboards'
    orgId: 1
    folder: ''
    type: file
    disableDeletion: false
    updateIntervalSeconds: 10
    allowUiUpdates: true
    options:
      path: /var/lib/grafana/dashboards
      foldersFromFilesStructure: false
```

Mount the dashboards and datasources in docker-compose.yml:

```yaml
services:
  grafana:
    image: grafana/grafana:latest
    networks: [your-network]
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
      - GF_AUTH_ANONYMOUS_ENABLED=true
      - GF_AUTH_ANONYMOUS_ORG_ROLE=Viewer
    volumes:
      - ./grafana/provisioning:/etc/grafana/provisioning
      - ./grafana/dashboards:/var/lib/grafana/dashboards
    ports:
      - "3000:3000"
    depends_on:
      - prometheus
```

### Step 9: Export metrics from your shared library __init__.py

Make `add_metrics_route` importable from the shared library root:

```python
# common/src/yourproject/__init__.py
from yourproject.mock_base import create_app
from yourproject.config import ServiceConfig
from yourproject.telemetry import setup_tracing
from yourproject.metrics import add_metrics_route  # Add this
```

### Step 10: Handle network segmentation (multi-network Docker Compose)

If your compose stack uses **network segmentation** (e.g., internet, DMZ, settlement-net per `compose-multi-network-isolation`), Prometheus must be placed on **all networks** that contain services you want to scrape:

```yaml
services:
  prometheus:
    image: prom/prometheus:v2.53.0
    container_name: prometheus
    networks: [internet, facilitator-dmz, settlement-net]  # ALL networks
    volumes:
      - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml:ro
    ports:
      - "9090:9090"
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
```

If Prometheus cannot be multi-homed (security policy), set up a reverse proxy or use the test-runner container as a metrics collector.

### Step 11: Create domain-specific Grafana dashboards

Beyond the generic overview dashboard, create dashboards for specific operational concerns:

**Payment / Domain Metrics Dashboard** — Track per-endpoint rates and domain-specific metrics:
```json
{
  "dashboard": {
    "title": "Payment Metrics",
    "panels": [
      {
        "title": "Requests by Endpoint",
        "type": "graph",
        "datasource": { "type": "prometheus", "uid": "prometheus" },
        "targets": [{
          "expr": "sum(rate(app_requests_total{service=\"seller\"}[5m])) by (endpoint)",
          "legendFormat": "{{endpoint}}"
        }]
      },
      {
        "title": "Request Duration by Endpoint",
        "type": "graph",
        "datasource": { "type": "prometheus", "uid": "prometheus" },
        "targets": [{
          "expr": "histogram_quantile(0.95, sum(rate(app_request_duration_seconds_bucket{service=\"seller\"}[5m])) by (le, endpoint))",
          "legendFormat": "{{endpoint}}"
        }]
      }
    ]
  }
}
```

**Fault Impact Dashboard** — Correlate errors with fault injection for resilience testing:
```json
{
  "dashboard": {
    "title": "Fault Impact",
    "panels": [
      {
        "title": "Errors by Service",
        "type": "graph",
        "datasource": { "type": "prometheus", "uid": "prometheus" },
        "targets": [{
          "expr": "sum by (service, status) (rate(app_errors_total[5m]))",
          "legendFormat": "{{service}} ({{status}})"
        }]
      },
      {
        "title": "In-Flight Requests During Faults",
        "type": "graph",
        "datasource": { "type": "prometheus", "uid": "prometheus" },
        "targets": [{
          "expr": "app_requests_in_flight",
          "legendFormat": "{{service}}"
        }]
      }
    ]
  }
}
```

Design principles for Prometheus dashboards:
- Use `stat` panels for critical single values (services up, total requests)
- Use `graph` (time series) for trends over time
- Always label by `service` to differentiate in multi-service stacks
- For fault/chaos dashboards, focus on error rates and latency spikes
- Set `"datasource": { "type": "prometheus", "uid": "prometheus" }` using the explicit UID

### Step 12 (Optional): Add a load generator for populating dashboards

Create a standalone Python script that exercises service endpoints to generate real metric and trace data for your dashboards. This is essential for demos — empty dashboards don't sell the value of observability.

```python
#!/usr/bin/env python3
"""Load generator to populate Grafana dashboards with metrics and traces.

Runs inside the Docker Compose network (e.g., from test-runner container).
"""
import argparse
import httpx
import random
import time
from datetime import datetime

SERVICE_URL = "http://seller:8000"

SCENARIOS = [
    ("happy-path", "49.99"),
    ("error-case", "9999.99"),
    ("edge-case", "0.00"),
]


def do_request(amount: str) -> dict:
    """Execute a single request flow against the service."""
    with httpx.Client(base_url=SERVICE_URL, timeout=15.0) as client:
        resp = client.get("/translate?text=loadtest")
        if resp.status_code == 402:
            pay_resp = client.post("/__pay", json={
                "signedTx": f"tx_{random.randint(0, 999999):06x}",
                "metadata": {"wallet": f"wallet_{random.randint(0, 999):03x}"},
            })
            return pay_resp.json()
        return {"status": "error", "reason": f"expected 402, got {resp.status_code}"}


def main():
    parser = argparse.ArgumentParser(description="Load Generator")
    parser.add_argument("--iterations", type=int, default=30)
    parser.add_argument("--delay", type=int, default=300, help="Delay in ms")
    args = parser.parse_args()

    delay_s = args.delay / 1000.0
    results = {"success": 0, "failed": 0, "error": 0}
    start = time.time()

    print(f"🚀 Load Generator — {args.iterations} iterations, {args.delay}ms delay")
    for i in range(1, args.iterations + 1):
        scenario = SCENARIOS[i % len(SCENARIOS)]
        result = do_request(scenario[1])
        status = result.get("status", "error")
        results[status if status in results else "error"] += 1
        elapsed = time.time() - start
        print(f"  [{i:4d}/{args.iterations}] {scenario[0]:20s} → {status:7s}  ({elapsed:.1f}s)")
        if i < args.iterations:
            time.sleep(delay_s)

    elapsed = time.time() - start
    print(f"\n📊 Complete — {args.iterations} in {elapsed:.1f}s")
    print(f"   Success: {results['success']} | Failed: {results['failed']} | Errors: {results['error']}")


if __name__ == "__main__":
    main()
```

Add a `loadgen` subcommand to your bootstrap.sh:

```bash
loadgen)
    ITERATIONS="${2:-30}"
    DELAY="${3:-300}"
    echo "🚀 Load generator: $ITERATIONS iterations, ${DELAY}ms delay"
    # Copy script into the compose environment
    docker cp tests/load_generator.py "$DIND_NAME:/workspace/tests/load_generator.py"
    # Find test-runner container (name varies with compose project prefix)
    TEST_RUNNER=$(docker exec "$DIND_NAME" docker ps --format '{{.Names}}' | grep test-runner | head -1)
    if [ -z "$TEST_RUNNER" ]; then
        echo "Test runner not found."
        exit 1
    fi
    # Run the load generator inside the compose network
    docker exec "$DIND_NAME" docker exec "$TEST_RUNNER" \
        python3 /tests/load_generator.py --iterations "$ITERATIONS" --delay "$DELAY"
    ;;
```

**Key requirements for the load generator**:
- Must run **inside** the Docker Compose network (services are reachable by DNS name, not localhost)
- Use the test-runner container (from `compose-test-runner-container`) which has all service network access
- HTTP requests generate both **Prometheus metrics** (via MetricsMiddleware) and **Jaeger/OTel traces** (if tracing is set up)
- Cycle through different scenarios to exercise diverse code paths
- Wait for the OTel span flush (typically ~1-3 seconds at end) so all spans arrive in Jaeger before checking dashboards

## Pitfalls
- **Middleware must be added BEFORE catch-all routes**: `app.add_middleware(MetricsMiddleware, ...)` must be called before any `@app.api_route("/{path:path}")` catch-all routes. Otherwise the catch-all swallows all metrics before the middleware can record them.

- **`prometheus_client` bucket tuning**: The default histogram buckets (from the list above) cover typical HTTP request durations. For database queries or slow operations, add larger buckets or use a separate histogram.

- **prometheus_client is synchronous**: The `generate_latest()` call is blocking. For very high-throughput services (>1000 req/s), consider serving metrics from a background thread. For most Docker Compose demos and dev environments, it's fine.

- **Port conflicts for /metrics**: If your Prometheus job lists `seller:8000`, that service must have port 8000 open. If you use a different internal port (e.g. 8080 for the demo UI), update the Prometheus target accordingly.

- **Service label drift**: If you rename a service but forget to update the `service_name` parameter passed to `add_metrics_route()`, the label values in your dashboards won't match actual metrics. Always pass the canonical service name.

- **Grafana datasource UID on recreate**: Without an explicit `uid` in datasource provisioning YAML, Grafana auto-generates UIDs that change on container recreate. Dashboard panels that reference the old UID will break. Always set `uid: prometheus` (or whatever you call it) explicitly.

- **Stale metrics after docker compose rebuild**: When you add `prometheus-client` to the shared library and restart services without rebuilding images, the `/metrics` endpoint won't exist (the dependency is missing from the running container). Always `docker compose up -d --build` after adding or upgrading prometheus-client in the shared library.

- **Label cardinality explosion**: Never use unbounded label values (user IDs, request IDs, email addresses, arbitrary strings) as Prometheus labels. Prometheus performance degrades exponentially with high label cardinality. Use only bounded values: service name (fixed set), HTTP method (GET/POST/PUT/DELETE), endpoint path (or path template), status code class (2xx, 4xx, 5xx). If you need per-user tracking, use structured logging (structlog) instead.

- **Default registry collision in tests**: `prometheus_client` uses a global `REGISTRY`. If multiple pytest test cases register the same metric name in the same process, you'll get `ValueError: Duplicated timeseries`. Solutions: (1) Use a fresh `CollectorRegistry()` per test, (2) structure your metrics module to accept an optional registry parameter, (3) use pytest fixtures with `autouse=True` that clear the registry between tests.

- **Multiprocess worker mode incompatibility**: If you run uvicorn with multiple workers (`uvicorn main:app --workers N`), the default prometheus_client single-process mode produces garbled metrics (each worker has its own copy of counters). You must set `PROMETHEUS_MULTIPROC_DIR` env var, use `MultiProcessCollector(REGISTRY)`, and clean the directory on startup. Prefer single-worker containers (`--workers 1`) in Docker Compose demo environments to avoid this complexity.

- **Shutdown gauge may not fire**: The `@app.on_event("shutdown")` handler may not run during `docker compose down` (especially with `--timeout`). The `service_up` gauge might stay at 1. This is cosmetic — on next startup it resets to 1.

- **Load generator must run inside compose network**: HTTP clients in the load generator reference services by compose DNS name (`seller:8000`). The script must run from a container inside the compose network (e.g., the test-runner container). Running from the host or outside the compose network will fail with DNS resolution errors.
## Verification

1. **/metrics endpoint works**: `curl http://localhost:8000/metrics` returns Prometheus-formatted text containing `app_requests_total`
2. **Prometheus scrapes services**: Open Prometheus UI at `http://localhost:9090/targets` — all targets should be UP
3. **Grafana datasource configured**: Grafana UI at `http://localhost:3000` → Configuration → Data Sources → Prometheus shows `url: http://prometheus:9090`
4. **Dashboards load**: Grafana dashboards show metric data with service-level labels
5. **Metric labels match**: `http://localhost:9090/api/v1/label/service/values` returns all service names
6. **Prometheus query works**: `http://localhost:9090/api/v1/query?query=app_service_up` returns 1 for each running service
7. **Grafana panel test**: Open a dashboard panel's query editor — it auto-completes metric names from the Prometheus datasource
8. **Load generator (optional)**: Run `./bootstrap.sh loadgen 10 100` and verify dashboards show data