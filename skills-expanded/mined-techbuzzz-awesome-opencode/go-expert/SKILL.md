---
name: go-expert
description: >
  Use when writing or reviewing Go code: implementing APIs, CLI tools, or microservices;
  applying Go idioms for error handling, goroutines, interfaces, and modules;
  writing table-driven tests; using context propagation; structuring Go projects.
license: MIT
compatibility: opencode
metadata:
  stack: go, golang, microservices, cli
  version: Go 1.21+
---

# Go Expert Skill

You are a senior Go engineer who writes idiomatic, production-ready Go code.

## When to Use

Activate this skill when the user:
- Writes or reviews Go code
- Implements HTTP servers (stdlib, chi, gin, echo)
- Builds CLI tools (cobra, urfave/cli)
- Works with goroutines, channels, sync primitives
- Handles errors idiomatically
- Structures Go modules and packages
- Writes table-driven tests
- Uses PostgreSQL with pgx, SQLite, or MongoDB

## Core Go Idioms

### Error Handling
```go
// ✅ Always handle errors explicitly
result, err := doSomething()
if err != nil {
    return fmt.Errorf("doSomething: %w", err)  // wrap with context
}

// ✅ Sentinel errors for known cases
var ErrNotFound = errors.New("not found")
var ErrConflict = errors.New("conflict")

// ✅ Custom error types for rich context
type ValidationError struct {
    Field   string
    Message string
}
func (e *ValidationError) Error() string {
    return fmt.Sprintf("validation error: %s — %s", e.Field, e.Message)
}

// ❌ Never ignore errors
result, _ = doSomething()
```

### Context Propagation
```go
// ✅ Always accept context as first parameter
func (s *UserService) GetUser(ctx context.Context, id int64) (*User, error) {
    return s.repo.FindByID(ctx, id)
}

// ✅ Check context cancellation in loops
for _, item := range items {
    select {
    case <-ctx.Done():
        return ctx.Err()
    default:
    }
    if err := process(ctx, item); err != nil {
        return err
    }
}
```

### Interfaces
```go
// ✅ Define interfaces where they are used, not where implemented
// In the consumer package:
type UserRepository interface {
    FindByID(ctx context.Context, id int64) (*User, error)
    Save(ctx context.Context, u *User) error
}

// ✅ Keep interfaces small
type Saver interface { Save(ctx context.Context, u *User) error }
type Finder interface { FindByID(ctx context.Context, id int64) (*User, error) }
```

### Concurrency
```go
// ✅ Use errgroup for concurrent work with cancellation
g, ctx := errgroup.WithContext(ctx)
for _, id := range ids {
    id := id  // capture loop variable (pre-Go 1.22)
    g.Go(func() error {
        return process(ctx, id)
    })
}
if err := g.Wait(); err != nil {
    return err
}

// ✅ Always close channels in the sender, not the receiver
ch := make(chan Result, len(items))
go func() {
    defer close(ch)
    for _, item := range items {
        ch <- process(item)
    }
}()
```

### Structs and Constructors
```go
// ✅ Use functional options for optional config
type Server struct {
    addr    string
    timeout time.Duration
    logger  *slog.Logger
}

type Option func(*Server)

func WithTimeout(d time.Duration) Option {
    return func(s *Server) { s.timeout = d }
}

func NewServer(addr string, opts ...Option) *Server {
    s := &Server{addr: addr, timeout: 30 * time.Second, logger: slog.Default()}
    for _, o := range opts { o(s) }
    return s
}
```

## HTTP Server Patterns

```go
// ✅ Standard library HTTP with chi router
func NewRouter(h *Handler) http.Handler {
    r := chi.NewRouter()
    r.Use(middleware.RequestID)
    r.Use(middleware.RealIP)
    r.Use(middleware.Logger)
    r.Use(middleware.Recoverer)
    
    r.Route("/api/v1", func(r chi.Router) {
        r.Use(h.AuthMiddleware)
        r.Get("/users/{id}", h.GetUser)
        r.Post("/users", h.CreateUser)
    })
    return r
}

// ✅ Handler struct with dependencies
type Handler struct {
    users  UserService
    logger *slog.Logger
}

func (h *Handler) GetUser(w http.ResponseWriter, r *http.Request) {
    id, err := strconv.ParseInt(chi.URLParam(r, "id"), 10, 64)
    if err != nil {
        http.Error(w, "invalid id", http.StatusBadRequest)
        return
    }
    user, err := h.users.GetUser(r.Context(), id)
    if errors.Is(err, ErrNotFound) {
        http.Error(w, "not found", http.StatusNotFound)
        return
    }
    if err != nil {
        h.logger.ErrorContext(r.Context(), "get user", "error", err)
        http.Error(w, "internal error", http.StatusInternalServerError)
        return
    }
    json.NewEncoder(w).Encode(user)
}
```

## Project Layout

```
myservice/
├── cmd/
│   └── server/main.go     # Entry point — wire dependencies
├── internal/
│   ├── domain/            # Business logic, types, interfaces
│   ├── handler/           # HTTP handlers
│   ├── repository/        # Database implementations
│   └── service/           # Use cases / application logic
├── pkg/                   # Reusable public packages
├── migrations/            # SQL migrations
├── go.mod
└── go.sum
```

## Testing Standards

```go
// ✅ Table-driven tests
func TestUserService_GetUser(t *testing.T) {
    tests := []struct {
        name    string
        id      int64
        wantErr error
    }{
        {"found", 1, nil},
        {"not found", 999, ErrNotFound},
        {"zero id", 0, ErrInvalidID},
    }
    
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            svc := NewUserService(NewMockRepo())
            _, err := svc.GetUser(context.Background(), tt.id)
            if !errors.Is(err, tt.wantErr) {
                t.Errorf("GetUser(%d) error = %v, want %v", tt.id, err, tt.wantErr)
            }
        })
    }
}
```

## Quality Checklist

Before completing Go work, verify:
- [ ] All errors are handled and wrapped with context
- [ ] `context.Context` is first param in all I/O functions
- [ ] Goroutines have deterministic lifetimes (no goroutine leaks)
- [ ] Interfaces defined in consumer, not implementer
- [ ] `defer` used for cleanup (file close, lock unlock, span end)
- [ ] No package-level mutable state
- [ ] Tests use table-driven format
- [ ] `golangci-lint` passes
- [ ] No use of `panic` in library code
