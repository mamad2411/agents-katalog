---
name: go-testcontainers
description: Use when writing integration tests with testcontainers-go — Postgres/Redis/Kafka containers, lifecycle, reuse, CI cost, parallelism.
metadata:
  added: 2026-05-18
  last_reviewed: 2026-05-18
  type: language
  languages: [go]
  status: active
  invokes_shell: false
  shell_reviewed: "valksor 2026-05-18"
  related: [go-essentials, go-testing, go-pgx, ci-github-actions, ci-gitlab-ci]
---

# Go testcontainers

**Iron Law: one container per test package, started in `TestMain` or a `sync.Once`, torn down via `t.Cleanup`. Pin images by digest. Wait strategies are non-negotiable — never `time.Sleep` waiting for "ready".**

**Versions:** Current `v0.x` (latest minor) · No LTS series — _Pre-1.0 but production-stable; many users on `v0.30+`. Pin a minor version in `go.mod` and read the changelog before bumping — module APIs (e.g., `postgres`, `redis`) sometimes change shape._

## When to use vs sqlmock / redismock / fakes

| Tool                                | Use when                                                                                                                                |
| ----------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| **testcontainers-go**               | integration tests that exercise real query plans, real migrations, real Redis eviction — anything that mocks would lie about            |
| **pgxmock / sqlmock**               | unit tests for repository logic where you assert "this exact SQL was sent with these params"; fast (no Docker), no real query semantics |
| **redismock**                       | same trade-off as pgxmock for Redis                                                                                                     |
| **in-memory fakes** (your own)      | service-layer unit tests where the storage is an interface; the fake captures the behavior contract                                     |
| **modernc.org/sqlite (in-process)** | for SQLite-backed code, no container needed; runs in the test process                                                                   |

Mocks are fast (~µs). Containers are slow (1-5s startup) but real. Use mocks for hot-path unit tests; reserve containers for repository + integration suites.

## Postgres example (with wait.ForSQL)

```go
import (
    "github.com/testcontainers/testcontainers-go"
    "github.com/testcontainers/testcontainers-go/modules/postgres"
    "github.com/testcontainers/testcontainers-go/wait"
)

func setupPostgres(t *testing.T) string {
    ctx := context.Background()
    container, err := postgres.Run(ctx,
        "postgres:17.2-bookworm@sha256:<digest>",          // pin by digest
        postgres.WithDatabase("app_test"),
        postgres.WithUsername("test"),
        postgres.WithPassword("test"),
        testcontainers.WithWaitStrategy(
            wait.ForSQL("5432/tcp", "pgx", func(host string, port nat.Port) string {
                return fmt.Sprintf("postgres://test:test@%s:%s/app_test?sslmode=disable", host, port.Port())
            }).WithStartupTimeout(60*time.Second),
        ),
    )
    if err != nil { t.Fatalf("start postgres: %v", err) }
    t.Cleanup(func() {
        if err := container.Terminate(context.Background()); err != nil {
            t.Logf("terminate: %v", err)                    // log, don't fail — test already passed/failed
        }
    })
    dsn, err := container.ConnectionString(ctx, "sslmode=disable")
    if err != nil { t.Fatalf("dsn: %v", err) }
    return dsn
}
```

`wait.ForSQL` actually opens a connection — `wait.ForListeningPort` returns too early (Postgres listens before it accepts queries during init). Use `ForSQL` or `ForLog("database system is ready to accept connections").WithOccurrence(2)`.

## Redis example (with wait.ForLog)

```go
import "github.com/testcontainers/testcontainers-go/modules/redis"

container, err := redis.Run(ctx,
    "redis:7.4-bookworm@sha256:<digest>",
    redis.WithLogLevel(redis.LogLevelVerbose),
    testcontainers.WithWaitStrategy(
        wait.ForLog("Ready to accept connections").WithStartupTimeout(30*time.Second),
    ),
)
```

For Kafka, MinIO, Vault, generic services: `testcontainers.GenericContainer` with `ContainerRequest{Image, ExposedPorts, WaitingFor, Env, ...}`. Module packages (`modules/postgres`, `modules/redis`, `modules/kafka`) wrap the common boilerplate.

## Lifecycle: TestMain vs per-test vs sync.Once

```go
// Recommended: one container per package, shared across all tests in that package
var pgDSN string

func TestMain(m *testing.M) {
    ctx := context.Background()
    container, dsn := mustStartPostgres(ctx)
    pgDSN = dsn
    code := m.Run()
    _ = container.Terminate(ctx)                          // best-effort
    os.Exit(code)
}

func TestUserRepo_Create(t *testing.T) {
    db := mustConnect(t, pgDSN)
    truncateTables(t, db)                                  // per-test reset, NOT per-test container
    // ... test body
}
```

| Strategy                               | Startup cost                        | Isolation                                            |
| -------------------------------------- | ----------------------------------- | ---------------------------------------------------- |
| Container per test                     | ~1-5s × N tests                     | perfect — slow                                       |
| Container per package (`TestMain`)     | once per package                    | shared — truncate/reset between tests                |
| Container per process (`sync.Once`)    | once total across packages          | requires global state plumbing; usually not worth it |
| Container per subtest with `WithReuse` | first start full, rest milliseconds | dev-time iteration only — NOT for CI                 |

Default to "one per package, truncate between". The truncate-and-seed pattern keeps tests deterministic without paying the container-startup tax repeatedly.

## Reuse (dev only — never CI)

```go
container, _ := postgres.Run(ctx, image,
    postgres.WithDatabase("app_test"),
    testcontainers.WithReuse(true),                       // looks for an existing container with same hash
)
```

`WithReuse` keeps the container alive between `go test` runs locally — speeds the inner loop. **Never enable in CI**: parallel CI jobs would share + corrupt the same container. Gate it behind an env var: `if os.Getenv("TC_REUSE") == "1" { ... }`.

## Parallelism

```go
func TestRepoA(t *testing.T) {
    t.Parallel()
    db := mustConnect(t, pgDSN)
    // Each parallel test gets its own schema or DB so they don't stomp each other.
    schema := uniqueSchema(t)
    _, _ = db.Exec(`CREATE SCHEMA ` + schema)
    t.Cleanup(func() { _, _ = db.Exec(`DROP SCHEMA ` + schema + ` CASCADE`) })
    // ... use schema as the SET search_path target
}
```

One container, many isolated schemas. For Redis, use per-test key prefixes (`t.Name() + ":"`) or `SELECT n` to pick a different logical DB (0-15 by default).

For full per-package parallelism, set `go test -p N` where N is the CPU count — testcontainers handles concurrent container creation if Docker daemon can keep up.

## CI cost: GitHub Actions vs GitLab CI

| CI                                   | Docker availability                                                                              | Cost notes                                                                        |
| ------------------------------------ | ------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------- |
| **GitHub Actions** (`ubuntu-latest`) | Docker pre-installed, runs natively — no DinD                                                    | Container pulls add 10-30s; cache via `setup-buildx-action` if reusing images     |
| **GitLab CI** (shared runners)       | Docker-in-Docker service required: `services: [docker:dind]` and `DOCKER_HOST=tcp://docker:2375` | DinD overhead is real (~5-15s per job); use `docker:dind-rootless` where possible |
| **Self-hosted runner**               | mount the host `docker.sock` (`-v /var/run/docker.sock:/var/run/docker.sock`)                    | Fast, no DinD tax. Security trade-off — containers can break out to host docker   |
| **Earthly / dagger**                 | their own container runtime; testcontainers works but you pay per nested container               | Mostly worth it for monorepo-wide caching                                         |

Pin images by digest (`postgres:17.2-bookworm@sha256:...`) so CI doesn't re-download on every tag bump and the test surface is reproducible.

## Image pinning

```go
const pgImage = "postgres:17.2-bookworm@sha256:abc123...def"     // digest, not tag
```

`postgres:17` floats — a minor upstream change can break a test on a Tuesday. Digest pins are reproducible; bump intentionally with `docker manifest inspect` to get the new digest. Same rule for Redis, Kafka, etc.

## Cleanup discipline

- `t.Cleanup(func() { container.Terminate(...) })` — runs even on `t.Fatal`
- Don't `defer container.Terminate(...)` in a helper — defer fires when the helper returns, not when the test does
- `Terminate` returns an error from Docker; log it, don't fail the test (the test result is what matters)
- The reaper (Ryuk) auto-kills orphaned containers ~10s after the test process exits — your safety net if cleanup is missed. Disable only with `TESTCONTAINERS_RYUK_DISABLED=true` (rarely correct)

## Anti-patterns

- `time.Sleep(5 * time.Second)` after start instead of `wait.ForSQL` / `wait.ForLog` — flaky
- Image tags without digest (`postgres:17`) — upstream tag rewrites silently change your test surface
- Container per test in CI — minutes of startup overhead per file; share at package level
- `WithReuse(true)` enabled in CI — parallel jobs share + corrupt the container
- Forgetting `t.Cleanup` — orphan containers pile up on dev machines (Ryuk catches most but not all)
- Bind-mounting host paths into the container (`testcontainers.WithMounts`) — non-reproducible, leaks state between runs; copy fixtures with `WithFiles` instead
- Asserting on Docker-internal hostnames (`postgres` instead of `container.Host(ctx)`) — works on Linux DinD, breaks on macOS Docker Desktop
- Running 50 containers in parallel on a 16GB laptop — Docker OOMs silently; cap parallelism in CI and dev

## Red flags

| Thought                                             | Reality                                                                                          |
| --------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| "Tests pass locally, flake on CI"                   | Wait strategy is `ForListeningPort`; switch to `ForSQL`/`ForLog`                                 |
| "Container startup is killing my feedback loop"     | One per package + truncate between tests; consider `WithReuse(true)` locally                     |
| "I'll just `docker-compose up` instead"             | Containers leak between `go test` invocations; testcontainers ties lifecycle to the test process |
| "Why does the same test fail differently each run?" | Image tag floated; pin by digest                                                                 |

## Hand-off

For pgx pool sizing, prepared statements, and TCP keepalives inside the test DSN connection: `Skill(go-pgx)`. For table-driven tests, `t.Parallel`, and helper patterns: `Skill(go-testing)`. For wiring testcontainers into GitHub Actions jobs (Docker availability, cache): `Skill(ci-github-actions)`. For GitLab CI DinD setup: `Skill(ci-gitlab-ci)`. For Go idioms, error wrapping, modules: `Skill(go-essentials)`.
