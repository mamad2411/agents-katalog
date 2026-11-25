---
name: golang-http
description: "When to activate: net/http server, HTTP handlers, middleware, ServeMux, timeouts, TLS, HTTP client in Go"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: engineering
  language: go
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# Go net/http Patterns

## HTTP Server with Timeouts

```go
func NewServer(addr string, handler http.Handler) *http.Server {
    return &http.Server{
        Addr:              addr,
        Handler:           handler,
        ReadTimeout:       5 * time.Second,
        WriteTimeout:      10 * time.Second,
        IdleTimeout:       120 * time.Second,
        ReadHeaderTimeout: 2 * time.Second,
        MaxHeaderBytes:    1 << 20,  // 1 MB
    }
}
```

## ServeMux and Handlers (Go 1.22+)

```go
mux := http.NewServeMux()

// Go 1.22+ pattern matching with method and path
mux.HandleFunc("GET /users",          listUsers)
mux.HandleFunc("POST /users",         createUser)
mux.HandleFunc("GET /users/{id}",     getUser)
mux.HandleFunc("PUT /users/{id}",     updateUser)
mux.HandleFunc("DELETE /users/{id}",  deleteUser)

// Path value extraction
func getUser(w http.ResponseWriter, r *http.Request) {
    id := r.PathValue("id")
    // ...
}
```

## Middleware Chain

```go
type Middleware func(http.Handler) http.Handler

func Chain(h http.Handler, middlewares ...Middleware) http.Handler {
    for i := len(middlewares) - 1; i >= 0; i-- {
        h = middlewares[i](h)
    }
    return h
}

func RequestID(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        id := r.Header.Get("X-Request-ID")
        if id == "" { id = uuid.New().String() }
        w.Header().Set("X-Request-ID", id)
        ctx := context.WithValue(r.Context(), requestIDKey{}, id)
        next.ServeHTTP(w, r.WithContext(ctx))
    })
}

func Logging(logger *slog.Logger) Middleware {
    return func(next http.Handler) http.Handler {
        return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
            start := time.Now()
            rw := &responseWriter{ResponseWriter: w, status: 200}
            next.ServeHTTP(rw, r)
            logger.Info("request",
                "method", r.Method,
                "path", r.URL.Path,
                "status", rw.status,
                "duration", time.Since(start),
            )
        })
    }
}

type responseWriter struct {
    http.ResponseWriter
    status int
}
func (rw *responseWriter) WriteHeader(code int) {
    rw.status = code
    rw.ResponseWriter.WriteHeader(code)
}

// Wire up
handler := Chain(mux, RequestID, Logging(logger), Recovery)
```

## JSON Helpers

```go
func writeJSON(w http.ResponseWriter, status int, v any) {
    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(status)
    if err := json.NewEncoder(w).Encode(v); err != nil {
        slog.Error("encode response", "err", err)
    }
}

func readJSON(r *http.Request, v any) error {
    r.Body = http.MaxBytesReader(nil, r.Body, 1<<20)  // 1 MB limit
    dec := json.NewDecoder(r.Body)
    dec.DisallowUnknownFields()
    if err := dec.Decode(v); err != nil {
        return fmt.Errorf("decode: %w", err)
    }
    return nil
}
```

## HTTP Client Best Practices

```go
var httpClient = &http.Client{
    Timeout: 10 * time.Second,
    Transport: &http.Transport{
        MaxIdleConns:        100,
        MaxIdleConnsPerHost: 20,
        IdleConnTimeout:     90 * time.Second,
        TLSHandshakeTimeout: 5 * time.Second,
        DisableKeepAlives:   false,
    },
}

func get(ctx context.Context, url string) ([]byte, error) {
    req, err := http.NewRequestWithContext(ctx, http.MethodGet, url, nil)
    if err != nil { return nil, err }
    req.Header.Set("Accept", "application/json")

    resp, err := httpClient.Do(req)
    if err != nil { return nil, err }
    defer resp.Body.Close()

    body, err := io.ReadAll(io.LimitReader(resp.Body, 10<<20))  // 10 MB
    if err != nil { return nil, err }

    if resp.StatusCode >= 400 {
        return nil, fmt.Errorf("HTTP %d: %s", resp.StatusCode, body)
    }
    return body, nil
}
```

## TLS Configuration

```go
tlsCfg := &tls.Config{
    MinVersion:               tls.VersionTLS13,
    PreferServerCipherSuites: true,
}

srv := &http.Server{
    Addr:      ":443",
    Handler:   mux,
    TLSConfig: tlsCfg,
}
srv.ListenAndServeTLS("cert.pem", "key.pem")

// Let\'s Encrypt with autocert
m := autocert.Manager{
    Cache:      autocert.DirCache("/var/www/.cache"),
    Prompt:     autocert.AcceptTOS,
    HostPolicy: autocert.HostWhitelist("example.com"),
}
srv.TLSConfig = m.TLSConfig()
```

## Common Anti-Patterns

- **`http.DefaultServeMux`** — use `http.NewServeMux()` to avoid package-level route pollution
- **No timeouts on server** — without timeouts, slow clients hold goroutines forever
- **`http.DefaultClient` for outbound calls** — no timeout; always create a custom client
- **Not limiting request body size** — use `http.MaxBytesReader` to prevent DoS via large bodies
- **Not closing response body** — always `defer resp.Body.Close()` after checking `err`
