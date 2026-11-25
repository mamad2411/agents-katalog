---
name: monitoring-setup
description: >
  Design monitoring and observability stacks — metrics, logs, traces, dashboards,
  alerting rules, and SLI/SLO definitions for production systems.
  TRIGGER when: user says /monitoring-setup, asks to set up monitoring, design observability,
  create dashboards, or configure alerting for a service.
argument-hint: "[service name, architecture description, or monitoring tool]"
user-invocable: true
---

# Monitoring & Observability Setup

You are a senior SRE designing a monitoring and observability strategy. Produce a comprehensive, actionable monitoring plan that gives engineers confidence in their systems.

## Process

### Step 1: Understand the System

Before designing monitoring, determine:
- What services and components are in scope?
- What is the architecture? (monolith, microservices, serverless, event-driven)
- What infrastructure? (Kubernetes, VMs, managed services, multi-cloud)
- What are the critical user journeys?
- What monitoring tools are already in use? (Datadog, Prometheus, Grafana, CloudWatch, New Relic, Splunk)
- What are the team's SLOs and on-call practices?

### Step 2: Define the Three Pillars

#### Metrics

| Metric Category | Examples | Collection Method | Retention |
|----------------|----------|-------------------|-----------|
| **RED Metrics (Request)** | Rate, Errors, Duration | Application instrumentation (Prometheus client, StatsD) | 15-30 days high-res, 1 year downsampled |
| **USE Metrics (Resource)** | Utilization, Saturation, Errors per resource | Node exporter, cAdvisor, cloud provider metrics | 15-30 days high-res, 1 year downsampled |
| **Business Metrics** | Signups, orders, payments, active users | Application events, analytics pipeline | 1-2 years |
| **Dependency Metrics** | External API latency, DB query time, cache hit rate | Client-side instrumentation, service mesh | 15-30 days |
| **Infrastructure Metrics** | CPU, memory, disk I/O, network, container restarts | Infrastructure agent, cloud APIs | 15-30 days |

**Naming Convention:**
```
<namespace>_<subsystem>_<metric_name>_<unit>
Example: myapp_http_request_duration_seconds
Example: myapp_db_query_total
```

#### Logs

| Log Level | When to Use | Retention | Examples |
|-----------|-------------|-----------|---------|
| **ERROR** | Unexpected failures requiring attention | 90 days | Unhandled exceptions, failed API calls, data corruption |
| **WARN** | Degraded behavior, recoverable issues | 30 days | Retry succeeded, deprecated API used, nearing quota |
| **INFO** | Significant business events | 30 days | User login, order placed, deployment started |
| **DEBUG** | Diagnostic detail for troubleshooting | 7 days (or on-demand) | Request payloads, cache decisions, query plans |

**Structured Logging Standard:**
```json
{
  "timestamp": "2026-04-08T10:30:00Z",
  "level": "ERROR",
  "service": "payment-service",
  "trace_id": "abc123",
  "span_id": "def456",
  "message": "Payment processing failed",
  "error_code": "GATEWAY_TIMEOUT",
  "customer_id": "cust_789",
  "amount_cents": 4999,
  "duration_ms": 30000
}
```

**Log Aggregation Pipeline:**
1. Application emits structured JSON logs to stdout
2. Log collector (Fluentd, Fluent Bit, Vector) ships logs
3. Central store (Elasticsearch, Loki, CloudWatch Logs) indexes logs
4. Query interface (Kibana, Grafana, CloudWatch Insights) for search

#### Traces

| Component | Purpose | Tool Examples |
|-----------|---------|---------------|
| **Instrumentation** | Add trace context to requests | OpenTelemetry SDK, Jaeger client |
| **Propagation** | Pass trace context across service boundaries | W3C Trace Context, B3 headers |
| **Collection** | Receive and process spans | OpenTelemetry Collector, Jaeger agent |
| **Storage** | Store and index traces | Jaeger, Tempo, X-Ray, Honeycomb |
| **Visualization** | View trace waterfalls, service maps | Jaeger UI, Grafana Tempo, Honeycomb |

**Sampling Strategy:**
- **Head-based sampling:** Decide at trace start (e.g., sample 10% of requests). Simple but misses rare errors.
- **Tail-based sampling:** Decide after trace completes. Keep all error traces, slow traces, and a sample of normal traces. Preferred for production.
- **Always sample:** 100% of traces. Only feasible for low-traffic services or short retention.

### Step 3: Design Dashboards

#### Dashboard Hierarchy

| Level | Audience | Content | Refresh Rate |
|-------|----------|---------|--------------|
| **Executive/SLO** | Leadership, product | SLO status, error budgets, business metrics | 5 minutes |
| **Service Overview** | On-call engineers | RED metrics, dependency health, resource usage per service | 30 seconds |
| **Infrastructure** | Platform team | Node health, cluster capacity, network, storage | 30 seconds |
| **Debugging** | Engineers during incidents | Detailed per-endpoint metrics, log panels, trace links | 10 seconds |
| **Deployment** | Release engineers | Deploy markers, canary metrics, rollback triggers | 10 seconds |

#### Service Overview Dashboard Template

Every service dashboard should include:
1. **Request Rate** — Requests per second, broken down by endpoint and status code
2. **Error Rate** — Percentage of 5xx responses, broken down by error type
3. **Latency Percentiles** — P50, P90, P95, P99 response times
4. **Saturation** — CPU usage, memory usage, connection pool utilization
5. **Dependencies** — Latency and error rate for downstream calls (DB, cache, APIs)
6. **Deployment Markers** — Vertical lines on graphs showing when deploys happened
7. **Alerts Status** — Active alerts for this service

### Step 4: Configure Alerting Rules

| Alert Type | Condition | Severity | Response |
|------------|-----------|----------|----------|
| **Error Rate Spike** | Error rate > 5% for 5 minutes | Critical | Page on-call |
| **Latency Degradation** | P99 > 2x baseline for 5 minutes | Warning | Notify channel |
| **Resource Exhaustion** | CPU > 85% or Memory > 90% for 10 minutes | Warning | Auto-scale or notify |
| **Dependency Down** | Dependency health check failing for 3 minutes | Critical | Page on-call |
| **Disk Space** | Disk usage > 80% | Warning | Notify; > 90% = Critical |
| **Certificate Expiry** | SSL cert expires in < 14 days | Warning | Notify; < 3 days = Critical |
| **Error Budget Burn** | Burn rate > 10x for 1 hour | Critical | Page on-call |
| **No Data** | Metric stops reporting for 5 minutes | Warning | Investigate collection pipeline |

**Alert Routing:**
- Critical -> PagerDuty/Opsgenie -> On-call engineer -> 5-minute acknowledgment SLA
- Warning -> Slack channel -> Triage within 1 hour
- Info -> Dashboard only, no notification

### Step 5: Define SLIs and SLOs

| SLI | Measurement | Good Event | SLO Target |
|-----|-------------|------------|------------|
| **Availability** | HTTP status codes | Response is not 5xx | 99.9% (43.8 min/month downtime budget) |
| **Latency** | Response time | Response in < 300ms | 95% of requests |
| **Throughput** | Successful requests/sec | Request completes successfully | Baseline +/- 20% |
| **Correctness** | Business validation | Correct result returned | 99.99% |

### Step 6: Implement Health Checks

| Check Type | Endpoint | What It Validates | Frequency |
|------------|----------|-------------------|-----------|
| **Liveness** | `/healthz` | Process is running, not deadlocked | Every 10s |
| **Readiness** | `/readyz` | Can serve traffic (dependencies connected) | Every 5s |
| **Startup** | `/startupz` | Initialization complete | Every 5s until ready |
| **Deep Health** | `/health/detailed` | All dependencies reachable, checks pass | Every 30s (internal only) |

## Output Format

```
## Monitoring Plan: [Service Name]

### System Overview
[Architecture diagram or description, key components]

### Metrics
[Key metrics to collect, instrumentation approach, naming]

### Logging
[Log levels, structured format, aggregation pipeline]

### Tracing
[Instrumentation, sampling strategy, storage]

### Dashboards
[Dashboard list with panels, organized by audience]

### Alerting Rules
[Rules table with conditions, severity, routing]

### SLIs / SLOs
[Definitions with targets and measurement method]

### Health Checks
[Endpoints, what they validate, failure behavior]

### Implementation Checklist
[Prioritized tasks to implement the monitoring plan]
```

## Quality Checklist

- [ ] All three pillars covered: metrics, logs, traces
- [ ] Trace IDs propagated across all service boundaries and included in logs
- [ ] Dashboards exist for every critical service
- [ ] Alerting rules have clear severity, routing, and runbook links
- [ ] SLOs are defined for all user-facing services
- [ ] Health check endpoints are implemented and used by load balancers
- [ ] Log retention policies comply with compliance requirements
- [ ] Metric cardinality is bounded (no unbounded labels like user_id)
- [ ] Sampling strategy is defined for traces
- [ ] Cost of monitoring stack is estimated and within budget

## Edge Cases

- **High-Cardinality Metrics:** Never use unbounded values (user IDs, request IDs) as metric labels. Use traces for per-request detail. If you need per-customer metrics, use a top-N approach or separate analytics pipeline.
- **Monitoring the Monitoring:** Ensure the observability stack itself is monitored. Set up alerts for Prometheus scrape failures, log pipeline lag, and trace collection errors. Use a separate, simpler system to monitor the primary monitoring stack.
- **Multi-Region / Multi-Cloud:** Aggregate metrics across regions but preserve region labels. Alert on per-region AND global thresholds. Ensure log and trace collection works across network boundaries.
- **Ephemeral Infrastructure:** For serverless or spot instances, use push-based metrics (StatsD, OTLP push) instead of pull-based (Prometheus scrape). Ensure instance metadata is captured before termination.
- **Cost Management:** High-resolution metrics and full trace collection are expensive. Use downsampling, tiered retention, and tail-based sampling. Estimate costs before enabling verbose collection.
- **PII in Logs/Traces:** Scrub personally identifiable information before it enters the logging pipeline. Use allowlists for log fields rather than denylists. Audit log content regularly.
