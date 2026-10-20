---
description: Cold path flat handlers, outbox, pkg/coldpath, no Provider layers, idempotency
globs:
  - internal/notify/**
  - internal/payment/**
  - internal/ledger/**
  - internal/costsync/**
  - internal/controlplane/**
  - internal/identity/**
  - internal/fraud/**
  - pkg/coldpath/**
  - cmd/control/**
  - cmd/ivt-detector/**
  - cmd/fraud-scorer/**
alwaysApply: false
---

# Cold Path - Admin, Payment, Ledger

## Purpose

Cold path = stdlib HTTP, Postgres transactions, outbox, webhooks, background pollers, admin API, ML training/inference sidecars. Not `/track`, gnet, or filter `Check` (see `hot-path.mdc`). Overrides generic abstraction defaults in `code-style.mdc`. Anti-slop: `anti-slop.mdc`.

Reference: `architecture.mdc`, `control-plane.mdc`, `data-layer.mdc`, `licensing.mdc`.

## Philosophy

Minimum LoC with correct idempotency, audit trail, and operator honesty. Flat control flow beats layered enterprise patterns. ~30 lines of sequential Go beats 3 files + 2 interfaces.

**Density target:** one `Service` struct, sqlc `db.Queries` called directly, workers in `*_worker.go` started from `main` or `OpenModule.StartWorkers`.

## Forbidden (grep before submit)

| Category | Forbidden |
| :--- | :--- |
| Admin handler without RBAC | New `/api/v1` route without `RequirePermission` / `RequireAnyPermission` matching OpenAPI `x-permissions` (`control-plane.mdc` **RBAC**, **RB-S1**) |
| Client-only authorization | Citing nav filter or `user.role` as access control without server `403` test (`frontend-slop.mdc` **RB-L***) |
| Architecture ceremony | Clean/hexagonal layers, GoF Provider/Factory/Strategy registries |
| Single-impl interfaces | `type NotifierProvider interface` with one Slack sender |
| Bundles | `ProviderBundle`, `NewProvidersFromConfig`, `map[string]any` JSON builders |
| Subtrees | `dto/`, `mappers/`, `usecase/`, `repositories/` |
| sqlc wrappers | Repository interface wrapping sqlc when `db.Queries` suffices |
| Parallel types | Entity + Model + View + DTO for same table |
| Mocks | Mock scaffolding unless user explicitly asks |
| Goroutine spawn | `go` spawn inside send/checkout/fetch - async only via outbox/worker tickers at module bootstrap |
| HTMX | Admin fragments - JSON `/api/v1` only (`control-plane.mdc`) |
| Redis admin | `KEYS`, `FLUSHALL`, `FLUSHDB` (`cold_path_static_gate.sh`) |
| N+1 | O(N) DB round-trips in loops on changed files (`cold_path_static_gate.sh`) |
| Silent handlers | `_ = json.Unmarshal` / `_ = w.Write` in handlers (`anti_slop_gate.sh`) |
| Test hooks | `testing.Testing()` or `os.Getenv("CI")` in production code |

Grep touched package: `interface {`, `Mock`, `Factory`, `map[string]any`.

## Allowed provider style (functions, not interfaces)

```go
SendSlack(ctx, cfg, breaker, recipient, title, body string) error
CreateCheckout(ctx, cfg, provider, amountMicro, ...) (ref, url string, err error)
```

Not: `type NotifierProvider interface`, indirection maps, adapter trees.

## Types and I/O boundaries

| Rule | Detail |
| :--- | :--- |
| Source of truth | HTTP body struct or **sqlc row** - no parallel API DTO + service DTO + mapper file |
| Admin JSON | `FooDTO` with `json:"snake_case"` in handler/service file beside route |
| Replica/pubsub | `fooReplicaDTO` with json tags near serialization only |
| Mapping | One step at boundary: `db.Row -> toFooDTO()` or `db.Row -> campaignmodel.Campaign` |
| Errors | Sentinels in `errors.go`; `fmt.Errorf("...: %w", err)`; `errors.Is` at HTTP boundary via `mapServiceError` / `writeServiceError` |
| Context | `context.Context` on every I/O boundary (DB, Redis, HTTP client) |

## pkg/coldpath helpers

Shared cold HTTP/JSON/UUID utilities - use instead of ad-hoc copies:

| Helper | Use |
| :--- | :--- |
| `ReadLimitedBody(w, r, maxBytes)` | All admin/payment/webhook bodies |
| `DecodeRequestOrBadRequest[T]` | Typed handler decode + 400 |
| `DecodeBody[T]` | After size-limited read |
| `DefaultMaxBody` | 65536 (64 KiB) default |
| `SelfServePaymentIntentMaxBody` | 16 KiB |
| `PaymentWebhookMaxBody` | 64 KiB |
| `AlertmanagerWebhookMaxBody` | 1 MiB |
| `ParsePathUUID` / `ParseUUID` | Path params |

Gate: `bash scripts/ci/static/cold_path_json.sh` - `TestReadLimitedBody`, `TestColdPathJSON`, `TestLoginBodySizeLimit`.

Cold path uses `encoding/json` - never the hot-path DFA/jsonScanBudget stack.

## Mutation validation (fail-closed)

Admin and payment mutations must **not** reach Postgres, Redis, or outbox until validation passes. Client-side checks are UX only; **server pipeline is authoritative** (`frontend-slop.mdc` **Mutation validation and error contract**).

| Stage | Rule |
| :--- | :--- |
| Decode | `DecodeRequestOrBadRequest` / `ReadLimitedBody` -- reject oversize and malformed JSON with `400` |
| Domain | Call package `Validate*` / sentinels **before** sqlc write in the same handler or service |
| Business | License limits, budget/revision conflicts, FK existence -- map to `mapServiceError` codes |
| Persist | TX rollback on failure; outbox in same TX only after domain success |
| Respond | `writeServiceError(w, err)` -- never `200` on error; no `_ =` on decode (`anti_slop_gate.sh`) |

**Banned:** blind `INSERT` from request struct; validation only in `web/`; leaking SQL/stack in `error.message`.

**Tests:** `mapServiceError` / validation `*_holdout*` beside changed logic; OpenAPI key parity tests when DTO changes.

**Error responses:** every failure path uses `writeServiceError` or `httpresponse.Error` with truthful status -- never `200` on error (`frontend-slop.mdc` **Explicit error handling vs error slop** ES1-ES7, EH-F*).

## Control plane topology

```
Clients -> cmd/control -> controlplane / adminapi / workers -> Postgres
Config mutations -> outbox_events in same PG transaction -> OutboxWorker applies Redis side effects
Tracker never receives direct Redis writes from admin handlers
```

Routes:

- `/api/v1/*` - operators and automation.
- `/api/v1/selfserve/*` - advertiser API keys.
- `/admin/*` - deprecated; do not extend.

Workers (control only): outbox, volume meter, recon, ledger invariant, slot migration, brand MAB, bid-floor optimizer, ops scraper, shard-0 catchup. Never run in tracker.

## Outbox patterns

Polling over `LISTEN/NOTIFY` (`tradeoffs.mdc`):

| Rule | Detail |
| :--- | :--- |
| Claim | `SELECT ... FOR UPDATE SKIP LOCKED` |
| Poll interval | Active 20 ms; idle backoff 250 ms |
| Stuck reclaim | `PROCESSING` reclaim after 1 min |
| Handler error | Row stays pending, retries |
| Permanent failure | Mark failed + ops alert |
| Idempotency | Duplicate event IDs must not double-apply (`ON CONFLICT`, idempotency keys) |

Alert: `ad_management_outbox_oldest_pending_seconds` > 30 s.

## Payment and settlement

- Stripe webhooks -> `payment.payment_outbox` -> in-process `SettlementHandler` -> `balance_ledger`.
- No settlement RPC; no synchronous balance update in webhook handler beyond outbox insert.
- Budget authority: Postgres `current_spend` + `balance_ledger`; Redis budgets are operational limits reconciled async.

## Postgres access

- sqlc per service: `internal/<svc>/db/`, queries in `queries/*.sql`.
- No raw `fmt.Sprintf` SQL (`sql_safety_gate.sh`).
- Batch queries over N+1: preload IDs, `WHERE id = ANY($1::uuid[])`, join in one round-trip.
- Transactions: scope minimal rows; `FOR UPDATE` only when ordering requires.

## ML / fraud (cold only)

- Train: `model/`; infer: `cmd/fraud-scorer`, `cmd/ivt-detector`.
- Scores -> control ops HTTP -> outbox -> Redis `ml:score:boost:*`.
- Hot path reads snapshot only - never import `internal/fraud` scoring into tracker.
- `ivt-detector` pauses when outbox `PENDING` > 500.

## Concurrency rules

- Synchronous under `ctx` inside handler/service methods.
- Async via existing worker tickers: outbox poll, payment outbox, notifier dispatch.
- No unbounded goroutine per webhook/request.
- Graceful shutdown: drain workers, respect `context` cancel on in-flight HTTP.

## Package layout

Flat under `internal/<name>/`:

- `service.go`, `service_<domain>.go`, `handler.go`, `handler_<area>.go`, `*_worker.go`, `errors.go`.
- Allowed subdirs: `db/`, `queries/`, `migrations/`, `pb/` (generated).
- Exceptions: `controlplane/authz/`, `controlplane/outboxpb/`.
- Banned new subtrees: `providers/`, `services/`, `usecase/`, `dto/`.
- God packages forbidden: ceilings and bridge rules in `modular-monolith.mdc`. `controlplane` is composition root only — domain logic in `internal/<domain>/`.
- Micro-packages forbidden: no stub domain dirs, no `internal/common` — minimum viable extraction + `doc.go` in same PR (`modular-monolith.mdc`).
- `doc.go` mandatory: detailed package doc at package root (`comments.mdc`, `modular-monolith.mdc`). Edit in the same PR when adding a package.

## Tests - keep vs delete

**Delete** useless tests:

- Pure arithmetic wrappers.
- Stdlib-only behavior (e.g. `json.Marshal` roundtrip with no app logic).
- Nil receiver smoke with no contract.
- Field echo without behavior.
- Static route meta smoke duplicated elsewhere.
- Duplicate coverage of same sqlc query.

**Keep / add:**

- Idempotency under duplicate webhook/outbox replay (`*_fault_test.go`).
- Body size limit regressions (`TestColdPathJSON`).
- Transaction boundary tests with real testcontainers (`*_integration_test.go` per `anti-slop.mdc`).
- `AssertBudgetInvariant` on any spend path change.

## Admin UI (cold surface)

React 19 + TypeScript in `web/`. Styling: Tailwind utilities in TSX; entry `web/src/styles/app.css` (`@tailwind` + fonts only). **No `globals.css`.**

Anti-slop: `ui.mdc`, `anti-slop.mdc`. Run `bash scripts/ci/admin/web.sh` before claiming UI done.

## Verification

```bash
go test ./internal/<touched>/... -short -count=1
bash scripts/ci/static/cold_path_static.sh
bash scripts/ci/static/cold_path_json.sh
bash scripts/ci/static/anti_slop.sh
```

## Related rules

`anti-slop.mdc`, `boundaries.mdc`, `code-style.mdc`, `control-plane.mdc`, `fault-tests.mdc`, `ui.mdc`.
