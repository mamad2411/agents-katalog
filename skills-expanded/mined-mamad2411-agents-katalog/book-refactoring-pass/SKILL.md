---
name: book-refactoring-pass
description: Guides behavior-preserving refactoring with small, reversible steps. In strict tasks, mandatory before the first implementation edit to existing production code; in default/lite tasks, use on demand when structural friction, duplication, long functions, tangled responsibilities, unsafe cleanup, or explicit delivery requirements affect the change.
---

# Book Refactoring Pass

Use this Skill as a focused refactoring check before or during implementation.

It is derived from the `mini` rule style of `agent-rules-books`. It is a strict development gate for existing-production-code edits and an on-demand engineering lens in other structural-risk scenarios; it does not replace project rules, tests, task artifacts, source/LSP/contract impact analysis, or code review.

## Strict Development Gate

Whenever a strict task will modify existing production code, run this Skill before the first implementation edit to existing production code, even when the expected result is that no refactoring is needed.

Emit a separate visible review:

```text
Refactoring Review
Status: proceed | refactor-first | blocked
Review mode: normal | safety-seam-only
Existing-code scope: ...
Behavior that must remain unchanged: ...
Structural friction: ...
Decision and smallest safe step: ...
Safety net and validation: ...
Deferred refactors: ...
```

- `proceed`: in normal mode, the existing structure is safe enough for the requested edit; `no refactor needed` is a valid explicit conclusion.
- `refactor-first`: perform only the smallest behavior-preserving structural change allowed by the current review mode, validate it, and rerun the required gate before feature or fix edits.
- `blocked`: required behavior evidence, a safety net plan, or the Skill is unavailable; state the blocker and do not edit production behavior.

If `book-legacy-change-safety` is also mandatory, its review normally reaches `characterized` before this gate runs. Controlled exception: a legacy `seam-required` result may invoke this Skill in `safety-seam-only` mode. That mode may design and implement only the recorded behavior-preserving test seam, must validate observational equivalence, and must return to legacy review to establish the safety net. After legacy reaches `characterized`, rerun this Skill in normal mode before feature / fix edits.

## When To Use

- Strict: every development task that modifies existing production code. In default/lite, use this Skill when structural risk, project rules, or explicit delivery requirements apply.
- Existing code structure is making a requested change risky or awkward.
- A change mixes behavior changes with cleanup.
- Duplication, long functions, feature envy, primitive obsession, or tangled responsibilities are blocking clarity.
- A review needs to decide whether a refactor should happen now or be deferred.

When existing production code will not be modified, do not use this Skill for simple text, docs, config-only edits, broad rewrites, speculative architecture changes, or code that is already easy to change safely unless the user explicitly requests the review or another concrete structural risk warrants it.

## Workflow

1. Identify the observable behavior that must remain unchanged.
2. Confirm the available safety net: tests, characterization checks, manual repro, snapshots, or focused inspection.
3. Separate structural refactoring from behavior changes.
4. Prefer the smallest reversible move that lowers the current task risk.
5. Preserve public contracts unless the task explicitly changes them.
6. In `safety-seam-only` mode, reject feature behavior, bug-fix behavior, broad cleanup, or any structural change not required by the recorded test seam.
7. Run the project validation appropriate to the touched code.

## Output

Always emit the visible `Refactoring Review` for a strict gate. When used in a task-level record, also write only task-specific conclusions to `implement.md`, `design.md`, or the check summary:

- Current friction.
- Behavior that must not change.
- Proposed refactoring steps or explicit `no refactor needed`.
- Safety net and validation command.
- Deferred refactors, if any.

Only long-term conventions belong in `docs/spec`.

## Stop Conditions

Stop refactoring when the requested change is safe and clear enough. The mandatory review does not require a refactor; never invent cleanup merely to produce `refactor-first`, and do not keep improving code outside the task boundary.
