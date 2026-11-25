---
name: harness-maintain
description: Orchestrate the MAINTAIN phase — understand the codebase (if unfamiliar) then safely remove dead code, duplication, and tech debt. Use after shipping or on an accumulating codebase. Sequences /onboard and /refactor-clean, delegates to the harness-claude:refactor-cleaner agent, and halts before ambiguous deletions.
---

# /harness-maintain — run the Maintain phase

Thin orchestrator over the Maintain skills. Behavior-preserving by default.

## Sequence

1. **`/harness-claude:onboard`** — **only if** the codebase is unfamiliar or you've been away from it.
   Build a lean codemap (structure, entry points, conventions, where things live) so
   cleanup is safe. If you already know the codebase, **skip** and say so.

2. **`/harness-claude:refactor-clean`** — **delegate to the `harness-claude:refactor-cleaner` agent**:
   - Find candidates with analyzers (knip/depcheck/ts-prune/ruff/vulture) or the graph.
   - **Confirm truly unused before deleting** (all references, dynamic usage).
   - Consolidate duplication (DRY); split files >800 lines by responsibility.
   - Small reversible steps; run tests/build after each.

3. **Ambiguity gate:** if a deletion or consolidation is non-obvious or could change
   behavior, **HALT** — report it and let the user decide. When a "cleanup" turns into a
   redesign, route to `/harness-claude:architect` instead.

## Rules
- Behavior-preserving only. No feature/API changes unless asked.
- Never delete something you didn't confirm unused.
- Keep diffs reviewable. Do not run git write operations.

## Output
What was removed/consolidated (with reference checks), what was deliberately left, and
confirmation tests/build still pass.
