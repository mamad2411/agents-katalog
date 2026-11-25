---
name: go-slog
description: Use when adding structured logging in Go 1.21+ — JSON handler, attrs, context propagation, correlation IDs, no free-form messages.
metadata:
  added: 2026-05-18
  last_reviewed: 2026-05-18
  type: language
  languages: [go]
  status: active
  invokes_shell: false
  shell_reviewed: "valksor 2026-05-17"
  related: [go-essentials, go-chi, observability-essentials]
---

# Go log/slog

**Iron Law: production logs are JSON. Every log line carries a correlation ID. Values are structured attrs, NEVER concatenated into the message string.**

## Why slog (vs zap / zerolog)

| Logger          | Verdict                                                                                         |
| --------------- | ----------------------------------------------------------------------------------------------- |
| **slog**        | stdlib (1.21+), structured-by-default, handler-pluggable, zero deps — **default choice**        |
| **zap**         | ~2x faster on hot paths, sugared API; pick only when you've measured and slog is the bottleneck |
| **zerolog**     | similar speed to zap, chainable API; same caveat                                                |
| **log.Println** | dead. Free-form, unparseable, no level, no fields.                                              |

The micro-benchmark gap (slog ~500ns/op vs zap ~200ns/op) is irrelevant for 99% of services. Match the stdlib unless you've proven otherwise.

## Bootstrap

```go
// Pick the level from $LOG_LEVEL (default INFO). Use a LevelVar so the level can be
// changed at runtime (e.g., via an admin endpoint) without restarting.
var levelVar = new(slog.LevelVar)  // package-level so other code can flip it

func levelFromEnv() *slog.LevelVar {
    switch strings.ToUpper(os.Getenv("LOG_LEVEL")) {
    case "DEBUG": levelVar.Set(slog.LevelDebug)
    case "WARN":  levelVar.Set(slog.LevelWarn)
    case "ERROR": levelVar.Set(slog.LevelError)
    default:      levelVar.Set(slog.LevelInfo)
    }
    return levelVar
}

func setupLogger() *slog.Logger {
    h := slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{
        Level:     levelFromEnv(),               // INFO default, DEBUG via $LOG_LEVEL
        AddSource: false,                        // true only in dev — adds file:line, costly
        ReplaceAttr: func(_ []string, a slog.Attr) slog.Attr {
            if a.Key == slog.TimeKey { a.Value = slog.StringValue(a.Value.Time().UTC().Format(time.RFC3339Nano)) }
            return a
        },
    })
    logger := slog.New(h).With(
        slog.String("service", "myapp"),
        slog.String("version", buildVersion),
    )
    slog.SetDefault(logger)        // sets default for log/slog package-level helpers
    return logger
}
```

`slog.SetDefault` updates `log` package routing too — `log.Println` calls now go through slog. One handler per process; mixing JSON and Text in one app is a parser nightmare.

## Levels

| Level   | Use                                                          |
| ------- | ------------------------------------------------------------ |
| `DEBUG` | local dev, opt-in via env; can be verbose                    |
| `INFO`  | normal operations — server start, request completed, job ran |
| `WARN`  | degraded state, recoverable — retry succeeded, fallback used |
| `ERROR` | something failed — log once, return wrapped error to caller  |

There is no `FATAL`. If it's fatal, `log.Fatal` or `os.Exit` after the log — don't invent a level. There is no `TRACE` — use `DEBUG` with attrs.

## Attrs — not message strings

```go
// WRONG — unparseable, can't filter, can't aggregate
slog.Info(fmt.Sprintf("user %s logged in from %s", userID, ip))

// RIGHT — structured, queryable
slog.Info("user logged in",
    slog.String("user_id", userID),
    slog.String("ip", ip),
    slog.Duration("auth_ms", elapsed),
)
```

For perf-sensitive sites use `LogAttrs` (avoids the variadic `...any` allocation):

```go
logger.LogAttrs(ctx, slog.LevelInfo, "request done",
    slog.String("method", r.Method),
    slog.Int("status", rec.Status),
    slog.Duration("dur", time.Since(start)),
)
```

## Context propagation — correlation IDs

```go
type ctxKey struct{}
var loggerKey = ctxKey{}

func WithLogger(ctx context.Context, l *slog.Logger) context.Context {
    return context.WithValue(ctx, loggerKey, l)
}
func From(ctx context.Context) *slog.Logger {
    if l, ok := ctx.Value(loggerKey).(*slog.Logger); ok { return l }
    return slog.Default()
}

// In HTTP middleware:
func slogMiddleware(base *slog.Logger) func(http.Handler) http.Handler {
    return func(next http.Handler) http.Handler {
        return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
            reqID := middleware.GetReqID(r.Context())     // chi RequestID
            l := base.With(
                slog.String("request_id", reqID),
                slog.String("method", r.Method),
                slog.String("path", r.URL.Path),
            )
            ctx := WithLogger(r.Context(), l)
            next.ServeHTTP(w, r.WithContext(ctx))
        })
    }
}

// In handlers/services:
go func(ctx context.Context) { From(ctx).Info("job started", ...) }(ctx)
```

Every log line in the request lifecycle now carries `request_id` — trivial to grep across services.

## Groups + nested attrs

```go
slog.Info("db query",
    slog.Group("db",
        slog.String("op", "SELECT"),
        slog.String("table", "users"),
        slog.Duration("dur", d),
    ),
)
// → "db":{"op":"SELECT","table":"users","dur":"3.2ms"}
```

Group related attrs — keeps query DSLs (Loki, Datadog) clean.

## Custom handlers

`slog.Handler` is an interface — wrap, filter, redact, route by attr. Common pattern: redact handler that scrubs `password`, `token`, `authorization` from attrs before delegating to JSON handler.

## Anti-patterns

- `log.Println("user", uid, "did", action)` after slog adoption — free-form, mixed sources
- Multiple handler types in one process — half your logs JSON, half text
- `slog.Info(fmt.Sprintf(...))` — defeats the entire point
- Logging AND returning the error — caller logs again, double-write
- `AddSource: true` in prod — runtime cost per call; only in dev
- No correlation ID — cannot trace a request across services
- `DEBUG` left on in production — log volume explodes, cost spikes
- Logging secrets — passwords, tokens, PII into a JSON line that lands in a 90-day retention bucket

## Red flags

| Thought                         | Reality                                                               |
| ------------------------------- | --------------------------------------------------------------------- |
| "JSON is hard to read in dev"   | Pipe through `jq`, or use TextHandler **only in dev** via env switch. |
| "Just one printf for debugging" | It ships to prod, gets parsed as garbage, costs $$ to ingest.         |
| "slog is too verbose"           | The verbosity is the value — every field is queryable.                |
| "I'll add request IDs later"    | First incident without them means a retrofit in a hurry.              |

## Hand-off

For tracing + metrics + alerts: `Skill(observability-essentials)`. For HTTP middleware wiring: `Skill(go-chi)`. For error wrapping rules: `Skill(go-essentials)`.
