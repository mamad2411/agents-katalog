# AGENTS.md — services/core

> **AI Primer:** Read this file completely before writing, editing, or scaffolding any code in this service.
> Check `../../docs/TASKS/02_Task_List` for tasks.
> This file is your complete context for the Go backend service.

---

## Service Overview

| Concern        | Technology                          |
| -------------- | ----------------------------------- |
| Language       | Go 1.26.1                           |
| HTTP Framework | stdlib `net/http` (`http.ServeMux`) |
| Database       | PostgreSQL 18 via `pgx/v5`          |
| Query Layer    | sqlc (code-generated — `sql/sqlc/`) |
| Migrations     | golang-migrate (`sql/migrations/`)  |
| WebSocket      | `gorilla/websocket`                 |
| Scheduler      | `gocron/v2`                         |
| API Docs       | Swagger via `swaggo/http-swagger`   |
| Auth           | middleware, not implemented yet     |

---

## Package Structure

```
services/core/
├── cmd/
│   ├── core/
│   │   └── main.go          ← entrypoint: loads env, starts App
│   └── db_tool/
│       └── main.go          ← standalone DB utility tool
├── pkg/
│   ├── app/                 ← wires all handlers, hub, scheduler; mounts routes
│   │   ├── app.go           ← App struct, Start(), dependency injection
│   │   ├── config.go        ← Config struct (Env, Port, Host, AllowedOrigin)
│   │   ├── routes.go        ← all HTTP route registrations
│   │   └── healthcheck.go   ← GET /healthcheck handler
│   ├── docs/
│   │   ├── docs.go          ← Swagger docs generation
│   │   ├── swagger.json     ← generated Swagger spec (DO NOT edit manually)
│   │   └── swagger.yaml     ← generated Swagger spec in YAML (DO NOT edit manually)
│   ├── {feature}/           ← one folder per domain (agents, execution, file_system, etc.)
│   │   ├── domain.go        ← pure Go structs (no db tags)
│   │   ├── dto.go           ← request/response structs with swaggo annotations
│   │   ├── interface.go     ← IService and IRepository interfaces
│   │   ├── repository.go    ← sqlc-backed data access
│   │   ├── service.go       ← business logic, calls repository
│   │   ├── handler.go       ← HTTP handlers, calls service
│   │   └── mappers.go       ← domain ↔ sqlc conversions
│   ├── cli_runner/          ← process execution without sh -c
│   │   ├── runner.go        ← tokenizes command string, builds exec.Cmd
│   │   └── stream.go        ← merges stdout/stderr, emits lines to a channel
│   ├── config/
│   │   └── database.go      ← DATABASE_URL env loading
│   ├── database/
│   │   ├── database.go      ← pgxpool.Connect wrapper
│   │   └── manager.go       ← transaction manager
│   ├── middleware/
│   │   ├── auth.go          ← auth middleware (currently commented out in routes.go)
│   │   ├── logging.go       ← request logging
│   │   └── middleware.go    ← Chain() helper
│   ├── scheduler/
│   │   └── scheduler.go     ← gocron-based job scheduler
│   ├── shared/
│   │   ├── os.go            ← WSL ↔ Windows path normalization, WORKSPACE_ROOT
│   │   ├── api_errors.go    ← shared HTTP error helpers
│   │   ├── dto.go           ← shared request/response types
│   │   └── utils.go         ← misc utilities
│   ├── websocket/
│   │   ├── hub.go           ← broadcast hub, topic subscriptions
│   │   ├── client.go        ← per-connection WebSocket client
│   │   └── handler.go       ← GET /ws upgrade handler
├── sql/
│   ├── migrations.go        ← embeds migration files for golang-migrate
│   ├── migrations/          ← Goose-style *.up.sql / *.down.sql files
│   ├── queries/             ← sqlc source .sql query files
│   └── sqlc/                ← generated Go code (DO NOT edit manually)
├── Makefile
├── sqlc.yaml
└── go.mod
```

---

## Commands

```bash
cd services/core

make run            # run API locally (go run ./cmd/core)
make build          # build binary → bin/core
make tidy           # go fmt + go mod tidy
make migrate/up     # apply pending migrations
make migrate/down   # rollback one migration
make reset          # drop + recreate + migrate + seed
make generate       # regenerate sqlc after SQL changes
make docs           # generate Swagger docs from code annotations
make db/sync        # migrate/up + generate
```

---

## Domain Package Layout

Every package under `pkg/` follows this exact shape. New features **must** match:

```
domain.go      ← structs (pure Go — no db tags)
dto.go         ← request/response JSON types with swaggo annotations
interface.go   ← IService and IRepository interfaces
repository.go  ← sqlc-backed data access
service.go     ← business logic, calls repository
handler.go     ← HTTP handlers, calls service
mappers.go     ← domain ↔ sqlc conversions
```

Handler calls Service. Service calls Repository. Handlers **never** call repositories directly.

## Environment Variables

| Variable         | Description                          | Default / Example                                                        |
| ---------------- | ------------------------------------ | ------------------------------------------------------------------------ |
| `DATABASE_URL`   | PostgreSQL connection string         | `postgres://postgres:postgres@localhost:5432/automation?sslmode=disable` |
| `PORT`           | HTTP listen port                     | `8080`                                                                   |
| `HOST`           | HTTP listen host                     | `localhost`                                                              |
| `WORKSPACE_ROOT` | Root path for file-system operations | `/mnt/d`                                                                 |
| `ALLOWED_ORIGIN` | WebSocket CORS allowed origin        | `http://localhost:3000` (use `*` for dev)                                |

---

## Key Conventions

- **No `sh -c`.** `cli_runner/runner.go` tokenizes command strings directly. Agent `cli_command_template` must be a plain command — no shell syntax.
- **stdlib router only.** Routes use `http.ServeMux` method-pattern syntax: `"POST /pipeline/{id}/trigger"`. Never add Chi, Gin, or Fiber.
- **sqlc is source of truth.** After editing `sql/queries/*.sql` or `sql/migrations/*.sql`, run `make generate`. Never hand-edit `sql/sqlc/`.
- **Path normalization.** `pkg/shared/os.go` handles WSL ↔ Windows paths. `WORKSPACE_ROOT` defaults to `/mnt/d`.
- **Auth middleware is commented out.** The `middleware.Auth` line in `routes.go` is intentionally disabled. Some project queries use a hardcoded owner ID. Treat as current behavior.
- **WebSocket topic format:** `execution:{id}` — keep this consistent when adding new broadcast events.
- **Transaction manager:** Use `database.Manager` for any multi-step writes that must be atomic.

---

## What NOT to Do

- Do NOT edit files in `sql/sqlc/` — generated by sqlc via `make generate`.
- Do NOT use `sh -c` or shell operators in agent command templates — the runner rejects them.
- Do NOT call a repository from a handler directly — route through the service layer.
- Do NOT use third-party HTTP routers (Chi, Gin, Fiber) — stdlib `ServeMux` only.
- Do NOT enable or modify `middleware.Auth` without a full auth implementation plan.
- Do NOT add new migrations without a matching `.down.sql` file.
