---
name: go-slog-handlers-custom
description: >
  Custom slog.Handler implementations in Go: Handle/WithAttrs/WithGroup,
  wrapping handlers (redaction, sampling, fan-out), level dynamics, and testing
  handlers. Use when standard JSON/text handlers are insufficient for owned apps.
---

# Go slog Custom Handlers

## Scope And Authorization

- **In scope:** Logging pipelines in code you maintain.
- **Out of scope:** Handlers that exfiltrate logs to third parties without authorization.
- Custom handlers must remain concurrency-safe; never log secrets.
- Pair with `go-slog-structured-logging` for adoption patterns and `logging-message-style`.

## When To Use

- Redacting sensitive attributes centrally.
- Sampling high-volume debug logs.
- Dual-writing to OTLP + stdout.
- Adding static service attributes without caller burden.
- Bridging slog to an existing enterprise log SDK.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| slog adoption / levels / context | `go-slog-structured-logging` |
| Log message wording | `logging-message-style` |
| OpenTelemetry traces | `go-otel-autoinstrument` |
| Go style | `go-style-conventions` |
| Implementation quality | `code-quality-standards` |

## Concepts

| Method | Contract |
| --- | --- |
| `Enabled(ctx, level)` | Fast gate |
| `Handle(ctx, record)` | Emit one record; record invalid after return |
| `WithAttrs` | Return handler with bound attrs |
| `WithGroup` | Namespace subsequent attrs |
| Wrap | Compose behaviors |

Records must be cloned if retained asynchronously (`record.Clone()`).

## Workflow

### 1. Prefer wrap over rewrite

```go
// Wrap JSON handler with redaction
base := slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{Level: slog.LevelInfo})
h := NewRedactHandler(base, []string{"password", "token", "authorization"})
slog.SetDefault(slog.New(h))
```

### 2. Minimal middleware handler

```go
type MiddlewareHandler struct {
    next slog.Handler
    // hooks
}

func (h *MiddlewareHandler) Enabled(ctx context.Context, l slog.Level) bool {
    return h.next.Enabled(ctx, l)
}

func (h *MiddlewareHandler) Handle(ctx context.Context, r slog.Record) error {
    // inspect/transform attrs via r.Attrs
    return h.next.Handle(ctx, r)
}

func (h *MiddlewareHandler) WithAttrs(attrs []slog.Attr) slog.Handler {
    return &MiddlewareHandler{next: h.next.WithAttrs(attrs)}
}

func (h *MiddlewareHandler) WithGroup(name string) slog.Handler {
    return &MiddlewareHandler{next: h.next.WithGroup(name)}
}
```

Always propagate `WithAttrs`/`WithGroup` to `next`.

### 3. Redaction pattern

```go
func redactAttr(a slog.Attr) slog.Attr {
    switch strings.ToLower(a.Key) {
    case "password", "token", "secret", "authorization":
        return slog.String(a.Key, "[REDACTED]")
    }
    if a.Value.Kind() == slog.KindGroup {
        // recurse group values as needed
    }
    return a
}
```

Apply during `Handle` by rebuilding attrs or using replace attr hook on `HandlerOptions.ReplaceAttr` when sufficient — custom handler only if replace is not enough.

### 4. Sampling handler

```go
// Allow all >= Error; sample Info at 1%
if r.Level < slog.LevelError && !sampler.Allow() {
    return nil
}
```

Document sampling ratios; never sample away security audit events.

### 5. Fan-out / async

```go
// Fan-out: call multiple next handlers; decide error aggregation
// Async: clone record, enqueue; drop policy under backpressure
r2 := r.Clone()
```

Backpressure: prefer drop+metric over unbounded queues.

### 6. Dynamic level

```go
var levelVar slog.LevelVar
levelVar.Set(slog.LevelInfo)
h := slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{Level: &levelVar})
// HTTP debug endpoint authorized to flip levelVar — protect it
```

### 7. Test handlers

```go
var buf bytes.Buffer
h := slog.NewTextHandler(&buf, nil)
logger := slog.New(h)
logger.Info("x", "k", "v")
// assert buf contents
```

For custom handlers, use `slog.New` + capture next with a recording stub implementing `slog.Handler`.

### 8. Verify

- Concurrent `Info` from many goroutines without data races (`go test -race`).
- WithGroup nesting matches expectations in JSON output.
- Redaction covers nested maps if required.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Composition | Wrap std handlers | Reimplement JSON encoding poorly |
| Async | Clone records | Use record after Handle returns |
| Secrets | Central redaction | Hope callers remember |
| Groups | Propagate WithGroup | Drop groups silently |
| Sampling | Never sample audit | Sample auth failures away |

## Output Checklist

- [ ] Handler implements all four methods correctly
- [ ] WithAttrs/WithGroup delegated
- [ ] Record clone if async
- [ ] Concurrency race-tested
- [ ] Redaction/sampling policies documented
- [ ] Tests with stub/buffer
- [ ] Default logger wired in main
- [ ] `code-quality-standards` applied

## Rules

- Do not log secrets; redact by default for sensitive keys.
- Clone records before retaining.
- Keep Enabled cheap.
- Prefer ReplaceAttr for simple cases; custom handler for multi-step pipelines.
- Adoption patterns live in `go-slog-structured-logging`.
