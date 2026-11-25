---
name: rust-feature-slice
audience: team
description: >
  Feature-based vertical-slice architecture for Rust using Axum routers, handler functions, and
  service traits. No DI framework — dependencies wired manually via Arc<dyn Trait> in Axum
  State. CQRS via trait separation: reader traits for queries, writer traits for commands. Use
  when scaffolding Rust features, creating Axum feature modules, adding service layers, or
  organizing Rust code by feature rather than technical layer. Not for
  microservice/inter-process boundaries — scopes to module organization within a single Rust
  binary.
---

# Rust Feature Slice Architecture

> "Organize code by what it does, not by what it is. A feature folder contains everything needed to deliver a capability — not everything that happens to be a handler."
> -- Adapted from Jimmy Bogard

> "In Rust, there is no DI framework. There is ownership. Design your dependencies so that ownership is clear, and wiring becomes mechanical."
> -- Rust Architecture Principle

## Core Philosophy

Vertical slice architecture in Rust organizes code by feature (domain capability) rather than technical layer (handlers, services, repositories). Each feature is a Rust module containing everything needed to deliver that capability: router, handlers, service trait, service implementation, request/response types, and tests.

Rust has no dependency injection framework. Dependencies are wired manually using `Arc<dyn Trait>` stored in Axum's `State<AppState>`. This is not a limitation — it is explicit, compile-time-verified dependency wiring. The `AppState` struct is the composition root.

CQRS in Rust is a naming convention enforced by trait design: `OrderReader` (query methods) and `OrderWriter` (command methods) are separate traits, potentially implemented by the same struct. This separation makes the read/write boundary explicit without requiring a library.

**Non-Negotiable Constraints:**

1. **Feature module isolation** — no `use crate::features::other_feature::` in handlers. Features communicate through shared types in a `common` or `domain` module, not through direct imports.
2. **Service traits, not concrete types** — `Arc<dyn OrderService>` in `AppState`, not `Arc<OrderServiceImpl>`. This enables testing with mock implementations.
3. **`Arc<dyn Trait>` for shared state** — not `Mutex<ConcreteType>`. The trait defines the contract; the `Arc` provides shared ownership.
4. **`Result<T, AppError>` on all handlers** — handlers return `Result<impl IntoResponse, AppError>`. No panics, no unwrap in handler code.
5. **Handler thinness** — handlers extract request data, call the service, and return the response. Business logic belongs in the service, not the handler.

The 10 domain principles, the knowledge-base lookup map, and the anti-pattern catalog live in
`references/principles-and-anti-patterns.md`. The AI discipline rules (trait-not-concrete-in-state,
thin handlers, async-trait selection) and error-recovery procedures live in
`references/discipline-and-recovery.md`.

## Workflow

```
DETECT (before scaffolding)
    [ ] Check for existing AppState struct (src/state.rs or src/app.rs)
    [ ] Check for existing features/ directory structure
    [ ] Identify Rust edition and async runtime (Cargo.toml)
    [ ] Check for existing error types (AppError)
    [ ] Identify database access pattern (SQLx, Diesel, none)

        |
        v

SCAFFOLD (create feature module)
    [ ] Create src/features/<name>/mod.rs (re-exports)
    [ ] Create src/features/<name>/router.rs (Axum Router with State)
    [ ] Create src/features/<name>/service.rs (trait + impl)
    [ ] Create src/features/<name>/models.rs (request/response types)
    [ ] Create src/features/<name>/errors.rs (feature error type)
    [ ] Create tests/features/<name>/integration_test.rs

        |
        v

REGISTER (wire into app)
    [ ] Add service to AppState struct
    [ ] Add Arc<dyn Trait> initialization in app startup
    [ ] Merge feature Router into main app Router
    [ ] Add From<FeatureError> for AppError

        |
        v

VERIFY
    [ ] cargo build (no errors)
    [ ] cargo test (all tests pass)
    [ ] cargo clippy -- -D warnings (no warnings)
```

**Exit criteria:** Feature module created, registered in app, tests pass, Clippy clean.

## State Block

```
<rust-feature-slice-state>
phase: DETECT | SCAFFOLD | REGISTER | VERIFY | COMPLETE
feature_name: [name]
edition: [2015 | 2018 | 2021 | 2024]
async_runtime: [tokio | async-std | none]
app_state_exists: [true | false]
features_dir_exists: [true | false]
app_error_exists: [true | false]
files_created: [comma-separated list]
build_status: [pass | fail | not-run]
test_status: [pass | fail | not-run]
last_action: [description]
next_action: [description]
</rust-feature-slice-state>
```

## Output Template

The scaffold reports the files it creates and modifies, then a verification gate:

```markdown
## Rust Feature Slice Scaffold: [feature-name]

### Files to Create
- [ ] `src/features/[name]/{mod,router,service,models,errors}.rs`
- [ ] `tests/features/[name]/integration_test.rs`

### Files to Modify
- [ ] `src/state.rs` — add `Arc<dyn [Name]Service>` field
- [ ] `src/app.rs` or `src/main.rs` — merge feature Router, initialize service
- [ ] `src/errors.rs` — add `From<[Name]Error> for AppError`

### Verification
- [ ] `cargo build` · `cargo test` · `cargo clippy -- -D warnings` all pass
```

Full, ready-to-fill code for every file (mod/models/errors/service/router, `AppState`, `AppError`,
integration test) is in `references/feature-module-template.md`. The five Axum state-injection
patterns (single state, `FromRef`, nested state, `Extension` vs `State`, mock injection) are in
`references/state-injection-patterns.md`.

## Integration with Other Skills

| Skill | Relationship |
|-------|-------------|
| `axum-scaffolder` | Provides the HTTP layer patterns (middleware, OpenAPI, auth). Use `rust-feature-slice` for module organization; use `axum-scaffolder` for HTTP infrastructure. |
| `sqlx-migration-manager` | When the feature requires database access, `sqlx-migration-manager` provides the safe migration and query patterns for the service implementation. |
| `rust-architecture-checklist` | After scaffolding, run `rust-architecture-checklist` to verify the feature follows ownership, trait, and error handling conventions. |
| `rust-security-review` | After scaffolding, run `rust-security-review` to verify the feature's auth middleware, input validation, and error handling are secure. |
| `dotnet-vertical-slice` | Parallel skill for .NET/Blazor codebases. Same vertical slice philosophy; different ecosystem. |
