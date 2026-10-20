# AGENTS.md

Use this file with [CLAUDE.md](./CLAUDE.md) before making changes in this directory.

# Layer: `state` (persistence)

**Position in the architecture:** Layer 3. Above `runtime/` and `ops/`, below `plan/` and `engine/`.

## Single responsibility

Persist execution state, events, and receipts to disk (or other backends via the `StorageBackend` trait in `ops/storage/`). Provides resumable execution by reloading state.

## Import rules

`state` modules MAY import from `crate::runtime::*`, `crate::ops::*`, `crate::types`, external crates.
`state` modules MUST NOT import from `crate::engine::*` or `crate::plan::*`.
Enforced by `.github/workflows/architecture-guard.yml`.

## What lives here

- `state/execution_state/` — `ExecutionState`, receipt persistence, schema migration, and atomic filesystem I/O (was `shipper-state`)
- `state/events/` — Append-only JSONL event log (was `shipper-events`)
- `state/store/` — `StateStore` trait + filesystem impl (was `shipper-store`)

