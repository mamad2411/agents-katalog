# packages/analytics — AGENTS.md

## What this package owns

`@t/analytics` is the **server-side DI registrar and infrastructure layer** for the analytics
cluster. It re-exports the `AnalyticsTracker` port from `@t/analytics-types`, provides the
concrete server implementations (`PostHogAnalyticsTrackerImpl`, `NoOpAnalyticsTracker`,
`RequestAnalyticsTrackerImpl`), and owns `registerAnalyticsDI()` — the single call a server-side
composition root makes to wire analytics into the DI container. No app or package instantiates an
analytics impl directly; they all resolve through `dependencyKeys.global.ANALYTICS`.

## Layout

```
src/
  entities/
    ports/           # re-exports AnalyticsTracker + RequestAnalyticsTracker from @t/analytics-types
    schemas/         # re-exports EventSchema from @t/analytics-types
    types/           # re-exports all domain types from @t/analytics-types
  infrastructure/
    NoOpAnalyticsTracker.ts          # default fallback; swallows all events
    PostHogAnalyticsTrackerImpl.ts   # posthog-node impl — god-node (~19 edges)
    RequestAnalyticsTrackerImpl.ts   # per-request scoped wrapper
  dependency-injection/
    registerAnalyticsDI.ts           # composition-root entry point (see below)
  utils/             # (none yet — add pure helpers here, not in infrastructure)
```

Note: there is no `utils/` directory; add one when pure, SDK-free helpers are needed.

## DI registrar

File: `packages/analytics/src/dependency-injection/registerAnalyticsDI.ts`

```ts
registerAnalyticsDI(container: Container, opts: RegisterAnalyticsDIOptions): void
// opts: { config: ConfigRepository, environment: Environment, service: Service }
```

Selection order (first match wins):
1. `environment === "testing"` → `NoOpAnalyticsTracker`
2. `config.analytics.enabled === false` → `NoOpAnalyticsTracker`
3. `!config.analytics.apiKey` → throws `Error` (hard-fail; set `POSTHOG_ENABLED=false` to opt out)
4. otherwise → `PostHogAnalyticsTrackerImpl`

Lifetimes: global tracker = `singleton` (`dependencyKeys.global.ANALYTICS`);
request tracker = `scoped` (`dependencyKeys.request.REQUEST_ANALYTICS`).

## Consumers

- `apps/api` — server composition root; calls `registerAnalyticsDI` with `service: "api"`
- `@t/billing`, `@t/logging` — resolve `ANALYTICS` to call `captureRevenue` / `captureException`
- `apps/web` (server components / route handlers) — resolves `REQUEST_ANALYTICS` via middleware

## Conventions

- Port-first: consumers import `AnalyticsTracker` from `@t/analytics-types`, never the impl class.
- `NoOpAnalyticsTracker` is the **always-safe default**; never bind `undefined` as a fallback.
- Every event emitted by `PostHogAnalyticsTrackerImpl` carries stamped reserved super-props
  (`$environment`, `$service`) — callers cannot override these.
- PII scrubbing lives in `@t/analytics-types/redaction/scrubPii`; server impl calls it on every
  user-controlled payload before forwarding to posthog-node.
- No raw `PostHog` client usage outside `PostHogAnalyticsTrackerImpl`.
- `registerAnalyticsDI` must hard-fail on missing `apiKey` when `enabled` is not explicitly false —
  no silent NoOp fallback for misconfiguration.

## Links

- Architecture spec: `docs/architecture/platform/analytics/analytics.md`
- Phase checklists: `docs/architecture/platform/analytics/` (phase-01 through phase-08)
- Shared types/port: `packages/analytics-types/AGENTS.md`
- Browser impl: `packages/analytics-browser/AGENTS.md`
- RN impl: `packages/analytics-rn/AGENTS.md`
