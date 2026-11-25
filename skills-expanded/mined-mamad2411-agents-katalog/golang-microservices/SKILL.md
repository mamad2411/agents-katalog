---
name: golang-microservices
description: "When to activate: Go microservices, service discovery, health checks, graceful shutdown, config, Docker, service-to-service calls"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: engineering
  language: go
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# Go Microservices Patterns

## Service Structure

```
svc-user/
├── cmd/server/main.go      # entry point
├── internal/
│   ├── config/config.go    # env-based config
│   ├── handler/            # HTTP/gRPC handlers
│   ├── service/            # business logic
│   ├── repository/         # data access
│   └── domain/             # models, errors
├── proto/                  # protobuf definitions
├── Dockerfile
└── go.mod
```

## Config from Environment

```go
type Config struct {
    Port        int           `env:"PORT"         envDefault:"8080"`
    DatabaseURL string        `env:"DATABASE_URL,required"`
    JWTSecret   string        `env:"JWT_SECRET,required"`
    LogLevel    string        `env:"LOG_LEVEL"    envDefault:"info"`
    ShutdownTO  time.Duration `env:"SHUTDOWN_TIMEOUT" envDefault:"10s"`
    UserSvcURL  string        `env:"USER_SVC_URL,required"`
}

func LoadConfig() (Config, error) {
    var cfg Config
    return cfg, env.Parse(&cfg)
}
```

## Server with Graceful Shutdown

```go
func main() {
    cfg, err := config.Load()
    if err != nil { log.Fatalf("config: %v", err) }

    logger := slog.New(slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{
        Level: parseLogLevel(cfg.LogLevel),
    }))

    db, err := database.Connect(cfg.DatabaseURL)
    if err != nil { logger.Error("db connect", "err", err); os.Exit(1) }

    repo := repository.NewPostgres(db)
    svc := service.New(repo, logger)
    h := handler.New(svc, logger)

    mux := http.NewServeMux()
    h.RegisterRoutes(mux)
    mux.HandleFunc("/health", healthHandler(db))
    mux.HandleFunc("/ready",  readyHandler(db))

    srv := &http.Server{
        Addr:         fmt.Sprintf(":%d", cfg.Port),
        Handler:      mux,
        ReadTimeout:  5 * time.Second,
        WriteTimeout: 10 * time.Second,
        IdleTimeout:  120 * time.Second,
    }

    go func() {
        logger.Info("server starting", "port", cfg.Port)
        if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
            logger.Error("server error", "err", err)
            os.Exit(1)
        }
    }()

    quit := make(chan os.Signal, 1)
    signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
    <-quit

    logger.Info("shutting down...")
    ctx, cancel := context.WithTimeout(context.Background(), cfg.ShutdownTO)
    defer cancel()
    srv.Shutdown(ctx)
    db.Close()
}
```

## Health and Readiness Endpoints

```go
func healthHandler(db *sql.DB) http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
        // /health — is the process alive?
        w.Header().Set("Content-Type", "application/json")
        json.NewEncoder(w).Encode(map[string]string{"status": "ok"})
    }
}

func readyHandler(db *sql.DB) http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
        // /ready — can the service serve traffic?
        ctx, cancel := context.WithTimeout(r.Context(), 2*time.Second)
        defer cancel()
        if err := db.PingContext(ctx); err != nil {
            w.WriteHeader(http.StatusServiceUnavailable)
            json.NewEncoder(w).Encode(map[string]string{"status": "not ready", "error": err.Error()})
            return
        }
        json.NewEncoder(w).Encode(map[string]string{"status": "ready"})
    }
}
```

## Service-to-Service Client

```go
type UserClient struct {
    base   string
    client *http.Client
}

func NewUserClient(baseURL string) *UserClient {
    return &UserClient{
        base: baseURL,
        client: &http.Client{
            Timeout: 5 * time.Second,
            Transport: &http.Transport{
                MaxIdleConns:        100,
                MaxIdleConnsPerHost: 20,
                IdleConnTimeout:     90 * time.Second,
            },
        },
    }
}

func (c *UserClient) GetUser(ctx context.Context, id string) (User, error) {
    req, _ := http.NewRequestWithContext(ctx, http.MethodGet, c.base+"/users/"+id, nil)
    resp, err := c.client.Do(req)
    if err != nil { return User{}, fmt.Errorf("get user: %w", err) }
    defer resp.Body.Close()

    if resp.StatusCode == http.StatusNotFound { return User{}, ErrUserNotFound }
    if resp.StatusCode != http.StatusOK {
        return User{}, fmt.Errorf("unexpected status: %d", resp.StatusCode)
    }

    var user User
    return user, json.NewDecoder(resp.Body).Decode(&user)
}
```

## Dockerfile

```dockerfile
FROM golang:1.23-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-s -w" -o server ./cmd/server

FROM gcr.io/distroless/static-debian12
COPY --from=builder /app/server /server
EXPOSE 8080
ENTRYPOINT ["/server"]
```

## Common Anti-Patterns

- **No readiness vs liveness distinction** — Kubernetes needs both; failing readiness removes from LB, failing liveness restarts
- **Global `http.DefaultClient`** — it has no timeout; always create a custom client with `Timeout`
- **Not draining connections on shutdown** — `srv.Shutdown(ctx)` waits for active connections; don't skip it
- **Hardcoded service URLs** — inject via environment; support service discovery (Consul, K8s DNS)
- **Synchronous service calls without circuit breaker** — add `github.com/sony/gobreaker` for resilience
