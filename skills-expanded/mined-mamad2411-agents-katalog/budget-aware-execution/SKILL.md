# Budget Aware Execution

## When To Use

Use this skill when the workflow is consuming turns quickly, the remaining budget is visibly low, or the task has already entered a loop of exploratory actions without new evidence.

Use it for:

- hover or reveal workflows that can spiral into repeated attempts
- long transactional tasks near turn budget
- sessions where the next few actions must be chosen carefully

Do not use it as the default mode for every task.
Do not use it to justify early abandonment when there is still enough budget for normal execution.

## Procedure

1. Pause and restate the smallest remaining success target.
2. Stop exploratory actions that are not producing new evidence.
3. Prefer one verification-rich action over multiple speculative actions.
4. Batch reading and note-taking before the next mutation where possible.
5. If the task cannot reasonably complete within the remaining budget, preserve the best partial state and report what remains.
6. Treat the final turns as a controlled recovery window, not as a place for blind retries.

## Required Evidence

- Current turn budget or clear evidence that the workflow is near budget exhaustion
- Most recent verified page state
- The exact remaining sub-goal

## Common Failures

- Continuing normal exploratory behavior even after repeated non-progressing turns
- Spending the final turns on retries with no new information
- Calling `done` without explaining what remains unfinished

## Verification

- Prefer deterministic checks that confirm whether the remaining goal is already satisfied.
- If incomplete, report the narrowest unresolved step rather than claiming broad failure.

## Relevance

This skill is intended for harness-wide execution discipline, especially in workflows that can waste turns through repeated attempts.

Current strongest evidence:

- `tests/e2e/hover-menus.test.ts` or equivalent hover-menu pathologies

Additional candidate targets:

- any `max_turns` trace with repeated exploratory actions
- future transactional or cart flows that spiral near budget exhaustion
