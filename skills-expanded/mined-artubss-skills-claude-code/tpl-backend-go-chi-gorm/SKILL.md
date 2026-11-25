---
name: tpl-backend-go-chi-gorm
description: Template do pack (backend/04-go-chi-gorm.md). Orienta o agente em APIs, servicos e arquitetura backend alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: backend/04-go-chi-gorm.md
  generated_by: install_pack_templates_as_claude_skills
---

# PROJECT: Go REST API (Chi + GORM)

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `backend/04-go-chi-gorm.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

## STACK

| Technology | Version | Purpose |
|------------|---------|---------|
| Go | 1.22+ | Language + runtime |
| Chi | v5 | HTTP router + middleware |
| GORM | v2 | ORM + migrations |
| PostgreSQL | 16 | Primary database |
| pgx/v5 | 5.x | PostgreSQL driver |
| golang-jwt/jwt | v5 | JWT tokens |
| bcrypt | stdlib | Password hashing |
| testify | v1.9+ | Assertions + mocking |
| slog | stdlib (1.21+) | Structured logging |
| golangci-lint | 1.58+ | Linting suite |
| godotenv | 1.5+ | .env loader for dev |

---

## PROJECT STRUCTURE

```
cmd/
└── api/
    └── main.go           # Entry point: setup + server.ListenAndServe
internal/
├── config/
│   └── config.go         # Config struct + Load() from env
├── server/
│   └── server.go         # Chi router setup, middleware chain, routes
├── handlers/
│   └── users/
│       ├── handler.go    # HTTP handler methods (thin, calls service)
│       └── handler_test.go
├── services/
│   └── users/
│       ├── service.go    # Business logic interface + implementation
│       └── service_test.go
├── repositories/
│   └── users/
│       ├── repository.go # GORM queries implementing interface
│       └── repository_test.go
├── models/
│   └── user.go           # GORM model structs
├── middleware/
│   ├── auth.go           # JWT verification middleware
│   ├── logger.go         # Request logging middleware
│   └── recover.go        # Panic recovery middleware
├── dto/
│   └── users/
│       ├── request.go    # Input structs with validate tags
│       └── response.go   # Output structs (no sensitive fields)
└── database/
    └── database.go       # GORM db connection + AutoMigrate
go.mod
go.sum
.golangci.yml
Makefile
```

---

## ARCHITECTURE RULES

- **Handler → Service → Repository** — never skip levels
- Define interfaces in the **consumer** package (service defines its repo interface)
- Handlers receive `*Handler` with service interface injected via constructor
- Services receive `Repository` interface — not the concrete struct
- No global state — pass dependencies explicitly (no `db` package-level variable)
- All exported functions have godoc comments (`// FunctionName does X`)
- JSON tags on all struct fields — never rely on Go's default capitalization
- Time fields: always `time.Time` with `json:"created_at"` (UTC, no timezone stored)

---

## GO-SPECIFIC RULES

### Error Handling Pattern

**Rule:** Never ignore errors. Wrap with context. Return early on error.

```go
// Good — wrap errors with context
func (s *UserService) GetByID(ctx context.Context, id string) (*models.User, error) {
    user, err := s.repo.FindByID(ctx, id)
    if err != nil {
        if errors.Is(err, gorm.ErrRecordNotFound) {
            return nil, ErrUserNotFound // sentinel error
        }
        return nil, fmt.Errorf("UserService.GetByID: %w", err)
    }
    return user, nil
}

// Handler (convert service errors to HTTP responses)
func (h *UserHandler) GetUser(w http.ResponseWriter, r *http.Request) {
    id := chi.URLParam(r, "id")
    user, err := h.svc.GetByID(r.Context(), id)
    if err != nil {
        if errors.Is(err, service.ErrUserNotFound) {
            respondError(w, http.StatusNotFound, "user not found")
            return
        }
        slog.ErrorContext(r.Context(), "failed to get user", "error", err, "id", id)
        respondError(w, http.StatusInternalServerError, "internal error")
        return
    }
    respondJSON(w, http.StatusOK, toUserResponse(user))
}
```

### Interface Pattern

```go
// internal/repositories/users/repository.go
type UserRepository interface {
    FindByID(ctx context.Context, id string) (*models.User, error)
    FindByEmail(ctx context.Context, email string) (*models.User, error)
    Create(ctx context.Context, user *models.User) error
    Update(ctx context.Context, user *models.User) error
    Delete(ctx context.Context, id string) error
}
```

### Goroutine Safety Rules

- **Never** share mutable state between goroutines without a mutex or channel
- Use `context.Context` for cancellation — always accept `ctx context.Context` as first param
- Goroutines spawned in handlers must be tracked (use `errgroup.Group` or waitgroup)
- Database operations: GORM's `*gorm.DB` is safe for concurrent use (connection pool)
- Never close over loop variables in goroutines — capture explicitly

### Chi Middleware Pattern

```go
// internal/server/server.go
func NewRouter(cfg *config.Config, userHandler *userhandler.Handler) *chi.Mux {
    r := chi.NewRouter()

    // Global middlewares (order matters)
    r.Use(middleware.RequestID)
    r.Use(middleware.RealIP)
    r.Use(loggerMiddleware.New(slog.Default()))
    r.Use(recoverMiddleware.New())
    r.Use(chimiddleware.Timeout(30 * time.Second))

    r.Get("/health", func(w http.ResponseWriter, r *http.Request) {
        w.WriteHeader(http.StatusOK)
    })

    r.Route("/api/v1", func(r chi.Router) {
        r.Post("/auth/login", userHandler.Login)
        r.Post("/auth/register", userHandler.Register)

        r.Group(func(r chi.Router) {
            r.Use(authmiddleware.Authenticate(cfg.JWTSecret))
            r.Get("/users/me", userHandler.Me)
            r.Patch("/users/me", userHandler.UpdateMe)
        })
    })

    return r
}
```

### JWT Auth Middleware

```go
// internal/middleware/auth.go
func Authenticate(secret string) func(http.Handler) http.Handler {
    return func(next http.Handler) http.Handler {
        return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
            header := r.Header.Get("Authorization")
            if !strings.HasPrefix(header, "Bearer ") {
                http.Error(w, `{"error":"unauthorized"}`, http.StatusUnauthorized)
                return
            }
            tokenStr := header[7:]
            token, err := jwt.Parse(tokenStr, func(t *jwt.Token) (interface{}, error) {
                if _, ok := t.Method.(*jwt.SigningMethodHMAC); !ok {
                    return nil, fmt.Errorf("unexpected signing method: %v", t.Header["alg"])
                }
                return []byte(secret), nil
            })
            if err != nil || !token.Valid {
                http.Error(w, `{"error":"invalid or expired token"}`, http.StatusUnauthorized)
                return
            }
            claims := token.Claims.(jwt.MapClaims)
            ctx := context.WithValue(r.Context(), ctxKeyUserID, claims["sub"])
            next.ServeHTTP(w, r.WithContext(ctx))
        })
    }
}
```

### GORM Hooks

```go
// internal/models/user.go
func (u *User) BeforeCreate(tx *gorm.DB) error {
    u.ID = uuid.New().String()
    hashed, err := bcrypt.GenerateFromPassword([]byte(u.Password), bcrypt.DefaultCost)
    if err != nil {
        return fmt.Errorf("failed to hash password: %w", err)
    }
    u.Password = string(hashed)
    return nil
}
```

---

## ROUTING TABLE

| Trigger | Method | Route | Middleware | Handler |
|---------|--------|-------|-----------|---------|
| Register | POST | `/api/v1/auth/register` | — | UserHandler.Register |
| Login | POST | `/api/v1/auth/login` | — | UserHandler.Login |
| Refresh token | POST | `/api/v1/auth/refresh` | — | UserHandler.Refresh |
| Get my profile | GET | `/api/v1/users/me` | Authenticate | UserHandler.Me |
| Update profile | PATCH | `/api/v1/users/me` | Authenticate | UserHandler.UpdateMe |
| List users | GET | `/api/v1/users` | Authenticate, RequireAdmin | UserHandler.List |
| Get user | GET | `/api/v1/users/{id}` | Authenticate, RequireAdmin | UserHandler.Get |
| Delete user | DELETE | `/api/v1/users/{id}` | Authenticate, RequireAdmin | UserHandler.Delete |
| Health check | GET | `/health` | — | inline |

---

## QUALITY GATES

Before opening a PR, verify ALL of the following:

- [ ] `golangci-lint run ./...` passes with zero warnings
- [ ] `go test ./... -race -count=1` passes — no race conditions
- [ ] `go vet ./...` clean
- [ ] Coverage: `go test ./... -coverprofile=cover.out` ≥ 75%
- [ ] `go build ./cmd/api/...` compiles without warnings
- [ ] No `interface{}` — use `any` (Go 1.18+) or specific types
- [ ] All context parameters are first argument: `func F(ctx context.Context, ...)`
- [ ] No `log.Fatal` outside of `main.go`
- [ ] Database errors wrapped with context: `fmt.Errorf("repo.FindByID: %w", err)`
- [ ] Struct fields have `json` tags — no default field name exposure

---

## FORBIDDEN

- **NEVER** use `panic()` for error handling — only for truly unrecoverable init failures
- **NEVER** use package-level `db` variables — inject via constructor
- **NEVER** use `interface{}` as a shortcut — define real types
- **NEVER** ignore returned errors: `_, _ = someFunc()` is forbidden
- **NEVER** use `time.Sleep` inside request handlers — use context deadlines
- **NEVER** log secrets, tokens, or passwords even in debug logs
- **NEVER** use `http.DefaultClient` for external requests (no timeout) — configure a client
- **NEVER** store pointers to loop variables in goroutines — capture by value
- **NEVER** use `os.Exit` outside `main.go`
- **NEVER** skip `-race` flag in CI test runs
