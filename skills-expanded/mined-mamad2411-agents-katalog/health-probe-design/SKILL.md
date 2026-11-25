# Skill: Health Probe Design (`lb_health_probe_design`)

Design and configure health probes/health checks for load balancers across Azure, AWS, and GCP. Health probes are the most under-designed component of any load-balanced architecture — a misconfigured probe causes cascading backend removal, false-positive failures, and service outages.

---

## Health Probe Fundamentals

A health probe determines whether a backend instance can receive traffic. Get these five parameters right:

| Parameter | Description | Recommended Default |
|---|---|---|
| **Protocol** | HTTP, HTTPS, TCP, or gRPC | HTTP/HTTPS for L7 (validates app logic); TCP for L4 (validates port reachability) |
| **Path** | URL path for HTTP/HTTPS probes | `/healthz` or `/health` — a dedicated endpoint, not your homepage |
| **Interval** | Time between probe checks | 15–30 seconds for most workloads |
| **Timeout** | Max wait for probe response | 5–10 seconds (must be less than interval) |
| **Unhealthy threshold** | Consecutive failures to mark unhealthy | 2–3 failures (avoids single-blip removals) |
| **Healthy threshold** | Consecutive successes to mark healthy | 2 checks (prevents premature traffic return) |

---

## Custom Health Endpoints — Best Practice

Never probe your application's homepage (`/`) or a static file. Build a **dedicated health endpoint**:

```python
# Example /healthz endpoint (Python Flask)
@app.route('/healthz')
def health_check():
    checks = {}
    # Check database connectivity
    try:
        db.session.execute(text('SELECT 1'))
        checks['database'] = 'ok'
    except Exception:
        checks['database'] = 'fail'
        return jsonify(checks), 503
    # Check cache connectivity
    try:
        redis_client.ping()
        checks['cache'] = 'ok'
    except Exception:
        checks['cache'] = 'fail'
        return jsonify(checks), 503
    return jsonify(checks), 200
```

**Design rules for /healthz:**
1. Return HTTP 200 only when the instance can serve real traffic.
2. Check critical dependencies (database, cache, message queue) but set per-check timeouts to avoid probe timeout.
3. Do NOT check non-critical dependencies — a logging service outage should not remove a healthy backend.
4. Keep the endpoint lightweight — no authentication, no heavy queries.
5. Return structured JSON for diagnostic visibility.

---

## Azure Health Probes

### Azure Load Balancer (Standard)

```bash
# TCP probe on port 443, 15s interval, 2 consecutive failures
az network lb probe create \
  --resource-group myRG \
  --lb-name myLB \
  --name health-probe \
  --protocol Tcp \
  --port 443 \
  --interval 15 \
  --threshold 2
```

- Supports **TCP** and **HTTP/HTTPS** probes.
- HTTP probes expect 200 response; anything else = unhealthy.
- Default interval: 15s. Minimum: 5s.
- Source IP: 168.63.129.16 — ensure NSGs allow this.

### Application Gateway v2

```bash
# Custom HTTP probe with host header and path
az network application-gateway probe create \
  --resource-group myRG \
  --gateway-name myAppGW \
  --name custom-probe \
  --protocol Https \
  --host-name-from-http-settings true \
  --path /healthz \
  --interval 30 \
  --timeout 10 \
  --threshold 3 \
  --match-status-codes 200-399
```

- Supports **custom match conditions**: status codes (e.g., 200-399) and body content matching.
- Can inherit host name from HTTP settings or use explicit host.
- Default probe is created automatically but uses `/` — always override with a custom probe.

### Azure Front Door

- Front Door health probes run from **every edge PoP** — be aware of probe volume on your origin.
- Use `HEAD` method to reduce bandwidth: `--probe-method HEAD`.
- Probe interval minimum: 5s. For low-traffic origins, use 30s or higher to avoid excessive probe traffic.

---

## AWS Health Checks

### ALB Target Group

```bash
# HTTP health check on /healthz
aws elbv2 create-target-group \
  --name my-targets \
  --protocol HTTPS \
  --port 443 \
  --vpc-id vpc-0123456789abcdef0 \
  --health-check-protocol HTTPS \
  --health-check-path /healthz \
  --health-check-interval-seconds 30 \
  --health-check-timeout-seconds 5 \
  --healthy-threshold-count 2 \
  --unhealthy-threshold-count 3 \
  --matcher HttpCode=200
```

- **Matcher** supports ranges: `200-299`, or specific: `200,302`.
- **gRPC health checks** supported: use `--health-check-protocol HTTPS` with gRPC matcher.
- **Grace period**: Use `--target-deregistration-delay` (default 300s) to drain connections before removing targets.

### NLB Target Group

- NLB supports **TCP**, **HTTP**, and **HTTPS** health checks.
- TCP check: SYN → SYN-ACK = healthy. Simple but doesn't validate app logic.
- HTTP/HTTPS health checks on NLB: Use for L4 pass-through with L7 validation.
- **Important**: NLB health checks come from the NLB nodes' IPs in your subnet — ensure security groups allow them.

---

## GCP Health Checks

```bash
# HTTP health check
gcloud compute health-checks create http my-health-check \
  --port=8080 \
  --request-path=/healthz \
  --check-interval=15s \
  --timeout=5s \
  --healthy-threshold=2 \
  --unhealthy-threshold=3

# gRPC health check
gcloud compute health-checks create grpc my-grpc-check \
  --port=50051 \
  --grpc-service-name=myservice
```

- GCP health checks are **global resources** shared across LB types.
- Supports HTTP, HTTPS, HTTP/2, TCP, SSL, and gRPC protocols.
- **Source IP ranges**: Health checks come from `35.191.0.0/16` and `130.211.0.0/22` — firewall rules must allow these.
- **Logging**: Enable health-check logging for diagnostic visibility: `--enable-logging`.

---

## Grace Periods and Startup Probes

For containers and VMs with slow startup (Java apps, large model loading):

- **Azure AppGW**: No native startup probe — tune probe interval/thresholds and verify current limits in Azure documentation.
- **AWS ALB**: There is no `initial_health_check` target attribute. Use ECS or Auto Scaling health-check grace periods, target group slow start for gradual traffic ramp, and adjusted health-check thresholds; verify current target group attributes: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/edit-target-group-attributes.html.
- **GCP**: Use startup probes/health checks supported by the backend platform and verify current load-balancer health-check behavior in GCP documentation.

---

## Common Health Probe Mistakes

1. **Probing `/` instead of `/healthz`** — Homepage may return 200 even when the app can't process requests.
2. **Checking too many dependencies** — If your probe checks a non-critical logging service, a logging outage removes all backends.
3. **Timeout ≥ Interval** — Probes stack up and never return timely results.
4. **Missing firewall rules** — Forgetting to allow the probe source IPs (168.63.129.16, NLB subnet IPs, 35.191.0.0/16).
5. **No grace period for slow starts** — Containers killed before they finish initializing.

**Analysis only — verify against vendor documentation before applying.**
