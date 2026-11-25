---
name: golang
description: "Golang backend development skill for REST APIs with Chi router, PostgreSQL, and layered architecture. Use when implementing Go backend code."
---

# Golang Backend Development

## Purpose

This skill provides the knowledge and conventions for building production-grade Go REST APIs. It covers project structure, layered architecture (Handler -> Service -> Repository), database access with PostgreSQL, routing with Chi, and all supporting concerns (config, logging, error handling, validation, graceful shutdown). The go-dev agent uses this skill to implement backend API code that integrates with a React frontend.

## Project Structure

```
project-root/
  cmd/
    server/
      main.go                # Entry point: config load, DI wiring, server start, graceful shutdown
  internal/
    config/
      config.go              # Struct with env tags, Load() function
    handler/
      health.go              # Health check handler
      {resource}.go          # HTTP handlers per resource (one file per domain entity)
      response.go            # Shared JSON response helpers (Success, Error, Paginated)
    service/
      {resource}.go          # Business logic per resource
    repository/
      {resource}.go          # Database queries per resource
    model/
      {resource}.go          # Domain structs, DB models
      errors.go              # Custom error types
    middleware/
      auth.go                # JWT/session auth middleware
      cors.go                # CORS configuration
      logging.go             # Request logging middleware
      recovery.go            # Panic recovery middleware
      request_id.go          # Request ID injection
    router/
      router.go              # Chi router setup, route registration, middleware chain
  migrations/
    000001_initial.up.sql    # golang-migrate format: {sequence}_{name}.{direction}.sql
    000001_initial.down.sql
  sqlc/                      # Optional: sqlc configuration and generated code
    sqlc.yaml
    query/
      {resource}.sql
    db/                      # Generated code (do not edit)
  go.mod
  go.sum
  Dockerfile
  .env.example
```

## Key Patterns

### Layered Architecture

The codebase follows strict layering. Dependencies flow inward only:

```
HTTP Request
  -> Middleware (auth, logging, CORS, recovery)
    -> Handler (parse request, validate, call service, write response)
      -> Service (business logic, orchestrate repos, enforce rules)
        -> Repository (database queries, no business logic)
          -> PostgreSQL
```

**Rules:**
- Handlers NEVER import repository packages or access the database directly.
- Repositories NEVER contain business logic, validation, or HTTP concepts.
- Services own all business rules and orchestrate one or more repositories.
- Each layer communicates through Go interfaces defined in the consuming package.

### Dependency Injection via Constructor Functions

Every layer uses constructor injection. No global state, no init() for wiring.

```go
// repository/user.go
type UserRepository struct {
    db *pgxpool.Pool
}

func NewUserRepository(db *pgxpool.Pool) *UserRepository {
    return &UserRepository{db: db}
}

// service/user.go
type UserService struct {
    repo *repository.UserRepository
}

func NewUserService(repo *repository.UserRepository) *UserService {
    return &UserService{repo: repo}
}

// handler/user.go
type UserHandler struct {
    svc *service.UserService
}

func NewUserHandler(svc *service.UserService) *UserHandler {
    return &UserHandler{svc: svc}
}
```

Wiring happens in `cmd/server/main.go`:

```go
db := mustConnectDB(cfg)
userRepo := repository.NewUserRepository(db)
userSvc := service.NewUserService(userRepo)
userHandler := handler.NewUserHandler(userSvc)
r := router.New(userHandler, ...)
```

### Chi Router

Chi is the preferred HTTP router. It is stdlib-compatible (`net/http` handlers).

```go
package router

import (
    "github.com/go-chi/chi/v5"
    chimw "github.com/go-chi/chi/v5/middleware"
)

func New(userH *handler.UserHandler) chi.Router {
    r := chi.NewRouter()

    // Global middleware stack (order matters)
    r.Use(chimw.RequestID)
    r.Use(chimw.RealIP)
    r.Use(middleware.Logger)       // custom structured logging
    r.Use(middleware.Recovery)     // panic recovery
    r.Use(middleware.CORS)         // CORS for React frontend
    r.Use(chimw.Timeout(30 * time.Second))

    // Health check (no auth)
    r.Get("/healthz", handler.HealthCheck)

    // API routes
    r.Route("/api/v1", func(r chi.Router) {
        // Public routes
        r.Post("/auth/login", authH.Login)
        r.Post("/auth/register", authH.Register)

        // Protected routes
        r.Group(func(r chi.Router) {
            r.Use(middleware.Auth)

            r.Route("/users", func(r chi.Router) {
                r.Get("/", userH.List)
                r.Post("/", userH.Create)
                r.Route("/{id}", func(r chi.Router) {
                    r.Get("/", userH.GetByID)
                    r.Put("/", userH.Update)
                    r.Delete("/", userH.Delete)
                })
            })
        })
    })

    return r
}
```

### PostgreSQL with pgx

Use `pgxpool` for connection pooling. Never use `database/sql` directly for PostgreSQL.

```go
import "github.com/jackc/pgx/v5/pgxpool"

func ConnectDB(ctx context.Context, databaseURL string) (*pgxpool.Pool, error) {
    config, err := pgxpool.ParseConfig(databaseURL)
    if err != nil {
        return nil, fmt.Errorf("parsing database URL: %w", err)
    }
    config.MaxConns = 25
    config.MinConns = 5
    config.MaxConnLifetime = time.Hour

    pool, err := pgxpool.NewWithConfig(ctx, config)
    if err != nil {
        return nil, fmt.Errorf("creating connection pool: %w", err)
    }
    if err := pool.Ping(ctx); err != nil {
        return nil, fmt.Errorf("pinging database: %w", err)
    }
    return pool, nil
}
```

**Query option A: sqlc (preferred for type safety)**

Define SQL in `.sql` files, generate Go code:

```sql
-- sqlc/query/user.sql
-- name: GetUserByID :one
SELECT id, email, name, created_at FROM users WHERE id = $1;

-- name: ListUsers :many
SELECT id, email, name, created_at FROM users ORDER BY created_at DESC LIMIT $1 OFFSET $2;

-- name: CreateUser :one
INSERT INTO users (email, name, password_hash) VALUES ($1, $2, $3) RETURNING id, email, name, created_at;
```

**Query option B: GORM**

Use only when project already has GORM or PRD specifies it. Prefer sqlc/pgx otherwise.

### Database Migrations

Use `golang-migrate` with file-based migrations.

```bash
migrate create -ext sql -dir migrations -seq {name}
migrate -path migrations -database "$DATABASE_URL" up
migrate -path migrations -database "$DATABASE_URL" down 1
```

Migration files are pure SQL. One up file, one down file per migration. Down migrations must be reversible.

### Error Handling

Define domain error types in `internal/model/errors.go`:

```go
package model

import "errors"

var (
    ErrNotFound      = errors.New("resource not found")
    ErrConflict      = errors.New("resource already exists")
    ErrUnauthorized  = errors.New("unauthorized")
    ErrForbidden     = errors.New("forbidden")
    ErrBadRequest    = errors.New("bad request")
    ErrInternal      = errors.New("internal server error")
)

// ValidationError carries field-level validation details.
type ValidationError struct {
    Field   string `json:"field"`
    Message string `json:"message"`
}

type ValidationErrors []ValidationError

func (ve ValidationErrors) Error() string {
    return fmt.Sprintf("%d validation error(s)", len(ve))
}
```

Always wrap errors with context using `fmt.Errorf("doing thing: %w", err)`. Handlers map domain errors to HTTP status codes:

```go
func mapErrorToStatus(err error) int {
    switch {
    case errors.Is(err, model.ErrNotFound):
        return http.StatusNotFound
    case errors.Is(err, model.ErrConflict):
        return http.StatusConflict
    case errors.Is(err, model.ErrUnauthorized):
        return http.StatusUnauthorized
    case errors.Is(err, model.ErrForbidden):
        return http.StatusForbidden
    case errors.Is(err, model.ErrBadRequest):
        return http.StatusBadRequest
    default:
        return http.StatusInternalServerError
    }
}
```

### Configuration

Use environment variables. Load with `envconfig` or `viper`.

```go
package config

import "github.com/kelseyhightower/envconfig"

type Config struct {
    Port        int    `envconfig:"PORT" default:"8080"`
    DatabaseURL string `envconfig:"DATABASE_URL" required:"true"`
    JWTSecret   string `envconfig:"JWT_SECRET" required:"true"`
    CORSOrigins string `envconfig:"CORS_ORIGINS" default:"http://localhost:3000"`
    LogLevel    string `envconfig:"LOG_LEVEL" default:"info"`
    Environment string `envconfig:"ENVIRONMENT" default:"development"`
}

func Load() (*Config, error) {
    var cfg Config
    if err := envconfig.Process("", &cfg); err != nil {
        return nil, fmt.Errorf("loading config: %w", err)
    }
    return &cfg, nil
}
```

### Request/Response JSON

Use dedicated request and response structs. Never bind directly to domain models.

```go
// handler/user.go
type CreateUserRequest struct {
    Email    string `json:"email" validate:"required,email"`
    Name     string `json:"name" validate:"required,min=2,max=100"`
    Password string `json:"password" validate:"required,min=8"`
}

type UserResponse struct {
    ID        string    `json:"id"`
    Email     string    `json:"email"`
    Name      string    `json:"name"`
    CreatedAt time.Time `json:"created_at"`
}
```

Validate with `go-playground/validator`:

```go
import "github.com/go-playground/validator/v10"

var validate = validator.New()

func decodeAndValidate[T any](r *http.Request) (T, error) {
    var req T
    if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
        return req, fmt.Errorf("%w: %s", model.ErrBadRequest, err.Error())
    }
    if err := validate.Struct(req); err != nil {
        return req, toValidationErrors(err)
    }
    return req, nil
}
```

### Structured Logging

Use `log/slog` (stdlib, Go 1.21+). No external logging libraries needed.

```go
logger := slog.New(slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{
    Level: slog.LevelInfo,
}))
slog.SetDefault(logger)

slog.Info("server starting", "port", cfg.Port, "env", cfg.Environment)
slog.Error("query failed", "err", err, "user_id", userID)
```

### Graceful Shutdown

```go
func main() {
    // ... setup ...

    srv := &http.Server{
        Addr:         fmt.Sprintf(":%d", cfg.Port),
        Handler:      r,
        ReadTimeout:  15 * time.Second,
        WriteTimeout: 15 * time.Second,
        IdleTimeout:  60 * time.Second,
    }

    go func() {
        slog.Info("server listening", "addr", srv.Addr)
        if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
            slog.Error("server error", "err", err)
            os.Exit(1)
        }
    }()

    quit := make(chan os.Signal, 1)
    signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
    <-quit

    slog.Info("shutting down server")
    ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
    defer cancel()

    if err := srv.Shutdown(ctx); err != nil {
        slog.Error("server shutdown error", "err", err)
    }
    pool.Close()
    slog.Info("server stopped")
}
```

### Docker Multi-Stage Build

```dockerfile
FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-s -w" -o /server ./cmd/server

FROM alpine:3.19
RUN apk --no-cache add ca-certificates
WORKDIR /app
COPY --from=builder /server .
COPY migrations/ ./migrations/
EXPOSE 8080
CMD ["./server"]
```

## Conventions

### Naming

- Package names: lowercase, single word, no underscores. `handler` not `handlers`.
- Files: lowercase, snake_case. `user_repository.go`.
- Interfaces: verb-noun or -er suffix. `UserReader`, `Authenticator`.
- Constructors: `NewXxx` pattern.
- Error variables: `ErrXxx` pattern.
- Context: always first parameter, named `ctx`.
- Unexported helpers: keep in same file as caller.

### Module Conventions

- Module path matches repo: `github.com/{org}/{repo}`.
- Run `go mod tidy` after adding dependencies.
- Pin major versions. Use `go get package@latest` for updates.

### Linting

Run `golangci-lint run ./...` before reporting. Key linters:
- `errcheck`: all errors must be handled.
- `govet`: catches common mistakes.
- `staticcheck`: advanced static analysis.
- `unused`: no dead code.

### Testing Conventions

- Test files: `{name}_test.go` in same package.
- Table-driven tests for multiple cases.
- Use `testify/assert` or stdlib `testing` only.
- Repository tests use a test database or `pgxmock`.
- Handler tests use `httptest.NewRecorder()` and `httptest.NewRequest()`.

### Comments

- All exported functions, types, and constants MUST have doc comments.
- Comment format: `// FunctionName does X.` (starts with the name).
- Package comment in one file per package (usually `doc.go` or the primary file).

## Knowledge Strategy

- **Patterns to capture:** Successful handler/service/repo patterns, middleware implementations, query patterns, error handling approaches discovered during implementation.
- **Examples to collect:** Working endpoint implementations (full vertical slice), migration patterns, test patterns.
- **Update permission:** Agents may freely add/update files in `references/`. Changes to `SKILL.md` or `scripts/` require user approval.
