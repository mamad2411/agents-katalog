---
name: execution-engine
description: Use when implementing an approved plan or a scoped engineering task in Codex.
---

# Execution Engine

Implement in small, verifiable slices.

## Loop

1. Read the files that own the behavior.
2. Update the visible plan if there are multiple steps.
3. Make the smallest clean patch.
4. Run the focused check for that slice.
5. Integrate with neighboring code.
6. Run broader checks proportional to risk.
7. Perform a skeptic pass before handoff.

## Patch Discipline

- Prefer existing patterns, helpers, tokens, schemas, and tests.
- Do not refactor unrelated code.
- Do not revert user changes.
- Add comments only where they prevent real confusion.
- Use structured parsers/APIs over ad hoc string manipulation when available.

## Progress Discipline

- Keep at most one plan step in progress.
- If discovery changes the plan, update the plan rather than forcing the old one.
- When blocked, try the cheapest alternate route before handing back.

## Done Criteria

- Original request behavior is addressed.
- Focused verification ran or is explicitly blocked.
- Related edge cases were considered.
- Final response lists not-run checks honestly.

