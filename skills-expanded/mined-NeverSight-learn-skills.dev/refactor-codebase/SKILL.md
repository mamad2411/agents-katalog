---
name: refactor-codebase
description: Incrementally refactor and rearchitect a codebase toward a scalable structure using a phased plan. Use when the user wants to restructure code, improve architecture, reduce coupling, reorganize modules, or migrate toward a cleaner design without breaking the working system.
---

# Refactor Codebase

Restructure a codebase incrementally toward a scalable architecture. Never attempt the full restructure in one go — always produce a phased plan first and execute one phase at a time.

## Quick Start

1. Explore the current codebase structure.
2. Write a refactor PRD describing the target architecture.
3. Use `/prd-to-plan` to break the PRD into phased vertical slices.
4. Execute one phase at a time, verifying the system still works after each.

## Workflow

### 1. Audit the current structure

Before proposing anything, read the codebase to understand:

- Folder layout and module boundaries
- Coupling hotspots (files imported everywhere, god classes/modules)
- Naming inconsistencies and mixed responsibilities
- Existing test coverage (indicates refactor risk)
- Build/lint/test tooling in use

Ask the user: what pain are you trying to fix? (slow builds, hard to navigate, hard to extend, team scaling, etc.)

### 2. Define the target architecture

Write a short **Refactor PRD** in `./plans/refactor-prd.md` covering:

- **Problem**: what is wrong with the current structure
- **Goals**: what the restructured codebase should achieve
- **Target structure**: a rough folder/module diagram of the end state
- **Out of scope**: what will NOT be touched
- **Constraints**: must stay green (tests pass), no feature changes, incremental only

> Do NOT skip this step. A vague goal produces a vague plan.

### 3. Generate a phased plan with `/prd-to-plan`

Invoke `/prd-to-plan` with the refactor PRD. Each phase must be:

- A thin vertical slice (one concern at a time — e.g. "move auth module", "extract shared utils", "flatten nested routes")
- Independently verifiable (run tests, lint, or build after each phase)
- Safe to stop after (no half-migrated state left behind)

Each phase in the plan should include:

- **What moves / changes**: specific files or folders in scope
- **Migration strategy**: copy-then-delete, re-export shim, codemods, etc.
- **Verification step**: the command to run to confirm nothing broke

### 4. Execute one phase at a time

For each phase:

1. Read every file in scope before touching anything.
2. Make the structural change (move, rename, extract, inline).
3. Update all imports — use codemod tooling if available (e.g. `ts-morph`, `jscodeshift`, `sed`).
4. Run the verification step (tests, build, lint).
5. Commit with a message referencing the phase (e.g. `refactor: phase 1 – extract auth module`).
6. Report back to the user before starting the next phase.

> Stop between phases. Do not chain phases together without user confirmation.

### 5. Update the plan as you go

After each phase, mark it complete in the plan file and note any surprises (files that were harder to move than expected, new dependencies discovered). This keeps the plan accurate for the next session.

## Guardrails

- Never change behavior during a structural refactor. If a bug is spotted, note it — do not fix it in the same commit.
- Do not rename things as part of a move. Move first, rename in a separate phase.
- If the codebase has no tests, flag this before starting. Suggest adding a smoke-test or integration test as Phase 0.
- If a phase would require touching more than ~20 files, split it further.
- Preserve git history where possible — prefer `git mv` over delete + create.

## References

- See [REFERENCE.md](REFERENCE.md) for common architecture patterns and migration strategies by language/framework.
