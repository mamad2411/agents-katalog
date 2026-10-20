# AGENTS.md

Use this file with [CLAUDE.md](./CLAUDE.md) before making changes in this directory.

# Module: `crate::state::store`

**Layer:** state (layer 3)
**Single responsibility:** `StateStore` trait + filesystem-backed implementation. Pluggable persistence backend for execution state, events, and receipts.
**Was:** standalone crate `shipper-store` (absorbed in Phase 2 decrating).

## Layout

- `mod.rs` — the `StateStore` trait, `validate_schema_version`, and module wiring.
- `fs.rs` — the `FileStore` type + `impl StateStore for FileStore`.
- `tests.rs` — unit, behavior, and proptest coverage.
- `snapshot_tests.rs` — `insta` snapshot tests for persisted JSON/JSONL formats.
- `path_edge_case_tests.rs` — unicode/spaces/emoji/nested path coverage.

## Public-to-crate API

- `StateStore` — persistence trait (save/load/clear for state, receipt, events; schema validation).
- `FileStore` — filesystem-backed impl (writes atomically under the configured state dir).
- `validate_schema_version` — free function for validating receipt/state/plan schema version strings.

## Public path (backcompat)

For historical compatibility, the module is still reachable as `shipper::store::*`
via a `#[path]` attribute in `crates/shipper/src/lib.rs`. The physical layout
lives under `state/store/` to match the layered architecture (layer 3: state).

When the events+state absorption PR lands, a `state/mod.rs` exists and can
expose `pub(crate) mod store;` to make `crate::state::store` usable internally.
The public `shipper::store` re-export stays either way.

## Invariants

- Trait stays as a trait — has multiple impls (filesystem, future cloud, mock for tests).
- Filesystem impl writes atomically via temp file + rename (see `crate::state::save_state`).
- Tests exercise corrupt/truncated/empty-JSON inputs — load must never panic.
- Snapshots live under `crates/shipper/src/snapshots/shipper__state__store__snapshot_tests__*.snap`.

