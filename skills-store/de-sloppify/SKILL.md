---
name: de-sloppify
description: >
  Systematic code cleanup pipeline for .NET projects. Runs 7 ordered steps:
  formatting, unused usings, analyzer warnings, dead code removal, TODO resolution,
  sealed class audit, and CancellationToken propagation. Each step is verified
  independently with tests between phases. Load this skill when: "clean up",
  "de-sloppify", "tidy up", "remove dead code", "code cleanup", "housekeeping",
  "tech debt", "fix warnings", "seal classes", "add CancellationToken",
  "unused usings", "format code".
---

# /de-sloppify — 7-Step Cleanup Pipeline

## What

Runs an ordered, verified cleanup pipeline over a .NET codebase. Order matters:
formatting first (it touches every file — get the churn out of the way before
anything else), dead code late (earlier steps reveal it). Random cleanup misses
things and creates merge conflicts; the pipeline doesn't.

Three rules make it safe:

1. **Verify after each step** — `dotnet build` + `dotnet test` between steps. A
   cleanup that breaks something is worse than the mess it was fixing.
2. **Commit per step** — each step is its own commit, so a bad Step 4 reverts
   without losing Steps 1-3.
3. **Safe removals only** — before deleting "dead" code, check for reflection,
   DI-convention, and serialization usage that Roslyn cannot see.

Per-step commands, safety checklists, and code examples live in
`references/cleanup-steps.md` — read it before executing.

## When

- "Clean up", "tidy up", "de-sloppify", "housekeeping", "tech debt"
- After a large feature merge or dependency upgrade (new warnings accumulate)
- Pre-release hardening, or a scheduled quarterly cleanup sprint
- Before performance work (dead code out, classes sealed for devirtualization)
- Never mixed with feature work — cleanup commits stay pure

## How

### Step 0: Pick the Steps

| Scenario | Steps to run |
|----------|-------------|
| Full cleanup pass / pre-release / quarterly | All 7 |
| Quick tidy before PR | 1, 2, 6 |
| After large feature merge | 1, 2, 3, 4 |
| After dependency upgrade | 2, 3 |
| Before performance work | 4, 6 |
| CI warning threshold exceeded | 3 only |
| Tech debt sprint | 4, 5 |

### Steps 1-7 (execute in order, details in references/cleanup-steps.md)

| # | Step | Tool | Commit message |
|---|------|------|----------------|
| 1 | Format all code | `dotnet format` | `chore: apply dotnet format` |
| 2 | Remove unused usings | `dotnet format analyzers --diagnostics IDE0005` | `chore: remove unused using statements` |
| 3 | Fix analyzer warnings | MCP `get_diagnostics` → triage by category | `chore: fix analyzer warnings` |
| 4 | Remove dead code | MCP `find_dead_code` + **safety check** (reflection/DI/serialization grep) | `chore: remove dead code` |
| 5 | Resolve TODOs | grep TODO/HACK/FIXME → fix, file issue, or delete | `chore: resolve TODO comments` |
| 6 | Seal non-inherited classes | MCP `get_type_hierarchy` per candidate + test-project grep | `chore: seal non-inherited classes` |
| 7 | Propagate CancellationToken | MCP `detect_antipatterns` → trace async chains | `chore: propagate CancellationToken through async chains` |

After every step: `dotnet build` + `dotnet test`, then commit. If a step breaks
the build or tests, fix or revert that step before continuing — never carry a
red state into the next step. Delegate structural steps (4, 6, 7) to the
`refactor-cleaner` agent.

### Final Report

```markdown
## De-Sloppify Report

| Step | Changes | Files Affected |
|------|---------|----------------|
| 1. Format | Applied consistent formatting | 23 files |
| 2. Usings | Removed 47 unused usings | 18 files |
| 3. Analyzers | Fixed 12 warnings (8 nullability, 3 unused vars, 1 obsolete) | 9 files |
| 4. Dead Code | Removed 3 unused types, 5 unused methods | 6 files |
| 5. TODOs | Fixed 2, created issues for 3, removed 1 stale | 5 files |
| 6. Sealed | Sealed 14 classes | 14 files |
| 7. CancellationToken | Added propagation to 8 async chains | 11 files |

**Total: 7 commits, 86 files improved**
```

## Example

```
User: /de-sloppify — full pass before the release

Claude: Running the 7-step pipeline...

Step 1: dotnet format — 23 files reformatted. Build + tests green. Committed.
Step 2: IDE0005 — 47 unused usings removed across 18 files. Green. Committed.
Step 3: 12 warnings triaged: 8 nullability fixed with null checks,
  3 unused vars removed, 1 CS0618 migrated off the obsolete API. Committed.
Step 4: find_dead_code → 9 candidates. Safety check: PaymentProcessor is
  registered via DI convention — kept. Removed 3 types, 5 methods. Committed.
Step 5: 6 TODOs → 2 fixed, 3 became issues (#141-#143), 1 stale removed. Committed.
Step 6: 14 classes sealed (2 skipped: xUnit fixture base, virtual members). Committed.
Step 7: 8 async chains now propagate ct end-to-end. Committed.

7 commits, 86 files improved. Full report above.
```

## Related

- `references/cleanup-steps.md` — per-step commands, safety checks, examples
- `/verify` — run the full verification pipeline after cleanup
- `/health-check` — re-grade the project to quantify the improvement
- `/code-review` — cleanup handles style; review handles logic and design
