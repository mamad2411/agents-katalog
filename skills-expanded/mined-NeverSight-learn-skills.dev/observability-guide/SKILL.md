---
name: observability-guide
description: Design vendor-agnostic observability so you can ask any question of a running system. Use when adding logging, metrics, traces, wide events, alerting, uptime monitoring, error tracking, or session replay; shipping a production feature; or investigating an incident with missing telemetry.
---

# Observability Guide

## Definition

Observability is the ability to ask **any question** about a running system and get an answer — without deploying new code. If answering a question requires adding an instrument and redeploying, the system is not observable.

## When to use

- Adding logging, metrics, traces, wide events, alerting, uptime monitoring, error tracking, or session replay.
- Shipping a production feature that needs telemetry.
- Investigating an incident and finding gaps in telemetry.
- Designing an alerting or SLO strategy.

**Not for** live hands-on debugging of a running issue — use a dedicated debugging skill for that. This skill designs and improves telemetry.

## Data shapes — the five orders of instrumentation

| Shape | Question it answers |
|-------|---------------------|
| Error | What broke? |
| Trace | Where did time go? |
| Log | What was true and why? |
| Metric | How is it trending? |
| Wide Event | What happened, with full context, so I can slice by any dimension? |

### Wide events, briefly

A wide event is **one structured event per request (or hop)** carrying 20–100+ attributes across infra, HTTP, user, business, dependencies, feature flags, and error context. It is high-cardinality and queryable without pre-aggregation. The standard implementation is an **OpenTelemetry span with rich attributes**. See `references/wide-events.md`.

## Supporting disciplines

| Discipline | Purpose | Example tools |
|------------|---------|---------------|
| Uptime monitoring | External reachability checks | Uptime Kuma, UptimeRobot |
| Alerting / incident management | Route and manage alerts | Alertmanager, Incident.io, PagerDuty |
| Error tracking | Capture and triage exceptions | Sentry, Rollbar |
| Session replay | Replay user sessions | (replay in DataDog/Sentry/others) |
| APM backends | Store and query signals | DataDog, Grafana, Honeycomb, New Relic |

## Quick process

1. Define the questions you need answered.
2. Pick the data shapes that answer them.
3. Instrument (OpenTelemetry-first).
4. Set up alerting and uptime checks.
5. Verify a question end-to-end.

## Proactive bug detection

- **Release markers** — annotate deploys so differential analysis finds regressions.
- **Error-rate baselines** — alert on sustained deviation from normal, not single errors.
- **SLO-based alerts** — alert when error budget burns faster than planned.
- **Anomaly detection** — flag metric behavior outside learned bounds.
- **Synthetic checks** — scripted probes of critical user journeys.
- **Drill-down workflow** — `metric spike → trace → wide event → code fix`.

## Vendor note

Instrument with **OpenTelemetry** as the vendor-neutral baseline; exporters emit the same signals to any backend (DataDog, Grafana, Honeycomb, New Relic, Sentry). No vendor lock-in in the code.

## References

- `references/wide-events.md` — what wide events are and how to emit them.
- `references/signals.md` — overlap tie-breakers, retention, sampling, code snippets.
- `references/red-use-alerting.md` — RED/USE metrics, alerting rules, SLOs, uptime.
- `references/opentelemetry-quickstart.md` — OTel setup, spans, propagation, sampling.