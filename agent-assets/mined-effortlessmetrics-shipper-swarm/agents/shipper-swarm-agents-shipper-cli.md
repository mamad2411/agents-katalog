# AGENTS.md

Use this file with [CLAUDE.md](./CLAUDE.md) before making changes in this directory.

This file provides agent-specific guidance for working in crate shipper-cli.

## Scope

- Crate: shipper-cli
- Path: crates/shipper-cli
- Workspace root: repository root for the current checkout; use repo-relative paths from this file
- Primary entry: src/lib.rs (`run()`); `src/main.rs` is the thin binary shim

## Useful commands

```bash
cargo check -p shipper-cli
cargo test -p shipper-cli
cargo test -p shipper-cli --all-features
cargo fmt -p shipper-cli
cargo clippy -p shipper-cli --all-targets --all-features -- -D warnings
```

## Context

- Keep changes small and targeted to the crate’s existing abstractions.
- Preserve public API compatibility unless the request explicitly asks for breaking changes.
- When touching serialization or state formats, update tests and related snapshots in the same crate.
- Prefer using existing fixtures and helpers rather than introducing inline test data.

For full workspace guidance, see [../../CLAUDE.md](../../CLAUDE.md).
