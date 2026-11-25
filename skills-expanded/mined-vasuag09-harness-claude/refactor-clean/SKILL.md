---
name: refactor-clean
description: Remove dead code, duplication, and tech debt safely during the Maintain phase. Use after shipping, or when a codebase has accumulated cruft. Delegates to the harness-claude:refactor-cleaner agent. Behavior-preserving only.
---

# /refactor-clean — safe cleanup

Goal: a leaner, more modular codebase without changing behavior.

## Do this
1. **Delegate to `harness-claude:refactor-cleaner`**, or inline:
2. Find candidates with analyzers when present (knip/depcheck/ts-prune/ruff/vulture),
   else `mgrep`/graph (or `Grep`/`Glob` if those are unavailable): unused exports/imports/files, dead branches, duplicated logic,
   stray debug code, oversized files (>800 lines).
3. **Confirm truly unused** before deleting — check all references, including dynamic
   usage. When unsure, leave it and report.
4. Consolidate duplication into one well-named utility; split oversized files by
   responsibility. Small, reversible steps; run tests/build after each.

## Constraints
Behavior-preserving. No feature/API changes unless asked. Keep diffs reviewable; if a
cleanup turns into a redesign, stop and route to `/harness-claude:architect`.

## Exit criterion
Cruft removed with reference checks, tests/build still green, change documented.
