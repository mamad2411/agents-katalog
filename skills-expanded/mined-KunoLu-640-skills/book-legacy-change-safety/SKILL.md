---
name: book-legacy-change-safety
description: Guides safe changes to legacy or weakly tested code by characterizing behavior before editing. In strict tasks, mandatory before the first behavior-changing edit for existing-behavior bug fixes or existing code with unclear behavior, low coverage, hidden dependencies, or high regression risk; in default/lite tasks, use on demand when those risks or explicit delivery requirements are present.
---

# Book Legacy Change Safety

Use this Skill when the main risk is not the requested change itself, but the uncertainty around existing behavior.

It is derived from the `mini` rule style of `agent-rules-books` and is intended to complement `diagnosing-bugs`, `tdd`, source/LSP/contract impact analysis, and project validation.

## Strict Development Gate

In a strict task, run this Skill before the first behavior-changing edit when either condition is true:

- The task fixes a bug in existing observable behavior.
- Existing target code has weak / missing tests, unclear or undocumented behavior, hidden dependencies, or high regression risk.

Emit a separate visible review:

```text
Legacy Change Safety Review
Status: characterized | needs-safety-net | seam-required | blocked
Behavior to change: ...
Behavior to preserve: ...
Current reproduction evidence: ...
Safety net: ...
Hidden dependencies / seam: ...
Validation plan: ...
Review mode: normal | safety-seam-only
```

- `characterized`: current behavior was reproduced or otherwise established, preserved behavior is explicit, and an adequate safety net exists.
- `needs-safety-net`: the safety net can be added without production-code edits; add or select the smallest characterization / regression check, then rerun this Skill.
- `seam-required`: current and preserved behavior are established, but the safety net cannot be installed without a production seam. Record the exact seam scope, invoke `book-refactoring-pass` in `safety-seam-only` mode, implement and validate only that behavior-preserving seam, then return here to establish the safety net and reach `characterized`.
- `blocked`: current behavior, required dependencies, the Skill, or a safe reproduction path is unavailable; state the blocker and do not change behavior.

When `book-refactoring-pass` is also mandatory, this gate normally reaches `characterized` first. `seam-required` is the only exception and authorizes no feature / fix behavior or unrelated cleanup.

## When To Use

- Strict: every existing-behavior bug fix and every existing-code change matching a listed uncertainty or regression-risk signal. In default/lite, use this Skill when those signals, project rules, or explicit delivery requirements apply.
- The target code has weak or missing tests.
- The current behavior is unclear, accidental, or undocumented.
- Dependencies are hidden behind globals, singletons, network calls, files, time, randomness, or external services.
- A bug fix could change behavior that other callers rely on.

When neither mandatory condition matches, do not use this Skill for cleanly tested new code, docs-only work, or simple isolated edits with obvious behavior and low blast radius unless the user requests it or another concrete legacy risk warrants it.

## Workflow

1. State the exact behavior to change.
2. State the behavior that must be preserved.
3. Reproduce the current behavior before editing.
4. Add the smallest useful safety net, such as a characterization test, focused unit test, integration check, or manual script. If this requires a production seam, emit `seam-required` before editing.
5. Introduce a seam only through the `safety-seam-only` loop above, then rerun this Skill and complete the safety net.
6. Make the smallest behavior change that satisfies the task only after `characterized`.
7. Run focused tests first, then the project validation required by the changed area.

## Output

Always emit the visible `Legacy Change Safety Review` for a strict gate. When used in a task-level record, also record:

- Current observed behavior.
- Preserved behavior.
- Added or chosen safety net.
- Dependency seam, if introduced.
- Validation command and result.

If a lesson is learned because a regression, tool mistake, or workflow error occurred, use `lessons-record`; otherwise do not create a lesson.

## Guardrails

Do not rewrite legacy code just to make it nicer. Stabilize first, change second, improve only where the current task needs it; a mandatory review may conclude `characterized` without introducing a new seam when the existing safety net is sufficient.
