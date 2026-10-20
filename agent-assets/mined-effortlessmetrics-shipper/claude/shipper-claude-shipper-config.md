# CLAUDE.md

This file provides agent-specific guidance for working in crate shipper-config.

## Scope

- Crate: shipper-config
- Path: crates/shipper-config
- Workspace root: h:\Code\Rust\shipper
- Primary entry: src/lib.rs

## Useful commands

```bash
cargo check -p shipper-config
cargo test -p shipper-config
cargo test -p shipper-config --all-features
cargo fmt -p shipper-config
cargo clippy -p shipper-config --all-targets --all-features -- -D warnings
```

## Context

- Keep changes small and targeted to the crate’s existing abstractions.
- Preserve public API compatibility unless the request explicitly asks for breaking changes.
- When touching serialization or state formats, update tests and related snapshots in the same crate.
- Prefer using existing fixtures and helpers rather than introducing inline test data.

For full workspace guidance, see [../../CLAUDE.md](../../CLAUDE.md).