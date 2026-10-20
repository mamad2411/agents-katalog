# AGENTS.md

Use this file with [CLAUDE.md](./CLAUDE.md) before making changes in this directory.

# Layer: `ops` (I/O primitives)

**Position in the architecture:** Layer 1 (bottom). The lowest layer of the `shipper-core` crate.

## Single responsibility

Talk to the outside world: filesystem, git binary, cargo subprocess, OS, network.

## Import rules

`ops` modules MUST NOT import from any higher layer:
- ❌ `use crate::engine::...`
- ❌ `use crate::plan::...`
- ❌ `use crate::state::...`
- ❌ `use crate::runtime::...`

`ops` modules MAY import from:
- ✅ `crate::types` (re-exports of `shipper-types`)
- ✅ External crates (`anyhow`, `serde`, `tokio`, etc.)
- ✅ Other `crate::ops::*` modules (with care — prefer `mod.rs` facades over deep paths)

These are enforced by `.github/workflows/architecture-guard.yml`.

## What lives here

Each absorbed I/O microcrate gets its own folder under `ops/`:

- `ops/auth/` — Cargo registry token resolution (was `shipper-auth`)
- `ops/git/` — Git cleanliness checks, context capture (was `shipper-git`)
- `ops/lock/` — Advisory file lock (was `shipper-lock`)
- `ops/process/` — Cross-platform command execution (was `shipper-process`)
- `ops/cargo/` — Cargo metadata + cargo publish invocation (was `shipper-cargo`)
- `ops/storage/` — Storage backend trait + filesystem impl (was `shipper-storage`)

## What does NOT live here

- `shipper-registry`, `shipper-webhook`, `shipper-sparse-index` — these are public crates that `shipper-core` depends on directly. No internal wrapper inside `ops/`.
- Domain types — those live in `shipper-types`.
- Orchestration — that's `engine/`.

## Boundary discipline

- Each subfolder has its own `mod.rs` facade. Other modules talk through the facade, not by reaching into deep paths.
- Default visibility: `pub(crate)`. Only items truly part of `shipper-core`'s public API get `pub`.
- Each subfolder has its own local guidance files (`CLAUDE.md` and matching `AGENTS.md`) describing its single responsibility.

