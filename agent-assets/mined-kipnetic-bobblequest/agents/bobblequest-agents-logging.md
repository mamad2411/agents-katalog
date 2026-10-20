# @t/logging — Agent Guide

## What this owns

The **port contract** for all logging in the monorepo. Ships the abstract `Logger` class (the port),
`LogContext` / `LogArg` / `LogPayload` types, `LogLevel` / `LogType` enums, the winston-backed
concrete implementations (`WinstonLogger`, `GlobalLogger`, `RequestLogger`), PII redaction, OTLP
transport to PostHog, and Awilix DI registrars. Every other package and app depends on the port —
never on a concrete impl.

## Layout

```
packages/logging/
  index.ts                          public barrel; factory helpers createLogger / createGlobalLogger / createRequestLogger
  version.ts                        VERSION constant stamped into every log record
  entities/
    ports/     Logger.ts            abstract Logger port — extend this, resolve this
    types/     LogContext.ts        requestId, userId, fileName, metadata
               otlpConfig.ts       OTLPConfig interface
    enums/     index.ts            LogLevel, LogType
  infrastructure/
    winstonLogger.ts                WinstonLogger : Logger (base impl)
    globalLogger.ts                 GlobalLogger extends WinstonLogger
    requestLogger.ts                RequestLogger extends WinstonLogger
    redactors.ts                    DEFAULT_REDACT_PATHS, buildRedactConfig, redactFormat
    errorSerializer.ts              errorSerializerFormat (nested Error flattening)
    quietMode.ts                    isGlobalQuietMode / setGlobalQuietMode
    transports/
      otlpTransport.ts              OTLPWinstonTransport + circuit breaker (CLOSED/OPEN/HALF_OPEN)
      transportFactory.ts           getOrCreateOTLPTransport singleton (env-gated)
  dependency-injection/
    registerLoggerDI.ts             GlobalLogger singleton -> dependencyKeys.global.LOGGER
    registerLoggerFactoryDI.ts      createGlobalLogger factory -> dependencyKeys.global.LOGGER_FACTORY
  __tests__/                        vitest suite (childLogger, levelMethods, quietMode, etc.)
```

## DI registrar

C:\Users\jager\OneDrive\Documents\GitHub\template-repo\packages\logging\dependency-injection\registerLoggerDI.ts

```ts
import { registerLoggerDI } from "@t/logging"
registerLoggerDI(container, { context: { requestId: "global" }, redactExtraPaths: ["ssn"] })
// resolves as: container.resolve(dependencyKeys.global.LOGGER)  -> GlobalLogger singleton
```

Legacy factory registrar (preserved for `@t/analytics` / `@t/errors` call sites):
C:\Users\jager\OneDrive\Documents\GitHub\template-repo\packages\logging\dependency-injection\registerLoggerFactoryDI.ts

## Consumers

- `apps/api` — primary server consumer; calls `registerLoggerDI` in `composition.ts`
- `apps/web`, `apps/website` — resolve logger via container
- `@t/analytics`, `@t/errors`, `@t/billing`, `@t/ai` — depend on the `Logger` port
- Platform impls: `@t/logging-browser` (web/Electron), `@t/logging-rn` (React Native)
  — both wrap this port's `ConsoleLogger` in `AnalyticsBridgedLogger` for analytics dedup

## Conventions

- **Port-first.** Inject `Logger` from `@t/logging-types`; never import a concrete class in app code.
- **No raw `console.*` in app code.** Use the resolved `Logger` instance everywhere.
- **Structured logs.** Always pass `{ message, metadata }` objects — avoid bare string calls.
- **PII redaction runs first.** `redactFormat` is the first format in every transport pipeline;
  adding fields to `DEFAULT_REDACT_PATHS` or `redactExtraPaths` covers all sinks automatically.
- **OTLP is env-gated.** Attaches only when `POSTHOG_API_KEY` is set AND `ENVIRONMENT !== "testing"`.
  Never force-attach in tests — set `ENVIRONMENT=testing` instead.
- **One OTLP singleton per process.** `getOrCreateOTLPTransport()` — never construct the transport
  directly; duplicate instances leak `BatchLogRecordProcessor` timers.
- **`fatal` emits at wire-level `error` + adds `"severity": "fatal"`.** Do not use `level: "fatal"`
  as a key — winston's `Object.assign` would clobber `level`.

## Links

C:\Users\jager\OneDrive\Documents\GitHub\template-repo\docs\architecture\platform\logging.md
