# @t/logging-rn — Agent Guide

## What this owns

The **React Native / Expo platform implementation** of the `Logger` port from `@t/logging-types`.
Mirrors the browser package shape: `ConsoleLogger` (structured `console.*`, RN-compatible),
`AnalyticsBridgedLogger` (decorator that forwards `warn` / `error` / `fatal` to
`AnalyticsTracker.captureException`), an Awilix DI registrar, and a factory helper. No Node-only
APIs; no `process.stdout` references.

## Layout

```
packages/logging-rn/src/
  index.ts
  infrastructure/
    ConsoleLogger.ts                Logger impl via structured console.*  (RN-safe)
    ConsoleLogger.test.ts
    AnalyticsBridgedLogger.ts       Decorator: delegates all levels; bridges warn/error/fatal -> analytics
    AnalyticsBridgedLogger.test.ts
    errorSerializer.ts              Shared error flattening util
    errorSerializer.test.ts
    redactors.ts                    PII redact helpers
    redactors.test.ts
  dependency-injection/
    registerLoggerRnDI.ts           Registers Logger singleton; wraps in AnalyticsBridgedLogger when analytics present
    registerLoggerRnDI.test.ts
  factories/
    createReactNativeLogger.ts      Factory helper (non-DI usage)
    createReactNativeLogger.test.ts
```

## DI registrar

C:\Users\jager\OneDrive\Documents\GitHub\template-repo\packages\logging-rn\src\dependency-injection\registerLoggerRnDI.ts

```ts
import { registerLoggerRnDI } from "@t/logging-rn"
registerLoggerRnDI(container, {
  context:   { requestId: "rn-global", userId: currentUser.id },
  analytics: analyticsTrackerInstance,   // omit to skip bridge
})
// resolves as: container.resolve(dependencyKeys.global.LOGGER)
//   -> AnalyticsBridgedLogger(ConsoleLogger) when analytics provided
//   -> ConsoleLogger                          otherwise
```

## Consumers

- `apps/mobile` — Expo app; bootstraps logger in the app composition root (typically
  `apps/mobile/src/composition.ts` or equivalent)
- `@t/analytics` bridge: `AnalyticsBridgedLogger` calls `tracker.captureException` so that
  `warn` / `error` / `fatal` log lines are also sent as PostHog exceptions — dedup is handled by
  the analytics tracker, not here

## Conventions

- **Port-first.** Import `Logger` from `@t/logging-types` in app/feature code; never reference
  `ConsoleLogger` or `AnalyticsBridgedLogger` outside this package or its DI registrar.
- **No raw `console.*` in app code.** Resolve `Logger` from the container; use that instance.
- **No Node-only APIs.** This package must remain RN-safe. No `process.stdout`, no `fs`, no `os`.
  If a util needs to branch, gate it behind a platform check or keep it out of this package.
- **AnalyticsBridgedLogger is opt-in via DI options.** Pass `analytics` to opt in; omit for a plain
  `ConsoleLogger`. Never construct `AnalyticsBridgedLogger` directly in app code.
- **`debug` and `info` do not forward to analytics.** Only `warn`, `error`, and `fatal` bridge to
  `captureException`; high-frequency levels would saturate PostHog quotas.
- **Structured logs only.** Pass `{ message, metadata }` objects. Metadata is especially valuable
  in mobile: include `screen`, `sessionId`, or device context where available.
- **`child()` propagates the bridge.** `AnalyticsBridgedLogger.child()` returns a new
  `AnalyticsBridgedLogger` — the analytics link survives child creation.
- **Tests.** Use vitest (not `bun test`). The package's `"scripts.test"` resolves to `vitest run`.

## Links

C:\Users\jager\OneDrive\Documents\GitHub\template-repo\docs\architecture\platform\logging.md
