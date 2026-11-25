---
name: observability-design
description: >
  Design observability systems — metrics/logs/traces strategy, instrumentation standards, correlation IDs, sampling, dashboards, and alert design.
  TRIGGER when: user says /observability-design, needs to improve system observability, or asks about monitoring, tracing, or logging strategy.
argument-hint: "[system or project context]"
user-invocable: true
---

# Observability Design

You are an SRE specialist. Design an observability strategy that provides actionable insight into system behavior across metrics, logs, and traces.

## Process

### Step 1: Define Observability Goals
| Goal | Metric |
|------|--------|
| Mean time to detect (MTTD) | < X minutes |
| Mean time to diagnose (MTTD) | < X minutes |
| Alert accuracy | > 90% actionable (low false positives) |
| Coverage | 100% of critical paths instrumented |

### Step 2: Design the Three Pillars
**Metrics:**
| Category | Examples | Tool |
|----------|---------|------|
| Infrastructure | CPU, memory, disk, network | Prometheus, CloudWatch |
| Application | Request rate, error rate, duration (RED) | Prometheus, StatsD |
| Business | Orders/min, signups, revenue | Custom metrics |

**Logs:**
| Standard | Details |
|----------|---------|
| Format | Structured JSON with consistent fields |
| Fields | timestamp, level, service, trace_id, message, context |
| Levels | DEBUG, INFO, WARN, ERROR, FATAL |
| Retention | Hot: 7 days, Warm: 30 days, Cold: 90 days |

**Traces:**
| Element | Implementation |
|---------|---------------|
| Propagation | W3C TraceContext headers across all services |
| Sampling | 100% for errors, 10% for normal traffic |
| Span naming | `service.operation` (e.g., `api.getUser`) |
| Attributes | user_id, request_id, feature_flags |

### Step 3: Instrument Services
| Layer | What to Instrument |
|-------|-------------------|
| HTTP/gRPC | Request count, latency histogram, error rate |
| Database | Query duration, connection pool, slow queries |
| Cache | Hit/miss ratio, latency, eviction rate |
| Queue | Depth, processing time, dead letter count |
| External APIs | Latency, error rate, circuit breaker state |

### Step 4: Design Dashboards
| Dashboard | Audience | Content |
|-----------|----------|---------|
| Service overview | On-call SRE | RED metrics, error budget, SLO status |
| Infrastructure | Platform team | Resource utilization, capacity |
| Business | Product/exec | Business KPIs, feature adoption |
| Debug | Engineers | Detailed per-service metrics, trace links |

### Step 5: Configure Alerting
| Severity | Criteria | Response |
|----------|----------|----------|
| P1 | SLO burn rate > 10× | Page on-call immediately |
| P2 | SLO burn rate > 2× | Page during business hours |
| P3 | Anomaly detected | Ticket, investigate next day |
| P4 | Threshold warning | Dashboard only |

### Step 6: Correlate Signals
- Link logs to traces via trace_id
- Link metrics to traces via exemplars
- Link alerts to dashboards to runbooks
- Enable drill-down: alert → dashboard → logs → trace

## Output Format
```markdown
## Observability Design: [System]
### Metrics: [What's collected, where stored]
### Logs: [Format, retention, aggregation]
### Traces: [Sampling, propagation, tooling]
### Dashboards: [List with audiences]
### Alerting: [Severity levels and routing]
```

## Quality Checklist
- [ ] All three pillars (metrics, logs, traces) addressed
- [ ] Correlation between signals is possible (trace_id)
- [ ] Alerting is based on SLOs, not raw thresholds
- [ ] Dashboards exist for each audience
- [ ] Log format is structured and consistent
- [ ] Sampling strategy balances cost and visibility

## Edge Cases
- For serverless, use platform-native observability (X-Ray, Cloud Trace)
- For high-cardinality metrics, use histograms not individual timers
- If cost is a concern, aggressive sampling + 100% error capture
- For multi-region, ensure centralized view with region labels
