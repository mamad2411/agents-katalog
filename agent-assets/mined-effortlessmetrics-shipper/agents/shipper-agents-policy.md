# AGENTS.md

Use this file with [CLAUDE.md](./CLAUDE.md) before making changes in this directory.

# runtime/policy

Publish policy evaluation logic — derives effective safety/verify/readiness flags from `PublishPolicy` + explicit overrides.

Absorbed from the former `shipper-policy` microcrate (Phase 2 decrating) and now lives as a crate-private module within `shipper-core`.

## API surface (crate-private)

- `PolicyKind` — runtime-agnostic policy enum (`Safe` / `Balanced` / `Fast`).
- `PolicyEffects` — derived booleans: `run_dry_run`, `check_ownership`, `strict_ownership`, `readiness_enabled`.
- `evaluate(kind, no_verify, skip_ownership, strict_ownership, readiness_enabled) -> PolicyEffects` — pure, no-I/O.
- `apply_policy(&RuntimeOptions) -> PolicyEffects` — convenience for the full options struct.
- `policy_effects(&RuntimeOptions)` — back-compat alias for `apply_policy`, consumed by `crate::engine`.

## Invariants

- `Safe`  — conservative passthrough: all flags honored.
- `Balanced` — ownership checks always disabled; dry-run/readiness honored.
- `Fast`  — constant `false` across every output field (ignores all inputs).
- Monotonic: `count(Safe) >= count(Balanced) >= count(Fast)` for any given flag set.

## Layer discipline

This module lives in `crate::runtime::*` (Layer 2). It must remain:

- Pure data + pure functions (no I/O, no orchestration).
- Free of imports from `crate::engine::*`, `crate::plan::*`, `crate::state::*`.
- Visible only within the `shipper-core` crate (`pub(crate)`).

See [`../CLAUDE.md`](../CLAUDE.md) for full layer rules.

