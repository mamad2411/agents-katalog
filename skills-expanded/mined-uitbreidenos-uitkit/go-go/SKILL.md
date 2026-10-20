---
name: "go"
description: "Go project layout, HTTP handlers, interfaces, goroutines, error wrapping, table-driven tests, slog logging"
---

# Go Skill

## When to activate
- Building a Go HTTP service or CLI tool
- Structuring a Go project with `cmd/`, `internal/`, `pkg/`
- Writing HTTP handlers with `net/http`, chi, or gin
- Implementing interfaces, embedding, and composition patterns
- Writing concurrent code with goroutines, channels, and `sync` primitives
- Error handling, wrapping, and sentinel errors
- Writing table-driven tests

## When NOT to use
- Node.js, Python, or other language services — different ecosystems
- Protobuf/gRPC services without prior gRPC setup context
- Pure scripting tasks — shell or Python are better fits

## Instructions

### Project layout
```
myapp/
├── cmd/
│   └── server/
│       └── main.go         # Entry point — thin, just wires and starts
├── internal/               # Private packages — not importable externally
│   ├── config/
│   ├── handler/
│   ├── service/
│   └── store/
├── pkg/                    # Public packages — importable by other modules
│   └── apierr/
├── go.mod
└── go.sum
```

### main.go — wiring only
```go
// cmd/server/main.go
package main

import (
    "context"
    "log/slog"
    "net/http"
    "os"
    "os/signal"
    "syscall"
    "time"

    "myapp/internal/config"
    "myapp/internal/handler"
    "myapp/internal/store"
)

func main() {
    cfg := config.MustLoad()
    db := store.MustConnect(cfg.DatabaseURL)
    defer db.Close()

    mux := handler.NewMux(db, cfg)

    srv := &http.Server{
        Addr:         ":" + cfg.Port,
        Handler:      mux,
        ReadTimeout:  10 * time.Second,
        WriteTimeout: 30 * time.Second,
        IdleTimeout:  60 * time.Second,
    }

    go func() {
        slog.Info("server starting", "addr", srv.Addr)
        if err := srv.ListenAndServe(); err != http.ErrServerClosed {
            slog.Error("server error", "err", err)
            os.Exit(1)
        }
    }()

    quit := make(chan os.Signal, 1)
    signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
    <-quit

    ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
    defer cancel()
    srv.Shutdown(ctx)
}
```

### Error handling
```go
// Define sentinel errors for expected conditions
var (
    ErrNotFound   = errors.New("not found")
    ErrDuplicate  = errors.New("duplicate entry")
    ErrForbidden  = errors.New("forbidden")
)

// Wrap errors with context — use %w to preserve unwrapping
func (s *UserStore) GetByID(ctx context.Context, id string) (*User, error) {
    var u User
    err := s.db.QueryRowContext(ctx, `SELECT id, email FROM users WHERE id = $1`, id).
        Scan(&u.ID, &u.Email)
    if errors.Is(err, sql.ErrNoRows) {
        return nil, fmt.Errorf("user %s: %w", id, ErrNotFound)
    }
    if err != nil {
        return nil, fmt.Errorf("user store get: %w", err)
    }
    return &u, nil
}

// Caller checks behavior, not message strings
user, err := store.GetByID(ctx, id)
if errors.Is(err, ErrNotFound) {
    http.Error(w, "not found", http.StatusNotFound)
    return
}
```

### HTTP handlers with chi
```go
// internal/handler/users.go
type UserHandler struct {
    svc UserService
}

func (h *UserHandler) Register(r chi.Router) {
    r.Get("/users/{id}", h.GetUser)
    r.Post("/users", h.CreateUser)
}

func (h *UserHandler) GetUser(w http.ResponseWriter, r *http.Request) {
    id := chi.URLParam(r, "id")
    user, err := h.svc.GetUser(r.Context(), id)
    if err != nil {
        renderError(w, err)
        return
    }
    renderJSON(w, http.StatusOK, user)
}

func renderJSON(w http.ResponseWriter, code int, v any) {
    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(code)
    json.NewEncoder(w).Encode(v)
}

func renderError(w http.ResponseWriter, err error) {
    switch {
    case errors.Is(err, ErrNotFound):
        http.Error(w, "not found", http.StatusNotFound)
    case errors.Is(err, ErrForbidden):
        http.Error(w, "forbidden", http.StatusForbidden)
    default:
        slog.Error("internal error", "err", err)
        http.Error(w, "internal server error", http.StatusInternalServerError)
    }
}
```

### Interfaces
```go
// Define interfaces where they're used (consumer side), not where implemented
// internal/handler/users.go
type UserService interface {
    GetUser(ctx context.Context, id string) (*User, error)
    CreateUser(ctx context.Context, req CreateUserRequest) (*User, error)
}

// Keep interfaces small — 1-3 methods preferred
// io.Reader, io.Writer are the canonical examples

// Embedding for composition
type ReadWriter interface {
    io.Reader
    io.Writer
}
```

### Concurrency patterns
```go
// Fan-out with errgroup
import "golang.org/x/sync/errgroup"

func fetchAll(ctx context.Context, ids []string) ([]*User, error) {
    g, ctx := errgroup.WithContext(ctx)
    results := make([]*User, len(ids))

    for i, id := range ids {
        i, id := i, id // capture loop vars
        g.Go(func() error {
            u, err := store.GetByID(ctx, id)
            if err != nil {
                return err
            }
            results[i] = u
            return nil
        })
    }

    if err := g.Wait(); err != nil {
        return nil, err
    }
    return results, nil
}

// Worker pool
func processJobs(ctx context.Context, jobs <-chan Job) {
    const workers = 10
    var wg sync.WaitGroup
    for range workers {
        wg.Add(1)
        go func() {
            defer wg.Done()
            for job := range jobs {
                if err := process(ctx, job); err != nil {
                    slog.Error("job failed", "id", job.ID, "err", err)
                }
            }
        }()
    }
    wg.Wait()
}
```

### Context propagation
```go
// Always propagate context as first argument
func (s *Service) DoWork(ctx context.Context, id string) error {
    // Pass ctx to all downstream calls
    user, err := s.store.GetByID(ctx, id)
    if err != nil {
        return err
    }
    return s.notifier.Send(ctx, user.Email)
}

// Store request-scoped values in context only for cross-cutting concerns
// (tracing IDs, auth info) — never for optional function parameters
type contextKey string
const requestIDKey contextKey = "request_id"

func WithRequestID(ctx context.Context, id string) context.Context {
    return context.WithValue(ctx, requestIDKey, id)
}
func GetRequestID(ctx context.Context) string {
    id, _ := ctx.Value(requestIDKey).(string)
    return id
}
```

### Table-driven tests
```go
func TestGetUser(t *testing.T) {
    tests := []struct {
        name    string
        id      string
        want    *User
        wantErr error
    }{
        {"found", "123", &User{ID: "123", Email: "a@b.com"}, nil},
        {"not found", "999", nil, ErrNotFound},
        {"empty id", "", nil, ErrNotFound},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            svc := newTestService(t)
            got, err := svc.GetUser(context.Background(), tt.id)
            if !errors.Is(err, tt.wantErr) {
                t.Fatalf("err = %v, want %v", err, tt.wantErr)
            }
            if diff := cmp.Diff(tt.want, got); diff != "" {
                t.Errorf("mismatch (-want +got):\n%s", diff)
            }
        })
    }
}
```

### Logging with slog
```go
// Structured logging — never fmt.Println in production code
slog.Info("request completed", "method", r.Method, "path", r.URL.Path, "status", 200, "duration_ms", elapsed.Milliseconds())
slog.Error("db query failed", "query", "getUserByID", "err", err)

// Set up JSON logger in main
logger := slog.New(slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{
    Level: slog.LevelInfo,
}))
slog.SetDefault(logger)
```

## Example

**User:** Build a Go HTTP API for a to-do list: create, list, and complete tasks. PostgreSQL backend, chi router, structured logging, graceful shutdown.

**Expected output:**
- `cmd/server/main.go` — wires store, handler, starts server with graceful shutdown
- `internal/store/task.go` — `TaskStore` with `Create`, `List`, `Complete` methods using `database/sql`
- `internal/handler/tasks.go` — `TaskHandler` with `Register(r chi.Router)`, JSON responses
- `internal/handler/tasks_test.go` — table-driven tests with a mock store

---
