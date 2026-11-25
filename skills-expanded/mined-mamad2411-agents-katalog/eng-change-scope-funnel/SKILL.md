---
name: eng-change-scope-funnel
description: Narrow the true change surface before editing through keyword search, call-chain tracing, and blast-radius analysis, producing a whitelist of files to modify. Use between planning and execution, or before any risky change, to prevent collateral edits.
---

# Change Scope Funnel

A pre-edit discipline that converts a broad task description into an explicit, evidence-backed whitelist of files allowed to change. Everything outside the whitelist is off-limits without restarting the funnel.

## Why: The Collateral Edit Problem

Unscoped edits drift into neighboring code: renamed symbols break callers, shared utilities get reshaped for one consumer, config tweaks leak across environments. The funnel makes the change surface explicit before the first edit lands.

## Four-Stage Funnel Procedure

```
Stage F1: Keyword Net (broad)
    grep/glob for task keywords, symbol names, error strings, config keys
           │  output: candidate file set C1
           ▼
Stage F2: Call-Chain Trace (directional)
    for each candidate entry point: who calls it, what it calls,
    which routes/tests/configs reference it
           │  output: dependency-closed set C2
           ▼
Stage F3: Blast Radius Classification
    for each file in C2: DIRECT (must change) / ADJACENT
    (may need signature updates) / SAFE-TOUCH-NOT
           │  output: classified set C3
           ▼
Stage F4: Whitelist Contract
    emit the final table; execution may modify only DIRECT +
    explicitly promoted ADJACENT files
```

---

## Whitelist Contract Template

```markdown
# Change Scope Whitelist: <task>

| File | Class | Reason | Expected Change Size |
|---|---|---|---|
| `src/services/order.ts` | DIRECT | Core logic per plan Task 2 | ~40 lines |
| `src/services/__tests__/order.test.ts` | DIRECT | Regression coverage | new cases |
| `src/api/routes.ts` | ADJACENT | Only if signature changes | watch-list |

**Out of scope (must not change)**: <explicit list>
**Funnel evidence**: search patterns used, trace depth, total candidates considered
```

## Integration Rules

- **eng-plan**: Run the funnel during Phase 2 (Codebase Intelligence) to ground the plan's file list in evidence.
- **eng-execute**: Treat the whitelist as a hard boundary. A required edit outside the whitelist halts execution and re-runs stages F2 to F4 with the new information.
- **eng-refactor-lifecycle**: Mandatory before each strangler phase to keep steps small.
- **eng-hotfix-emergency-lifecycle**: Compressed single-pass funnel; still produces the whitelist before touching code.

## Anti-Patterns This Gate Blocks

- Editing a shared utility for one consumer without tracing other callers.
- Renaming/moving files not referenced by any plan task.
- Config changes beyond the environment named in the task.
- Drive-by refactors riding along an unrelated fix.

## Checkable Completion Criteria

- [ ] Candidate set built from real search commands with recorded patterns.
- [ ] Every whitelisted file carries a class, reason, and expected size.
- [ ] Out-of-scope list is explicit.
- [ ] Execution stayed inside the whitelist; any escape triggered a documented re-funnel.