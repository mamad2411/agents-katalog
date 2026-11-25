---
name: ci-cd-rust
description: "Applies when creating or modifying CI/CD pipelines for Rust projects. Covers cargo/target caching, cargo-tarpaulin/llvm-cov coverage, clippy linting, and cargo audit."
---

# Rust CI/CD

## Setup and caching

Use `dtolnay/rust-toolchain@stable` (or `nightly`) for the toolchain. Use `Swatinem/rust-cache@v2` for caching:

Cached paths:
- `~/.cargo/registry/index`
- `~/.cargo/registry/cache`
- `~/.cargo/git/db`
- `target/` (build artifacts)

Key file: `Cargo.lock`.

## Install

```bash
cargo fetch    # pre-download dependencies (optional, for cache warming)
```

## Coverage

```bash
# cargo-tarpaulin (stable Rust, Linux only)
cargo tarpaulin --out xml --output-dir coverage/

# cargo-llvm-cov (all platforms, more accurate)
cargo llvm-cov --codecov --output-path codecov.json
```

## Linting

```bash
cargo clippy -- -D warnings    # treat warnings as errors
cargo fmt --check              # format check
```

## Dependency audit

```bash
cargo audit                    # known vulnerabilities
cargo deny check               # license + advisory + ban checks
```

## Rust-specific gotchas

1. Rust builds are slow — caching `target/` with `Swatinem/rust-cache` cuts rebuild time by 50-80%.
2. Use `CARGO_INCREMENTAL=0` in CI for faster clean builds and more reproducible results.
3. Set `RUSTFLAGS="-C debuginfo=0"` for test-only builds to reduce `target/` cache size.
4. Run `cargo clippy` and `cargo fmt` in a separate job from tests — they're fast and independent.
5. For workspaces, `cargo test --workspace` runs all crate tests in one invocation.
6. Pin the toolchain version in `rust-toolchain.toml` for reproducibility.

## Sources

- https://github.com/dtolnay/rust-toolchain
- https://github.com/Swatinem/rust-cache
- https://github.com/xd009642/tarpaulin
