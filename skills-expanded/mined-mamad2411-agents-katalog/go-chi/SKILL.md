---
name: go-chi
description: Use when building HTTP services with chi — routing, middleware composition, sub-routers, context-first handlers.
metadata:
  added: 2026-05-18
  last_reviewed: 2026-05-18
  type: language
  languages: [go]
  status: active
  invokes_shell: false
  shell_reviewed: "valksor 2026-05-17"
  related: [go-essentials, go-concurrency, go-slog]
---

# Go chi

**Iron Law: middleware is a pipeline — compose top-down, never mutate `*http.Request` without recording, always plumb `r.Context()`. Handlers stay `http.Handler`-compatible.**

## Why chi (vs gin / echo / stdlib)

| Framework                          | Verdict                                                                                                               |
| ---------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| **chi**                            | stdlib-compatible (`http.Handler`), zero deps, minimal magic — pick for services that should outlive the framework    |
| **gin**                            | fast, batteries-included, custom `Context` — fine if team already knows it; locks you in                              |
| **echo**                           | similar to gin, slightly cleaner API; same lock-in                                                                    |
| **stdlib `http.ServeMux` (1.22+)** | now does path patterns + methods — sufficient for ≤ 20 routes; chi wins past that for middleware groups + sub-routers |

## Router skeleton

```go
r := chi.NewRouter()
r.Use(middleware.RequestID)
r.Use(middleware.RealIP)
r.Use(middleware.Recoverer)         // catches panics → 500 + log
r.Use(middleware.Timeout(30 * time.Second))
r.Use(slogMiddleware(logger))       // your structured logger

r.Get("/healthz", healthz)
r.Route("/api/v1", func(r chi.Router) {
    r.Use(authMiddleware(tokens))   // scoped to /api/v1/*
    r.Get("/users/{userID}", getUser)
    r.Mount("/admin", adminRouter())
})

srv := &http.Server{
    Addr: ":8080", Handler: r,
    ReadHeaderTimeout: 5 * time.Second,   // mitigate Slowloris
    BaseContext: func(net.Listener) context.Context { return rootCtx },
}
```

`Mount` for sub-routers from other packages, `Route` for inline grouping. Don't nest more than 3 deep — refactor into a sub-router with its own file.

## Route params + context

```go
func getUser(w http.ResponseWriter, r *http.Request) {
    id := chi.URLParam(r, "userID")              // path param
    q  := r.URL.Query().Get("include")           // query param
    u, err := svc.Get(r.Context(), id)           // ALWAYS pass r.Context()
    if err != nil { writeErr(w, err); return }
    writeJSON(w, u)
}
```

Never call `context.Background()` inside a handler — you lose cancellation, deadlines, and request-scoped values (request ID, trace span, auth principal).

## Middleware contract

```go
func authMiddleware(verify func(string) (*Principal, error)) func(http.Handler) http.Handler {
    return func(next http.Handler) http.Handler {
        return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
            // Strip Bearer prefix and validate non-empty before calling verify.
            // Passing the raw "Bearer <tok>" string to a JWT/HMAC verifier produces subtle
            // accept-on-partial-match bugs in some libraries.
            auth := r.Header.Get("Authorization")
            const prefix = "Bearer "
            if !strings.HasPrefix(auth, prefix) || len(auth) <= len(prefix) {
                http.Error(w, "unauthorized", http.StatusUnauthorized); return
            }
            p, err := verify(strings.TrimPrefix(auth, prefix))
            if err != nil { http.Error(w, "unauthorized", http.StatusUnauthorized); return }
            ctx := context.WithValue(r.Context(), principalKey{}, p)
            next.ServeHTTP(w, r.WithContext(ctx))   // r.WithContext, not mutate
        })
    }
}
```

`principalKey{}` is an unexported empty struct — never a string. Provide a typed getter: `func PrincipalFrom(ctx context.Context) (*Principal, bool)`.

## chi-provided middleware worth using

| Middleware                | Use                                                                   |
| ------------------------- | --------------------------------------------------------------------- |
| `middleware.RequestID`    | adds `X-Request-ID` — feed into logger + propagate to downstreams     |
| `middleware.RealIP`       | trust `X-Forwarded-For` ONLY behind a known proxy                     |
| `middleware.Recoverer`    | last-resort panic → 500; always wrap with structured logger first     |
| `middleware.Timeout`      | per-request deadline — backed by `ctx.Done()`; handlers MUST check    |
| `middleware.Compress`     | gzip/br negotiation                                                   |
| `middleware.StripSlashes` | one canonical form — pick `Strip` or `Redirect`, not both             |
| `middleware.Throttle`     | concurrent-request cap; for token bucket use `golang.org/x/time/rate` |

## Testing

```go
r := chi.NewRouter()
r.Get("/users/{id}", getUser)
req := httptest.NewRequest("GET", "/users/42", nil)
rec := httptest.NewRecorder()
r.ServeHTTP(rec, req)        // exercises router + middleware + handler
if rec.Code != http.StatusOK {
    t.Fatalf("status = %d, want 200; body=%s", rec.Code, rec.Body.String())
}
```

No special test client — `httptest` works because chi is `http.Handler`. Stdlib assertions only (`go-testing` lists testify packages as anti-pattern). See `Skill(devkit:go-testing)` for table-driven patterns.

## Anti-patterns

- Nesting `Route`/`Mount` more than 3 deep — middleware order becomes unreadable
- Middleware that mutates `r` directly instead of `r.WithContext(...)` — breaks downstream
- `context.Background()` in handlers — lose deadline, cancellation, request ID
- String-keyed context values — name collisions; use unexported typed keys
- Calling `chi.URLParam` in middleware before the router has bound it — empty string
- One giant `routes.go` with 200 routes — split by domain, mount sub-routers
- `middleware.Logger` (chi's bundled one) in production — use structured (`Skill(go-slog)`)
- Skipping `ReadHeaderTimeout` on `http.Server` — Slowloris CVE class
- `panic` inside handler relying on Recoverer for control flow — error returns are the path

## Red flags

| Thought                                | Reality                                                                              |
| -------------------------------------- | ------------------------------------------------------------------------------------ |
| "I'll grab the user ID from a global"  | request-scoped data belongs in `r.Context()`, full stop                              |
| "Middleware order doesn't matter"      | RequestID before logger; Recoverer last; auth before business — order is correctness |
| "Just use `gin.Context` — it's faster" | µs differences vs ergonomic lock-in; the bottleneck is your DB                       |
| "I'll do auth in the handler"          | scattered auth = missed auth; do it in middleware bound to the protected sub-router  |

## Hand-off

For request-scoped concurrency (errgroup, cancellation, fan-out): `Skill(go-concurrency)`. For structured request logs: `Skill(go-slog)`. For testing handlers and middleware: `Skill(go-testing)`.
