# CLAUDE.md

This file provides agent-specific guidance for working in crate shipper-encrypt.

## Scope

- Crate: shipper-encrypt
- Path: crates/shipper-encrypt
- Workspace root: h:\Code\Rust\shipper
- Primary entry: src/lib.rs

## Useful commands

```bash
cargo check -p shipper-encrypt
cargo test -p shipper-encrypt
cargo test -p shipper-encrypt --all-features
cargo fmt -p shipper-encrypt
cargo clippy -p shipper-encrypt --all-targets --all-features -- -D warnings
```

## Context

- Keep changes small and targeted to the crate’s existing abstractions.
- Preserve public API compatibility unless the request explicitly asks for breaking changes.
- When touching serialization or state formats, update tests and related snapshots in the same crate.
- Prefer using existing fixtures and helpers rather than introducing inline test data.

For full workspace guidance, see [../../CLAUDE.md](../../CLAUDE.md).