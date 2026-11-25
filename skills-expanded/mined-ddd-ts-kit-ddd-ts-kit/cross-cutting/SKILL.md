---
name: cross-cutting
description: >-
  Use for logs, metrics, traces, error tracking, audit log, retry, timeout, circuit breaker,
  cache, rate limit, choosing a logger, correlation id, tenant or session, a home-made
  Logger, UserContext or paginated result, on aspects/*, standard/*, a tracing or audit
  import in domain or application.
allowed-tools:
  - Read
  - Edit
  - Bash(npx ddd-ts-kit generate *)
  - Bash(npx ddd-ts-kit check *)
  - Bash(npx ddd-ts-kit explain *)
---

# Cross-cutting concerns

A handler that logs, measures, retries, reports and audits is five concerns hiding one use
case. Business code states the business; everything else is attached from outside, in
`src/platform/` and in adapters. `@ddd-ts-kit/aspects`, `audit`, `redis` and `tracing` are
refused in `domain/` and `application/` even when an allow-list names them, and tracing is
imported by the platform, `main.ts` and `apps/` only (`tracing/platform-only`).

## Where each concern goes

| Need | Put it | With |
|---|---|---|
| log and measure every use case | bus middlewares, `src/platform/buses/` | `loggingMiddleware`, `metricsMiddleware` |
| the logger itself | `src/platform/observability/create-logger.ts` | the kernel `Logger` port; `stack.logger` chooses the adapter: `stdout` (default), `pino` or `winston` |
| trace the application | `src/platform/observability/tracing.ts`, first import of `main.ts`, and the instrumentation given to the kernel module | [tracing.md](tracing.md) |
| report unexpected failures | the boundaries, never a use case | the kernel `ErrorReporter` port; `stack.errors: sentry` wires `@ddd-ts-kit/sentry` (Sentry or GlitchTip) in `src/platform/observability/errors.ts` |
| who did what | around the use cases, in `src/platform/audit/` | [audit-trail.md](audit-trail.md) |
| retry, timeout, circuit breaker on an outside call | the adapter's declaration or binding; defaults in `src/platform/resilience/` | `@Adapter(Port, { kind, aspects })`, or `.with(retry(...), timeout(...))` in an explicit module |
| the same, when the policy is part of what the adapter is | the adapter class, in `infrastructure/` only | `@Retry`, `@Timeout` of `@ddd-ts-kit/aspects/decorators` (`aspects/outside-in`) |
| run without an outside system (a sandbox, a demo, an environment for examiners, a provider not ready yet) | a simulated adapter in `infrastructure/external/`, bound to the port like the remote one, never the fake of `test/fakes/` | `generate adapter <ctx> <Port> --kind simulated`: answers in memory as the system would, through its translator of `infrastructure/anti-corruption/`; no retry nor timeout, nothing leaves the process |
| cache a read of another system or context | the gateway or external adapter | `cached({...})`; never a repository of aggregates |
| keep the answers of a read in the browser or a shared cache (Varnish, a CDN) | `cache` of the controller or its route group, never in the use case | a cache policy of `@ddd-ts-kit/http` (`private` with `etag` for a caller, `public` with `tags` only for what is the same for everybody); `stack.httpCache: varnish` puts Varnish in front. A `public` answer of a route that knows its caller names `Authorization`, `Cookie` or the tenant header in `vary`, and Cloudflare or Bunny ignore `Vary`. Never a decision of authorization shared across actors: the HTTP caching concept page |
| purge the answers a change made stale | a `before-commit` handler of the domain event | `CacheInvalidation.invalidate([cacheTag('calendar', id)])` of the kernel (`platform.cacheInvalidation` when wired by hand), from every event that changes what a kept answer shows, its version included: purged after the commit, through the outbox; never `CachePurger` in a use case |
| rate limit | in front of the HTTP layer | the kernel `RateLimiter` port |

`npx ddd-ts-kit generate adapter <ctx> <Port> [--kind external|gateway] [--decorators]`
writes an adapter with its policy attached (`retry` then `timeout`); `--kind simulated` writes
one with no policy, which answers in memory. Order when composing,
outermost first: logging and metrics, then retry, then circuit breaker, then timeout. Each
attempt then counts for the breaker and has its own time limit, and an open circuit ends
the retries at once.

An `external` or `gateway` adapter that states no policy gets the default one of
`src/platform/resilience/` (2 seconds per attempt). Left to it and given the port of an adapter
that states a longer limit, it is cut first, under its own name: `aspects/timeout-covers-delegate`
reports that case, and the `TimeoutError` of the default policy says so in its message. State the
policy of the outer adapter, `ownPolicy(timeout(<ms>))`, or `ownPolicy()` alone when it only hands
the call over. The rule reads declarations and container bindings only: on a platform wired by
hand, a limit read at run time, a port bound twice or under a condition, check it yourself.

## What may be recorded

By a log, a span, a metric, an error report: class, method, context, duration, error code,
correlation and trace identifiers, the actor's identifier. Never arguments, results, error
messages or full URLs: they carry personal data and secrets. `privacy/no-personal-data-in-logs`
(a warning) reports a call to the logger or the metrics that names a field a `personalFields`
declaration or the `personal` option of an event says is personal data: log the opaque id.

## Error reporting

An unexpected failure is reported once, by the first boundary that sees it: a 5xx response,
a command failing on something that is not a business refusal, an integration event buried
after its retries, a failed job, a crash of the process. A `DomainError` is an answer, not an
incident: it is mapped to a status and never reported. Handlers throw; they never call the
reporter, and never catch to log.

## Standard interfaces

Before declaring a type for one of these, use the kernel's (`standard/no-parallel-interface`):

| Concept | Kernel | Extend through |
|---|---|---|
| who acts, how they authenticated | `Actor`, `Session` | `ActorExtensions`, `SessionExtensions` |
| correlation, causation, tenant, origin | `ExecutionContext` in the `ExecutionScope` | `ExecutionContextExtensions` |
| logs, metrics, cache, lock, rate limit, jobs, errors, HTTP purges | `Logger`, `Metrics`, `Cache`, `Lock`, `RateLimiter`, `JobScheduler`, `ErrorReporter`, `CacheInvalidation`, `CachePurger` | an adapter of the port |
| lists | `Page`, `PageRequest` | generics |
| audit columns, tenant column | `AuditStamp`, `TenantScoped` | |

Extension is declaration merging in one file of `src/platform/`
(`declare module '@ddd-ts-kit/kernel' { interface SessionExtensions { ... } }`). A second
`UserContext`, `ILogger` or `PaginatedResult` is a defect.

## Who may read the execution scope

Infrastructure and the platform: audit columns, tenant scoping, log fields, the correlation
id and the tenant on published events. A key of a shared store (cache, rate limit, lock) in a
multi-tenant project is confined with `tenantCacheKey` or `tenantKey`; `cached` confines
its own, `shared: true` for a read meant for every tenant; a job states
`tenancy: 'global'` or `'per-tenant'`; platform staff read across tenants through
`acrossTenants`, audited, never through a role. Use cases receive what they need as data of the command or query
(skill `ddd-ts-kit:access-control`). The domain sees none of it.

## Tests

The test application exposes in-memory implementations: `logger.entries`, `metrics.samples`,
`errors.reports`, `cache`, `clock`. A resilience policy is tested once, on the adapter, with
a fake that fails on demand; use cases are tested without it.
