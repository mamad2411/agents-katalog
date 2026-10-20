---
name: toolchain-rust
description: "Rust project toolchain -- cargo build, test, clippy, formatting, and cross-compilation."
metadata: {"thinkfleetbot":{"emoji":"🦀","requires":{"bins":["cargo"]}}}
---

# Rust Toolchain

Common commands for Rust projects.

## Build & run

```bash
cargo build
cargo build --release
cargo run
cargo run --release
cargo run -- --arg1 value1
```

## Testing

```bash
cargo test
cargo test -- --nocapture         # Show stdout
cargo test test_name              # Run specific test
cargo test --lib                  # Lib tests only
cargo test --doc                  # Doc tests only
```

## Linting

```bash
cargo clippy -- -W clippy::all
cargo clippy --fix                # Auto-fix suggestions
```

## Formatting

```bash
cargo fmt
cargo fmt -- --check              # Check only (CI)
```

## Dependencies

```bash
cargo add serde --features derive
cargo add tokio --features full
cargo remove unused-crate
cargo update                      # Update Cargo.lock
cargo tree                        # Dependency tree
cargo audit                       # Security audit
```

## Documentation

```bash
cargo doc --open
cargo doc --no-deps
```

## Benchmarks

```bash
cargo bench
```

## Check (fast compile check)

```bash
cargo check
cargo check --all-targets
```

## Cross-compilation

```bash
rustup target add x86_64-unknown-linux-musl
cargo build --release --target x86_64-unknown-linux-musl
```

## Workspace

```bash
cargo build --workspace
cargo test --workspace
cargo build -p my-crate           # Specific crate
```

## Notes

- `Cargo.toml` defines the project manifest and dependencies.
- `cargo check` is faster than `cargo build` for catching errors.
- Use `clippy` as the primary linter; it catches common Rust anti-patterns.
