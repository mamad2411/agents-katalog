# @t/logging-browser — Agent Guide

## What this owns

The **browser / Electron platform implementation** of the `Logger` port from `@t/logging-types`.
Provides `ConsoleLogger` (structured `console.*` output) and `AnalyticsBridgedLogger` (decorator
that forwards `warn` / `error` / `fatal` to `AnalyticsTracker.captureException` for dedup with
PostHog). Ships an Awilix DI registrar and a factory helper.

## Layout

```
packages/logging-browser/src/
  index.ts
  infrastructure/
    ConsoleLogger.ts                Logger impl via structured console.*
    ConsoleLogger.test.ts
    AnalyticsBridgedLogger.ts       Decorator: delegates all levels; bridges warn/error/fatal -> analytics
    AnalyticsBridgedLogger.test.ts
    errorSerializer.ts              Shared error flattening util
    errorSerializer.test.ts
    redactors.ts                    PII redact helpers (browser-safe subset)
    redactors.test.ts
  dependency-injection/
    registerLoggerBrowserDI.ts      Registers Logger singleton; wraps in AnalyticsBridgedLogger when analytics present
    registerLoggerBrowserDI.test.ts
  factories/
    createBrowserLogger.ts          Factory helper (non-DI usage)
    createBrowserLogger.test.ts
```

## DI registrar

C:\Users\jager\OneDrive\Documents\GitHub\template-repo\packages\logging-browser\src\dependency-injection\registerLoggerBrowserDI.ts

```ts
import { registerLoggerBrowserDI } from "@t/logging-browser"
registerLoggerBrowserDI(container, {
  context:   { requestId: "browser-global", userId: currentUser.id },
  analytics: analyticsTrackerInstance,   // omit to skip bridge
})
// resolves as: container.resolve(dependencyKeys.global.LOGGER)
//   -> AnalyticsBridgedLogger(ConsoleLogger) when analytics provided
//   -> ConsoleLogger                          otherwise
```

## Consumers

- `apps/web` — Next.js client components; bootstraps logger in client-side composition root
- `apps/desktop` (Electron renderer) — same pattern as web
- `@t/analytics` bridge: `AnalyticsBridgedLogger` calls `tracker.captureException` so that
  `warn` / `error` / `fatal` log lines are also captured as PostHog exceptions — no double-fire,
  because the analytics tracker deduplicates by error identity

## Conventions

- **Port-first.** Import `Logger` from `@t/logging-types`; never reference `ConsoleLogger` or
  `AnalyticsBridgedLogger` outside this package or its DI registrar.
- **No raw `console.*` in app code.** Resolve `Logger` from the container and use that.
- **AnalyticsBridgedLogger is opt-in via DI options.** Pass `analytics` to opt in; omit to get a
  plain `ConsoleLogger`. Never construct `AnalyticsBridgedLogger` directly in app code.
- **`debug` and `info` do not forward to analytics** — only `warn`, `error`, and `fatal` do. This is
  intentional; high-volume debug/info would saturate PostHog event quotas.
- **Structured logs only.** Pass `{ message, metadata }` objects; bare string calls are acceptable
  for simple cases but `metadata` fields improve searchability.
- **`child()` propagates the bridge.** `AnalyticsBridgedLogger.child()` returns a new
  `AnalyticsBridgedLogger` wrapping the inner logger's child — the analytics link is never lost.

## Links

C:\Users\jager\OneDrive\Documents\GitHub\template-repo\docs\architecture\platform\logging.md
