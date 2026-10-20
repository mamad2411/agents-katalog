---
name: observability-pro
description: "Monitoring, logging, tracing, alerting, dashboards, SLOs, incident response. Use when setting up or improving observability stacks."
---

# Observability Pro

## Purpose

Build comprehensive observability: structured logging, distributed tracing, metrics, dashboards, SLO-based alerting, and incident response runbooks.

## When to Use

**Use this when:**
- Setting up structured logging, distributed tracing, or Prometheus metrics for a service
- Defining or reviewing SLOs, error budgets, and alerting rules
- Writing or improving incident response runbooks and on-call documentation

**Use this ESPECIALLY when:**
- A production system lacks request tracing across service boundaries and debugging requires log archaeology
- Alerts are firing constantly (alert fatigue) or never firing when they should (silent failures)
- A post-incident review reveals the team lacked the visibility to detect or diagnose the issue quickly

**Don't skip when:**
- Adding a new microservice — it must emit the Four Golden Signals from day one
- Onboarding a new service to an existing observability stack (OTel, Grafana, PagerDuty)
- Any change touches logging configuration, metric collection, or alerting thresholds

## Core Patterns

### 1. Structured Logging

```typescript
// Pino / Winston structured logging
import pino from 'pino'

const logger = pino({
  level: process.env.LOG_LEVEL || 'info',
  formatters: {
    bindings: (bindings) => ({ pid: bindings.pid, host: bindings.hostname }),
  },
  redact: {
    paths: ['req.headers.authorization', 'req.body.password', 'req.body.ssn', '*.creditCard'],
    censor: '[REDACTED]',
  },
  serializers: {
    req: (req) => ({ method: req.method, url: req.url, requestId: req.id }),
    res: (res) => ({ statusCode: res.statusCode }),
    err: pino.stdSerializers.err,
  },
})

// Usage
logger.info({ req, res, duration: 42 }, 'request completed')
logger.error({ err, requestId: req.id }, 'payment processing failed')
logger.warn({ userId, threshold: 0.9 }, 'user approaching rate limit')
```

### 2. Distributed Tracing (OpenTelemetry)

```typescript
import { trace, context } from '@opentelemetry/api'
import { NodeTracerProvider } from '@opentelemetry/sdk-trace-node'
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-http'

const provider = new NodeTracerProvider()
provider.register()

const tracer = trace.getTracer('senior-dev-squad')

// Auto-instrument HTTP, gRPC, DB calls
// Manual instrumentation for custom spans
async function processPayment(orderId: string) {
  const span = tracer.startSpan('payment.process', {
    attributes: { 'order.id': orderId },
  })

  return await context.with(trace.setSpan(context.active(), span), async () => {
    try {
      const result = await stripeClient.charges.create(...)
      span.setStatus({ code: SpanStatusCode.OK })
      return result
    } catch (err) {
      span.recordException(err)
      span.setStatus({ code: SpanStatusCode.ERROR, message: err.message })
      throw err
    } finally {
      span.end()
    }
  })
}
```

### 3. Metrics & Dashboards

```typescript
// Prometheus metrics
import prometheus from 'prom-client'

const httpRequestDuration = new prometheus.Histogram({
  name: 'http_request_duration_seconds',
  help: 'HTTP request duration in seconds',
  labelNames: ['method', 'path', 'status'],
  buckets: [0.01, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10],
})

const activeRequests = new prometheus.Gauge({
  name: 'http_requests_active',
  help: 'Number of active HTTP requests',
})

// The Four Golden Signals:
// 1. Latency: http_request_duration_seconds (histogram)
// 2. Traffic: http_requests_total (counter, by route)
// 3. Errors: http_requests_errors_total (counter, by status)
// 4. Saturation: memory_usage_bytes, cpu_usage_percent (gauges)
```

### 4. SLOs & Alerting

```yaml
# prometheus-alerts.yml
groups:
  - name: senior-dev-squad
    rules:
      # Latency SLO: 99% of requests < 500ms
      - alert: HighLatency
        expr: |
          histogram_quantile(0.99,
            rate(http_request_duration_seconds_bucket[5m])
          ) > 0.5
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "P99 latency > 500ms for 5 minutes"
          runbook: "https://runbooks.seniordev.io/high-latency"

      # Error budget: < 0.1% errors over 30 days
      - alert: ErrorBudgetBurning
        expr: |
          (1 - sum(rate(http_requests_errors_total[1h]))
                / sum(rate(http_requests_total[1h])))
          < 0.999
        for: 1h
        labels:
          severity: page
        annotations:
          summary: "Error rate > 0.1% in last hour"
```

### 5. Incident Response Runbook

```markdown
## Incident: High Latency / Errors

### Triage (0-5 min)
1. Check dashboard: link
2. Check recent deploys: link
3. Check alerts: PagerDuty
4. Acknowledge incident

### Investigate (5-15 min)
1. Check logs: `grep requestId=XYZ logs/app.log | jq .`
2. Check traces: Jaeger / Grafana Tempo
3. Check metrics: CPU, memory, DB connections
4. Check recent code changes: git log --oneline -10

### Mitigate
- Rollback: `git revert HEAD && git push`
- Scale up: `kubectl scale deployment app --replicas=5`
- Feature flag: `cli feature disable new-checkout`
- Rate limit: Increase limits for known good users

### Resolve
1. Confirm fix in staging
2. Deploy fix
3. Monitor for 15 minutes
4. Update status page
5. Schedule postmortem
```

### Checklist

- [ ] Structured JSON logging (not text)
- [ ] Request IDs propagated across all services
- [ ] PII redacted from logs automatically
- [ ] Distributed tracing across all services (OpenTelemetry)
- [ ] The Four Golden Signals: latency, traffic, errors, saturation
- [ ] SLOs defined and measured (SLI → SLO → error budget)
- [ ] Alert fatigue prevention (alert on symptoms, not causes)
- [ ] Runbooks for every alert type
- [ ] Dashboards for: app, infra, business, and SLOs
- [ ] Log retention policy (hot/warm/cold tiers)
- [ ] On-call rotation with escalation policy
- [ ] Postmortem template with blameless culture

## Related Skills

- **devops-release-engineer** — pairs directly: deploy pipelines emit the logs and metrics this skill instruments; coordinate when adding observability to a new service at release time
- **backend-senior-engineer** — structured logging and OpenTelemetry span instrumentation live in application code; involve this skill when adding tracing to business logic layers
- **performance-engineer** — SLO thresholds and the Four Golden Signals overlap with latency profiling; use together when diagnosing systemic slowdowns
- **docker-k8s-pro** — container and pod metrics (CPU, memory, restart counts) feed Prometheus; coordinate when setting up kube-state-metrics or Grafana dashboards for a Kubernetes workload
- **security-reviewer** — log redaction of PII and secrets is a security concern as much as an observability one; cross-reference when defining redact paths in structured loggers
- **cloud-security-auditor** — CloudTrail, VPC Flow Logs, and cloud-native alerting are the cloud layer of observability; use when instrumenting AWS/GCP/Azure infrastructure alongside application-level signals
