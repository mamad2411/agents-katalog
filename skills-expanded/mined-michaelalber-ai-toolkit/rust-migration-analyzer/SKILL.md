---
name: rust-migration-analyzer
audience: team
description: >
  Analyzes Rust migration paths: C/C++ to Rust rewrites via incremental FFI strangler fig, and
  Rust modernization (edition upgrades 2015->2018->2021->2024, deprecated-crate replacement, sync to
  async). Assesses risk, quantifies effort, and produces a phased plan — does NOT perform the
  migration. Use when migrating C/C++ to Rust, upgrading editions, modernizing legacy Rust,
  replacing deprecated crates, or planning sync-to-async. Not when you want to execute the
  migration (assessment only), or the codebase is already current stable Rust with no legacy.
---

# Rust Migration Analyzer

> "The best migration is the one that never happens. The second best is the one that is incremental, reversible, and tested at every step."
> -- Migration Principle

> "Rust's FFI is the seam. Rewrite module by module, behind a C ABI, with tests on both sides."
> -- C/C++ to Rust Migration Principle

## Core Philosophy

Rust migration analysis covers two distinct contexts:

**Context A: C/C++ → Rust Rewrite**
The FFI boundary is the migration seam. The strangler fig pattern applies: rewrite one module at a time, expose it through a C ABI, and let the C/C++ codebase call the Rust implementation. The C/C++ side does not know it is calling Rust. Tests run against the C/C++ behavior before rewriting; the same tests run against the Rust implementation after. When all modules are rewritten, the C/C++ wrapper is removed.

**Context B: Rust Modernization**
Edition upgrades (2015→2018→2021→2024) are largely mechanical — `cargo fix --edition` handles most of the work. Crate replacements require API compatibility analysis. Sync-to-async migration requires introducing a Tokio runtime and converting function signatures throughout the call chain.

This skill assesses, quantifies risk, and produces a phased migration plan. It does NOT perform the migration. The plan produced by this skill is the input to the implementation phase.

**Non-Negotiable Constraints:**

1. **Assess before plan** — understand the full scope before recommending a migration path. A partial assessment produces a partial plan.
2. **Characterization tests before rewriting** — for C/C++ rewrites, characterization tests against the existing behavior must exist before any Rust code is written.
3. **Incremental migration only** — no big-bang rewrites. Every migration step must be independently deployable and reversible.
4. **FFI safety is explicit** — every `extern "C"` boundary must be documented with the invariants that make it safe.
5. **Edition upgrades are mechanical** — `cargo fix --edition` handles most of the work. Manual intervention is required only for the cases it cannot handle.

The 10 domain principles, the knowledge-base lookup map, and the anti-pattern catalog live in
`references/assessment-principles.md`. The AI discipline rules (assess-before-recommend,
characterization-tests-first, incremental-only) and error-recovery procedures live in
`references/discipline-and-recovery.md`.

## Workflow

```
SCAN (understand the current state)
    [ ] Identify migration context: C/C++ rewrite OR Rust modernization
    [ ] Count lines of code by category (pure Rust, unsafe, FFI, tests)
    [ ] Run: cargo outdated (for Rust modernization)
    [ ] Run: cargo audit (for Rust modernization)
    [ ] Run: grep -rn "unsafe\|extern" src/ (for FFI analysis)
    [ ] Measure test coverage: cargo tarpaulin or cargo llvm-cov
    [ ] Identify Rust edition (for modernization)
    [ ] Identify async runtime (for async migration)

        |
        v

ASSESS (risk scoring)
    [ ] Score each migration scenario by: Effort, Risk, Blocker potential
        (scoring dimensions + per-scenario detail: references/migration-risk-matrix.md)
    [ ] Identify dependencies between migration steps
    [ ] Identify the critical path
    [ ] Identify quick wins (low effort, high value)

        |
        v

PLAN (phased migration)
    [ ] Define migration phases in dependency order
    [ ] For each phase: scope, effort estimate, risk, success criteria
    [ ] Define rollback plan for each phase
    [ ] Identify test requirements for each phase
    [ ] For C/C++ rewrites, ground FFI mechanics in references/ffi-patterns.md

        |
        v

REPORT  (templates: references/output-templates.md)
    [ ] Risk matrix (scenarios × dimensions)
    [ ] Migration phase plan
    [ ] FFI boundary inventory (for C/C++ rewrites)
    [ ] Dependency update plan (for Rust modernization)
    [ ] Recommended tooling
```

**Exit criteria:** Risk matrix produced; phased migration plan delivered; FFI inventory complete (if applicable).

## State Block

```
<rust-migration-state>
phase: SCAN | ASSESS | PLAN | REPORT | COMPLETE
migration_context: c_cpp_rewrite | rust_modernization | both | unknown
rust_edition: 2015 | 2018 | 2021 | 2024 | unknown
async_runtime: tokio | async-std | none | unknown
loc_total: [N]
loc_unsafe: [N]
loc_ffi: [N]
test_coverage: [percentage | unknown]
cargo_audit_status: clean | N CVEs | not-run
cargo_outdated_count: [N | not-run]
ffi_boundary_count: [N]
migration_phases_planned: [N]
last_action: [description]
next_action: [description]
</rust-migration-state>
```

## Output Template

The REPORT phase delivers up to four artifacts, with fill-in Markdown templates in
`references/output-templates.md`:

- **Risk Matrix** — every migration scenario scored by Effort, Risk, Blocker Potential, and Recommended Order.
- **Migration Phase Plan** — phases in dependency order, each with scope, effort, risk, prerequisites, success criteria, rollback, and tools.
- **FFI Boundary Inventory** (C/C++ rewrites) — every `extern "C"` function with direction, invariants, risk, and migration priority.
- **Dependency Update Plan** (Rust modernization) — `cargo outdated` / `cargo audit` findings with a per-crate replacement order.

## Integration with Other Skills

| Skill | Relationship |
|-------|-------------|
| `rust-architecture-checklist` | After migration, run `rust-architecture-checklist` to verify the migrated code follows Rust idioms. |
| `rust-security-review` | After migration, run `rust-security-review` to verify the migrated code is secure. |
| `sqlx-migration-manager` | If the migration includes database schema changes, use `sqlx-migration-manager` for the database migration lifecycle. |
| `legacy-migration-analyzer` | Parallel skill for .NET Framework → .NET 10 migrations. Same assessment philosophy; different ecosystem. |
| `supply-chain-audit` | When `cargo audit` finds CVEs during the assessment, `supply-chain-audit` provides deeper analysis. |
