---
name: follow-lang-rust
description: Create or improve Rust projects with Clean Architecture and workspaces
argument-hint: "[scope|setup-project]"
related:
  - deep-review-codebase
  - follow-tool-cargo
  - follow-test
  - follow-tool-mutants-rs
  - follow-tool-nextest
  - follow-architecture
  - follow-create-rust-cli
  - follow-create-rust-crate
  - follow-create-web-wasm
  - deep-research
  - follow-best-practice
---

## Goal

Guide Rust application development for maximum safety, quality, and performance

## Scope

For creating or improving Rust projects, single crate and workspace. Package: `SKILL.md` entry + `references/toolchain.md` (ecosystem-tool table) + `workflows/setup-project/SKILL.md` (argument `setup-project` — first-time scaffold with toolchain pin and quality gates); verify the current stable toolchain and Cargo behavior via `/deep-research` at use time (official docs: https://www.rust-lang.org/learn, Cargo: https://doc.rust-lang.org/cargo/)

## Execute

### 1. Project Planning

> Goal: plan architecture and choose dependencies per project type

1. Identify the project location in the monorepo; decide workspace vs single crate
2. Define architecture: Clean Architecture or standard (run `/follow-architecture`)
3. Pick the async runtime: tokio (default), async-std, or smol
4. Database: SQLx (default), Diesel, or SeaORM; API: Axum (default), Actix-web, or Rocket; TUI: Ratatui; WASM: wasm-bindgen + wasm-pack
5. Run `/deep-research` + `/follow-best-practice` to confirm current versions/editions and the latest idiomatic Rust practices before adding crates or writing new code

### 2. Install And Scaffold

> Goal: set up the toolchain and project skeleton

1. New project → run the workflow `workflows/setup-project/SKILL.md` (argument `setup-project`): toolchain pin, `cargo new`, workspace choice, layout, quality gates from the first commit, verify
2. Tool inventory (clippy, fmt, nextest, deny/audit, miri, bench/profiling) → `references/toolchain.md`
3. Naming: files `snake_case`, types `PascalCase`; `mod.rs` as barrel exports only
4. For Clean Architecture, separate layers: domain, application, infrastructure — then run `/deep-review-codebase`

### 3. Configuration

> Goal: configure Cargo, toolchain, and build profiles

1. `Cargo.toml` — workspace (`members`, `exclude`, `default-members`, glob support) or single crate; pin the channel and components in `rust-toolchain.toml`
2. Workspace inheritance: shared metadata in `[workspace.package]` with `version.workspace = true` etc. in members; shared versions in `[workspace.dependencies]` with `{ workspace = true }`; shared lints in `[workspace.lints.*]` with `[lints] workspace = true`
3. `.cargo/config.toml` for build config (e.g. `[build] jobs`); set sccache for shared compilation cache
4. Profiles (root `Cargo.toml` only): dev with `debug = "line-tables-only"`, `incremental = true`, deps `debug = false`; release with `lto = true`, `codegen-units = 1`, `strip = true` (add `opt-level`/`panic = "abort"` per target)
5. Create a `justfile` for dev scripts (`mise use -g just`)

### 4. Quality Enforcement

> Goal: configure lints, security checks, and test infrastructure

1. Run `/follow-tool-cargo` for Cargo lint rules, Clippy config, and workspace lint inheritance
2. Set `unsafe_code = "forbid"` in workspace lints; Clippy `correctness`/`perf` deny, `style`/`suspicious` warn; `dbg_macro`/`todo`/`print_stdout`/`print_stderr` warn
3. `cargo-deny` for license/advisory checks (RUSTSEC advisory DB); `cargo-audit` for vulnerability scans
4. rustdoc: `#![warn(missing_docs)]`, `RUSTDOCFLAGS="-D rustdoc::all"` in CI
5. `cargo-nextest` for parallel tests, `cargo-llvm-cov` for coverage, Miri for UB detection in CI

### 5. Verification

> Goal: confirm compile, lint, format, and tests all pass

1. `cargo check --workspace` → `cargo clippy` → `cargo fmt --check`
2. `cargo nextest run` and `cargo test --doc` (nextest doesn't run doctests)
3. `cargo build --release` succeeds; WASM projects also build `--target wasm32-unknown-unknown`
4. On failure → run `/resolve-errors`

### 6. Testing Strategy

> Goal: define the testing strategy per project type

1. Run `/follow-test` for general strategy; `/follow-tool-nextest` for the runner
2. `#[cfg(test)]` unit tests inline; `tests/` for integration; `assert!`/`assert_eq!`/`#[should_panic]`
3. Business logic → `proptest` property-based tests; complex logic → `/follow-tool-mutants-rs` mutation testing
4. Every public API gets a doc example that uses `?`, never `unwrap()`

## Rules

### 1. Code Standards

- Follow Rust API Guidelines and naming conventions (RFC 430); implement common traits (`Debug`, `Clone`, `Default`, `Display`, eq/ord/`Hash`) where meaningful
- Imports ordered: `std` → external → internal (`crate::`)
- No `unwrap()` in production; use `?` and typed errors; prefer traits for abstraction
- Builder pattern for complex constructors; newtype pattern for domain types

### 2. Error Handling

- `thiserror` for library error enums, `anyhow` for applications; `#[from]` conversions; `.context()` at boundaries; error types implement `std::error::Error`

### 3. Documentation

- `//!` crate-level docs; document every public item with `# Errors`, `# Panics`, `# Safety` sections as applicable

### 4. Async Patterns

- tokio default; structured concurrency with `JoinSet`; cancellation via `CancellationToken`; `Send + Sync` bounds for shared state; `tokio::select!` for concurrent races; `Arc<T>` across tasks; never `block_on` inside async context

### 5. Performance

- Avoid allocations in hot paths: `&str` over `String`, `Cow<T>`, `SmallVec`; benchmark with `criterion` in `benches/` and profile with `cargo flamegraph`; tune `[profile.release]` (`lto`, `codegen-units = 1`)

### 6. Dependency Management

- Declare `rust-version` (MSRV); feature flags for optional functionality; keep the dependency tree minimal; `[workspace.dependencies]` for shared versions; check with `cargo sort` + `cargo outdated`; avoid floating ranges

### 7. CI/CD

- GitHub Actions: parallel fmt/clippy/check/test; matrix stable/beta/nightly/MSRV and cross-platform (incl. WASM/ARM); `cargo-deny`, `nextest`, `llvm-cov`, Miri; install CI tools with `taiki-e/install-action`

- Use /follow-create-rust-cli if needed
- Use /follow-create-rust-crate if needed
- Use /follow-create-web-wasm if needed

## Expected Outcome

- Correctly structured Rust project (crate or workspace) with Clean Architecture where applied
- Memory-safe, performant code with robust error handling
- Comprehensive tests: unit, integration, doctests, property-based, mutation
- Security passing `cargo-deny`/`cargo-audit` with `unsafe_code` forbidden
- Documentation complete under `missing_docs` enforcement
- Strict CI/CD pipeline green: fmt, clippy, check, nextest, coverage, Miri
