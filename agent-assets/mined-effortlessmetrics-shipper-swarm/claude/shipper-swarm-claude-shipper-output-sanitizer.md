# CLAUDE.md

This file provides agent-specific guidance for working in crate shipper-output-sanitizer.

## Scope

- Crate: shipper-output-sanitizer
- Path: crates/shipper-output-sanitizer
- Workspace root: h:\Code\Rust\shipper
- Primary entry: src/lib.rs

## Useful commands

```bash
cargo check -p shipper-output-sanitizer
cargo test -p shipper-output-sanitizer
cargo test -p shipper-output-sanitizer --all-features
cargo fmt -p shipper-output-sanitizer
cargo clippy -p shipper-output-sanitizer --all-targets --all-features -- -D warnings
```

## Context

- Keep changes small and targeted to the crate’s existing abstractions.
- Preserve public API compatibility unless the request explicitly asks for breaking changes.
- When touching serialization or state formats, update tests and related snapshots in the same crate.
- Prefer using existing fixtures and helpers rather than introducing inline test data.

For full workspace guidance, see [../../CLAUDE.md](../../CLAUDE.md).