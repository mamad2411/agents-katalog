---
name: sui-move-guide
description: Route Sui Move engineering tasks to the smallest applicable skill sequence. Use when a developer asks which Sui Move standard applies, wants help routing a Move task, or wants the complete Sui Move development flow.
---

# Sui Move Guide

Route the task to the smallest set of Sui Move skills that covers the risk. This skill is an explicit catalog, not a coding standard by itself.

## Skills

- `$sui-move-architecture`: package boundaries, module responsibilities, minimal state, canonical authority, dependency direction, on-chain scope, abilities, capabilities, and cross-package seams.
- `$sui-move-source-style`: module and function names, file sections, imports, visibility, `self` receiver naming, receiver syntax, direct UID access, pinned framework functions and macros, parameter and local discipline, API vocabulary, docs, and test-only seams.
- `$sui-move-security`: fail-fast ordering, authorization, signed actions, replay, bounded work, arithmetic, custody, external seams, time, oracles, randomness, pause, versioning, and upgrades.
- `$sui-move-events-errors`: completed-fact events, minimal payloads, native metadata, replay schemas, identity, ordering, wrapper/emitter architecture, stable error registries, abort ownership, and compatibility.
- `$sui-move-testing`: risk-based tests, exact failures, guard precedence, stateful hot-potato fixtures, property tests, event replay, dependency verification, and release gates.
- `$sui-move-patterns`: selection and application of reusable designs for misplaced cross-package logic, ephemeral authorization proofs, sealed adapter handoffs, deferred fungibility receipts, and emergency shared-state replacement.
- `$sui-move-review`: one full audit across all five standards.

## Common routes

### Design a new package or major feature

1. Run `$sui-move-architecture` before defining public ABI or storage.
2. Run `$sui-move-security` before settling authority, lifecycle, or economic transitions.
3. Apply `$sui-move-source-style` while writing modules.
4. Apply `$sui-move-events-errors` when defining transition diagnostics and indexing ABI.
5. Apply `$sui-move-testing` before implementation is complete.
6. Finish with `$sui-move-review`.

### Change an existing state transition

Apply `$sui-move-security`, `$sui-move-source-style`, and `$sui-move-testing`. Add `$sui-move-events-errors` when event, error, guard precedence, or replay behavior can change. Add `$sui-move-architecture` when state ownership, authority, abilities, visibility, or package boundaries can change.

### Add or change a module, type, or public API

Apply `$sui-move-architecture` and `$sui-move-source-style`. Add
`$sui-move-security` for any authority, asset, lifecycle, or shared-state type.
For published code, preserve existing function signatures and datatype layouts;
the focused skills own permitted constraint relaxation and state migration.

### Upgrade a package or migrate state

Apply `$sui-move-architecture`, `$sui-move-security`,
`$sui-move-source-style`, and `$sui-move-testing`. Add
`$sui-move-events-errors` when indexed behavior can change. Treat published ABI
and old-version reachability as compatibility constraints; the focused skills
own the detailed upgrade, migration, dependency, and test rules.

### Add events or errors

Apply `$sui-move-events-errors`, then `$sui-move-testing`. Add `$sui-move-security` when the diagnostic change exposes a new guard, authorization check, or economic transition.

### Audit redundancy or simplify Move code

Apply `$sui-move-architecture` to storage and public seams. Apply
`$sui-move-events-errors` to whole events and payload fields. Apply
`$sui-move-source-style` to parameters, helpers, and locals. Use
`$sui-move-testing` before removing a fact or seam, and add
`$sui-move-security` when simplification can change guards, authority, assets,
or evaluation order.

### Build or repair tests

Apply `$sui-move-testing`. Also apply the skill that owns the behavior under test; tests must prove the rule, not invent it.

### Select, compare, or apply a reusable pattern

Apply `$sui-move-patterns` when the task explicitly asks for a named pattern,
compares reusable implementation shapes, or matches one of its promoted design
problems. Then apply the focused skills that own the selected pattern's
architecture, security, source, event, and testing invariants. Do not load the
patterns skill for ordinary standards work that does not require pattern
selection.

### Review a branch or pull request

Use `$sui-move-review`. It loads all five standards and reports findings by severity.

## Routing rule

When uncertain, include security and testing. Do not load every skill for a narrow naming question, and do not treat source style as a substitute for architecture or security.
