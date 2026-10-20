# Layer: `plan` (planning algorithms)

**Position in the architecture:** Layer 4. Above `state/`, `runtime/`, `ops/`, below `engine/`.

## Single responsibility

Build a deterministic, topologically-ordered publish plan from the workspace metadata. Filter publishable crates, sort by dependency graph, group into parallel-eligible levels.

## Import rules

`plan` modules MAY import from `crate::state::*`, `crate::runtime::*`, `crate::ops::*`, `crate::types`, external crates.
`plan` modules MUST NOT import from `crate::engine::*`.
Enforced by `.github/workflows/architecture-guard.yml`.

## What lives here

- `plan/` (top-level files: `mod.rs`, plus split sub-files) — main planning logic (was `shipper-plan`)
- `plan/levels/` — Wave grouping for parallel publish (was `shipper-levels`)
- `plan/chunking/` — Plan chunking for large workspaces (was `shipper-chunking`)
