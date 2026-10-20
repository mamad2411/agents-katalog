# Rust Conventions

Conventions for systems-level and service work built with Rust. Applies to any feature the
framework targets at a Rust codebase — CLI tools, backend services, or shared library crates.

## Architecture
ALWAYS follow Clean Architecture layers: Domain → UseCases → Adapters → Frameworks.
NEVER let domain types import adapter or framework crates.
ALWAYS define traits in the use-case layer, implement in adapter crates.
ALWAYS use constructor-style `new()` or builder patterns — no naked public fields on domain types.
NEVER use `unwrap()` or `expect()` in library code — only in tests or unreachable branches with a comment explaining why.
ALWAYS handle errors explicitly with `?` — no silent swallows.
ALWAYS set explicit timeouts on every network call.
NEVER use raw SQL without parameterized queries.
ALWAYS use the expand/contract pattern for database migrations.

## Project Tooling
- **Build / dependency manager**: `cargo` — pin exact versions in `Cargo.lock`; check in `Cargo.lock`
  for binaries, omit it for library crates.
- **Formatter**: `rustfmt` — `cargo fmt --all`; enforce in CI.
- **Linter / complexity**: `cargo clippy -- -D warnings` — treat every Clippy warning as a build
  failure. For cognitive complexity specifically, enable
  `#![warn(clippy::cognitive_complexity)]` and cap at `6` (enforces the framework-wide `< 7` budget).
- **Supply-chain audit**: [`cargo-deny`](https://embarkstudios.github.io/cargo-deny/) — ban known
  yanked crates, enforce license allow-lists, block duplicate versions. `cargo audit` for CVE scanning.
- **Unsafe code**: `#![forbid(unsafe_code)]` at every crate root. If `unsafe` is genuinely
  required (FFI, performance-critical primitives), it MUST be documented in an ADR and isolated to
  a single `unsafe_impl/` module with a `# Safety` doc comment on every `unsafe` block.

## Project Structure
Follows standard Cargo workspace layout:
- `crates/<name>/src/` — one crate per bounded context or architectural layer
- `src/lib.rs` — library entry point for single-crate projects
- `src/main.rs` — binary entry point; keep thin — delegate immediately to a `run()` fn in `lib.rs`
- `src/<domain>/mod.rs` — top-level module file for non-trivial sub-domains
- `tests/` — integration tests (separate from `#[cfg(test)]` unit tests); one file per feature area

File naming follows Rust community convention: `snake_case.rs`, one public top-level type or module
per file for large types. Small related types (newtypes, enums, errors) may share a file.

## Error Handling
- **Library crates**: [`thiserror`](https://github.com/dtolnay/thiserror) — derive typed
  `Error` enums that callers can `match` on.
- **Application / binary crates**: [`anyhow`](https://github.com/dtolnay/anyhow) — ergonomic
  `Result<T, anyhow::Error>` with context chaining (`.context("...")`).
- NEVER mix `thiserror` and `anyhow` in the same crate — library boundary is the dividing line.
- ALWAYS propagate with `?`; only `unwrap()` / `expect()` where an invariant is truly unreachable
  and the panic message explains why.

## Async
- **Runtime**: [`tokio`](https://tokio.rs/) — the standard default for networked services.
  For embedded or no-std targets, this choice is an ADR-worthy decision — document the alternative
  (`embassy`, `smol`, bare `futures`) and the reason.
- **Async in traits**: native `async fn` in traits is stable since Rust 1.75 and is the correct
  default for non-object-safe trait bounds. For object-safe dynamic dispatch
  (`Box<dyn MyTrait>`), [`async-trait`](https://github.com/dtolnay/async-trait) remains necessary
  until `dyn async Fn` stabilizes — annotate with `#[async_trait]` only when dynamic dispatch
  is explicitly needed.
- ALWAYS use `tokio::time::timeout()` for network calls — never an unbounded `.await`.
- NEVER `block_on()` from within an async context — it deadlocks on single-threaded runtimes.

## Testing & QA Tooling
- **Unit tests**: inline `#[cfg(test)] mod tests { ... }` per module — the Rust idiom; tests live
  next to the code they verify.
- **Integration tests**: `tests/` directory, one file per feature boundary; uses the public API only.
- **Property-based testing**: [`proptest`](https://github.com/proptest-rs/proptest) — generate
  random inputs and verify invariants (`prop_assert!`). Prefer over hand-written edge cases for
  numeric, string, and collection inputs.
- **Parameterized / table-driven tests**: [`rstest`](https://github.com/la10736/rstest) — `#[rstest]`
  + `#[case(...)]` for table-driven tests; `#[fixture]` for shared setup, equivalent to
  `t.Run()` table tests in Go.
- **Trait mocking**: [`mockall`](https://github.com/asomers/mockall) — `#[automock]` on traits;
  generates `MockMyTrait` structs with `.expect_method()` / `.returning(...)` Mockito-style
  expectations. Use only in unit tests — never ship `mockall` in production code paths.
- **Fake / synthetic data**: [`fake`](https://github.com/cksac/fake-rs) (`fake = { features = ["derive"] }`)
  — derive-based fake generation for domain structs; `Faker::fake()` for scalars. Closest Rust
  equivalent to `gofakeit` / `@faker-js/faker`.
- **Mutation testing** (ADR-008 clause 2): `cargo-mutants` — a candidate, **not yet verified** against a
  real project. Verify before relying on its score: a mutant that did not compile, or timed out,
  must never be counted as killed.
- **Performance testing**: k6 — same as every other language here. For micro-benchmarks,
  `cargo bench` with [`criterion`](https://github.com/bheisler/criterion.rs) — statistical
  regression detection, HTML reports.
- **Reporting**: `cargo test --no-fail-fast -- -Z unstable-options --format json` piped to
  [`cargo2junit`](https://github.com/johnterickson/cargo2junit) for JUnit XML output into the CI
  reporting aggregator.

## Quick Reference

```rust
// Complexity: < 7 — enforce with clippy::cognitive_complexity capped at 6 in CI
// File naming: snake_case.rs, one top-level public type per file for large types
// Architecture: Domain / UseCases / Adapters / Frameworks — no framework imports in domain
// Errors: thiserror in libs, anyhow in binaries; never unwrap() in lib code
// Async: tokio runtime; native async fn in traits (1.75+); async-trait for dyn dispatch only
// Unsafe: #![forbid(unsafe_code)] at crate root; ADR required to unlock
// Safety fitness function: cargo clippy -- -D warnings in CI
// Tests: #[cfg(test)] inline units, tests/ integration, proptest, rstest, mockall
// Benchmarks: criterion
```

---
*Part of the [ai-assistant-dot-files](https://github.com/orieken/loom) Context Engineering Framework by Oscar Rieken — licensed under [CC BY 4.0](https://github.com/orieken/loom/blob/main/LICENSE-CONTENT.md). If you copy or adapt this file, please keep this attribution.*
