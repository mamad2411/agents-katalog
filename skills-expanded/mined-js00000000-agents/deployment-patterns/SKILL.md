---
name: deployment-patterns
description: Deployment workflows, CI/CD pipeline patterns, Docker containerization, health checks, rollback strategies, and production readiness checklists.
---

# Deployment Patterns

Production deployment workflows and CI/CD best practices for Fusion Labs projects.

## When to Activate

- Setting up CI/CD pipelines
- Dockerizing an application
- Planning deployment strategy
- Implementing health checks
- Preparing for a production release
- Configuring environment-specific settings

## Deployment Strategies

### Rolling Deployment (Default)

Replace instances gradually — old and new versions run simultaneously.

```
Instance 1: v1 → v2  (update first)
Instance 2: v1        (still v1)
Instance 3: v1 → v2  (update last)
```

**Use when:** Standard deployments, backward-compatible changes

### Blue-Green Deployment

Run two identical environments. Switch traffic atomically.

```
Blue  (v1) ← traffic
Green (v2)   idle, running new version

# After verification:
Blue  (v1)   idle (standby)
Green (v2) ← traffic
```

**Use when:** Critical services, zero-tolerance for issues

### Canary Deployment

Route a small percentage of traffic to the new version first.

```
v1: 95% of traffic
v2:  5% of traffic (canary)
→ If healthy, gradually increase to 100%
```

**Use when:** High-traffic services, risky changes

## CI/CD Pipeline

### GitHub Actions

```yaml
name: CI/CD

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test-backend:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16-alpine
        env:
          POSTGRES_USER: testuser
          POSTGRES_PASSWORD: testpass
          POSTGRES_DB: testdb
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-go@v5
        with:
          go-version: '1.22'
      - run: go vet ./...
      - run: go test -race -cover ./...

  test-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: npm
      - run: npm ci
      - run: npm run lint
      - run: npx tsc --noEmit
      - run: npm test -- --coverage

  build:
    needs: [test-backend, test-frontend]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - uses: docker/build-push-action@v5
        with:
          push: true
          tags: ghcr.io/${{ github.repository }}:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    environment: production
    steps:
      - name: Deploy
        run: echo "Deploying ${{ github.sha }}"
```

### Pipeline Stages

```
PR opened:
  lint → typecheck → unit tests → integration tests → preview deploy

Merged to main:
  lint → typecheck → tests → build image → deploy staging → smoke tests → deploy production
```

## Health Checks

### Go Health Check Endpoint

```go
func (h *Handler) HealthCheck(c *gin.Context) {
    checks := map[string]interface{}{}

    // Database check
    sqlDB, _ := h.db.DB()
    if err := sqlDB.Ping(); err != nil {
        checks["database"] = map[string]string{"status": "error", "message": err.Error()}
    } else {
        checks["database"] = map[string]string{"status": "ok"}
    }

    // Redis check
    if _, err := h.redis.Ping(c).Result(); err != nil {
        checks["redis"] = map[string]string{"status": "error", "message": err.Error()}
    } else {
        checks["redis"] = map[string]string{"status": "ok"}
    }

    allOK := true
    for _, v := range checks {
        if m, ok := v.(map[string]string); ok && m["status"] != "ok" {
            allOK = false
            break
        }
    }

    status := http.StatusOK
    if !allOK {
        status = http.StatusServiceUnavailable
    }

    c.JSON(status, gin.H{
        "status":  map[bool]string{true: "ok", false: "degraded"}[allOK],
        "version": os.Getenv("APP_VERSION"),
        "checks":  checks,
    })
}
```

## Environment Configuration

### Twelve-Factor App Pattern

```bash
# All config via environment variables — never in code
DATABASE_URL=postgresql://devuser:devpassword@localhost:5432/devdb
REDIS_URL=redis://:devpassword@localhost:6379/0
JWT_SECRET=${JWT_SECRET}
GIN_MODE=release
PORT=8080
```

### Go Configuration Validation

```go
type Config struct {
    DatabaseURL string `envconfig:"DATABASE_URL" required:"true"`
    RedisURL    string `envconfig:"REDIS_URL" required:"true"`
    JWTSecret   string `envconfig:"JWT_SECRET" required:"true"`
    Port        int    `envconfig:"PORT" default:"8080"`
    GinMode     string `envconfig:"GIN_MODE" default:"release"`
}

func LoadConfig() (*Config, error) {
    var cfg Config
    if err := envconfig.Process("", &cfg); err != nil {
        return nil, fmt.Errorf("load config: %w", err)
    }

    if len(cfg.JWTSecret) < 32 {
        return nil, errors.New("JWT_SECRET must be at least 32 characters")
    }

    return &cfg, nil
}
```

## Rollback Strategy

```bash
# Docker/Kubernetes: rollback to previous image
kubectl rollout undo deployment/app

# Docker Compose: roll back to previous image tag
docker-compose pull && docker-compose up -d

# Database: rollback migration (if reversible)
migrate -path migrations -database "$DATABASE_URL" down 1
```

### Rollback Checklist

- [ ] Previous image/artifact is available and tagged
- [ ] Database migrations are backward-compatible
- [ ] Feature flags can disable new features without deploy
- [ ] Monitoring alerts configured for error rate spikes
- [ ] Rollback tested in staging

## Production Readiness Checklist

### Application
- [ ] All tests pass (unit, integration)
- [ ] No hardcoded secrets in code or config files
- [ ] Error handling covers all edge cases
- [ ] Logging is structured (JSON) and does not contain PII
- [ ] Health check endpoint returns meaningful status

### Infrastructure
- [ ] Docker image builds reproducibly (pinned versions)
- [ ] Environment variables documented and validated at startup
- [ ] Resource limits set (CPU, memory)
- [ ] SSL/TLS enabled on all endpoints

### Monitoring
- [ ] Application metrics exported (request rate, latency, errors)
- [ ] Alerts configured for error rate > threshold
- [ ] Log aggregation set up
- [ ] Uptime monitoring on health endpoint

### Security
- [ ] Dependencies scanned for CVEs (`npm audit`, `go list -m all | nancy`)
- [ ] CORS configured for allowed origins only
- [ ] Rate limiting enabled on public endpoints
- [ ] Authentication and authorization verified

### Operations
- [ ] Rollback plan documented and tested
- [ ] Database migration tested against production-sized data
- [ ] Runbook for common failure scenarios

---

**Remember**: Deployment should be boring — automated, repeatable, and reversible. If you're nervous about deploying, improve the process.
