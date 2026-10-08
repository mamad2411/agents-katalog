# CLAUDE.md

Lerian Fetcher is an enterprise data extraction platform that unifies access to PostgreSQL, MySQL, Oracle, SQL Server, and MongoDB. It ships in two forms: as standalone Manager + Worker services, and as an **embedded runtime engine** (`pkg/engine`) that other Lerian products (Matcher, Reporter) import in-process.

- **Module:** `github.com/LerianStudio/fetcher/v2`
- **Go version:** Source of truth is `go.mod`; do not rely on stale toolchain guidance elsewhere.
- **Architecture:** Embedded runtime engine (`pkg/engine`) + Hexagonal Architecture + CQRS. The Manager and Worker now run *over* the engine — the engine owns the extraction rules, the services own the operational shell.
- **Services:** Manager (HTTP API, Fiber, port 4006) and Worker (RabbitMQ consumer)

## Commands

### Setup

```bash
make set-env              # Copy .env.example to .env for all components
make generate-master-key  # Generate APP_ENC_KEY (REQUIRED before services start)
make dev-setup            # Install tools (golangci-lint, mockgen, gosec) + tidy
```

### Build & Run

```bash
make build       # Build all components
make up          # Start all services with Docker Compose
make down        # Stop all services
make rebuild-up  # Rebuild and restart all services
```

### Test

```bash
make test-unit   # Unit tests
make test-e2e    # E2E tests (requires Docker, uses -tags=e2e)
make test-fuzzy  # Fuzz tests
make test-chaos  # Chaos tests with Toxiproxy (uses -tags=chaos)
make test-bench  # Benchmarks (BENCH=pattern BENCH_PKG=./path)
make test-all    # All suites sequentially
```

### Code Quality

```bash
make lint           # golangci-lint with --fix (28 linters, max cyclomatic complexity 18)
make format         # go fmt
make tidy           # go mod tidy
make sec            # gosec security analysis
make generate-docs  # Regenerate the canonical Huma OpenAPI 3.1 specification
make check-openapi  # Fail when the committed OpenAPI specification is stale
```

## Architecture

The codebase is a three-layer model: the **engine core** owns the rules, **compatibility adapters** bridge the engine's ports to real infrastructure, and **host applications** (Manager, Worker, or external products) own the operational shell.

### Engine core (`pkg/engine/`)

The embedded runtime — an importable, **infrastructure-free** core that owns the canonical *rules* of extraction: connection lifecycle, schema discovery/validation, query planning, extraction execution, result/error contracts, limits, and tenant-safety. It depends only on host-provided port interfaces, never on concrete infrastructure.

- Facade: `engine.New(opts ...Option) (*Engine, error)` in `pkg/engine/engine.go`. Construction validates required ports and applies `DefaultLimits()`.
- Ports (`pkg/engine/ports.go`): **required** — `ConnectorRegistry`, plus `CredentialProtector` when encrypted persistence is enabled; **optional** (graceful degradation) — `ConnectionStore`, `ExecutionStore`, `ResultSink`, `SchemaCache`, `ActiveExecutionChecker`, `Observability`.
- Operations: connection CRUD (`CreateConnection`, `GetConnection`/`GetConnectionByID`, `ListConnections`/`ListConnectionsPaged`, `Update*`, `Delete*`, `CheckActiveExecutions`), `TestConnection`, `DiscoverSchema`/`DiscoverSchemaFresh`/`ValidateSchema`, `PlanExtraction`, `ExecuteExtraction`.
- Execution modes: **Direct** (inline bytes + SHA-256 integrity), **Store** (via `ResultSink`, returns a reference), **Auto** (store if a sink is wired, else direct). `TenantID` is the *sole* isolation dimension — there is no organization or product concept in engine core.
- `pkg/engine/memory/` holds in-memory port implementations for tests and embedded examples only — **not** production persistence.
- **Boundary is build-enforced.** `pkg/engine/dependency_test.go` runs `go list -deps` and fails the build if the engine transitively imports any forbidden infrastructure (see Code Conventions below).

### Compatibility adapters (`pkg/enginecompat/`)

Bridge the engine's ports to Fetcher's real infrastructure so the standalone services preserve their exact behavior:

- `connectioncompat/` — Mongo connection repo ↔ `ConnectionStore`; job repo ↔ `ActiveExecutionChecker`. Carries the rich Mongo record (ProductName, SSL, UUID, metadata, timestamps) as opaque host bytes so no field is dropped and ProductName never becomes an engine scope dimension.
- `schemacompat/` — datasource factory + crypto ↔ `ConnectorFactory`; Redis ↔ `SchemaCache`; request-scoped connections via `WithResolvedConnections`.
- `datasource/` — the Worker's extraction `ConnectorFactory` (wraps `pkg/datasource`).
- `plugincrm/` — CRM detection helpers for the legacy CRM extraction path.
- `tablenorm/` — table/field key normalization at the host seam (the engine stays literal; normalization is a host *mechanic*).

### Manager (`components/manager/`)

HTTP API server on Fiber framework, port 4006.

- Entry point: `components/manager/cmd/app/main.go`
- HTTP handlers: `internal/adapters/http/in/`
- CQRS commands: `internal/services/command/` (Create, Update, Delete)
- CQRS queries: `internal/services/query/` (Get, List, Test, Validate)
- Schema cache: `internal/adapters/cache/` (Redis)
- DI and config: `internal/bootstrap/`
- **Runs over the engine.** Bootstrap wires *two* engine instances: a connection engine (`internal/bootstrap/connection_engine.go`) and a schema engine (`internal/bootstrap/schema_engine.go`). Connection CRUD and schema discovery/validation are delegated to the engine. **Test-connection is the exception** — it still goes directly through the datasource factory, not the engine. The Manager owns auth, license enforcement, HTTP shape, rate limiting, idempotency, RabbitMQ dispatch, and the `/health` + `/readyz` endpoints.

### Worker (`components/worker/`)

Async RabbitMQ consumer. Does NOT follow CQRS - uses a single `UseCase` struct in `internal/services/`.

- Entry point: `components/worker/cmd/app/main.go`
- Consumer: `internal/adapters/rabbitmq/`
- Extraction logic: `internal/services/`
- **Runs over the engine; the legacy direct extraction path was removed.** `internal/bootstrap/extraction_engine.go` wires a mandatory `EngineRunner` — a nil runner is a startup-fatal wiring error (`service.Validate()`), not a runtime panic. Generic extraction flows `UseCase` → `extract_engine.go` (`extractViaEngine`) → `EngineRunner.RunExtraction` → `engine.PlanExtraction` + `engine.ExecuteExtraction` (Direct mode). The Worker owns encrypt/store/HMAC, job-status lifecycle, and lib-streaming events *outside* the engine. `plugin_crm` extraction is the documented exception — it bypasses the engine entirely (legacy `extract_crm_data.go`: collection-prefix fan-out, filter-field hashing, PII decryption).

### Shared Packages (`pkg/`)

- `pkg/engine/` - **embedded runtime core** (facade, ports, planner, runner, contracts). Boundary enforced by `dependency_test.go`. `pkg/engine/memory/` = in-memory test/embedded harness.
- `pkg/enginecompat/` - compatibility adapters bridging engine ports to infrastructure: `connectioncompat/`, `schemacompat/`, `datasource/`, `plugincrm/`, `tablenorm/`.
- `pkg/model/` - domain entities (Connection, Job, Schema)
- `pkg/ports/` - repository interfaces in subdirectories: `connection/`, `job/`, `cache/`, `publisher/`, `storage/`, `messaging/`, `datasource/`
- `pkg/datasource/datasource_factory.go` - factory for multi-DB support (switch on connection type)
- `pkg/datasource/hostsafety/` - SSRF guard (safe-host validation); `pkg/datasource/sslmode/` - per-driver SSL mode allowlists
- `pkg/crypto/` - AES-256-GCM encryption, HMAC-SHA256 signing
- `pkg/errors.go` - custom error types (ValidationError, UnauthorizedError, ForbiddenError, etc.)
- `pkg/context.go` - Logger/Tracer injection via context
- `pkg/bootstrap/readyz/` - canonical `/readyz` readiness contract + `ValidateSaaSTLS` enforcement
- `pkg/resolver/` - internal datasource env loading (`DATASOURCE_{N}_*`) + multi-tenant resolution
- DB adapters: `pkg/postgres/`, `pkg/mysql/`, `pkg/oracle/`, `pkg/sqlserver/`, `pkg/mongodb/`
- Infrastructure: `pkg/rabbitmq/` (incl. `security_envelope.go` — route/tenant-bound HMAC), `pkg/redis/`, `pkg/seaweedfs/`, `pkg/storage/`, `pkg/ratelimit/`

## Code Conventions

**Engine boundary (`pkg/engine`):** The engine is infrastructure-free and the rule is enforced by `pkg/engine/dependency_test.go`. It MUST NOT import (directly or transitively): Fiber/swag, RabbitMQ (`amqp091-go`)/lib-streaming, Mongo driver/go-redis/SQL drivers (`pgx`, `go-sql-driver/mysql`, `go-mssqldb`, `go-ora`, `lib/pq`)/`database/sql`, `os/exec`/`plugin`, `net/http`/`net/rpc`, AWS SDK/`pkg/seaweedfs`, the local infra packages (`pkg/rabbitmq`, `pkg/storage`, `pkg/mongodb`, `pkg/redis`, `pkg/net/http`, `pkg/datasource`, the DB adapters, `pkg/ratelimit`, `pkg/bootstrap/readyz`), tenant-runtime middleware (`dispatch-layer`, `tenant-manager` — only their `/core` subpackages are allowed), `lib-auth`/`lib-license-go`, or `components/*/internal`. When working in the engine, keep infrastructure behind a port; put the concrete adapter in `pkg/enginecompat/` or the host. **Ask "is this a rule or a mechanic?"** — rules (validation, planning, limits, tenant-safety) go in the engine; mechanics (normalization, presentation, persistence, transport) go in the host seam.

**CQRS services (Manager only):** Struct with `Execute()` method. Constructor `NewXxx(deps...)`. Dependencies are port interfaces, never concrete implementations.

**HTTP operations:** Typed Huma callbacks in `internal/adapters/http/in/huma_*.go`, registered through the single runtime/spec assembly. Preserve the request context installed by auth/tenant middleware and read the product name from the `X-Product-Name` header when required. Return errors through the lib-commons RFC 9457 problem model.

**Error handling:** Use `pkg.ValidateBusinessError(constant.ErrXxx, "entityType", args...)` for business errors. Custom types in `pkg/errors.go` map to HTTP status codes.

**Context propagation:** Use `commons.NewTrackingFromContext(ctx)` for logger, tracer, requestID. Start OTel spans: `ctx, span := tracer.Start(ctx, "service.op"); defer span.End()`.

**Mocking:** `go.uber.org/mock` with `mockgen`. Mock files are `*.mock.go` alongside interfaces. Interfaces have `//go:generate mockgen` directives.

**Unit tests:** File alongside source (`xxx_test.go`). Use `testutil.TestContext()` for context, `gomock.NewController(t)` for mocks, `testify/assert` or `testify/require` for assertions.

**E2E tests:** Build tag `//go:build e2e`, in `tests/e2e/`. Each test must generate a unique product name via `e2eshared.GenerateProductName()` for isolation. Use `e2eshared.CreateTestConnection()` and `e2eshared.AssertJobCompleted()`.

**Fuzz tests:** In `tests/fuzz/`. **Chaos tests:** Build tag `//go:build chaos`, in `tests/chaos/`.

## Git Conventions

- Conventional commits: `type(scope): description`
- Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`
- Emojis are added automatically by `.githooks/commit-msg` - do NOT add them manually
- Branches: `feature/`, `fix/`, `hotfix/`, `docs/`, `refactor/`, `build/`, `test/`
- Protected branches: `main`, `develop`, `release-candidate`

## Gotchas

1. **Master key required:** Services will NOT start without `APP_ENC_KEY` in both `components/manager/.env` and `components/worker/.env`. Run `make generate-master-key` first.
2. **Build tags for tests:** E2E requires `-tags=e2e`, Chaos requires `-tags=chaos`. Without the tag, zero tests are found.
3. **Product name isolation in E2E:** Each test must use `e2eshared.GenerateProductName()` and pass it as `X-Product-Name` header for connections and `metadata.source` for jobs.
4. **Worker is NOT CQRS:** Uses a single `UseCase` struct, unlike the Manager.
5. **Ports are subdirectories:** Interfaces live in `pkg/ports/connection/`, `pkg/ports/job/`, etc. - not in a single file.
6. **Strict linting:** Max cyclomatic complexity 18, `io/ioutil` banned, strict shadow detection.
7. **`.env` files are gitignored:** Only `.env.example` files are committed.
8. **Distributed Docker Compose:** Infrastructure in `components/infra/docker-compose.yml`, Manager and Worker have their own.
9. **E2E requires GITHUB_TOKEN** for building Docker images with private dependencies. Use `E2E_SKIP_BUILD=true` to skip build.
10. **Engine imports are gated:** Adding an import to `pkg/engine` that pulls in any infrastructure dependency breaks `pkg/engine/dependency_test.go` (the build fails). Put the concrete dependency behind a port + an adapter in `pkg/enginecompat/`.
11. **Worker engine runner is mandatory:** There is no legacy fallback. A nil `EngineRunner` is a startup-fatal wiring error, not a runtime panic.
12. **`plugin_crm` bypasses the engine:** CRM extraction runs the legacy path (`extract_crm_data.go`), not `pkg/engine`. Changes to extraction semantics may need to be made in *both* places.
13. **License is fail-closed off `local`:** Any `DEPLOYMENT_MODE` other than (case-insensitive) `local` constructs a license client that `os.Exit(1)`s on invalid/expired/unreachable license. A blank or misspelled mode enforces.
14. **SSRF guard is multi-tenant only:** `hostsafety` host validation activates only when `MULTI_TENANT_ENABLED=true`; internal datasources are exempt. Single-tenant operators are not guarded.
15. **Legacy RabbitMQ signature fallback:** `RABBITMQ_ALLOW_LEGACY_BODY_SIGNATURE_FALLBACK=true` accepts old body-only HMAC signatures during a rolling drain. It is replay-susceptible — keep it off except during migration.

## Documentation Index

| File | Content |
|------|---------|
| `docs/PROJECT_RULES.md` | Architecture rules, patterns, project structure (~1200 lines) |
| `docs/pre-dev/fetcher-embedded-runtime/` | Engine design docs (PRD, TRD, feature map, tasks, subtasks) |
| `README.md` | Project overview, quick start, API endpoints, security model |
| `components/manager/README.md` | Manager service (HTTP control plane, runs over the engine) |
| `components/worker/README.md` | Worker service (async data plane, runs over the engine) |
| `tests/e2e/README.md` | E2E test conventions, patterns, test catalog |
| `components/manager/api/openapi.yaml` | Canonical OpenAPI 3.1 specification |
| `components/manager/api/requests.http` | API request examples for manual testing |
| `.golangci.yml` | Full linter configuration (28 linters) |

## Common Workflows

### Adding a new API endpoint

1. Add the typed callback and operation metadata in the appropriate `components/manager/internal/adapters/http/in/huma_*.go` file
2. Register the operation through the shared Huma assembly in `huma_operations.go`
3. Create command or query service in `internal/services/command/` or `internal/services/query/`
4. Wire dependencies in `internal/bootstrap/`
5. Run `make generate-docs` and `make check-openapi`

### Adding a new database adapter

1. Create package in `pkg/<dbtype>/`
2. Create model in `pkg/model/datasource/<dbtype>/`
3. Add case to the switch in `pkg/datasource/datasource_factory.go`
4. Add type constant in `pkg/constant/`
5. No engine change is needed: extraction reaches the new adapter through the engine's `Connector` port, implemented by `pkg/enginecompat/datasource`, which wraps the `pkg/datasource` factory. Add an SSL-mode allowlist entry in `pkg/datasource/sslmode/` if the driver supports TLS, and cover the engine path in tests.

### Writing a unit test

1. Create `xxx_test.go` alongside the source file
2. Use `testutil.TestContext()` for context with logger/tracer
3. Use `gomock.NewController(t)` + mock constructors from `*.mock.go`
4. Assert with `testify/assert` or `testify/require`

### Writing an E2E test

1. Create file in `tests/e2e/` with `//go:build e2e` tag
2. Call `t.Parallel()` first
3. Generate product name: `productName := e2eshared.GenerateProductName()`
4. Use `e2eshared.CreateTestConnection(t, ...)` for auto-cleanup
5. Use `e2eshared.AssertJobCompleted(t, ...)` for job polling

### Embedding the engine in a host application

1. Import `github.com/LerianStudio/fetcher/pkg/engine` — a **distinct module** from the `/v2` services, with a **zero third-party** dependency footprint and its own `v1` tag line (`pkg/engine/vX.Y.Z`). No infrastructure comes with it.
2. Implement the required ports (`ConnectorRegistry`, and `CredentialProtector` if using encrypted persistence) and any optional ports your host needs (`ConnectionStore`, `ResultSink`, `SchemaCache`, etc.).
3. Construct with `engine.New(engine.WithConnectorRegistry(...), ...)`; check the returned error.
4. For a working reference, read how the Manager (`components/manager/internal/bootstrap/connection_engine.go`, `schema_engine.go`) and Worker (`components/worker/internal/bootstrap/extraction_engine.go`) wire it via `pkg/enginecompat/*`. For tests, the `pkg/engine/memory/` harness satisfies every port in-memory.
