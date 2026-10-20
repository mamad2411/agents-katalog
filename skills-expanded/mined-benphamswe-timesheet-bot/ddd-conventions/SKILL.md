---
name: ddd-conventions
description: timesheet-bot DDD and Clean Architecture coding conventions - where types, ports and adapters go, how the domain is validated, and how external writes stay idempotent. Preloaded into go-coder.
user-invocable: false
---

# timesheet-bot coding conventions

Go paths (`internal/`, `cmd/`, `migrations/`) are relative to `services/timesheet-core/`. Go tools run there, or from the repo root with `go -C services/timesheet-core`.

## Where code goes

| You are adding | Put it in | Imports allowed |
|---|---|---|
| A value object shared by contexts | `internal/shared/kernel` | stdlib only |
| An entity, aggregate, domain event or repository interface | `internal/<ctx>/domain` | stdlib, kernel |
| A command handler or port interface | `internal/<ctx>/application` (ports in `ports.go`) | kernel, own domain, other contexts' **domain** types |
| An adapter (HTTP, DB, SDK) | `internal/<ctx>/infrastructure/<tech>` | anything except `interfaces/` |
| Entry points (CLI, Slack bot, scheduler, outbox relay) | `internal/interfaces/<kind>` | application packages |
| Concrete wiring | `cmd/timesheet/wire.go` only | everything |

A domain package must never import another context's domain. If two contexts need the same type, it goes in the kernel.

## Domain rules

- Value objects have unexported fields and a `NewX(...) (X, error)` constructor. `MustX` exists for tests and constants only.
- Aggregates expose behaviour methods, not setters. Every state change checks the status first and returns a wrapped sentinel error: `fmt.Errorf("%w: detail", ErrX)`.
- Transitions record a `domain.Event`. Repositories drain events with `PullEvents()` inside the save transaction (the outbox).
- Persisted state goes through `Snapshot()` and `Rehydrate()`. Only repositories call them.
- Time comes from `kernel.Clock` or a `now time.Time` parameter. Never call `time.Now()` in domain or application code.

## External input (Slack, Jira, Tempo, Claude)

- Convert at the adapter edge into kernel types. Invalid data is either dropped with a reason or returned as an error. It never reaches the aggregate unchecked.
- AI output is untrusted. It is translated into `Proposal` values and replayed through `Timesheet.AddEntry`. Validation errors are returned as `Input.Feedback`.
- Calendar days are computed once in the collector, using the configured timezone.

## External writes

- Every write to an external system is idempotent per unit of work. Persist the external id right after each successful call (see `SubmitHandler`) before calling again.
- HTTP clients come from `httpx.NewClient` (retries 429/5xx, honors Retry-After). Do not build a bare `http.Client` in adapters.

## Errors and secrets

- Wrap with context: `fmt.Errorf("resolve %s: %w", key, err)`. Compare with `errors.Is`.
- Secrets are read only via `config.Env(names...)`. Error messages name variables, never values. No secret in logs, fixtures or test names.

## Style

- Match the surrounding code: comment density, naming, table-driven tests.
- Declare interface compliance at compile time: `var _ application.WorklogGateway = (*Client)(nil)`.
