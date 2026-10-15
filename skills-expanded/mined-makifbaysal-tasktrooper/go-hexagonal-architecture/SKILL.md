---
name: go-hexagonal-architecture
category: architecture
description: Use when adding a use case, port, repository or adapter in a Go service — where each piece goes, how errors and transactions cross layers, and how to check the import direction
tech_stack: Go
source: uber-go/guide (Apache-2.0), adapted
---
# Hexagonal Architecture in Go

## Detect the repo's layout first

```
get_repo_tree   # look for domain/port/application/adapter-named folders
```

Follow the repository's own names for these folders (`internal/core`, `internal/service`, whatever it already uses) — don't rename them to match this skill. **Never restructure a repository that is not hexagonal in a feature task.** If the repo has no layering at all, follow its existing flat/package-by-feature style instead of introducing hexagonal boundaries unasked.

## Layers

- **Domain** (innermost): entities, value types, domain errors. Imports nothing from the outer layers — no Fiber, no pgx, no HTTP, no JSON tags driving behavior.
- **Ports**: interfaces (e.g. `internal/port`) describing what the application needs (repositories, clients) and offers (services).
- **Application**: use-case services orchestrating domain logic through ports. Depends on domain and ports only.
- **Adapters**: implementations at the edge — HTTP handlers, PostgreSQL repositories, external clients. Adapters import inward; nothing imports an adapter.

## Rules

- Dependency injection via constructors: `NewService(store port.Store, ...)`. No globals, no `init()`-time wiring (Uber: "Avoid `init()`", "Exit in Main").
- Cross-layer calls go through ports. A service never touches pgx directly; a handler never contains business logic.
- New behavior starts with the port interface and its domain types, then the service, then the adapter — the test for the service uses a fake or mock of the port (mockery-suite-tests).
- When adding a dependency, ask: does the domain need to know this exists? If yes, model it as a port; if no, keep it inside the adapter.
- **Verify interface compliance at compile time** (Uber): `var _ port.TaskStore = (*PGTaskStore)(nil)` next to the adapter's constructor — a missing method fails the build, not a runtime wiring panic.
- **Copy slices and maps at boundaries** (Uber) — a port implementation that hands back its internal slice lets the caller mutate state it doesn't own.

## Worked Example: "Archive a project"

1. **Domain errors:** `domain.ErrNotFound`, `domain.ErrConflict` (sentinel errors the adapters translate into and the handler's central mapper translates out of).
2. **Port:** `port.ProjectStore` with `Archive(ctx context.Context, id uuid.UUID) error`.
3. **Service + test:** the use case calls the port; the test uses the port's mock/fake — no database in this test.
4. **Postgres adapter:** translates driver errors into domain errors — `errors.Is(err, pgx.ErrNoRows)` → `domain.ErrNotFound`; `pgErr.Code == "23505"` → `domain.ErrConflict`. This translation happens in the adapter, never in the handler or service.
5. **Compile-time check:** `var _ port.ProjectStore = (*PGProjectStore)(nil)` beside the constructor.
6. **Handler:** maps through the one central error handler (fiber-rest-api) — no case-by-case mapping here.

## Transactions across ports

Model the transaction boundary as a port, not a leaked `*sql.Tx`/`pgx.Tx`: `port.TxRunner` with `WithinTx(ctx context.Context, fn func(ctx context.Context) error) error`. The Postgres adapter puts the `pgx.Tx` into the returned `ctx`; repository adapters use the tx-in-context when present, falling back to the pool otherwise. The transaction boundary belongs to the use case (application layer), which decides what must commit together — never to a repository method.

## Wiring

Constructors are called from `main`/a wiring package only — no package-level mutable globals holding dependencies (Uber "Avoid Global State").

## Verify the import direction

```
go list -deps ./internal/domain/... ./internal/application/... | grep -E '/internal/adapter|gofiber|jackc/pgx|database/sql'
```
Adjust the paths to the repo's actual package names. Must print nothing — any hit is a boundary violation.

## Smell Checklist

- A framework/driver import (`gofiber/fiber`, `jackc/pgx`, `database/sql`) anywhere under domain or application → boundary violation.
- A struct with both business rules and SQL strings → split into service + repository adapter.
- A handler longer than ~30 lines → logic belongs in the application service.
- A port method returning a framework type (`*fiber.Ctx`, `*sql.Rows`) instead of domain types.
- A repository adapter test that mocks the SQL driver instead of running against real Postgres.
