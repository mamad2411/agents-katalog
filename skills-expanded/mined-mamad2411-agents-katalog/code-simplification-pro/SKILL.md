---
name: code-simplification-pro
description: Simplify code by reducing accidental complexity, removing dead abstractions, clarifying boundaries, and improving readability without changing behavior. Use for cleanup, refactoring, large files, confusing modules, over-engineered code, and maintainability improvements.
---

# Code Simplification Pro

## Workflow

1. Identify the behavior that must stay unchanged.
2. Find complexity source: duplication, indirection, mixed responsibilities, dead paths, unclear names, or premature abstraction.
3. Make the smallest simplification that preserves behavior.
4. Prefer deleting code over adding abstraction when possible.
5. Verify behavior with tests, typecheck, or targeted manual checks.
6. Record refactor candidates or technical debt if cleanup is incomplete.

## Simplification Rules

- Respect Chesterton's Fence: understand why code exists before removing it.
- Do not combine simplification with feature changes unless necessary.
- Keep public APIs stable unless migration is in scope.
- Reduce cleverness when clarity is cheaper.

## Output

State what was simplified, behavior preserved, verification, and any remaining refactor candidate.
