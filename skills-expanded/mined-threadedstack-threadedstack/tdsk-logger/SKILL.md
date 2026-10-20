---
name: "tdsk-logger"
description: "Knowledge base for the Winston logging service repo"
tags: ["winston", "logging", "nodejs", "service", "express-middleware", "security"]
---
# Logger Repo Skill

## Overview

- Shared logging package (`@tdsk/logger`) consumed by backend, proxy, and CLI repos
- Two logger systems: CLI Logger (colored console) and API Logger (Winston structured)
- Express middleware for request/error logging
- Automatic secret redaction on stderr (passwords, tokens, API keys, credit cards)
- Environment config loader (`loadEnvs`) via `@keg-hub/parse-config`

## Directory Structure

```
repos/logger/
├── src/
│   ├── index.ts              # Main barrel (re-exports all modules)
│   ├── logger.ts             # CLI Logger class (Log) + Logger singleton
│   ├── apiLogger.ts          # API Logger + buildApiLogger factory + setupLogger
│   ├── middleware.ts          # setupLoggerReq, setupLoggerErr (express-winston)
│   ├── stdio.ts              # stderr interception for secret redaction (side-effect import)
│   ├── types/                # TCLILogger, TWinLogger, TLogOpts, TSetupLogger, etc.
│   └── utils/
│       ├── buildLogger.ts    # Winston logger factory (singleton pattern)
│       ├── safeReplacer.ts   # Secret redaction logic + injectUnsafe/replaceUnsafe
│       ├── injectKeyValues.ts # Dynamic secret injection into redaction list
│       ├── colors.ts         # ANSI color helpers (basic + bright + underline/dim)
│       ├── levels.ts         # Log level utilities (npm levels, compare, getLevelMethods)
│       ├── helpers.ts        # Re-exports from @keg-hub/jsutils
│       └── stripColors.ts    # ANSI escape code stripping
├── scripts/
│   ├── addToProcess.ts       # Adds envs to process.env (force/ignore options)
│   └── loadEnvs.ts           # Config loader (@keg-hub/parse-config, caches results)
├── configs/                  # tsup (CJS to dist/log/), biome, vitest
└── package.json
```

## Two Logger Systems

**CLI Logger** (`Log` class, `Logger` singleton): For CLI tools and terminal output. Colored console output with ANSI codes. Methods include `header()`, `subHeader()`, `pair()`, `label()`, `table()`, `highlight()`, color methods (`red`, `green`, `cyan`, etc.), state methods (`info`, `warn`, `error`, `success`, `fail`), and tag support (`setTag`, `removeTag`, `toggleTag`).

**API Logger** (`ApiLogger` singleton, `buildApiLogger(label?, level?, logger?)` factory): For backend/proxy services. Winston-powered structured logging. Formats messages as `{ message, label, data }`. **Known behavior**: `debug()`, `verbose()`, and `silly()` all map to Winston `info` level internally. Imports `stdio.ts` as side-effect for stderr redaction.

## Express Middleware

- `setupLoggerReq(app, middlewareOpts?)` — Request logging via `express-winston.logger`
- `setupLoggerErr(app, middlewareOpts?)` — Error logging via `express-winston.errorLogger`
- Metadata logging enabled at `verbose` level or higher

## Secret Redaction

Multi-layer protection via `safeReplacer.ts` and `stdio.ts`:
- **JSON serialization**: `safeReplacer()` as `JSON.stringify()` replacer
- **stdout + stderr interception**: `stdio.ts` hijacks both `process.stdout.write` and `process.stderr.write` with the same `replaceUnsafe()` call
- **Dynamic injection**: `injectKeyValues()` / `injectUnsafe()` add runtime secrets to redaction list
- **Patterns**: passwords, API keys, tokens, secrets, session IDs, credit cards, authorization headers
- **Bypass**: `STL_FORCE_DISABLE_SAFE=true` disables stderr redaction

## Environment Loading (`scripts/loadEnvs.ts`)

`loadEnvs(cfg)` loads environment configs using `@keg-hub/parse-config`. Searches: project root, `deploy/`, `~/.config/tdsk/`, plus custom locations. Caches in `__LOADED_ENVS__` (use `force: true` to reload). Calls `addToProcess()` to inject into `process.env`. Options: `env`, `name`, `force`, `override`, `ignore`, `locations`.

## Key Env Vars

- `NODE_ENV`: `production` → minimal JSON logging; non-production → pretty-printed with colors
- `TDSK_TEST_COLORS`: `0` or `false` → disable colors/strip ANSI codes
- `STL_FORCE_DISABLE_SAFE`: `true` → disable secret redaction on stderr

## Singletons

- `Logger` — CLI logger instance (from `logger.ts`)
- `ApiLogger` — Default API logger (from `buildApiLogger()` in `apiLogger.ts`)
- `__LOGGER` — Internal Winston instance (from `buildLogger()`)

## Integration Points

- **Backend**: `ApiLogger` for structured logging, `setupLoggerReq`/`setupLoggerErr` middleware
- **Proxy**: `ApiLogger` for gateway logging, secret injection for API keys
- **CLI**: `Logger` class for terminal output
- **Build**: tsup → `dist/log/` (CJS), sourcemaps enabled
- **Test**: Vitest with `loadEnvs({ force: true })` pre-setup
