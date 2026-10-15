---
name: rust-hexagonal
description: 'Hexagonal architecture (Ports & Adapters) for Rust backends. Use when: creating a new Rust backend, structuring a domain layer, defining ports as traits, implementing adapters (HTTP, DB, gRPC), wiring dependency injection, separating business logic from infrastructure, applying clean architecture in Rust, organizing modules for testability.'
argument-hint: 'Describe the feature or layer you want to scaffold (e.g., "user domain", "HTTP adapter for orders")'
---

# Hexagonal Architecture for Rust Backends

## Overview

Hexagonal Architecture (Ports & Adapters) isolates the **domain** from all external concerns. Nothing in domain or use cases ever imports an infrastructure crate.

**Call flow (always this direction):**
```
[ HTTP / CLI / gRPC ]  →  inbound  →  use case fns(R)  →  domain  →  R: Repository  →  outbound  →  [ DB / APIs ]
```

Dependencies point **inward only** (enforced via `Cargo.toml`):
```
app → inbound  ─┐
                ├→ domain  (model + errors + ports + use cases)
app → outbound ─┘
```

Three crates + one binary:
1. **`domain`** — entities, value objects, errors, port traits, use case implementations.
2. **`inbound` / `outbound`** — concrete adapter crates; depend only on `domain`, never each other.
3. **`app`** — binary; the only crate that knows all concrete types.

> **Is this still hexagonal?** Yes. The invariant holds: domain/use cases never depend on infrastructure.

### Merge use cases into `domain`, or keep a separate `application` crate?

| | **Layout A — merge (recommended)** | **Layout B — separate `application`** |
|---|---|---|
| **Crate count** | 4 | 5 |
| **`domain` deps** | may include `tokio` | stays fully dep-free |
| **Best for** | most projects | shared domain across multiple services or publishing domain as a lib |

> **`async-trait` rule:** With Rust ≥ 1.75 and static dispatch, native `async fn` in traits is
> sufficient — **no `async-trait` needed**. Only add it if you explicitly need `dyn Trait` object safety.

---

## Companion Skills

Load these skills when working on the corresponding layers:

| Layer | Skill | Covers |
|-------|-------|--------|
| Inbound (HTTP) | `http-actix-axum` | REST naming, status codes, RFC 9457 Problem Details, CORS, OWASP security headers, compression, versioning |
| Outbound (DB) | `sea-orm` | Migrations, entity generation, CRUD, relations, pagination, on-conflict, SeaORM v2 macros |

> These skills are **authoritative** for their layer. Prefer them over inline examples when detail is needed.

---

## Workspace Structure

```
my-app/
├── Cargo.toml          # workspace root
├── domain/             # lib — model, errors, ports, use cases (Layout A)
├── inbound/            # lib — HTTP/gRPC/CLI adapters  (actix-web preferred; axum supported)
├── outbound/           # lib — DB/cache adapters (SeaORM v2)
├── migration/          # lib — DB migrations (sea-orm-migration only; no domain imports)
└── app/                # bin — sole composition root
```

Layout B adds an `application/` crate between `domain` and `app`; `domain` then stays dep-free.

See [folder structure & Cargo.toml templates](./references/folder-structure.md).

---

## Key Rules

| Rule | Why |
|------|-----|
| `domain` never imports infrastructure crates | Portable, testable core |
| Port traits live in `domain` | Domain owns its own contracts |
| Use cases are **free async functions** generic over `R: Repository` | Static dispatch, no boilerplate trait impl |
| Inbound handlers are **generic** over `R: AppRepository` via `web::Data<AppState<R>>` | No concrete type leaks into the HTTP layer |
| `AppRepository` is a supertrait in `inbound` with a blanket impl | Outbound crates never import `inbound`; composition stays in `app` |
| `inbound` and `outbound` depend **only on `domain`** | No cross-adapter coupling |
| Prefer **`impl Iterator<Item = T>`** over `Vec<T>` in collection ports | Caller decides whether/how to allocate |
| Prefer **static dispatch** (generics); use `Arc<dyn Trait>` only when runtime polymorphism is needed | Zero-cost unless you opt in |
| No `async-trait` unless you need `dyn Trait` object safety | Native async fn in traits (Rust ≥ 1.75) |
| `app/main.rs` is the only file importing all concrete types | Single composition root |
| `AppRepository` supertrait may live in `domain/ports/mod.rs` when ≥ 2 port traits exist | Keeps the combined bound in domain; outbound never needs to import inbound |

---

## Scaffold Checklist

Load only the reference for the layer you're working on:

| Step | What | Reference |
|------|------|-----------|
| 1 | Domain model (entities, value objects) | [domain.md](./references/domain.md) |
| 2 | Domain errors | [domain.md](./references/domain.md) |
| 3 | Outbound port (repository trait) | [domain.md](./references/domain.md) |
| 4 | Use case functions | [domain.md](./references/domain.md) |
| 5 | DB migrations | [migrations.md](./references/migrations.md) |
| 6 | Outbound adapter (SeaORM repository) | [outbound.md](./references/outbound.md) + `sea-orm` skill |
| 7 | Inbound adapter (actix-web / axum) | [inbound.md](./references/inbound.md) + `http-actix-axum` skill |
| 8 | Wire & run | [bootstrap.md](./references/bootstrap.md) |

---

## Testing Strategy

| Layer | Approach |
|-------|----------|
| Domain model | Pure unit tests — no async, no mocks |
| Use case | `#[tokio::test]` + `mockall` mock of outbound port |
| Outbound adapter | SeaORM `MockDatabase` or test containers |
| Inbound adapter | `actix_web::test` with generic handler + mock repository |

See [testing reference](./references/testing.md).

---

## Recommended Crates

| Purpose | Crate |
|---------|-------|
| HTTP framework | `actix-web` (preferred) or `axum` |
| Async runtime | `tokio` |
| Database ORM | `sea-orm` v2 |
| Error handling | `thiserror` + `anyhow` |
| Async traits (opt-in) | `async-trait` (only if `dyn Trait` needed) |
| Mocking | `mockall` ≥ 0.12 |
| Serialization | `serde` + `serde_json` |
| Validation | `validator` |
| Tracing | `tracing` + `tracing-subscriber` |
| Config / env | `dotenvy` + `config` |

---

## Common Pitfalls

- **Domain importing infrastructure crates** — `domain/Cargo.toml` must list no `sea-orm`, `actix-web`, `axum`, etc.
- **Cross-adapter coupling** — `inbound` and `outbound` must not import each other; enforced by their `Cargo.toml`.
- **Handler holding a concrete service type** — `web::Data<OrderService<PgRepo>>` leaks the concrete type. Use `web::Data<AppState<R>>` where `R: AppRepository` to keep the adapter generic.
- **Unnecessary `async-trait`** — only add it when you need `dyn Trait`. With static dispatch and Rust ≥ 1.75, remove it from port traits.
- **`mockall::automock` on RPIT traits** — `#[automock]` compile-errors when a trait method returns `impl Trait` in return position (e.g. `async fn find_all() -> Result<impl Iterator<Item = T>, _>`). Only annotate traits with concrete return types. For RPIT traits write a hand-written fake struct in a `#[cfg(test)]` block — see [testing reference](./references/testing.md).
- **Returning `Vec<T>` from collection ports** — prefer `impl Iterator<Item = T>`; the adapter collects from DB internally but the interface stays flexible.
- **Leaking SeaORM types into domain** — `Model`, `ActiveModel`, column enums belong in `outbound/src/db/`. Map to domain structs in `mappers.rs` immediately.
- **Bloated `app/main.rs`** — extract `fn wire_orders(db)` helpers per bounded context; keep `main` under ~30 lines.
- **Using `.insert()` in `save()`** — always INSERT fails for existing records. Use an `ON CONFLICT … DO UPDATE` upsert (see `outbound.md`).
- **`find_all()` without pagination** — fetching entire tables into memory will OOM in production. Add `page`/`limit` or cursor parameters to collection port signatures before the table grows.
- **Expanding `AppRepository` with every new trait** — when adding a second bounded context (e.g. `CustomerRepository`), create a focused `CustomerAppRepository` supertrait rather than bolting it onto the existing one. Handlers that only handle orders should not receive a repo that also exposes customer operations.

---

## Scaling to Multiple Bounded Contexts

As the application grows beyond a single `orders` domain, organise by bounded context **within each crate** before splitting crates:

```
domain/src/
├── lib.rs              # pub mod orders; pub mod customers;
├── orders/
│   ├── mod.rs          # pub mod model; pub mod error; pub mod ports; pub mod use_cases;
│   └── …
└── customers/
    ├── mod.rs
    └── …

inbound/src/
├── state.rs            # separate AppRepository supertrait per context if needed
└── http/
    ├── orders/         # handlers, router, dto for orders
    └── customers/      # handlers, router, dto for customers

outbound/src/db/
├── orders/             # repository, entities, mappers
└── customers/
```

**When to split into separate crates / microservices:**

| Signal | Action |
|--------|--------|
| Two bounded contexts never share a DB transaction | Safe to extract into separate services |
| Compile times become painful | Move large bounded context to its own workspace |
| Independent deployment cadence required | Extract to its own binary (`app-orders`, `app-customers`) |
| Team ownership boundaries diverge | Separate repos with a shared `domain` lib published to a registry |
