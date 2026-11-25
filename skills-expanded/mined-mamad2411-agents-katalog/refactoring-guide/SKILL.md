---
name: refactoring-guide
description: SOTA refactoring and modularization principles that LLMs systematically miss. Covers language-agnostic principles plus.
allowed-tools: Read, Grep, Glob, Bash, Edit, Write
---

# Refactoring Guide

Principles that LLMs consistently get wrong during refactoring. This skill corrects systematic blind spots around coupling analysis, type-level design, module boundaries, and safe migration strategies.

The core problem: LLMs optimize for what code _looks like_ (structural similarity), but good modularization optimizes for how code _changes together_ (temporal cohesion). Every principle here addresses that gap.

> **Self-Evolving Skill**: This skill improves through use. If instructions are wrong, parameters drifted, or a workaround was needed — fix this file immediately, don't defer. Only update for real, reproducible issues.

## When to Use

- **Refactoring tasks**: Extract module, split file, reduce coupling, reorganize
- **Code review**: Spot smells and suggest the right fix (not the superficial one)
- **Architecture decisions**: Module boundaries, dependency direction, integration points
- **Proactively**: When you detect any signal from the Detection Heuristics table below

## Workflow

When refactoring, follow this sequence:

1. **Detect** — Scan the code against the Detection Heuristics table. Identify which smells are present.
2. **Diagnose** — For each smell, read the corresponding reference file to understand the correct principle.
3. **Plan** — Design the refactoring using the right technique. For multi-file changes (>3 files), use the Mikado Method (see `references/architecture.md`).
4. **Execute** — Apply changes. For shared interfaces, use expand-contract (see `references/tactical-moves.md`).
5. **Verify** — Confirm the refactoring reduced the specific coupling type identified in step 1.

## Detection Heuristics

Scan for these signals to identify which principle to apply:

| Signal                                                        | Likely Smell             | Principle                                        | Reference                   |
| ------------------------------------------------------------- | ------------------------ | ------------------------------------------------ | --------------------------- |
| Same group of parameters passed to 3+ functions               | Data clump               | Parse, don't validate — extract parameter object | `type-design.md` §1         |
| Method uses more of another class's fields than its own       | Feature envy             | Move method to where data lives                  | `module-boundaries.md`      |
| `if isinstance` / type switch with >2 branches                | Missing polymorphism     | Replace conditional with polymorphism            | `type-design.md` §2         |
| Import cycle between modules                                  | Acyclic violation        | Extract shared or invert dependency              | `module-boundaries.md` §2   |
| Boolean parameter on public API                               | Flag argument            | Split into separate methods or use enum          | `tactical-moves.md` §5      |
| `# TODO: remove after migration` older than 3 months          | Dead code                | Delete it now                                    | `tactical-moves.md` §1      |
| Function has both `return` and side effects (db/file/network) | Mixed concerns           | Functional core, imperative shell                | `architecture.md` §1        |
| Test requires mocking >3 dependencies                         | Over-coupling            | Missing a seam — identify and create one         | `structural-coupling.md` §1 |
| Changing one feature touches >3 directories                   | Wrong slicing            | Package by feature, not layer                    | `module-boundaries.md` §1   |
| Two modules that always change in the same PR                 | Under-modularized        | Common closure — merge them                      | `module-boundaries.md` §3   |
| One module changes for unrelated reasons                      | Divergent change         | Split by reason-for-change                       | `structural-coupling.md` §4 |
| One logical change touches 5+ files                           | Shotgun surgery          | Merge the scattered concern                      | `structural-coupling.md` §4 |
| `init()` must be called before `process()`                    | Temporal coupling        | Type-state pattern                               | `type-design.md` §4         |
| External API types used deep in business logic                | Leaked integration       | Anti-corruption layer at boundary                | `architecture.md` §2        |
| Same struct mutated in 3+ different modules                   | Unclear data ownership   | Designate owning module for each data type       | `structural-coupling.md` §5 |
| Vendor SDK types used in core logic                           | Volatility leak          | Wrap behind narrow stable interface              | `structural-coupling.md` §6 |
| Module exposes setters instead of operations                  | Undefended invariants    | Expose intention-revealing operations            | `module-boundaries.md` §5   |
| Infrastructure exceptions surface in business logic           | Error leakage            | Translate errors at module boundary              | `module-boundaries.md` §6   |
| Pass-through layer with no logic (just forwards calls)        | Fake modularity          | Remove unnecessary indirection                   | `tactical-moves.md` §9      |
| Module named `utils`, `common`, `helpers`, `shared`           | Dumping ground           | Split by actual consumer clusters                | `module-boundaries.md` §4   |
| Domain logic inside controllers, handlers, or jobs            | Misplaced business logic | Extract to domain module                         | `architecture.md` §1        |
| Services scattered across modules constructing own deps       | Missing composition root | Centralize wiring at app entry point             | `architecture.md` §5        |
| God service that coordinates AND decides everything           | Mixed orchestration      | Separate orchestration from computation          | `architecture.md` §1        |

## Principle Summary

Each principle is covered in detail in `references/`. Read the relevant file when you encounter its smell.

### Structural Coupling (`references/structural-coupling.md`)

1. **Seam identification** — Find natural seams before extracting; don't cut across them
2. **Connascence spectrum** — Coupling has 9 strength levels; refactor toward weaker forms
3. **Stability metrics** — Depend in the direction of stability (lower instability)
4. **Divergent change vs. shotgun surgery** — Opposites requiring opposite fixes; don't confuse them
5. **Data ownership** — Every data structure has one owning module; others read via contracts, never mutate
6. **Volatility isolation** — Wrap high-churn dependencies behind narrow stable interfaces

### Type-Level Design (`references/type-design.md`)

1. **Parse, don't validate** — Parse at boundaries into typed results; never pass raw input downstream
2. **Make illegal states unrepresentable** — Discriminated unions over boolean/optional fields
3. **Newtype / branded types** — Wrap primitives with distinct types to prevent semantic confusion
4. **Temporal coupling → type-state** — Return new types that expose only currently-valid methods

### Architecture (`references/architecture.md`)

1. **Functional core, imperative shell** — Pure functions for decisions, thin IO shell for effects
2. **Anti-corruption layer** — Translate external models at integration boundaries
3. **Strangler fig** — Incremental migration, never big-bang rewrites
4. **Mikado method** — For large refactors: try, record failures, revert, work bottom-up
5. **Composition root** — All wiring at one entry point, not scattered through modules

### Module Boundaries (`references/module-boundaries.md`)

1. **Package by feature, not layer** — Vertical slicing keeps feature changes local
2. **Acyclic dependencies** — Module graph must be a DAG
3. **Common closure** — Group by reason-for-change, not technical similarity
4. **Interface segregation** — Don't force consumers to depend on unused exports
5. **Invariant enforcement** — Modules defend their own invariants; expose operations, not setters
6. **Error boundary translation** — Each module translates errors to its own domain vocabulary

### Tactical Moves (`references/tactical-moves.md`)

1. **Deletion as refactoring** — Best refactoring often has negative line count
2. **Rule of three** — Wait for three instances before abstracting
3. **Inline then re-extract** — Flatten confused code first, then re-decompose cleanly
4. **Expand-contract** — For shared interfaces: add new alongside old, migrate, remove old
5. **Boolean parameter prohibition** — Split or use enum instead
6. **Configuration as explicit dependency** — Pass config, don't import globally
7. **Characterization tests first** — Pin behavior before refactoring
8. **Conway's law alignment** — Module boundaries should match team boundaries
9. **Over-modularization check** — Boundary must improve change isolation, not just organize files
10. **Module documentation template** — For each module: responsibility, ownership, dependencies, invariants, error model

### Rust-Specific (`references/rust-specific.md`)

Read when refactoring Rust codebases. Covers visibility as architecture, public API surface control, crate vs. module boundaries, Cargo features, workspace feature unification, and dependency policy tooling.

### Swift/macOS-Specific (`references/swift-macos-specific.md`)

Read when refactoring Swift codebases on macOS. Covers access control as architecture (`package` modifier), explicit import visibility (SE-0409), target/framework boundary selection, macro isolation, and API governance tooling.

## Post-Execution Reflection

After this skill completes, check before closing:

1. **Did the command succeed?** — If not, fix the instruction or error table that caused the failure.
2. **Did parameters or output change?** — If the underlying tool's interface drifted, update Usage examples and Parameters table to match.
3. **Was a workaround needed?** — If you had to improvise (different flags, extra steps), update this SKILL.md so the next invocation doesn't need the same workaround.

Only update if the issue is real and reproducible — not speculative.
