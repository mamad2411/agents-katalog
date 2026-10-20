# AGENTS.md

Use this file with [CLAUDE.md](./CLAUDE.md) before making changes in this directory.

# Module: `crate::state::events`

**Layer:** state (layer 3)
**Single responsibility:** Append-only JSONL event log for publish operations.
**Was:** standalone crate `shipper-events` (physically absorbed in PR #60 shim +
physical move)

## Public-to-crate API

- `EventLog` — in-memory append-only event log
- `EVENTS_FILE` — canonical event file name (`events.jsonl`)
- `events_path(state_dir)` — helper to build `<state_dir>/events.jsonl`

## Status

Physically absorbed: the full implementation lives in `mod.rs` (production
code), `tests.rs` (unit + snapshot tests), and `proptests.rs` (property-based
tests). Snapshots live in `snapshots/`. The standalone `shipper-events` crate
has been deleted from the workspace.

## Invariants

- Append-only: events are never deleted or reordered.
- One event per JSON object per line.
- File format is forward-compatible — readers ignore unknown event types.

