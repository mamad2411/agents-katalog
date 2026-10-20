# AGENTS.md

Use this file with [CLAUDE.md](./CLAUDE.md) before making changes in this directory.

# Module: `crate::runtime::execution`

**Layer:** runtime (layer 2)
**Single responsibility:** Shared execution primitives — backoff, error classification, package keys, state update locks.
**Was:** standalone crate `shipper-execution-core` (absorbed into the layered runtime module layout during the decrating effort).

## Public-to-crate API

- `backoff_delay`
- `classify_cargo_failure`
- `pkg_key`
- `update_state_locked`
- `resolve_state_dir`
- `short_state`

`update_state` remains public only as a hidden, deprecated compatibility shim
for legacy callers. New publish code MUST use the event-first engine
transition boundary; this shim writes `state.json` without an event and is not
an authoritative transition API. Its retirement is tracked by issue #153.

## Invariants

- Pure functions where possible.
- `update_state_locked`: caller must hold the appropriate lock before calling.
- `update_state`: legacy compatibility only; it mutates in-memory state, then persists without an event. Callers must tolerate the case where the in-memory mutation occurs even if the persist fails (known behavior, covered by tests). New code must not call it.

## Internal microcrate dependencies (transitional)

This module currently imports from `crate::state::execution_state`,
`shipper_retry`, `shipper_types`, and `shipper_cargo_failure`. As each of the
remaining microcrates is absorbed in subsequent PRs, these imports will be
rewritten to `crate::*` paths.
