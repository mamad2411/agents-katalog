---
name: observability-readiness
description: Logging, metrics, tracing, alerting, and audit trails so production problems are diagnosable from the outside. Use when adding logging, setting up monitoring or alerts, instrumenting a service, preparing for launch, or when the user says "logging", "monitoring", "observability", "alerts", "metrics", "audit trail", or "how do I know if it's working in prod".
---

# Observability Readiness

You cannot SSH into a bug report. Observability is the difference between "a user says it's broken" and knowing *which request, which tenant, which dependency, how often, since which deploy*. Instrument as you build — retrofitting during an incident is archaeology.

## The standard: every incident answerable in 4 questions

Design instrumentation so that during any incident you can answer, from dashboards/logs alone:
1. **Is it broken?** (error rate, health) 2. **Since when?** (deploy marker, first occurrence) 3. **For whom?** (which tenant/user/endpoint slice) 4. **Because of what?** (the failing dependency or code path, with one exemplar request traced end-to-end).

If any question requires adding a log line and redeploying to answer — the instrumentation failed; fix that gap after every incident.

## Logging rules

- **Structured (JSON/key-value), always.** `logger.info("payment_recorded", invoice_id=..., amount=..., tenant=...)` — grep-able, filterable, aggregatable. Prose logs are diary entries.
- **Correlation ID on every request**: generate/accept a request ID at the edge, carry it through every log line, background job it spawns, and outbound call header. This single habit turns log soup into stories.
- Levels mean things: `ERROR` = someone should look (a page-worthy fact, not "user typed wrong password"); `WARNING` = degraded/retried/suspicious; `INFO` = business events (order created, login, job completed); `DEBUG` = off in prod by default. If ERROR fires routinely, alerts die of fatigue.
- Log the *decision points*: every request's outcome (status, duration, principal), every external call (target, duration, outcome), every background job (start, outcome, duration), every auth failure with reason.
- Never log: secrets, tokens, passwords, full card/account numbers, raw PII you don't need (mask: `9000****01`). Dev-mock OTP logging must be gated by environment, not habit.
- Exceptions log with stack trace exactly **once**, at the level that handles them — catch-log-rethrow at every layer produces 5 copies and 0 clarity.

## Metrics — the minimum dashboard per service

- **Rate, errors, duration** (p50/p95/p99 — averages hide everything) per endpoint.
- Saturation: DB connection pool usage, queue depth + oldest-message age, memory/CPU, disk.
- **Business pulse**: 2–5 counters that mean "the product works" — orders/hour, logins/hour, OTPs delivered. Infrastructure metrics can be green while the business flatlines (e.g., SMS provider silently failing).
- Deploy markers on every graph — "what changed" is the first diagnostic question and deploys are the usual answer.

## Alerting — the discipline

- Alert on **symptoms users feel** (error rate up, latency up, queue age growing, business pulse flat), not on causes (CPU 80%). Causes go on dashboards for diagnosis, not pages.
- Every alert must be: actionable (there's something to *do*), with a threshold you can defend, and routed by severity (page vs next-morning). An alert nobody acts on gets deleted or demoted — an ignored channel of 50 daily alerts equals zero alerts.
- The three alerts every product needs from day one: service down (external uptime check hitting a real endpoint), error rate spike, and background-queue age (silent worker death is the classic invisible outage).

## Audit trail (separate concern from debugging)

For anything with money, inventory, or admin power: an append-only record of *who did what to what, when, from where* — written in the same transaction as the change, immutable (no UPDATE/DELETE grants), retained per compliance needs. This is a product feature and a legal shield, not logging.

## Pre-launch checklist

- [ ] Error tracker (Sentry-class) wired with release/version tagging, before launch — day-one bugs are the most frequent bugs.
- [ ] Uptime check on a real user-path endpoint, from outside your infrastructure.
- [ ] One request traceable end-to-end by ID through logs (test it: pick a request, tell its story).
- [ ] Log retention and access story known (where do logs go, for how long, who can see PII).
- [ ] You've rehearsed one fake incident: "payments are failing" — and answered the 4 questions from tooling alone.
