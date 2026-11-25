---
name: observability-and-slos
description: Instruments a system so production is explainable, and defines SLIs, SLOs and alerts worth waking for. Triggers - we could not tell what happened during the outage, what should we log, define an SLO, metrics, tracing, error budget, alert noise.
---

# Observability and SLOs

Monitoring tells you a known thing broke. Observability lets you answer a
question you did not anticipate, from data already emitted. The test is
concrete: **can you diagnose a novel production problem without deploying new
code?** If not, the system is not observable, however many dashboards exist.

Instrumentation is written with the feature, like tests. Retrofitting it during
an incident is archaeology.

## The three signals, used for their strengths

| Signal | Answers | Cost | Discipline |
|---|---|---|---|
| **Metrics** | "How much, how often, how slow" over time | Cheap, bounded | Low cardinality. A user id as a label will bankrupt you |
| **Logs** | "What exactly happened in this one case" | Expensive at volume | Structured, sampled, correlated |
| **Traces** | "Where did the time go across services" | Moderate | Propagate context across every boundary, including queues |

They are joined by a **correlation id** propagated through every call, log line,
span and message header. Without it, three signals are three disconnected
stories. This is the single highest-value thing to get right.

## Logging that helps later

- **Structured** (key-value/JSON), never interpolated prose. `user_id=123` is
  queryable; `"user 123 failed"` is not.
- Every line carries: correlation id, actor or tenant, operation, outcome,
  duration.
- Log **decisions and transitions**, not traversal. "Chose path B because X" is
  worth keeping; "entering function" is noise you pay to store.
- Levels with meaning: `ERROR` = a human must act; `WARN` = degraded but
  handled; `INFO` = business-significant event; `DEBUG` = off in production.
  If `ERROR` is noisy, people stop reading it and the one that mattered is lost.
- **Never log** secrets, tokens, or personal data. Redact at the logger.
- Log the failure **once**, where it is handled — not at every level it passes
  through.

## Metrics worth having

For every service, the four golden signals: **latency** (histogram, not average
— averages hide the tail), **traffic**, **errors** (rate, by class), and
**saturation** (the resource nearest its limit).

For every business capability, the events that matter: orders placed, jobs
completed, records ingested, drafts approved. **A business metric catches
outages that infrastructure metrics miss** — a service returning 200 while
processing nothing is invisible to CPU graphs.

Cardinality discipline: labels are for bounded dimensions (status, region,
endpoint). Unbounded values (user id, request id, URL with parameters) belong
in logs and traces.

## SLIs, SLOs, error budgets

- **SLI** — a measurement of user-visible behavior: *proportion of requests
  served successfully under 300 ms*. Measure as close to the user as possible;
  server-side success with a broken CDN is not success.
- **SLO** — the target for that SLI over a window: *99.5% over 30 days*.
- **Error budget** — the allowed failure: 0.5% of 30 days ≈ 3.6 hours.

Pick targets you can actually operate. 99.9% is 43 minutes a month — including
deploys, dependency failures and mistakes. Every extra nine multiplies cost.
Start lower and raise deliberately.

The budget is what makes an SLO useful: it converts "be reliable" into a
decision rule. Budget healthy → ship faster. Budget exhausted → reliability
work takes priority until it recovers. Agree the policy **before** the first
breach, when it is not personal.

## Alerts

Alert on **symptoms users feel**, not on causes. High CPU is not an incident;
requests failing is.

Every alert must satisfy all four:

1. A user-visible impact or an imminent one
2. A human action is required *now* — otherwise it is a dashboard or a ticket
3. A runbook exists with the first three steps (`incident-response`)
4. It fires rarely enough that people still read it

Burn-rate alerting on the error budget (fast burn → page; slow burn → ticket)
beats static thresholds: it scales with the actual promise and avoids paging
for a blip that consumes 0.1% of the budget.

An alert that fired more than ~3 times without action is broken — fix or delete
it. Alert fatigue is the mechanism by which real incidents get ignored.

## Exit checklist

- [ ] Correlation id generated at the edge and propagated everywhere, including
      async boundaries
- [ ] Logs structured, with actor, operation, outcome and duration
- [ ] No secrets or personal data in logs; failure logged once
- [ ] Four golden signals plus at least one business metric per capability
- [ ] Metric labels bounded; no unbounded cardinality
- [ ] SLI measured from the user's perspective; SLO and window written down
- [ ] Error budget policy agreed before it is needed
- [ ] Every alert: user impact, immediate action, runbook, low noise
