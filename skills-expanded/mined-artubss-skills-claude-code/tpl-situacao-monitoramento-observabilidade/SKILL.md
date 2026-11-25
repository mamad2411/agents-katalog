---
name: tpl-situacao-monitoramento-observabilidade
description: Template do pack (situacao/14-monitoramento-observabilidade.md). Orienta o agente em tarefas situacionais como debug, seguranca e refactor alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: situacao/14-monitoramento-observabilidade.md
  generated_by: install_pack_templates_as_claude_skills
---

# SITUATION: Monitoring & Observability Setup

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `situacao/14-monitoramento-observabilidade.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

## CONTEXT
Use this configuration when setting up or improving observability for a live application — adding metrics, structured logging, distributed tracing, alerting, SLO definitions, or runbook creation. Observability is not an add-on — an unmonitored production service is a liability you can't reason about. This configuration ensures you can answer: "Is the service healthy right now? How do I know? What do I do when it's not?"

## OBJECTIVES
- Instrument all three pillars of observability: metrics, logs, and traces
- Define SLOs/SLIs before incidents reveal you needed them
- Alert on symptoms (what users experience) not just causes (CPU usage)
- Create actionable runbooks linked from every alert
- Enable a developer to debug a production incident using only the observability stack

## APPROACH RULES

1. **Three pillars: metrics, logs, traces.** Metrics tell you something is wrong. Logs tell you what happened. Traces tell you where in the system it happened. You need all three for full observability.

2. **Alert on symptoms, not causes.** "Error rate > 1%" is a symptom — users are affected. "CPU > 80%" is a cause — but doesn't necessarily mean users are impacted. Start with symptom-based alerts.

3. **Every alert must have a runbook.** If an alert fires, the on-call engineer must know what to do. An alert without a runbook is just noise that trains people to ignore alerts. Runbook link must be in the alert body.

4. **SLO > SLA.** Define Service Level Objectives (SLOs) and track your error budget. If you're burning through error budget, slow down feature development and fix reliability. If you have budget headroom, safe to move fast.

5. **Structured logging everywhere.** Never `console.log("user logged in")`. Always `logger.info({ event: "user_login", userId: user.id, ip: req.ip })`. Structured logs are queryable. Strings are not.

6. **Correlation IDs across services.** Every request gets a unique trace/correlation ID at the entry point. Every log line, every downstream call includes that ID. Without this, distributed debugging is a nightmare.

7. **Monitor what users do, not just what systems do.** Business metrics (conversion rate, checkout completions, active users) belong on the same dashboard as technical metrics. When technical metrics are fine but business metrics drop, you have a bug.

## ROUTING TABLE

| If you encounter | Then |
|-----------------|------|
| No logging in the application | Add structured logger first (pino, winston, structlog). All existing console.log → logger.info/error. |
| console.log in production code | Replace with structured logger. console.log is not queryable, not leveled, not structured. |
| Alert without runbook | Write the runbook before the alert goes live. Template: What is this alert? What is the impact? What are the steps? |
| P99 latency not tracked | Add P95 and P99 latency histograms. Averages hide worst-case user experience. |
| Errors logged without stack trace | Fix immediately. Logs without stack traces are unusable for debugging. |
| Alert firing with no action taken | Either fix the condition or remove the alert. Alert fatigue kills incident response. |
| No distributed tracing | Add OpenTelemetry SDK. Instrument HTTP calls, DB queries, queue operations. |
| SLO not defined | Define Error Rate SLO (e.g., 99.9% of requests succeed) and Latency SLO (P95 < 500ms). |
| Logs growing without limit | Add log rotation. Set retention policies. Production logs: 30 days hot, 90 days cold. |
| Multiple services with no centralized logging | Implement log aggregation: ELK stack, Loki + Grafana, or Datadog/New Relic. |

## Three Pillars Implementation Guide

### Metrics (What is happening)
```typescript
// Using prom-client (Node.js)
import { Counter, Histogram, register } from 'prom-client'

const httpRequestDuration = new Histogram({
  name: 'http_request_duration_seconds',
  help: 'HTTP request duration in seconds',
  labelNames: ['method', 'route', 'status_code'],
  buckets: [0.01, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5]
})

const httpRequestTotal = new Counter({
  name: 'http_requests_total',
  help: 'Total HTTP requests',
  labelNames: ['method', 'route', 'status_code']
})

// Expose at /metrics endpoint
app.get('/metrics', async (req, res) => {
  res.set('Content-Type', register.contentType)
  res.send(await register.metrics())
})
```

### Logs (What happened)
```typescript
// Using pino (Node.js)
import pino from 'pino'

const logger = pino({
  level: process.env.LOG_LEVEL || 'info',
  base: { service: 'api', version: process.env.APP_VERSION },
  timestamp: pino.stdTimeFunctions.isoTime
})

// ✅ Good: structured, queryable
logger.info({ event: 'payment_processed', userId, amount, currency }, 'Payment processed')
logger.error({ err: error, userId, requestId }, 'Payment failed')

// ❌ Bad: string only, not queryable
console.log(`Payment failed for user ${userId}: ${error.message}`)
```

### Traces (Where it happened)
```typescript
// Using OpenTelemetry
import { trace, context, propagation } from '@opentelemetry/api'

const tracer = trace.getTracer('my-service')

async function processOrder(orderId: string) {
  const span = tracer.startSpan('processOrder', {
    attributes: { 'order.id': orderId }
  })
  
  try {
    await span.setAttribute('order.status', 'processing')
    const result = await doWork(orderId)
    span.setStatus({ code: SpanStatusCode.OK })
    return result
  } catch (err) {
    span.recordException(err)
    span.setStatus({ code: SpanStatusCode.ERROR })
    throw err
  } finally {
    span.end()
  }
}
```

## SLO Definition Template

```yaml
service: checkout-api
slos:
  - name: Checkout Success Rate
    description: Percentage of checkout requests that succeed
    sli: (sum of successful checkout requests) / (sum of all checkout requests)
    target: 99.5%
    measurement_window: 30 days
    error_budget: 0.5% → 216 minutes/month allowable downtime

  - name: Checkout Latency
    description: P95 latency for checkout endpoint
    sli: 95th percentile response time
    target: < 1000ms
    measurement_window: 30 days

alerts:
  - name: Checkout Error Rate Burn
    condition: Error budget burn rate > 5× for 1 hour
    severity: page (wake someone up)
    runbook: docs/runbooks/checkout-errors.md
```

## DO NOT

- **DO NOT** set up monitoring after the first incident — it's too late then
- **DO NOT** log PII (email, name, phone, card numbers) — mask or hash before logging
- **DO NOT** create alerts that can't be acted on — each alert needs a clear response procedure
- **DO NOT** use average latency as your primary metric — use P95 and P99
- **DO NOT** monitor only infrastructure (CPU, memory) and ignore application-level health
- **DO NOT** alert with CRITICAL severity on things that are informational
- **DO NOT** delete old logs without understanding retention requirements (GDPR, compliance)

## OUTPUT FORMAT

For each monitoring setup, deliver:

**Observability Coverage Matrix:**
```markdown
| Signal | Tool | Coverage | Retention | Alert? |
|--------|------|----------|-----------|--------|
| App logs | Loki | INFO+ in prod. DEBUG in staging | 30 days | On ERROR+ |
| Infrastructure metrics | Prometheus | CPU, memory, disk, network | 90 days | On threshold |
| App metrics | Prometheus | Request rate, error rate, latency histograms | 90 days | On SLO burn |
| Traces | Jaeger/Tempo | Sample rate: 10% prod, 100% staging | 7 days | On trace error |
| Uptime | Healthchecks.io | External probe every 60s | 365 days | On unavailable |

**Runbook Inventory:**
| Alert | Runbook | Owner | Last Verified |
|-------|---------|-------|---------------|
| High error rate | docs/runbooks/high-error-rate.md | Platform | 2024-01-01 |
```

## QUALITY GATES

- [ ] P95 and P99 latency tracked for all user-facing endpoints
- [ ] Error rate (5xx rate) tracked and alerting at > 1%
- [ ] Every log entry is structured JSON with at minimum: timestamp, level, service, message
- [ ] Correlation/trace IDs present in all logs for every request
- [ ] At least one SLO defined with error budget tracked on dashboard
- [ ] Every production alert has a linked runbook
- [ ] Runbook tested: follow it cold and confirm it resolves the described scenario
- [ ] PII not present in any log line (verified by audit sample)
- [ ] On-call rotation documented and first responder always identified
- [ ] Post-mortem template ready before first incident (not after)
