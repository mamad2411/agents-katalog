---
name: compose-observe-dashboard
description: "Build a terminal-based observability dashboard for running Docker Compose stacks: health status, cross-network reachability matrix, multi-hop flow tracing, and Jaeger distributed trace inspection. Ideal as a bootstrap.sh observe subcommand."
version: 1
created: 2026-05-16
updated: 2026-05-16
---
# Docker Compose Observability Dashboard

## When to Use

When you need a quick terminal-based observability dashboard for a running Docker Compose microservices stack: health status, cross-network reachability matrix, multi-hop flow tracing, and Jaeger distributed trace inspection. Useful as a `bootstrap.sh observe` subcommand for fast stack diagnostics without opening a browser.

## Procedure

### 1. Health check section

Reuse your verification gate health check, or run a simplified version:

```sh
echo "🔍 Observability Dashboard"
echo ""

# Option A: Source your verify library
. lib-verify.sh 2>/dev/null && _verify_health

# Option B: Inline quick check
for SVC in seller buyer gateway aml verifier offramp isogen banksim; do
    STATUS=$(docker exec "workspace-${SVC}-1" curl -sf -o /dev/null -w '%{http_code}' \
        "http://localhost:8000/health" 2>/dev/null || echo "000")
    ICON=$([ "$STATUS" = "200" ] && echo "✅" || echo "❌")
    echo "  $ICON $svc ($STATUS)"
done
```

### 2. Cross-network reachability matrix

Map which services can reach which, grouped by network segment:

```python
# Run from a test container that's multi-homed across all networks
docker exec <test-container> python3 -c '
import httpx
for net, svcs in [("internet", ["seller:8000","buyer:8000"]),
                   ("dmz", ["gateway:8000","aml:8000","verifier:8000"]),
                   ("settlement", ["offramp:8000","isogen:8000","banksim:8000"])]:
    for svc in svcs:
        try:
            r = httpx.get(f"http://{svc}/health", timeout=3)
            print(f"  [{net}] {svc}: {r.status_code}")
        except Exception as e:
            print(f"  [{net}] {svc}: UNREACHABLE ({type(e).__name__})")
'
```

This validates that:
- Services on the same network can reach each other
- Services on different networks can NOT reach each other (isolation works)
- Multi-homed services (verifier, gateway) bridge correctly

### 3. Multi-hop flow tracing

Trace a business-critical flow end-to-end, timing each span:

```python
docker exec <test-container> python3 -c '
import httpx, time
try:
    t0 = time.time()
    r = httpx.get("http://seller:8000/translate?text=hello")
    t1 = time.time()
    print(f"  [SPAN] buyer->seller translate: {r.status_code} ({(t1-t0)*1000:.0f}ms)")
    if r.status_code == 402:
        t2 = time.time()
        r2 = httpx.post("http://seller:8000/__pay", json={"signedTx": "mock"})
        t3 = time.time()
        print(f"  [SPAN] buyer->seller pay: {r2.status_code} ({(t3-t2)*1000:.0f}ms)")
        print(f"  [TRACE] Total: {((t3-t0)*1000):.0f}ms")
except Exception as e:
    print(f"  [FAIL] {type(e).__name__}: {e}")
'
```

**Customize this section** for your project's critical flow. The key pattern is:
1. Time each span (request/response pair)
2. Show the status code
3. Calculate total trace time

### 4. Jaeger distributed trace inspection

Query the Jaeger API to show which services are reporting traces:

```python
docker exec <test-container> python3 -c '
import httpx, time, json
time.sleep(1)  # Allow BatchSpanProcessor to flush
try:
    r = httpx.get("http://jaeger:16686/api/services", timeout=5)
    if r.status_code == 200:
        services = r.json().get("data", [])
        print(f"  Services: {len(services)} reporting")
        for svc in sorted(services)[:5]:
            print(f"    - {svc}")
        # Check specific services for recent traces
        for svc in ["buyer", "seller", "gateway"]:
            if svc in services:
                traces = httpx.get("http://jaeger:16686/api/traces",
                                   params={"service": svc, "limit": 3},
                                   timeout=5)
                if traces.status_code == 200:
                    data = traces.json().get("data", [])
                    print(f"  {svc}: {len(data)} recent trace(s)")
    else:
        print(f"  Jaeger API: {r.status_code}")
except Exception as e:
    print(f"  (Jaeger unavailable: {e})")
'
```

### 5. Print host-accessible URLs

```sh
echo ""
echo "Jaeger UI: http://localhost:16686"
```

### 6. Wire into bootstrap.sh as a subcommand

```sh
observe)
    if ! _dind_running; then echo "DinD not running."; exit 1; fi
    echo "🔍 Observability Dashboard"
    # ... call the sections above ...
    ;;
```

## Pitfalls

- **Jaeger flush delay** — OpenTelemetry SDKs use `BatchSpanProcessor` which buffers spans before exporting. After triggering a flow, wait ~1s before querying Jaeger, or you'll see stale or empty results.
- **Test container must be multi-homed** — The python3 code runs from a test container that must be on all networks you want to check. If it's only on one network, cross-network reachability checks to other segments will fail (which is actually useful — it proves isolation).
- **Container naming conventions** — `workspace-${SVC}-1` is Docker Compose's default (`<project>-<service>-<slot>`). If you use a custom project name or scale services, adjust the naming pattern.
- **httpx vs curl** — `httpx` is preferred when running inside Python containers (already installed). `curl -sf` works in alpine/general containers. Some minimal images have neither — install one or use `python3 -c "import urllib.request..."`.
- **Jaeger API version** — The `/api/services` and `/api/traces` endpoints are Jaeger v1 API. Jaeger v2 (OTLP-based) may use different endpoints. Check your Jaeger version.

## Verification

1. All services healthy → ✅ for each
2. Cross-network reachability shows correct isolation (services can't reach across networks unless multi-homed)
3. Flow trace shows timing per span and total
4. Jaeger section shows services reporting traces after a request
5. If Jaeger not deployed, falls back gracefully (prints "unavailable")
6. Host URL printed for browser access