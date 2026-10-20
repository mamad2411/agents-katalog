# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

`AGENTS.md` is the authoritative shared agent instruction file. Read it before
working, and follow it whenever this legacy compatibility file has drifted.

## What is Foundry

Foundry is a comprehensive, strongly-typed Rust backend framework built on Axum + Tokio + SQLx. It provides 5 runtime kernels (HTTP, CLI, Scheduler, Worker, WebSocket) with built-in auth, jobs, email, storage, validation, and plugin systems. The framework emphasizes thin app code — apps focus on domain logic while Foundry owns infrastructure.

## Build & Development Commands

```bash
make verify          # Full check: fmt + test + clippy + fixture checks (same as CI)
make verify-release  # Full check + package dry-run
make fmt             # cargo fmt
make fmt-check       # cargo fmt --check
make test            # cargo test --all-targets
make clippy          # cargo clippy --all-targets -- -D warnings
make fixture-check   # Tests blueprint_app + plugin_consumer_app fixtures
make api-docs        # Regenerate docs/api/ from cargo doc HTML
```

Single test: `cargo test --test <test_file_name>` (e.g., `cargo test --test auth_acceptance`)

Postgres tests: `cargo test --test database_acceptance` (requires `FOUNDRY_TEST_POSTGRES_URL` env var)

MSRV: Rust 1.94. CI tests on 1.94.1 and stable with Postgres 16.

## Architecture Overview

**Foundation layer** (`src/foundation/`): `AppBuilder` bootstraps the app via fluent API → builds a kernel → starts runtime. `AppContext` is the central DI container holding config, database, Redis, auth, etc. `AppTransaction` wraps DB transactions with after-commit callbacks.

**5 Kernels** (`src/kernel/`): HTTP (Axum), CLI (Clap), Scheduler (cron + Redis leadership), Worker (Redis job queues), WebSocket (channels + presence). Each is an independent async runtime.

**Database** (`src/database/`): AST-first query system — expressions compile to SQL via dialect-specific compilers. `Model` trait with lifecycle hooks, typed `ModelId<M>` (UUIDv7), relations (`belongs_to`, `has_one`, `has_many`, `many_to_many`), eager loading, projections, CTEs. Build-time codegen via `foundry-build` discovers migrations/seeders.

**Registry pattern**: All major systems use typed registries — routes, commands, schedules, validation rules, authenticatables, notification channels, plugins. IDs are semantic typed constants (e.g., `GuardId`, `JobId`, `ChannelId`). Duplicate registrations are detected (commands/schedules/channels/rules error; routes warn).

**Plugin system** (`src/plugin/`): Compile-time registry with dependency resolution, SemVer validation, and full lifecycle (`register` → `boot` → `shutdown`). Plugins can directly register any framework feature (guards, jobs, events, middleware, etc.) without ServiceProvider wrappers. See `blueprints/19-plugin-system-v2.md`.

## Key Design Principles

- **Strongly typed IDs everywhere** — no raw strings where typed identifiers exist (`ModelId<M>`, `GuardId`, `PolicyId`, `JobId`, etc.)
- **Trait-based extensibility** — `ServiceProvider`, `Plugin`, `ValidationRule`, `Job`, `Model`, `EmailDriver`, `StorageAdapter` are all traits
- **Consumer-thin model** — framework handles infrastructure; app code stays minimal (see `tests/fixtures/blueprint_app/` for the reference pattern)
- **Immutable temporal types** — `Clock`, `DateTime`, `LocalDateTime` are all immutable

## Workspace Structure

- `foundry` (root) — main framework crate
- `foundry-build` — build-time codegen for migrations/seeders discovery
- `foundry-macros` — proc macros (`#[derive(Model)]`, `#[derive(Validate)]`, etc.)
- `tools/foundry-api-doc/` — standalone API surface doc generator (parses `cargo doc` HTML)
- `tests/fixtures/blueprint_app/` — reference consumer app (must stay green)
- `tests/fixtures/plugin_*/` — plugin test fixtures (must stay green)
- `blueprints/` — design docs for major systems
- `examples/` — runnable examples for each subsystem

## Testing

Acceptance tests live in `tests/` as separate test files:
- `acceptance.rs` — general app
- `database_acceptance.rs` — queries (needs Postgres)
- `auth_acceptance.rs` — auth flows
- `phase2_acceptance.rs` — WebSocket + events + jobs
- `plugin_acceptance.rs` — plugin system
- `blueprint_fixture_acceptance.rs` / `plugin_fixture_acceptance.rs` — fixture validation

Test infra: `TestApp`, `TestClient`, `TestResponse`, `Factory` builder in `src/testing/`.

## Important Conventions

- When changing bootstrap or registry behavior, both fixture families must stay green
- Public API changes should update examples, docs, and acceptance fixtures
- Update `CHANGELOG.md` for user-visible changes
- See `docs/release-checklist.md` for release procedure
- See `docs/guides/` for consumer-facing usage guides (plugins, datatable, validation, etc.)
