---
name: generic-code-quality
description: Apply when writing, reviewing, or refactoring code in any language across the repo. Enforces file size limits, separation of concerns, SOLID, comment discipline, control flow, and red flags that demand immediate refactoring.
metadata:
  stack: [generic]
---

# Code Quality Standards

Language-agnostic standards. React/TypeScript examples are illustrative; the principles apply to C#, JS, TS, Python, anything.

## Comments

Default: **no comments**. Well-named identifiers carry the WHAT.

- **No design narrative in code.** If rationale, architecture, trade-offs, or invariants live in `docs/design/<feature>.md` or `docs/requirements/`, do not duplicate as code headers or doc-comments. Link from the design doc to the code, not the other way around.
- **Do not reference tasks, gates, PRs, requirement IDs, or task history** in code (no "Gate 5 wires…", "PoC: deferred until…", "see UR-IDV-013"). That belongs in commit messages, design docs, or decision logs (`memory/decisions.md`).
- **Keep only WHY comments**, and only when the WHY is non-obvious AND not captured nearby in a design doc: hidden constraints, subtle invariants, workarounds for specific bugs, platform quirks that would surprise a reader. One short line is almost always enough.
- Before writing a comment, ask: would removing this confuse a future reader who has read the relevant design doc? If no, don't write it.

## Control flow

- **Early returns (guard clauses)** over nested `if/else`.
- Handle simple / default case first → return → main logic at top indentation.
- A method/function with three levels of nesting almost always has a missed guard.

## Test discipline

Existing tests are the project's behavioural memory. Don't edit them because you happen to be in the file. The right action depends on the work type:

| Work type | What to do with tests |
|---|---|
| **New feature** | Write **new** tests only. Add to existing test files or create new ones. **Do not modify** existing tests. If a new test seems to conflict with an existing one, the existing test is probably wrong — flag it, don't silently rewrite it. |
| **Bug fix** | Write a **new** test that reproduces the bug. Modify an existing test only if it was insufficient (i.e. it *should* have caught this bug but didn't). When modifying, document why in the commit message — that's the audit trail of "we strengthened this test because it missed bug X." |
| **Changing an existing feature** | Modify the **existing** tests for that feature. This is the only case where editing existing tests is the primary action. New tests welcome for newly-added paths. |
| **Refactoring** | Tests should not change at all. If a refactor requires test changes, it's not a refactor — it's a behavioural change. Stop, reclassify, and follow the appropriate row. |

### Anti-patterns

- **Editing an unrelated test "while you're in there"** to make it pass after your change. Either your change broke it (revert and reconsider) or the test was already wrong (flag separately, fix in its own commit).
- **Loosening an existing assertion** (`expect(x).toBe(5)` → `expect(x).toBeGreaterThan(0)`) to make it pass. Tighten or rewrite deliberately; never loosen to chase green.
- **Removing a test because "it's now redundant"** without a clear duplication. Tests catch regressions; over-keeping is safer than over-pruning.
- **Renaming a test to match new behaviour.** If the behaviour changed, the test is now wrong on its assertions — fix those, don't just rename.
- **Adding `[Skip]` / `.skip` / `.only` to a flaky existing test** to keep CI green for the current PR. Flaky tests get fixed or quarantined with a dated TODO, not silently muted.

## File Size Limits

| Type | Target | Maximum |
|------|--------|---------|
| Components | 150-200 lines | 300 lines |
| Hooks | 150-200 lines | 300 lines |
| Utilities | 150-200 lines | 300 lines |

**If approaching limit**: Split into smaller, focused modules using composition.

## Separation of Concerns

Each module should have ONE clear responsibility:

### Components
- **Presentation**: Render UI based on props
- **Container**: Orchestrate data and state for children
- **Layout**: Handle positioning and structure

### Hooks
- **State management**: One domain of state
- **Data fetching**: One data source
- **Side effects**: One category of effects
- **Event handlers**: One category of events

### Utilities
- **Pure functions**: No side effects
- **Single purpose**: One transformation or calculation

## SOLID Principles

- **Single Responsibility**: Each function/component does ONE thing
- **Open/Closed**: Can extend without modifying existing code
- **Dependency Inversion**: Depend on abstractions (types/interfaces)

## React Best Practices

- **No prop drilling**: Use composition or context for props beyond 2 levels
- **Memoization**: Use `useMemo`/`useCallback` for expensive operations only
- **Type safety**: All props/returns properly typed (no `any`)
- **Error boundaries**: Wrap risky components where appropriate
- **Loading states**: Clear indicators for async operations

## File Organization

Place code in the correct location:

| Type | Location |
|------|----------|
| Shared hooks | `packages/hooks/` |
| Shared utilities | `packages/utils/` |
| Shared UI components | `packages/ui/` |
| App-specific hooks | `<frontend-app>/hooks/` or feature folder |
| App-specific utils | `<frontend-app>/lib/utils/` |
| App-specific components | `<frontend-app>/components/` or feature folder |
| Feature-specific code | Feature folder (co-located) |

## Code Duplication

- Extract patterns repeated 2+ times
- Place shared code in appropriate location:
  - `packages/utils/` - Pure utility functions
  - `packages/hooks/` - Shared React hooks
  - `packages/ui/` - Shared UI components
  - Feature folder - Feature-specific shared code

## Red Flags (Refactor Immediately)

- File exceeds 200 lines
- Function/hook has multiple responsibilities
- Code duplicated 2+ times
- Complex nested logic (>3 levels deep)
- Component has >5 props that aren't variants/handlers
- Prop drilling beyond 2 levels

## Package-Specific Patterns

Refer to package CLAUDE.md files for detailed patterns:
- `packages/ui/CLAUDE.md` - Component patterns, CVA, shadcn/ui
- `packages/hooks/CLAUDE.md` - Hook development patterns
- `packages/utils/CLAUDE.md` - Utility function patterns

## Before Presenting Code

1. Check file line count
2. Verify single responsibility
3. Scan for duplication
4. Review nesting depth
5. Confirm all types are explicit (no `any`)
