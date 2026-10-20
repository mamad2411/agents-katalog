# Transactional Act Check Act

## When To Use

Use this skill when the task requires a state-changing action, an intermediate check that the state actually changed, and only then a follow-up action.

Use it for workflows with an explicit act -> verify -> continue structure.

Do not use it as a generic fallback for every difficult task.
Do not use it for pure read-only research, broad open-ended navigation, or single-step actions that do not require an intermediate check.

## Procedure

1. Ground the current page and identify the target control and the expected state transition.
2. Resolve blockers such as modals or overlays before acting.
3. Perform exactly one state-changing action.
4. Re-ground the page immediately after that action.
5. Verify the expected state transition occurred.
6. Only after verification, perform the next action.
7. Repeat until the final success criteria are satisfied.

## Required Evidence

- Pre-action page state
- Post-action page state
- Evidence that the expected transition actually occurred

## Common Failures

- Combining multiple mutations before checking the first result
- Continuing after a click without confirming the page changed
- Using stale element assumptions after modals or navigation
- Treating this as a catch-all "hard task" skill instead of a specific transactional pattern

## Verification

- Prefer deterministic checks for text, visibility, button state, URL, or title changes.
- Use LLM verification only when the state change is visually obvious but not structurally easy to assert.

## Relevance

This skill is intended for real confirm-gated browser workflows such as account actions, settings changes, and status transitions.

Current strongest E2E target:

- `tests/e2e/continuation-act-check-act.test.ts`

Additional candidate targets:

- `tests/e2e/continuation-verify.test.ts`
- `tests/e2e/support-ticket.test.ts`
