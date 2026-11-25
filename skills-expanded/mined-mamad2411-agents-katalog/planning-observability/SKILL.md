---
name: planning-observability
description: Plans and implements observability — SLIs/SLOs and error budgets, structured logging, metrics (RED/USE), distributed tracing with OpenTelemetry, dashboards, and actionable alerts. Use when instrumenting a service, defining SLOs, setting up monitoring or alerting, reducing alert noise, or preparing a service for production.
metadata:
  role: system-architect
  version: "1.0"
---

# Planning observability

Goal: answer "is it working for users?" at a glance, and "why not?" within minutes.

## Workflow

1. **Pick critical user journeys** (login, search, checkout). Observability starts from the user, not the host.
2. **Define SLIs** per journey — a ratio of good events to valid events:
   - Availability: `successful requests / valid requests`
   - Latency: `requests faster than X ms / valid requests`
   - Freshness/correctness for pipelines: `records processed within N min / total`
3. **Set SLOs** with a window: "99.9% of checkout requests succeed over 28 days." Error budget = 1 − SLO. Agree on a policy for when the budget is spent (freeze risky launches, prioritize reliability work).
4. **Instrument** with OpenTelemetry (vendor-neutral) — see signals below.
5. **Alert on symptoms, not causes:** page on SLO burn rate; send cause-level signals (CPU, disk) to dashboards or tickets.
6. **Build dashboards** top-down: SLOs → RED per service → USE per resource → drill into traces/logs.
7. **Write a runbook** for every paging alert: what it means, first checks, mitigation, escalation.

## Signals

**Metrics**
- Services — RED: **R**ate, **E**rrors, **D**uration (histograms, not averages).
- Resources — USE: **U**tilization, **S**aturation, **E**rrors.
- Keep label cardinality bounded: never use user IDs, request IDs, or raw URLs as metric labels.

**Logs**
- Structured JSON, one event per line, with `timestamp`, `level`, `service`, `trace_id`, `span_id`, and a stable `event` name.
- Log decisions and failures, not every step. No secrets or PII; redact at the source.

**Traces**
- Propagate W3C Trace Context (`traceparent`) across every HTTP/gRPC call and message.
- Auto-instrument frameworks first; add manual spans around business operations and external calls.
- Use tail-based sampling to keep all errors and slow traces.

Correlate all three via `trace_id`.

## Alerting rules

Multi-window, multi-burn-rate alerts on SLOs (Google SRE Workbook), e.g. for a 99.9% / 30-day SLO:
- Page: burn rate ≥ 14.4 over 1 h **and** over 5 min (2% budget in 1 h)
- Page: burn rate ≥ 6 over 6 h **and** over 30 min (5% budget in 6 h)
- Ticket: burn rate ≥ 1 over 3 days

Every page must be actionable, urgent, and user-impacting. Delete or downgrade alerts nobody acts on.

## Readiness checklist

- [ ] SLIs/SLOs documented per critical journey
- [ ] RED metrics + traces + structured logs with trace correlation
- [ ] Burn-rate alerts routed to on-call; each has a runbook
- [ ] Dashboards: SLO overview, service RED, dependency health
- [ ] Health endpoints (liveness vs readiness) separated
- [ ] Synthetic checks for external availability
