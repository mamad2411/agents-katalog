---
name: observability-baseline
description: >-
  Standard observability (logging, metrics, tracing, alerts) for applications and
  infrastructure. Ensures systems are monitorable and debuggable in production.
when-to-use: >-
  Use when architecting new services, reviewing application code, designing
  monitoring for infrastructure, or diagnosing production issues. Apply to both
  new and legacy systems before they reach production.
categories:
  - operations
  - monitoring
  - observability
---

# Observability Baseline

Every service in production should have:
1. **Logging** — What happened and when
2. **Metrics** — How is the system performing
3. **Tracing** — How did a request flow through services
4. **Alerts** — Notify on problems

## Logging Baseline

### Log Levels
Use standard levels correctly:

| Level | When to use | Example |
| --- | --- | --- |
| **DEBUG** | Low-level troubleshooting details | "Parsing config: key=value" |
| **INFO** | Notable events in normal operation | "Service started", "User logged in" |
| **WARN** | Unexpected situation, not a failure | "Database connection timeout, retrying" |
| **ERROR** | Error that affects operation | "Request failed: 500 error", "Database down" |
| **FATAL** | System can't continue | "Out of memory", "Config file missing" |

### Required Log Fields
Every log should include:
```json
{
  "timestamp": "2024-03-15T10:30:00Z",  // When
  "level": "ERROR",                      // Severity
  "message": "User login failed",        // What
  "service": "auth-service",             // Which service
  "trace_id": "abc123def456",            // Request correlation ID
  "user_id": "user_42",                  // Context (if applicable)
  "request_id": "req_789",               // Request ID
  "error": {                             // Details if error
    "type": "AuthenticationError",
    "details": "Invalid password"
  }
}
```

### Structured Logging
- [ ] Use structured logs (JSON) not plain text
- [ ] Every log has: timestamp, level, message, service, trace_id
- [ ] Add context: user_id, request_id, environment
- [ ] **NEVER** log passwords, API keys, tokens, PII
- [ ] Mask sensitive data in logs (credit card numbers, SSNs)
- [ ] Use sanitization libraries (don't manually redact)

### Log Destinations
- [ ] Application logs → Centralized logging system (ELK, Datadog, CloudWatch)
- [ ] Access logs → Web server/load balancer logs
- [ ] Audit logs → Separate system for compliance (immutable, long retention)
- [ ] Debug logs → Local file (don't ship to central logging in prod)

### Retention & Compliance
- [ ] Normal logs: 7-30 days (depends on MTTR target)
- [ ] Audit logs: 1-7 years (depends on compliance requirement)
- [ ] Logs don't contain secrets (use masking)
- [ ] Access control on log systems (not everyone reads production logs)
- [ ] Logs encrypted in transit and at rest

---

## Metrics Baseline

### Key Metrics (RED method)

| Category | What to measure | Example |
| --- | --- | --- |
| **Rate** | Requests per second | 1,000 req/s |
| **Errors** | Failed requests per second | 10 errors/s (1% error rate) |
| **Duration** | Request latency (p50, p95, p99) | p99 latency = 200ms |

### Infrastructure Metrics

| Resource | Metric | Alert Threshold |
| --- | --- | --- |
| **CPU** | CPU utilization | >80% |
| **Memory** | Memory utilization | >85% |
| **Disk** | Disk usage | >90% |
| **Database** | Connection pool exhaustion | >90% of max connections |
| **Database** | Query latency (slow queries) | >1s |
| **Network** | Bandwidth utilization | >80% |
| **Network** | Packet loss | >0.1% |

### Application Metrics
- [ ] Request rate (req/sec per endpoint)
- [ ] Error rate (errors/sec per endpoint)
- [ ] Latency (p50, p95, p99 per endpoint)
- [ ] Cache hit rate (if using caching)
- [ ] Database connection pool usage
- [ ] Message queue depth (if using queues)
- [ ] Business metrics (e.g., orders/sec, active users)

### Metric Naming Convention
```
service_name.component.metric_name{tag1=value1,tag2=value2}

Examples:
- api.http.request_duration_ms{endpoint=/api/users,method=GET}
- db.query_duration_ms{database=orders,query_type=select}
- cache.hit_rate{cache=redis}
```

### Instrumentation
- [ ] Application instrumentation library installed (OpenTelemetry, StatsD)
- [ ] Key operations have timing metrics (database queries, API calls)
- [ ] Exceptions/errors tracked
- [ ] Custom business metrics captured
- [ ] Metrics published every 10-60 seconds

---

## Tracing Baseline

### Trace Data
Every request should generate a trace showing:
1. Request entry point (API gateway, message queue, scheduled job)
2. Service-to-service calls
3. Database queries
4. Caching operations
5. External API calls
6. Request exit (response sent, message published)

### Implementation
- [ ] Distributed tracing installed (Jaeger, Datadog APM, X-Ray)
- [ ] Trace IDs generated at request entry, propagated to all services
- [ ] Spans created for major operations (database, API calls)
- [ ] Span context passed in HTTP headers (W3C Trace Context standard)
- [ ] Errors attached to spans
- [ ] Sampler configured (e.g., 1% of requests traced in production)

### Example Trace
```
Request: GET /api/users/123  [trace_id: abc123]
  ├─ Authentication [duration: 5ms]
  │   └─ Query: SELECT * FROM users WHERE id=?  [duration: 2ms]
  ├─ Authorization [duration: 1ms]
  ├─ Business Logic [duration: 15ms]
  │   └─ Query: SELECT * FROM user_permissions WHERE user_id=? [duration: 8ms]
  │   └─ API Call: POST https://external-api/validate [duration: 50ms]
  ├─ Serialization [duration: 3ms]
  └─ Response [status: 200, duration: 74ms]
```

---

## Alerts Baseline

### Alert Types

| Type | Purpose | Frequency |
| --- | --- | --- |
| **Immediate** | Service down, data loss, security breach | Alert immediately, page on-call |
| **Urgent** | Degraded performance, high error rate | Alert immediately, page on-call |
| **Important** | Capacity concerns, trends | Alert, morning escalation |
| **Info** | FYI (deployments, scheduled maintenance) | Log, don't alert |

### Alert Criteria

❌ **Avoid alerting on:**
- Single metric spike (unless it's critical)
- Metrics without context (CPU high, but why?)
- Metrics that are too sensitive (triggers every minute)

✅ **Alert on:**
- Error rate > threshold for 2+ minutes
- Latency p95 > threshold for 2+ minutes
- Service health check failing 3+ times
- Disk usage > threshold for sustained period
- Security event (failed login attempts, unauthorized access)

### Alert Destination
- [ ] Immediate/Urgent → Slack + PagerDuty (pages on-call)
- [ ] Important → Slack + Email (morning review)
- [ ] Info → Logs only (no noise)

### Runbook Links
Every alert should link to a runbook:
```
⚠️ High Error Rate on API

Error rate exceeded 5% for 2 minutes.

Current Status:
- Error rate: 7.2%
- Affected endpoint: POST /api/orders
- Started: 2024-03-15 10:30:00

Runbook: [Click here](https://wiki.internal.com/runbooks/api-high-error-rate)

Actions:
1. Check API logs for error messages
2. Check database connection pool status
3. If database issue, check database runbook
4. If configuration issue, check recent deployments
```

---

## Observability for Different Components

### API Services
- [ ] Request rate per endpoint
- [ ] Error rate per endpoint
- [ ] Latency (p50, p95, p99)
- [ ] Status code distribution
- [ ] Authentication failures
- [ ] Request/response size (bandwidth)

### Databases
- [ ] Connection pool usage
- [ ] Query latency (slow query log)
- [ ] Replication lag (if replicated)
- [ ] Storage usage
- [ ] Lock contention
- [ ] Transaction rollback rate

### Message Queues
- [ ] Queue depth (messages waiting)
- [ ] Message processing latency
- [ ] Dead-letter queue size
- [ ] Consumer lag
- [ ] Throughput (messages/sec)

### Scheduled Jobs / Cron
- [ ] Execution duration
- [ ] Success/failure rate
- [ ] Last execution time
- [ ] Missed executions
- [ ] Data processed (if applicable)

### Infrastructure
- [ ] VM/container CPU, memory, disk
- [ ] Network bandwidth
- [ ] Load balancer latency, error rate
- [ ] Kubernetes pod restarts, OOMKilled events

---

## Observability Checklist

- [ ] **Logging**
  - [ ] Structured JSON logs in production
  - [ ] Log levels used correctly (DEBUG, INFO, WARN, ERROR, FATAL)
  - [ ] Trace IDs attached to all logs
  - [ ] Sensitive data masked (no passwords, tokens, PII)
  - [ ] Logs aggregated centrally (ELK, Datadog, etc.)
  - [ ] Retention policy defined

- [ ] **Metrics**
  - [ ] Request rate tracked
  - [ ] Error rate tracked
  - [ ] Latency tracked (p50, p95, p99)
  - [ ] Infrastructure metrics captured (CPU, memory, disk, network)
  - [ ] Custom business metrics (if applicable)
  - [ ] Metrics published every 10-60 seconds
  - [ ] Time-series database stores metrics (Prometheus, CloudWatch, Datadog)

- [ ] **Tracing**
  - [ ] Distributed tracing enabled
  - [ ] Trace IDs propagated across services
  - [ ] Spans created for major operations
  - [ ] Trace data stored (Jaeger, X-Ray, Datadog)
  - [ ] Sample rate configured (1-5% for production)

- [ ] **Alerts**
  - [ ] Error rate alert configured (threshold + duration)
  - [ ] Latency alert configured
  - [ ] Service health alert configured
  - [ ] Capacity alert configured (CPU, disk, connections)
  - [ ] Alert routing configured (Slack, PagerDuty)
  - [ ] Runbooks linked to alerts

- [ ] **Dashboards**
  - [ ] Service health dashboard (status of each service)
  - [ ] Performance dashboard (latency, error rate, throughput)
  - [ ] Infrastructure dashboard (CPU, memory, network)
  - [ ] Business dashboard (application-specific metrics)

---

## Deployment Checklist

Before deploying to production:

- [ ] Logging configured (application logs → central system)
- [ ] Metrics configured (application + infrastructure metrics)
- [ ] Distributed tracing configured (trace IDs generated and propagated)
- [ ] Alerts configured (critical paths monitored)
- [ ] Dashboards created (team can see system health)
- [ ] Runbooks written for on-call (how to debug issues)
- [ ] On-call rotation knows how to read logs/metrics
- [ ] Historical data available (can compare current state to baseline)

---

## Sample Observability Architecture

```
Application
  ├─ Logs → Fluent/Filebeat → ELK / Datadog
  ├─ Metrics → Prometheus exporter / StatsD → Prometheus / CloudWatch
  ├─ Traces → OpenTelemetry → Jaeger / X-Ray
  │
Infrastructure
  ├─ Logs → CloudWatch / ELK
  ├─ Metrics → CloudWatch / Prometheus
  │
Alerting
  ├─ High Error Rate → PagerDuty + Slack
  ├─ High Latency → Slack
  ├─ Capacity Issues → Slack
  │
Dashboards
  ├─ Service Health → Grafana / CloudWatch
  ├─ Performance Trends → Grafana / Datadog
  ├─ Business Metrics → Custom Dashboard
```
