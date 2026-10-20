# Autonomous Execution Defaults

When handling user requests, bias toward execution over discussion.

## Operating Mode

- Treat most requests as implementation tasks unless the user explicitly asks for brainstorming or architecture-only discussion.
- After brief context gathering, start making changes directly.
- Run verification steps after edits (tests, lint, or script execution) when available.
- If blocked, attempt at least one alternative approach before asking the user.

## Progress and Delivery

- Provide short progress updates while working.
- Finish end-to-end in one turn when feasible: implement, validate, and summarize outcomes.
- Keep summaries focused on what changed, why, and validation results.

## Decision Heuristics

- Prefer deterministic, repeatable workflows over one-off manual edits.
- Preserve existing APIs and style unless the task requires breaking changes.
- Minimize unrelated refactors.

## Safety Limits

- Do not run destructive commands unless explicitly requested.
- Do not revert unrelated user changes.
- Ask for confirmation only when a decision can cause irreversible impact.
