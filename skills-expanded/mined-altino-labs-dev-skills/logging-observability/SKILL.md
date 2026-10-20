---
name: logging-observability
description: >
  Logging and observability for any stack: what to log at each layer (and what never to log),
  log levels by environment, correlation IDs (OpenTelemetry / W3C traceparent as the default
  path, hand-rolled when that is costly), structured log format and why JSON in production,
  error tracking for uncaught errors and performance, the health check endpoint (liveness vs
  readiness), application metrics and what to monitor and alert on, and the required
  configuration. Invoke automatically when implementing logging at any layer,
  request interceptors/middlewares, uncaught error handling, error-tracker integration, health
  checks or metrics, in any language or framework.
---

# Logging & Observability

> **How to read the examples.** Every example in this skill is framework-free TypeScript —
> plain classes and functions, no decorators, no framework, no logging, error-tracking or
> metrics library. Read it as pseudo-code and translate it to the project's language and
> idioms. Stack-specific implementations (the framework's logger, the request interceptor /
> middleware, the error-tracker SDK setup, the health controller, the metrics instrumentation,
> the env var names) live in stack plugins — e.g. `dev-patterns:logging-observability` for
> NestJS/Fastify — and in the project's own delta skill
> (`.claude/skills/<project>-logging-observability/`), when they exist. Load them together with
> this skill.

## Who logs

- One logger per class/module, scoped with the class name as context — never a shared
  instance across classes and never bare `print`/`console` calls scattered through the code.
- The **domain layer (entities, value objects) never logs.** Logging happens only in use
  cases, infrastructure, the interface adapters (controllers/handlers, guards/middleware) and
  subscribers. Layers: `dev-core:clean-architecture`.
- Levels: *info* for normal operational events, *warn* for recoverable/degraded situations,
  *error* for failures that were caught and handled (or are about to be rethrown).

---

## What to log at each layer

### Allowed and required

| Layer | What to log |
|---|---|
| HTTP (request interceptor/middleware, if added) | Method, URL, status, duration, correlation ID |
| Use case | Failures on operations with a fallback/best-effort path (see below), relevant business decisions |
| Repository | Slow queries (>500ms), database errors |
| Event bus | Subscriber failure (*warn*, not *error* — one subscriber failing shouldn't look as severe as an unhandled exception; see `dev-core:domain-events`) |
| Scheduled job | Start, end, and summary result of each execution |
| Auth | Successful login, auth failure, token refresh |

**Best-effort / fire-and-forget pattern:** when a use case swallows a failure to keep
returning a generic response (e.g. password-reset and registration flows that must return
the same response whether or not the account exists, to avoid account enumeration), the
`catch` block must still log the error before continuing — silently swallowing the exception
with no log call makes the failure invisible everywhere.

```typescript
try {
  await this.mailer.sendResetLink(email);
} catch (err) {
  this.logger.error(`reset link not sent: ${(err as Error).message}`);   // never silent
}
return GENERIC_RESPONSE;
```

**Verify the underlying SDK actually throws before trusting a try/catch to catch anything.**
Some third-party clients resolve successfully with an `{ error }` field instead of rejecting.
A catch block around a call like that is dead code — nothing ever throws into it — and the
failure stays invisible despite the logging being "in place." Test the actual failure path
live, not just with a mock that assumes textbook reject-on-error behavior.

### Never log

- Passwords, access tokens, refresh tokens, API keys
- Sensitive personal data (government IDs, health or financial data, credentials)
- Full request body content in production
- Complete stack traces in API responses (internal logs only — `dev-core:error-handling`)

Identify the subject, never the secret: `{ email, error: err.message }`, not
`{ email, password, error }`.

---

## Log levels by environment

| Environment | Levels emitted |
|---|---|
| production | info, warn, error |
| staging | info, warn, error, debug |
| development | info, warn, error, debug, verbose/trace |

Configure the level once at bootstrap from configuration (not per call site), so debug and
verbose output disappear outside development without code changes.

---

## Correlation ID — the default path, and when to evaluate first

A correlation ID is a per-request identifier, accepted from an incoming header or generated at
the edge, echoed back on the response, and attached to every log line (and error report)
produced while handling that request — so one request can be traced across layers, services
and the error tracker.

**Default path: OpenTelemetry.** Where the stack has mature OpenTelemetry instrumentation
(Java/Spring, .NET, Python, Go — and Node), use it instead of a hand-rolled ID: the
auto-instrumentation accepts and propagates the W3C **`traceparent`** header, the trace ID *is*
the correlation ID, and it reaches log lines through the language's context propagation —
**MDC** in Java (Logback/Log4j2 OTel appenders), **`ILogger` scopes** in .NET (trace/span IDs
are added to scopes automatically), **`contextvars`** in Python (the OTel logging
instrumentation), **`context.Context`** in Go (pass `ctx` to `slog` with an OTel bridge). The
same trace then also links the error tracker and any downstream service. On these stacks this
is cheap enough to be a day-one default.

**Evaluate before adding — where it is costly.** On stacks without a request-scoped context
mechanism the logger can use, or where OTel instrumentation is immature, a correlation ID is
a legitimate next step once request volume or incident frequency makes plain log output hard
to trace — but **not a day-one requirement**. Hand-rolling it means auditing every existing
log call site so the ID actually reaches them (it doesn't happen automatically just because
the ID exists on the request; use the stack's request-scoped context mechanism where one
exists — e.g. `AsyncLocalStorage` in Node). Don't build it speculatively; add it when there's
a real incident-response need. The hand-rolled shape below uses an `x-correlation-id` header;
prefer accepting `traceparent` too if anything upstream sends it.

```typescript
// Edge middleware — framework-free shape (hand-rolled path)
function correlationId(req: Request, res: Response, next: () => void) {
  const id = req.headers['x-correlation-id'] ?? randomUUID();
  req.correlationId = id;
  res.setHeader('x-correlation-id', id);
  next();
}

// Request logging wrapper — one line per request, success or failure
async function logRequest(req: Request, res: Response, handler: () => Promise<void>) {
  const startedAt = Date.now();
  try {
    await handler();
    logger.info(`${req.method} ${req.url} ${res.statusCode} +${Date.now() - startedAt}ms [${req.correlationId}]`);
  } catch (err) {
    logger.error(`${req.method} ${req.url} failed +${Date.now() - startedAt}ms [${req.correlationId}]: ${(err as Error).message}`);
    throw err;
  }
}
```

Exclude health-check and metrics-scrape routes from request logging — every probe would
otherwise add a log line.

---

## Structured log format

Many frameworks' default logger writes human-readable text, **not** structured JSON. That's
sufficient for local development and reading the hosting platform's log viewer directly.
Structured JSON only exists if a JSON-emitting transport is deliberately configured — don't
assume downstream tooling can query fields like `correlationId` or `durationMs` unless
something actually emits this shape.

```json
{
  "level": "info",
  "message": "HTTP request completed",
  "correlationId": "a1b2c3d4-...",
  "method": "POST",
  "url": "/api/v1/orders/process",
  "durationMs": 142,
  "status": 200,
  "timestamp": "2024-05-28T14:32:00.000Z",
  "service": "your-app-api",
  "environment": "production"
}
```

**Why JSON in production:** log-aggregation tools index fields, so you can filter by
`correlationId`, `status` or `service` and aggregate `durationMs` instead of grepping free text.
Add the JSON transport when log volume justifies a log-aggregation tool — not before.

---

## Error tracking — uncaught errors and performance

Use an error tracker (such as Sentry) for unexpected errors and performance traces. Capture
happens at the edge, in the global error handler, **before** the error is mapped to the
transport response (`dev-core:error-handling`).

```typescript
function reportIfUnexpected(error: unknown, req: Request) {
  // Do not report expected domain errors (4xx)
  const isExpected = error instanceof AppException && httpStatusFor(error) < 500;
  if (isExpected) return;

  errorTracker.capture(error, {
    tags:  { correlationId: req.correlationId },
    user:  { id: req.user?.id },          // an ID only — never PII
    extra: { url: req.url },
  });
}
```

**Rule:** the error tracker captures only 5xx and unexpected errors. Domain errors (4xx) are
expected behavior — they do not pollute it.

**Order matters:** capture first, then let the error-mapping handler produce the response.
If the mapper runs first and swallows the error, the tracker never sees it.

Treat error tracking as a deliberate step: check whether the project has actually wired it in
(handler registered, DSN configured) before assuming anything is being captured in
production. A call to the error tracker must never fail the request — it is a non-critical
dependency (`dev-core:resilience-patterns`).

### Error tracking in client apps (web, mobile)

Three failure modes that unit tests do not catch, all seen in one real rollout:

- **Prove the configuration reached the shipped artifact.** Client builds inline public config
  (the tracker's DSN, API URLs) at build time; a value read in a way the bundler doesn't
  recognize is silently `undefined` in the browser/app, while tests pass because the test
  runner has the real environment. Check the built bundle (or a real browser request) — not
  only the tests — and send one deliberate test error end to end before calling it done.
- **Type the tracker's options with the SDK's own option type.** SDK majors rename and drop
  options; an untyped options object makes a removed option a silent no-op. Typed, it fails the
  build.
- **Re-read the privacy defaults on every SDK major.** Defaults can flip to *collecting* user
  info (IP), cookies, headers and request bodies. Set every data-collection category
  explicitly to the restrictive value, scrub events in `beforeSend` anyway, and enable the
  tracker's server-side "don't store IP addresses" option — a health or finance app must not
  ship personal data to a third-party processor by default.

Also watch the tracker's **quota**: one repeating error can spend a free plan's monthly
allowance in hours, after which every project's errors are dropped and every alert goes quiet.
Check usage after setup, and guard against bursts (server-side rate limits where the plan
allows, or dedupe in `beforeSend`).

---

## Health check endpoint

**What it checks:**

- **Liveness** (`/health/live`) — the process is up and able to answer. No dependency pings:
  a database outage must not make the platform restart a healthy process.
- **Readiness** (`/health/ready`) — the instance can serve traffic: critical dependencies
  (e.g. the database) respond. Degraded optional dependencies (cache, email) do not fail
  readiness — see `dev-core:resilience-patterns` (health check with dependency verification).

A common, valid starting point is a minimal live/ready pair returning `{ "status": "ok" }`
with no dependency ping. Add dependency checks when a false positive (process up, database
down) becomes a real risk or causes an incident.

**What it must not do:**

- Require authentication — the platform's probe has no credentials.
- Do expensive work (heavy queries, external calls without a short timeout) — it is called
  every few seconds.
- Expose internals (versions, connection strings, error details) — it is public.
- Live at a different path than the one the platform probes. If the app uses a global prefix
  (e.g. `/api/v1`), make sure the configured probe path matches the route that actually
  exists — and don't keep both a prefixed and an unprefixed version without recording which
  one the platform uses.

---

## Application metrics

Logs and metrics are different things. Logs record individual events; metrics are aggregated
values (counters, histograms, gauges) that a monitoring system scrapes or receives. Without
instrumentation, alert thresholds are decorative — there is no data to trigger them.

**Mandatory:**

1. **Request latency histogram** — labels: method, route (the route pattern, not the raw
   URL), status. Recorded in the same request wrapper that logs.
2. **Error counter** — labels: status code, error code. Incremented where unexpected errors
   are reported to the error tracker.

**Optional** (add per use case when relevant): counters for business events (e.g. domain
events published by name), gauges for current state (e.g. active database connections).

The metrics endpoint is **not public** — it reveals internal error codes, route latency and
throughput. Restrict it at the network level (IP allowlist, internal network, or a separate
internal port) rather than with user auth, and exclude it from request logging.

### What to monitor and alert on

| Metric | Source | Alert if |
|---|---|---|
| 5xx error rate | error counter | > 1% of requests |
| P95 latency | latency histogram | > 2000ms |
| Scheduled job failure | error tracker + log | Any failure |
| Failing event subscriber | log (warn) | > 3 consecutive failures |
| Delivery failures to external channels (email, push, webhooks — e.g. invalid/expired recipients) | log / counter | > 10% of deliveries |
| Memory usage | runtime default metrics | > 80% |
| Open database connections | connection-pool gauge | > 80% of pool |

This table is what to wire up once an alerting pipeline exists — don't treat it as monitored
until something actually emits and alerts on these values.

---

## Required configuration

Add to the project's env template (e.g. `.env.example`) — only once each piece is actually
wired in:

| Setting | Purpose |
|---|---|
| Error tracker DSN | Where error reports and traces are sent; empty disables reporting |
| Log level | `info` / `debug` / `verbose` — overrides the environment default |
| Environment name | `production` / `staging` / `development` — selects levels and tags reports |

Secrets among them (DSNs with auth tokens) follow `dev-core:secrets-rotation`.
