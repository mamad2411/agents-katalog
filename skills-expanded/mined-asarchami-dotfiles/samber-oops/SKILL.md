---
name: samber-oops
description: "context/wrap — structured error handling with samber/oops: wrap errors with stack traces, codes, and key-value attributes at every layer boundary. Use when wrapping errors through a call stack, attaching attributes (user ID, query, request, tenant) to failures, keeping messages low-cardinality for APM grouping, recovering panics at goroutine boundaries, or reviewing error paths for missing context."
license: MIT
---

# samber/oops

**Context/wrap.** Every error is a structured record — domain, attributes, code, trace — sufficient for an on-call engineer to diagnose it without the developer. The discipline is to **wrap** at every layer boundary, attach the context that layer knows, keep the message static and low-cardinality, and let variable data travel in `.With()` attributes so APM tools (Datadog, Loki, Sentry) group errors correctly.

## Steps — wrap an error

1. **Build with the fluent chain.** Start with `.In(domain)`, add `.Tags`, `.Code`, `.With`; finish with a terminal method: `.Errorf` (new error), `.Wrap`/`.Wrapf` (existing), `.Join` (combine), `.Recover` (panic).
   *Done when: every error carries a domain, and any error crossing a public boundary carries a machine-readable Code.*
2. **Wrap at each layer boundary.** Each package boundary adds the context it knows via `oops.Wrapf(err, "operation failed")`. `Wrap` returns nil for a nil err — call it directly, no nil check needed.
   *Done when: every layer boundary wraps exactly once, and no `if err != nil` guard wraps a Wrap.*
3. **Keep messages low-cardinality.** Put runtime values in `.With("user_id", userID)` and keep the message static — interpolating IDs breaks grouping in Datadog, Loki, and Sentry.
   *Done when: no error message interpolates a value that belongs in an attribute.*
4. **Enrich with identity and traffic.** `.Request`/`.Response` attach HTTP traffic, `.User`/`.Tenant` carry identity, `.Trace`/`.Span` carry correlation IDs, `.Hint`/`.Owner` point the next engineer to a runbook or team.
   *Done when: errors at handler/service boundaries carry request, identity, and trace context.*
5. **Recover at goroutine boundaries.** `.Recover(fn)` converts a panic into a structured error; add `.Code("panic_recovered")` and `.Hint(...)` so the recovery is actionable.
   *Done when: no `go func` or handler boundary lets a panic escape.*
6. **Read it back at the top.** Type-assert to `oops.OopsError` for Code/Domain/Tags/Context/Stacktrace; `oops.GetPublic(err, fallback)` for the user-safe message.
   *Done when: the top layer emits a diagnostic (stack + attributes) and a public message without extra plumbing.*

## Steps — review or audit

1. **Scan messages for interpolation.** *Done when: no message interpolates a runtime ID.*
2. **Check each boundary wraps once.** *Done when: every layer adds its own context, and no nil-check guards a Wrap.*
3. **Check panic boundaries.** *Done when: every goroutine/handler boundary recovers.*
4. **Verify attribute keys are stable.** *Done when: attribute keys are static identifiers, never values.*

## Reference

### Terminal methods

- `.Errorf(format, args...)` — create a new error
- `.Wrap(err)` — wrap an existing error
- `.Wrapf(err, format, args...)` — wrap with a message
- `.Join(err1, err2, ...)` — combine multiple errors
- `.Recover(fn)` / `.Recoverf(fn, format, args...)` — convert panic to error

### Builder methods

| Methods | Use case |
| --- | --- |
| `.With("key", value)` | Add custom key-value attribute (lazy `func() any` values supported) |
| `.WithContext(ctx, "key1", "key2")` | Extract values from Go context into attributes (lazy values supported) |
| `.In("domain")` | Set the feature/service/domain |
| `.Tags("auth", "sql")` | Add categorization tags (query with `err.HasTag("tag")`) |
| `.Code("iam_authz_missing_permission")` | Set machine-readable error identifier/slug |
| `.Public("Could not fetch user.")` | Set user-safe message (separate from technical details) |
| `.Hint("Runbook: https://doc.acme.org/doc/abcd.md")` | Add debugging hint for developers |
| `.Owner("team/slack")` | Identify responsible team/owner |
| `.User(id, "k", "v")` | Add user identifier and attributes |
| `.Tenant(id, "k", "v")` | Add tenant/organization context and attributes |
| `.Trace(id)` | Add trace / correlation ID (default: ULID) |
| `.Span(id)` | Add span ID representing a unit of work/operation (default: ULID) |
| `.Time(t)` | Override error timestamp (default: `time.Now()`) |
| `.Since(t)` | Set duration based on time since `t` (exposed via `err.Duration()`) |
| `.Duration(d)` | Set explicit error duration |
| `.Request(req, includeBody)` | Attach `*http.Request` (optionally including body) |
| `.Response(res, includeBody)` | Attach `*http.Response` (optionally including body) |
| `oops.FromContext(ctx)` | Start from an `OopsErrorBuilder` stored in a Go context |

### Layer-by-layer wrapping

```go
func Controller() error {
    return oops.In("controller").Trace(traceID).Wrapf(Service(), "user request failed")
}

func Service() error {
    return oops.In("service").With("op", "create_user").Wrapf(Repository(), "db operation failed")
}

func Repository() error {
    return oops.In("repository").Tags("database", "postgres").Errorf("connection timeout")
}
```

### Accessing error information

```go
if oopsErr, ok := err.(oops.OopsError); ok {
    fmt.Println("Code:", oopsErr.Code())
    fmt.Println("Domain:", oopsErr.Domain())
    fmt.Println("Tags:", oopsErr.Tags())
    fmt.Println("Context:", oopsErr.Context())
    fmt.Println("Stacktrace:", oopsErr.Stacktrace())
}

// Get public-facing message with fallback
publicMsg := oops.GetPublic(err, "Something went wrong")
```

### Output formats

```go
fmt.Printf("%+v\n", err)       // verbose with stack trace
bytes, _ := json.Marshal(err)  // JSON for logging
slog.Error(err.Error(), slog.Any("error", err))  // slog integration
```

### Context propagation

```go
func middleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        builder := oops.
            In("http").
            Request(r, false).
            Trace(r.Header.Get("X-Trace-ID"))

        ctx := oops.WithBuilder(r.Context(), builder)
        next.ServeHTTP(w, r.WithContext(ctx))
    })
}

func handler(ctx context.Context) error {
    return oops.FromContext(ctx).Tags("handler", "users").Errorf("something failed")
}
```

### Deep references

- **[Advanced patterns](./references/advanced.md)** — assertions, configuration, and additional logger examples

### Official resources

- [github.com/samber/oops](https://github.com/samber/oops)
- [pkg.go.dev/github.com/samber/oops](https://pkg.go.dev/github.com/samber/oops)

## Watch for

| Mistake | Fix |
| --- | --- |
| Interpolating user/tenant IDs into the message | Static message + `.With("user_id", id)` |
| `if err != nil { return oops.Wrapf(...) }` | `return oops.Wrapf(err, ...)` — nil-safe |
| Context added only at the log site | Wrap at each layer boundary |
| No Code on a public-boundary error | `.Code("snake_case_id")` at the edge |
| Panic escaping a goroutine | `.Recover` at the boundary |
| Message and attribute duplicating the same fact | One home per fact — the attribute |

## Cross-references

- → See `samber-slog` for logger integration with structured errors
- → See `samber-mo` for error-as-values and functional composition
- → See `samber-ro` for the oops error plugin inside reactive streams
- → See `go-safety` for error handling and nil-safety
- → See `go-observability` for structured logging and APM grouping
