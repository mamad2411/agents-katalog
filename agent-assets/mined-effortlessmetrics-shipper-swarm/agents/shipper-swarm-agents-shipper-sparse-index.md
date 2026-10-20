# AGENTS.md

Use this file with [CLAUDE.md](./CLAUDE.md) before making changes in this directory.

This file provides agent-specific guidance for working in crate shipper-sparse-index.

## Scope

- Crate: shipper-sparse-index
- Path: crates/shipper-sparse-index
- Workspace root: repository root for the current checkout; use repo-relative paths from this file
- Primary entry: src/lib.rs

## Useful commands

```bash
cargo check -p shipper-sparse-index
cargo test -p shipper-sparse-index
cargo test -p shipper-sparse-index --all-features
cargo fmt -p shipper-sparse-index
cargo clippy -p shipper-sparse-index --all-targets --all-features -- -D warnings
```

## Context

- Keep changes small and targeted to the crate’s existing abstractions.
- Preserve public API compatibility unless the request explicitly asks for breaking changes.
- When touching serialization or state formats, update tests and related snapshots in the same crate.
- Prefer using existing fixtures and helpers rather than introducing inline test data.

For full workspace guidance, see [../../CLAUDE.md](../../CLAUDE.md).
