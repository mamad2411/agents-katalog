---
name: rust-contract-spine
description: Clean up Rust codebases, plan safe refactors, eliminate contract drift, and implement a contract-spine authority chain across Cargo workspace crates. Use when the user asks to clean up Rust code, reduce duplication, plan a refactor, fix drift between CLI/config/API/DTO layers, design crate boundaries, consolidate parallel types, or build a single source-of-truth contract layer. Triggers on rust cleanup, workspace hygiene, contract spine, refactor plan, drift audit, dead code, duplicate DTOs, clap defaults drift, crate extraction. Use when the user runs /rust-contract-spine.
---

# Rust Contract Spine

## Goal

Turn a messy or drifting Rust workspace into a maintainable layout with one downward-flowing **contract spine**: shared types, errors, and validation live in low crates; runtime, CLI, HTTP, and SDK layers derive or translate explicitly instead of redefining contracts.

Use this skill for audits and planning as well as implementation. Ship alignment plus guardrails when fixing drift.

## Quick Start

1. Read `Cargo.toml`, `[workspace].members`, `crates/*`, root `src/`, binaries, and feature flags.
2. Pick the seam the user named (command, route, DTO family, config key, error code, crate boundary).
3. Map the current contract spine — or the absence of one.
4. Classify findings: duplicate, dead, duplicate+drift, boundary violation, missing guardrail.
5. Produce a phased refactor plan before large moves.
6. Fix authority first, align dependents, add CI or compile-time proof last.

## Modes

Choose one primary mode per request. Combine only when the user explicitly wants audit + fix.

| Mode | When | Deliverable |
|------|------|-------------|
| **Audit** | "what's wrong", "find drift", "cleanup report" | Ranked findings + contract matrix + phased plan |
| **Plan** | "how should we refactor", "design crate boundaries" | Dependency DAG + migration phases + exit criteria |
| **Spine** | "implement contract spine", greenfield or extraction | New or consolidated contract crate + translation boundaries |
| **Fix** | named seam is broken or duplicated | Authority change + downstream alignment + guardrail |

## Contract Spine Rules

- **One authority per contract family.** CLI args, config structs, HTTP bodies, DB rows, SDK types, and test fixtures must not each own independent truth unless semantics truly differ.
- **Flow downward.** `contract -> feature/adapter -> runtime/cli`. Lower crates never import runtime app state, routers, or global registries.
- **Explicit translation.** When layers differ on purpose (e.g. CLI flattening vs JSON nesting), name the mapper and document the boundary — do not call it drift.
- **Runtime shell stays thin.** Env loading, router wiring, worker spawn, and trait implementations live high; defaults and public shapes live on the spine.
- **Delete projections.** Remove intermediate structs that only mirror another contract with no added semantics.

Read [references/contract-spine.md](references/contract-spine.md) for spine anatomy, crate roles, and anti-patterns.

## Investigation Workflow

### 1. Establish the live seam

- Start from the entrypoint the user cares about: binary `main`, handler, clap command, public crate API.
- Trace imports and callers with `rg` before labeling anything dead.
- Confirm active workspace members vs incubating `crates/*` trees.

```powershell
cargo metadata --format-version 1
rg -n "struct|enum|#\[arg" crates/ src/
cargo tree -p <crate> --edges normal
```

### 2. Build the contract matrix

For each contract family:

| Column | Content |
|--------|---------|
| Contract | What callers think exists |
| Authority | Where it should live on the spine |
| Observed | What code/runtime actually does |
| Dependents | CLI, config, HTTP, storage, SDK, tests, docs, generated files |
| Drift class | shape, naming, behavioral, default-value, validation, ownership |
| Fix direction | consolidate, translate, regenerate, or delete |

### 3. Cluster duplicate and dead code

- Group by **behavior seam**, not single utility matches.
- `Duplicate + drift` outranks plain duplication.
- Mark **dead** only after import tracing and runtime seams agree.

For ranked cleanup reports with line counts and blame, also load `$audit-duplicate-dead-code`.

### 4. Sketch the target DAG

Before moving files:

- Classify: foundation (contracts), adapter, feature, runtime, incubation.
- Draw one-way edges. Flag back-edges from extracted crates into root as debt.
- Prefer many leaves, few aggregators.

For workspace extraction mechanics, also load `$rust-workspace-crates`.

### 5. Plan phases

Read [references/refactor-phases.md](references/refactor-phases.md). Default sequence:

1. **Inventory** — matrix + clusters, no code moves
2. **Spine bootstrap** — create or designate contract crate; move stable types/errors first
3. **Align surfaces** — CLI, config, HTTP, storage consume spine types or explicit mappers
4. **Prune** — delete dead trees and mirror structs
5. **Guard** — tests, `cargo check` matrix, generation checks, clippy/fmt gates

Each phase needs exit criteria before the next starts.

## Rust Drift Hotspots

Check these on every audit:

- **Parallel DTO families** — `FooRequest`, `FooInput`, `FooBody` with identical fields
- **Clap vs config defaults** — `#[arg(default)]`, env loader, and README disagree
- **Serde shape drift** — `rename`, `skip_serializing`, untagged enums copied inconsistently
- **Error code duplication** — `thiserror` in multiple crates for the same failure
- **Feature-flag leakage** — `cfg` gates hiding different public APIs per crate
- **Test fixture drift** — helpers building shapes that no longer match production types

For cross-surface drift taxonomy and guardrails, also load `$reduce-contract-drift`.

## Fix Order

1. Fix the highest-authority artifact (spine type, schema, clap definition, migration).
2. Regenerate or re-derive dependents (OpenAPI, SDK, catalog JSON).
3. Replace duplicated intermediate types with imports or thin mappers.
4. Add at least one durable guardrail:
   - seam-level integration test
   - `trybuild` / compile-fail test
   - generation diff check in CI
   - shared defaults helper used by CLI and config

## Default Deliverables

### Audit / plan request

- Contract seam and authority recommendation
- Contract matrix (or top N families)
- Ranked findings with evidence paths
- Phased refactor plan with exit criteria per phase
- Optional tracker-ready issue titles

### Fix / spine request

- Authority-side implementation
- Downstream alignment in touched crates
- Validation or CI guardrail
- `cargo check -p <crate>` for each touched crate, then workspace check

## Validation Commands

Run after every implementation phase:

```powershell
cargo fmt --all -- --check
cargo clippy --all-targets -- -D warnings
cargo check -p <touched-crate>
cargo test -p <touched-crate>
cargo tree -p <touched-crate> --edges normal
```

Adjust flags for the repo's CI (`--locked`, feature sets). Match the project's existing workflow.

## Reference Map

- [references/contract-spine.md](references/contract-spine.md) — spine layers, crate taxonomy, translation boundaries
- [references/refactor-phases.md](references/refactor-phases.md) — phased migration template and exit criteria
- [references/cleanup-checklist.md](references/cleanup-checklist.md) — Rust-specific audit checklist

## Related Skills

- `$rust-workspace-crates` — crate extraction and workspace layout
- `$reduce-contract-drift` — drift taxonomy and guardrails across surfaces
- `$audit-duplicate-dead-code` — quantified duplicate/dead cluster reports
- `$repo-audit-reporting` — formal audit writeups with provenance