# CLAUDE.md

This file provides agent-specific guidance for working in crate shipper-types.

## Scope

- Crate: shipper-types
- Path: crates/shipper-types
- Workspace root: h:\Code\Rust\shipper
- Primary entry: src/lib.rs

## Useful commands

```bash
cargo check -p shipper-types
cargo test -p shipper-types
cargo test -p shipper-types --all-features
cargo fmt -p shipper-types
cargo clippy -p shipper-types --all-targets --all-features -- -D warnings
```

## Context

- Keep changes small and targeted to the crate’s existing abstractions.
- Preserve public API compatibility unless the request explicitly asks for breaking changes.
- When touching serialization or state formats, update tests and related snapshots in the same crate.
- Prefer using existing fixtures and helpers rather than introducing inline test data.

For full workspace guidance, see [../../CLAUDE.md](../../CLAUDE.md).