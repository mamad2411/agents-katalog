---
name: follow-create-rust-crate
description: Build Rust library crates with Cargo following best practices
argument-hint: "[scope]"
related:
  - follow-create-cli
  - follow-create-sdk
  - follow-lang-rust
  - follow-release
  - follow-tool-cargo
  - run-test
  - deep-review-codebase
  - report

---
## Goal

Build Rust library crates with Cargo that have a clear public API, complete docs, passing tests, and are ready to publish to crates.io

## Scope

Use for building library crates in pure Rust or with FFI, covering `Cargo.toml`, `src/lib.rs`, tests, examples, documentation, and CI

- Rust stable + `edition = "2024"` in `Cargo.toml` — always confirm the latest versions with `/deep-research` + `/follow-best-practice` (not pinned in this file — per `/update-devin-global-skills`)

## Execute

### 1. Review Tech Stack

> Goal: Inspect the tech stack before creating

1. Run `/deep-research` + `/follow-best-practice` to confirm the latest versions and patterns, then run `/deep-review-codebase` to summarize the tech stack
2. Run `/deep-review-codebase` to review the tech stack, dependencies, and library design (create rust crate)
3. Record the reasons for choosing the stack and libraries for later reference (create rust crate)

### 2. Setup Project

> Goal: Create the crate structure

1. Run `cargo new --lib <crate-name>`
2. Create `justfile`, `rust-toolchain.toml`, `.gitignore`, `LICENSE`, `README.md`
3. Create the `src/`, `tests/`, `examples/`, `benches/` directories if needed
4. Split modules by responsibility

### 3. Configure Cargo.toml

> Goal: Define crate metadata and build profiles

1. Specify `name`, `version`, `edition`, `description`, `license`, `repository`, `keywords`, `categories`
2. Set `edition = "2024"`
3. Set `rust-version` if needed
4. Configure `[lib]`, setting `crate-type` to `["lib"]` or `["cdylib"]` for FFI
5. Configure `[profile.dev]` and `[profile.release]`

### 4. Write Public API

> Goal: Design `lib.rs` to be clear

1. Use `pub mod` for modules
2. Use `pub use` for re-exports that users commonly use
3. Write doc comments (`///`) on public types and functions
4. Use `#[cfg(...)]` for feature flags

### 5. Implement Modules

> Goal: Split the implementation by concern

1. Create modules in `src/{module}.rs`
2. Use `mod.rs` or `src/{module}.rs` per edition 2024
3. Use `thiserror` for error types
4. Never use `unwrap()` or `expect()` in library code

### 6. Add Tests

> Goal: Test units and integration

1. Create `tests/` for integration tests
2. Create `#[cfg(test)] mod tests` in `src/`
3. Use `benches/` for benchmarks if needed
4. Run `cargo test`, `cargo clippy`, `cargo fmt --check`

### 7. Add Documentation

> Goal: Generate rustdoc

1. Write doc comments for every public item
2. Use `# Examples` in doc comments
3. Run `cargo doc --no-deps`
4. Check that the docs have no broken links

### 8. CI And Release

> Goal: Configure CI and release

1. Create `.github/workflows/ci.yml` running `test`, `clippy`, `fmt`, `doc`
2. Create `.github/workflows/release.yml` for `cargo publish`
3. Run `/follow-release` when publishing

### 9. Ship

> Goal: Deliver the work

1. Run `/ship`
2. If `ship` fails → report the status

## Rules

- Use `snake_case` for modules, functions, variables
- Use `PascalCase` for types, traits
- Use `thiserror` for library errors, `anyhow` for examples/binaries
- Never use `unwrap()` in library code
- Specify `edition = "2024"`
- `crate-type` is `["lib"]` unless FFI is required

- Use /follow-create-cli if needed
- Use /follow-create-sdk if needed
- Use /follow-lang-rust if needed
- Use /follow-tool-cargo if needed
- Use /run-test if needed
- Use /report if needed

## Expected Outcome

- Rust crate builds with `cargo build`
- `cargo test` passes
- `cargo clippy` has no warnings
- `cargo doc` generates documentation
- Public API is clear through `lib.rs`
- Ready to publish to crates.io

