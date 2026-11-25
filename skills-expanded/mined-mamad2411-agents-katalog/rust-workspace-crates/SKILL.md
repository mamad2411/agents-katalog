---
name: rust-workspace-crates
description: Design and refactor Rust projects into a Cargo workspace with reusable crates under `crates/*`. Use when a Rust codebase has a growing `src/` tree, overlapping domain logic, mixed runtime/framework/business concerns, multiple binaries, or repeated helpers that should be extracted into focused internal crates. Useful for planning crate boundaries, choosing what stays in the root app crate, designing one-way dependencies, adding thin compatibility facades during migrations, and reviewing an existing `crates/*` layout for back-edges or over-coupling.
---

# Rust Workspace Crates

Use this skill to turn a growing Rust app into a workspace with a thin runtime shell and focused crates under `crates/*`.

## Quick Start

1. Inspect `Cargo.toml`, `[workspace].members`, root `src/`, existing binaries, and `crates/*`.
2. Classify code into portable domain logic, transport adapters, orchestration/workers, runtime/bootstrap shell, and incubation.
3. Sketch a dependency DAG before moving files. Keep dependencies one-way and prefer many leaves with few aggregators.
4. Extract lower-level crates first. When a lower crate needs runtime I/O, define a trait in the lower crate and implement it in the upper runtime crate.
5. Keep env/config loading, router wiring, global app state, framework middleware, and process bootstrap in the root app or dedicated runtime crate.
6. Leave thin compatibility facades at old paths during migrations when that reduces churn.

## Crate Taxonomy

- `foundation` crates: query builders, contracts, error types, planners, state machines, worker loops, schema helpers. Keep them free of web frameworks and app-state types.
- `adapter` crates: reusable transport or protocol layers that normalize requests, responses, payloads, or backend-specific semantics.
- `feature` crates: bounded business domains with storage logic and runtime traits.
- `runtime` crates: binaries or app shells that wire config, pools, routers, job spawning, and trait implementations.
- `incubation` crates: extracted code that lives under `crates/*` but is not yet an active workspace member. Mark this status explicitly instead of implying it is fully integrated.

## Boundary Rules

- Move framework-agnostic DTOs, services, planners, builders, retry loops, worker loops, and SQL helpers into `crates/<domain>`.
- Put runtime ports in the lower crate:
  - traits for pools, HTTP clients, registries, event sinks, audit sinks, row writers, or lookup services
- Implement those traits in the upper runtime crate.
- Avoid reverse edges from extracted crates back into the root crate. If an extracted crate imports the root app crate, treat that as partial extraction and document the debt.
- Avoid a crate per folder. Create a new crate only when the boundary is meaningful, reusable, or needed to control dependency direction.
- Keep compatibility modules thin. They should re-export or forward, not rebuild the moved logic.

## Extraction Workflow

1. Find seams with repeated logic, long modules, independent worker loops, portable query code, or transport-agnostic contracts.
2. Choose the first leaf crate. Prefer code with few upstream dependencies and no framework state.
3. Move that code into `crates/<name>/src/lib.rs` and submodules.
4. Replace direct runtime access with traits when needed.
5. Re-export through old root paths only if that reduces migration churn.
6. Add the crate to `[workspace].members` only when it is active.
7. Run focused crate checks first, then workspace checks.

## Dependency Heuristics

- Good:
  - `foundation -> foundation`
  - `adapter -> foundation`
  - `feature -> foundation/adapter`
  - `runtime -> everything it wires`
- Risky:
  - sibling crates calling back up into a binary or root crate
  - lower crates importing a global registry or app-state type
  - crates under `crates/*` without a clear active-vs-incubating status
  - extracted crates that still mix route handlers, bootstrap, and domain logic

## Validation

- Run `cargo metadata --format-version 1` and inspect workspace members.
- Run `cargo check -p <crate>` for touched crates and the runtime shell.
- Use `cargo tree -p <crate> --edges normal` or equivalent to spot back-edges and accidental heavy dependencies.
- Verify the root crate still owns config/env loading, router wiring, and process startup.
- Verify extracted crates can be understood from their `src/lib.rs` and `Cargo.toml` alone.

## Reference

Read [references/crate-patterns.md](references/crate-patterns.md) when you need a fuller taxonomy, a suggested file tree, a migration checklist, or anti-pattern examples.
