---
name: go-slog-structured-logging
description: >
  Adopt Go log/slog structured logging: Logger API, levels, JSON/text handlers,
  context attributes, default logger, migration from log/logrus/zap, and
  correlation with trace IDs. Use for owned Go services; pair with custom
  handlers skill for redaction/sampling.
---

# Go slog Structured Logging

## Scope And Authorization

- **In scope:** Application logging in codebases you maintain.
- **Out of scope:** Scraping or centralizing logs from systems without authorization.
- Never log secrets, tokens, passwords, or raw PII; prefer IDs.
- Pair with `go-slog-handlers-custom`, `logging-message-style`, `go-otel-autoinstrument`.

## When To Use

- New Go services choosing a logging API (stdlib slog is default recommendation).
- Migrating from `log.Printf` / logrus to structured JSON for production.
- Attaching request_id/trace_id consistently.
- Standardizing levels and attribute keys across microservices.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Custom Handler implementation | `go-slog-handlers-custom` |
| Log wording / UX of messages | `logging-message-style` |
| Metrics/traces backbone | `go-otel-autoinstrument` / observability skills |
| Go style general | `go-style-conventions` |
| Implementation quality | `code-quality-standards` |

## Concepts

| Piece | Role |
| --- | --- |
| `slog.Logger` | Structured logger methods (`Info`, `Error`, `LogAttrs`) |
| `slog.Handler` | Formats/emits records |
| `slog.Level` | Debug(-4), Info(0), Warn(4), Error(8) |
| Attrs | Key-value pairs (`"key", value` or `slog.String`) |
| Groups | Nested object namespaces |
| Default | `slog.Info` package funcs use default logger |
| Context | `InfoContext` for ctx-based handlers |

## Workflow

### 1. Bootstrap in main

```go
func main() {
    level := new(slog.LevelVar)
    level.Set(slog.LevelInfo)
    h := slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{
        Level: level,
        // AddSource: true, // optional; noisy/costly
    })
    logger := slog.New(h).With(
        "service", "checkout-api",
        "env", os.Getenv("APP_ENV"),
    )
    slog.SetDefault(logger)

    // pass logger via deps rather than only global when testing
}
```

### 2. Log with structured fields

```go
logger.Info("order created",
    "order_id", order.ID,
    "customer_id", order.CustomerID,
    "total_cents", order.TotalCents,
)

logger.Error("payment failed",
    "order_id", order.ID,
    "err", err,
)
```

Prefer `err` as last attr; use consistent snake_case keys.

### 3. Levels policy

| Level | Use |
| --- | --- |
| Debug | High-volume diagnostics (off in prod default) |
| Info | Normal business milestones |
| Warn | Degraded but handled |
| Error | Operation failed; needs attention |

Avoid Info per-request on ultra-hot paths without sampling.

### 4. Request context logger

```go
func Middleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        reqID := r.Header.Get("X-Request-Id")
        if reqID == "" {
            reqID = newID()
        }
        log := slog.Default().With("request_id", reqID)
        ctx := r.Context()
        // optional: store log in ctx with your own key type
        next.ServeHTTP(w, r.WithContext(ctx))
        log.Info("request completed",
            "method", r.Method,
            "path", r.URL.Path,
            "status", /* capture */,
        )
    })
}
```

Add `trace_id` from otel span context when tracing enabled.

### 5. Migration tips

| From | To |
| --- | --- |
| `log.Printf("%v", err)` | `slog.Error("...", "err", err)` |
| logrus fields | slog attrs |
| zap sugared | slog; zap bridge if gradual |

Keep a short attribute dictionary in docs (`order_id`, `user_id`, `peer`, …).

### 6. Testing

```go
func TestLogs(t *testing.T) {
    var buf bytes.Buffer
    log := slog.New(slog.NewTextHandler(&buf, nil))
    fn(log)
    if !strings.Contains(buf.String(), "order_id=") {
        t.Fatal(buf.String())
    }
}
```

Inject `*slog.Logger` into structs for testability.

### 7. Production checklist

- [ ] JSON handler in prod
- [ ] Level via env/config
- [ ] service/env attrs
- [ ] request/trace correlation
- [ ] No secrets in attrs
- [ ] Errors include `err`
- [ ] Handler redaction if needed (custom handlers skill)

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Message | Stable event name `"order created"` | Unique printf novels |
| Fields | Typed attrs | Giant sprintf blobs |
| Errors | `"err", err` | error only in message string |
| Cardinality | IDs | Full request bodies |
| Default | Set once in main | Random handlers per package |

## Output Checklist

- [ ] slog bootstrapped with JSON in prod
- [ ] Attribute naming guide published
- [ ] Levels documented
- [ ] Context/request correlation wired
- [ ] Secrets policy enforced
- [ ] Logger injection for tests
- [ ] Custom handler needs routed if any
- [ ] `code-quality-standards` applied

## Rules

- Structured key-values over string concat.
- Never log secrets/PII.
- Stable messages + dimensions for querying.
- Prefer stdlib slog for new code.
- Advanced pipelines → `go-slog-handlers-custom`.
