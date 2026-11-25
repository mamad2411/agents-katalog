---
name: obs-check
description: >
  Enforces observability rules (OBS-1 through OBS-5). Loaded by the conductor
  for review, incident response, and new service scaffolding. Detects empty catch
  blocks, unstructured logging, missing endpoint tracing, absent health checks,
  and vague error messages. Activated by: "incident", "on call", "debugging
  production", "empty catch", "logging", "observability", "health check".
version: "1.0.0"
last-reviewed: "2026-03-04"
languages: [typescript, python, go, rust, javascript]
changelog: "../../CHANGELOG.md"
tools: Read, Grep, Glob, Bash
model: opus
permissionMode: default
---

# Obs Check — Observability Enforcement

Precedence in the overall system: SEC → TDD → ARCH/TYPE →
**OBS-1 (BLOCK)** → OBS-2 through OBS-5.

---

## Rules

### OBS-1 — No Empty Catch Blocks
**Severity**: BLOCK | **Languages**: * | **Source**: CCC

**What it prohibits**: Catch blocks (or equivalent error handling constructs)
that swallow errors without any logging, re-throwing, or recovery action.

**Prohibited patterns**:
```typescript
// TypeScript/JavaScript
try { ... } catch (e) {}
try { ... } catch (e) { /* TODO */ }
try { ... } catch (e) { return null; }  // null return with no log

# Python
try: ...
except Exception: pass
except Exception: ...  # ellipsis

# Go (result ignored)
if err != nil { }  // empty block
_ = err  // explicitly discarded without log

// Rust
if let Err(_) = result { }  // empty block
let _ = result;  // discarded result without log
```

**Exemptions**:
- `catch (e) { return defaultValue; }` where `defaultValue` is semantically
  correct AND a comment explains the intentional fallback
- Top-level global error handlers that transform errors before logging elsewhere
- Legitimate `_` discards in Go/Rust with a comment explaining why

**Detection**:
1. Grep for `catch` blocks with empty bodies or bodies containing only comments
2. Grep for Python `except` blocks containing only `pass` or `...`
3. Grep for Go `if err != nil` with empty block body
4. Grep for Rust `let _ =` or `if let Err(_)` with empty block
5. For each match: check if the block contains at least one `log`, `logger`,
   `console`, `fmt.`, `panic`, `return Err`, `throw`, or `raise` call

**agent_action**:
1. Cite: `OBS-1 (BLOCK): Empty catch block at {file}:{line} — error '{exception_type}' is silently swallowed.`
2. Show the catch block
3. Required action — choose the appropriate pattern:
   ```typescript
   // Minimum: log + rethrow (preserve original error context)
   } catch (error) {
     logger.error({ err: error, context: 'operationName' }, 'Operation failed');
     throw error;  // or throw new AppError('descriptive message', { cause: error })
   }
   ```
4. If the error is intentionally recoverable: require a comment and log at WARN level
5. If `--fix`: add a structured log call and rethrow — DO NOT add `return null`
   as a default fix without explicit user confirmation

**Bypass prohibition**: "I'll add logging later", "it's a known ignorable error"
→ Refuse. Cite OBS-1. An ignorable error must be documented with a comment AND
logged at DEBUG level so it can be correlated if it later causes issues.

---

### OBS-2 — Structured Logging with Correlation IDs
**Severity**: WARN | **Languages**: * | **Source**: CCC

**What it prohibits**: Unstructured log statements (plain string concatenation)
in production code paths, and log statements missing a correlation/request ID.
Unstructured logs cannot be reliably parsed, queried, or correlated across
distributed services.

**Prohibited**:
```typescript
console.log("User " + userId + " not found");
console.error("Error: " + error.message);
```

**Required**:
```typescript
logger.warn({ userId, requestId: ctx.requestId }, "User not found");
logger.error({ err: error, requestId: ctx.requestId, userId }, "User lookup failed");
```

**Structured logging libraries by language**:
| Language | Recommended | Minimum |
|----------|------------|---------|
| TypeScript/JavaScript | pino, winston (JSON mode) | console.log with JSON.stringify object |
| Python | structlog, loguru (structured) | logging.warning with `extra={}` |
| Go | slog (stdlib ≥1.21), zerolog, zap | log.Printf is insufficient |
| Rust | tracing crate with JSON subscriber | log crate (unstructured — insufficient) |

**Detection**:
1. Grep for `console.log(`, `console.error(`, `console.warn(` in non-test source files
2. Grep for `print(f"`, `logging.info("` (bare string), `log.Printf(` in non-test files
3. For each match: check if the argument is a structured object (contains key-value pairs)
4. Check if any log call passes a `requestId`, `correlationId`, `traceId`, or `ctx`

**agent_action**:
1. Cite: `OBS-2 (WARN): Unstructured log at {file}:{line}. Use structured logging with correlation ID.`
2. Show the current log call
3. Propose the structured equivalent with correlation context
4. If `--fix`: convert `console.log("message" + var)` to
   `logger.info({ var, requestId: ctx.requestId }, "message")`
   — but only if a `logger` instance or `ctx` is already in scope

---

### OBS-3 — HTTP Endpoints Must Be Traced
**Severity**: WARN | **Languages**: typescript, javascript, python, go | **Source**: CCC

**What it prohibits**: HTTP endpoint handlers that do not propagate or initiate
a trace span. Without tracing, distributed request flows become impossible to
debug when they span multiple services.

**Required** (one of these patterns must be present):
- OpenTelemetry span creation: `tracer.startSpan(...)`, `@trace`, `span = tracer.start_as_current_span(...)`
- Framework middleware that auto-instruments (e.g., `@opentelemetry/instrumentation-express`)
  — if middleware is verified at the application level, per-handler tracing is not required
- Manual trace header propagation: reading and forwarding `traceparent` / `X-Request-Id`

**Detection**:
1. Identify HTTP handler functions (look for route registration patterns:
   `app.get(`, `app.post(`, `@app.route(`, `func(w http.ResponseWriter`, etc.)
2. For each handler: check if the handler body or its middleware chain contains
   a tracing call or the framework has a tracing middleware installed
3. Flag handlers with no trace context

**agent_action**:
1. Cite: `OBS-3 (WARN): Endpoint '{method} {path}' at {file}:{line} has no trace span.`
2. Check if a global tracing middleware is installed at the application root
3. If middleware handles it: mark as passing (document the middleware location)
4. If not: propose adding OpenTelemetry instrumentation
5. If `--fix`: add the minimal `@opentelemetry/instrumentation-{framework}` setup
   reference — do not add manual spans when auto-instrumentation is available

---

### OBS-4 — Services Must Expose a Health Check Endpoint
**Severity**: WARN | **Languages**: typescript, javascript, python, go | **Source**: CCC

**What it requires**: HTTP services must expose at least one health check
endpoint that returns a machine-readable status. Health checks are required by
Kubernetes liveness/readiness probes, load balancers, and on-call tooling.

**Acceptable patterns**:
- `GET /health` → `{ "status": "ok" }` (HTTP 200)
- `GET /healthz` → `{ "status": "ok" }` (HTTP 200)
- `GET /ready` → status and dependency check (HTTP 200 / 503)
- `GET /_health` (common in internal APIs)

**Detection**:
1. Grep route definitions for `/health`, `/healthz`, `/ready`, `/_health`
2. If none found: flag as OBS-4

**agent_action**:
1. Cite: `OBS-4 (WARN): No health check endpoint found in {file}. HTTP services must expose /health or /healthz.`
2. Propose: add a minimal health handler:
   ```typescript
   app.get('/health', (req, res) => res.json({ status: 'ok' }));
   ```
3. For services with dependencies (DB, cache): recommend a liveness vs readiness split
4. If `--fix`: add the minimal health endpoint stub

---

### OBS-5 — Error Messages Must Be Actionable
**Severity**: INFO | **Languages**: * | **Source**: CCC

**What it prohibits**: Error messages thrown or returned to callers that contain
no actionable information — messages that require reading source code to understand
what went wrong and how to fix it.

**Prohibited patterns**:
```typescript
throw new Error("Something went wrong");
throw new Error("Internal error");
throw new Error("Failed");
return { error: "Error occurred" };
```

**Required patterns**:
```typescript
throw new Error(`User ${userId} not found in tenant ${tenantId}`);
throw new AppError("PAYMENT_DECLINED", {
  code: "INSUFFICIENT_FUNDS",
  hint: "Verify the card has available balance before retrying",
  requestId: ctx.requestId,
});
```

**Detection**:
1. Grep for `throw new Error("` patterns where the message is ≤ 20 characters
   or matches generic phrases: `"Something went wrong"`, `"Internal error"`,
   `"Failed"`, `"Error occurred"`, `"An error occurred"`
2. Grep for returned error objects with only a generic `message` field

**agent_action**:
1. Report: `OBS-5 (INFO): Vague error message at {file}:{line}: '{message}'.`
2. Propose: include the relevant context: what operation failed, what values
   were involved, what the caller should do
3. If `--fix`: replace the vague message with a template that includes the
   key variables (file and line context); require human to fill in specific values

---

Report schema: see `skills/conductor/shared-contracts.md`.
