---
name: logging-strategy
description: Define a service's logging strategy — structured JSON, level discipline, redaction, sampling for noisy paths, cost-aware retention.
---

# logging-strategy

> Pin a logging strategy that's useful at 3am and not the company's biggest cloud bill.

## When to use

- A new service is being built and the logging is "println for now".
- An existing service is generating gigabytes a day with no one knowing what's in there.

## Procedure

1. **Structured JSON, one event per line**. No multi-line stack-trace lines without a delimiter.
2. **Required fields per event**:
   - `ts` — RFC3339 with timezone.
   - `level` — one of `debug | info | warn | error`.
   - `service` — service name.
   - `event` — short event name (snake_case).
   - `msg` — human-readable.
   - `trace_id` + `span_id` — when in a request context.
3. **Level discipline**:
   - **DEBUG** — off in prod by default. Toggleable per service or per request via a header.
   - **INFO** — significant state transitions. NOT request-level. NOT "got here".
   - **WARN** — recoverable anomaly the team should notice next business day.
   - **ERROR** — failed operations that need investigation.
4. **Per-request logs**:
   - One **access log** per inbound request, structured, with status, latency, route.
   - No additional info-level log per request unless something interesting happened.
5. **Redaction** — never log: passwords, tokens, full credit card numbers, full SSNs/PII. Log a hash or last-4 if needed. Use a redaction wrapper at the logger level, not per call site.
6. **Sampling** — for high-volume paths, sample debug/info logs (e.g. 1%). Always log 100% of errors.
7. **Retention** — match to the audit and debugging need, not the platform default.
   - Hot search: 7–14 days.
   - Cold archive (S3 etc.): 90 days or per compliance.
8. **No log-and-throw**. Log at the boundary that decides what to do (handler / job runner). Not at every catch.

## Output

```text
Logging strategy: refund-service

Format: JSON, one event per line.

Required fields: ts, level, service, event, msg, trace_id, span_id.

Levels in prod: INFO and above. DEBUG opt-in via X-Debug header (rate-limited to oncall).

Access logs:
  One per request. Fields: route, method, status, latency_ms, request_id,
  user_id (when authenticated, never anonymous user_id).

Redaction at logger:
  - card_number → last4 only.
  - email → hashed unless explicit allow-list (e.g. support tools).
  - bearer tokens → never.

Sampling:
  POST /healthz access log: 1%.
  Other info logs: 100%.
  Errors: 100%.

Retention:
  Hot search (Loki): 7 days.
  Cold archive (S3): 90 days; lifecycle to Glacier after 30.

Cost target: < $250/mo/service at current traffic. Reviewed monthly.
```

## Anti-patterns to avoid

- DEBUG-level logs in prod by default.
- Logging requests AND every catch block (double-bookkeeping).
- Logging the full request body "for debugging".
- "Logged and rethrew" patterns.
- Retention "forever" because no one knows what to delete.
