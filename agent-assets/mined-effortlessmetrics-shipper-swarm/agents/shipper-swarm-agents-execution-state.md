# AGENTS.md

Use this file with [CLAUDE.md](./CLAUDE.md) before making changes in this directory.

# Module: `crate::state::execution_state`

**Layer:** state (layer 3)
**Single responsibility:** Persist `ExecutionState` and `Receipt` to disk (atomic write, durable rename, schema-versioned migration).
**Was:** standalone crate `shipper-state` (physically absorbed in PR #60 shim +
physical move)

## Public-to-crate API

- Schema version constants: `CURRENT_RECEIPT_VERSION`, `MINIMUM_SUPPORTED_VERSION`, `CURRENT_STATE_VERSION`, `CURRENT_PLAN_VERSION`
- File name constants: `STATE_FILE`, `RECEIPT_FILE`
- Path helpers: `state_path()`, `receipt_path()`
- Plaintext I/O: `load_state`, `save_state`, `clear_state`, `has_incomplete_state`, `load_receipt`, `write_receipt`, `fsync_parent_dir`
- Encrypted I/O: `load_state_encrypted`, `save_state_encrypted`, `load_receipt_encrypted`, `write_receipt_encrypted`
- Migration: `validate_receipt_version`, `migrate_receipt`

## Status

Physically absorbed: the full implementation lives in `mod.rs` (production
code) and `tests.rs` (unit + snapshot tests, including two nested proptest
modules). Snapshots live in `snapshots/`. Integration tests moved to
`crates/shipper/tests/state_integration.rs`. The standalone `shipper-state`
crate has been deleted from the workspace.

## Invariants

- Writes are atomic: write to a `.tmp` sibling, fsync, then rename.
- Forward-compatible schema: unknown receipt versions are still deserialised best-effort.
- v1 → v2 migration fills missing `git_context` (null) and `environment` fields and rewrites `receipt_version`.

