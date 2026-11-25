---
name: structured-logging-axiom
description: Use when implementing structured logging, setting up Axiom observability, migrating from console.* to a centralized logger, or configuring Vercel Log Drains for log collection in Next.js apps
triggers:
  - structured logging
  - axiom
  - log drains
  - centralized logger
  - console migration
  - observability
  - correlation id
  - log levels
---

# Structured Logging & Axiom Infrastructure

Zero-dependency structured logging for Next.js with Axiom integration via Vercel Log Drains. No external SDK required.

## Architecture

```
Code -> createLogger('namespace') -> console.info(JSON) -> Vercel stdout -> Log Drain -> Axiom
```

## Logger Implementation

Create a centralized logger module that replaces all raw `console.*` calls:

```typescript
// lib/logger.ts
export type LogLevel = 'debug' | 'info' | 'warn' | 'error'

export interface Logger {
  debug(message: string, context?: Record<string, unknown>): void
  info(message: string, context?: Record<string, unknown>): void
  warn(message: string, context?: Record<string, unknown>): void
  error(message: string, error?: Error, context?: Record<string, unknown>): void
  child(context: Record<string, unknown>): Logger
}

export function createLogger(namespace: string, parentContext?: Record<string, unknown>): Logger
export function generateCorrelationId(): string
```

### Features

- **Namespaced loggers**: `createLogger('analyze-stream')` identifies the source module
- **Child loggers**: `log.child({ correlationId })` bakes in context for all subsequent calls
- **Log level filtering**: `LOG_LEVEL` env var override without redeploying
- **Dual output**: JSON in production (Axiom-compatible), human-readable in development
- **Reserved key protection**: Context keys colliding with log fields get `ctx_` prefix
- **Correlation IDs**: `generateCorrelationId()` for request tracing across log entries

### Usage

```typescript
import { createLogger, generateCorrelationId } from '@/lib/logger'

const log = createLogger('my-module')

// Basic usage
log.debug('Verbose detail', { rowIndex: 42 })
log.info('Operation started', { itemCount: 12450 })
log.warn('Threshold exceeded', { sizeMB: 48.2 })
log.error('Parse failed', error, { filename: 'data.csv' })

// Child logger — bakes in context for all subsequent calls
const correlationId = generateCorrelationId()
const reqLog = log.child({ correlationId, requestId: 'abc-123' })
reqLog.info('Processing started')    // auto-includes correlationId + requestId
reqLog.debug('Item parsed', { idx }) // merges with parent context

// Chained children accumulate context
const itemLog = reqLog.child({ itemId: 'item-001' })
itemLog.info('Item processed')  // has correlationId + requestId + itemId
```

## Log Levels

| Level | When to Use | Production Default |
|-------|------------|-------------------|
| `debug` | Verbose internals (row parsing, intermediate state) | Suppressed |
| `info` | Significant milestones (analysis started, export complete) | Logged |
| `warn` | Recoverable issues (no result found, threshold exceeded) | Logged |
| `error` | Failures requiring attention (parse crash, API error) | Logged |

### Runtime Override

Set `LOG_LEVEL` environment variable in Vercel to temporarily change log verbosity without redeploying:

```
LOG_LEVEL=debug  -> all levels logged
LOG_LEVEL=error  -> only errors logged
```

Validate the env var at startup — invalid values fall back to the environment default.

## Dual Output Format

**Development** (human-readable):
```
[2026-02-14T01:30:00.000Z] INFO  [my-module] Processing started {"itemCount":12450}
```

**Production** (JSON for Axiom):
```json
{"timestamp":"2026-02-14T01:30:00.000Z","level":"info","namespace":"my-module","message":"Processing started","itemCount":12450,"correlationId":"a1b2c3d4-k5m9n2"}
```

Format is selected at module load time based on `NODE_ENV`. Context fields are placed at the top level of JSON (not nested) for direct Axiom column indexing.

### Reserved Key Protection

If context contains keys that collide with log entry fields (`timestamp`, `level`, `namespace`, `message`, `error`, `stack`), they are auto-prefixed with `ctx_`:

```typescript
log.info('test', { message: 'user input' })
// JSON output: {"timestamp":"...","level":"info","message":"test","ctx_message":"user input"}
```

## Axiom Integration — Two Approaches

### Option A: Vercel Log Drains (Recommended)

Zero dependencies. Structured JSON goes to stdout, Vercel captures it, Log Drain webhook forwards to Axiom.

```
logger.ts -> console.info(JSON) -> Vercel stdout -> Log Drain webhook -> Axiom dataset
```

**Pros**: No npm packages, no code changes, no API keys in env vars, works with any logger that outputs to stdout
**Cons**: Only captures server-side logs (SSR/API routes), slight delay (~seconds), no client-side browser logs

**Setup**:
1. Create Axiom account at axiom.co (free tier: 500MB/day, 30-day retention)
2. Create a dataset (e.g., `my-app-logs`)
3. Vercel Dashboard -> Settings -> Integrations -> Axiom -> Install
4. Connect your project and select Log Drains
5. Deploy — logs start flowing automatically

### Option B: Axiom API Direct (For Client-Side or Custom Pipelines)

Send logs directly to Axiom's ingest API. Useful for browser-side logs or when you need guaranteed delivery.

```
logger.ts -> axiom.ingest([events]) -> HTTPS POST -> Axiom dataset
```

**Pros**: Works client-side (browser), guaranteed delivery, batch control, can send from Edge/Workers
**Cons**: Requires `@axiomhq/js` package (~8KB), needs `AXIOM_TOKEN` + `AXIOM_DATASET` env vars

**Setup**:
```bash
npm install @axiomhq/js
```

```typescript
// lib/axiom-transport.ts
import { Axiom } from '@axiomhq/js'

const axiom = new Axiom({ token: process.env.AXIOM_TOKEN! })

export async function flushToAxiom(events: Record<string, unknown>[]) {
  axiom.ingest(process.env.AXIOM_DATASET!, events)
  await axiom.flush()
}
```

Add a transport layer to the logger that buffers JSON entries and flushes in batches (e.g., every 5s or 50 events).

**When to consider Option B**:
- You need client-side (browser) error logs in Axiom (Log Drains only capture server stdout)
- You need guaranteed delivery (Log Drains are best-effort)
- You're deploying outside Vercel (e.g., Cloudflare Workers, self-hosted)
- You want custom batching, sampling, or routing logic

### Comparison

| Aspect | Log Drains (A) | Direct API (B) |
|--------|---------------|----------------|
| Dependencies | None | `@axiomhq/js` |
| Server-side logs | Yes | Yes |
| Client-side logs | No | Yes |
| Env vars needed | None (Vercel handles auth) | `AXIOM_TOKEN`, `AXIOM_DATASET` |
| Delivery guarantee | Best-effort | Guaranteed (with flush) |
| Latency | ~seconds | ~immediate on flush |
| Code changes | Zero | Transport layer needed |
| Works outside Vercel | No | Yes |

### Useful Axiom Queries

```
// All errors in the last hour
| where level == "error" | order by _time desc

// Trace a single request
| where correlationId == "a1b2c3d4-k5m9n2" | order by _time asc

// Slow operations by namespace
| where namespace == "reverse-geocode" | summarize avg(durationMs) by bin(_time, 5m)

// Error rate by namespace
| where level == "error" | summarize count() by namespace | order by count_ desc
```

## ESLint Guard

Enforce `no-console: 'error'` in ESLint flat config to prevent regression after migration:

```javascript
// eslint.config.mjs
import nextConfig from "eslint-config-next";

const eslintConfig = [
  ...nextConfig,
  { rules: { "no-console": "error" } },
  {
    files: ["**/*.test.ts", "**/*.test.tsx", "**/*.spec.ts", "**/*.spec.tsx", "e2e/**"],
    rules: { "no-console": "off" },
  },
];

export default eslintConfig;
```

Only the logger module itself has `eslint-disable-next-line` exceptions.

## Migration Patterns

When converting existing `console.*` calls to the structured logger:

| From | To |
|------|-----|
| `console.log('[API] File type:', fileType)` | `log.debug('File type detected', { fileType })` |
| `console.error('Failed:', error)` | `log.error('Failed', error instanceof Error ? error : undefined)` |
| `console.warn('No results for', address)` | `log.warn('No results found', { address })` |
| `console.log(\`Parsed ${count} rows\`)` | `log.info('Parsing complete', { count })` |
| `console.error(error.message); console.error(error.stack)` | `log.error('Operation failed', error)` (logger handles stack automatically) |

### Rules

- Strip prefix tags (`[API]`, `[FilePreview]`, `[SSE]`) — the namespace handles identification
- `console.log` -> `log.debug` (verbose) or `log.info` (milestones)
- `console.error` -> `log.error(message, errorObj?, context?)` — pass Error object as 2nd arg
- `console.warn` -> `log.warn(message, context?)`
- Replace string interpolation with context objects: template literals -> `{ key: value }`
- Combined console.error calls (message + stack) become a single `log.error` (logger extracts stack automatically)

## Pitfalls

### `removeConsole` in next.config.ts

Next.js `compiler.removeConsole` strips `console.*` calls from production bundles. This **silently kills logger output** since the logger calls `console.debug`/`console.info`/`console.warn`/`console.error` internally.

**Fix**: Disable `removeConsole`. The logger handles level filtering internally.

```typescript
// next.config.ts
compiler: {
  // Console stripping disabled — structured logger handles level filtering
  // internally and emits JSON for Axiom log drain ingestion.
},
```

### `next-axiom` is NOT a Drop-in

The `next-axiom` package does NOT auto-capture `console.*` calls. It provides its own Logger API that must be used explicitly. If you already have `createLogger`, adding `next-axiom` is redundant. Vercel Log Drains achieves the same result with zero dependencies.

### Module-Level Evaluation

`IS_PRODUCTION` and the format function (JSON vs human) should be evaluated at module load time. This avoids a runtime check on every log call but means test environments always use the human formatter unless you mock `NODE_ENV` before import.
