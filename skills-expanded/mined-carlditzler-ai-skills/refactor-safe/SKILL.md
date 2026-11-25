---
name: refactor-safe
description: Use for behavior-preserving refactors in Swift, Kotlin, Flutter, Tauri, Rust, or frontend code when the goal is better structure, clarity, ownership, or maintainability without intentionally changing product behavior.
---

# Refactor Safe

## Use when
- the user wants cleanup, extraction, reorganization, renaming, or modularization without product changes
- the code structure is slowing down future work but the visible behavior should stay the same
- a risky area needs characterization tests before or during a refactor

## Do not use when
- the main job is adding new behavior
- the requested change depends on a broad rewrite rather than a behavior-preserving refactor

## Working rules
- Preserve behavior first.
- Keep refactor work separate from feature work whenever possible.
- Add or verify characterization tests when confidence is low.
- Refactor in small mechanical steps that can be validated quickly.
- Do not rewrite stable code just to match personal taste.

## Workflow
1. State what is being improved and what behavior must remain unchanged.
2. Identify the tests and validations that protect the current behavior.
3. Make the smallest structural moves first.
4. Re-run focused validation after each risky stage.
5. Summarize the structural improvement and preserved behavior clearly.

## Quality bar
- Public contracts, storage formats, and serialized payloads stay stable unless the change explicitly includes them.
- Observability and useful tests should not get weaker after the refactor.
- The codebase should be easier to ship, not only prettier.

## Reference routing
- Read `references/refactor-checklist.md` for safe refactor steps.
- Read `references/release-quality-gates.md` when the refactor touches release-critical paths or contracts.
- Read `references/official-docs.md` only when a platform-specific rule affects the safe shape of the refactor.

## Output contract
Provide:
- behavior preserved
- structural changes made
- validation run
- whether the refactor is release-neutral, needs extra validation, or is not ready
