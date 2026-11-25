---
name: refactor-strict
description: Plan a strict refactor from source evidence, then optionally execute one bounded refactor slice only when authorized.
---
# refactor-strict

Use this skill when the user requests: Plan a strict refactor from source evidence, then optionally execute one bounded refactor slice only when authorized.

## Source prompt references

Primary prompt-system reference: `prompts/10_refactoring_strategy_and_plan.md and prompts/11_refactoring_execution_bounded.md`.

## Operating contract

1. Inspect repository/source material before making claims.
2. Separate facts, assumptions, recommendations, unknowns, blockers, failed validation, and not-run validation.
3. Do not claim implementation, readiness, tests, builds, deployments, pushes, or packaging unless actually evidenced.
4. If code or Git write actions are requested, apply the safe mutation gates from the base prompt.
5. Produce durable artifacts when the user asks for files or reusable output.
6. Use `$ARGUMENTS` as the user-supplied scope, branch, feature, component, or question when provided.

## Task argument

```text
$ARGUMENTS
```

## Required behavior

Load the relevant prompt-system file from the repository or plugin package if available. If it is not available, follow the summarized contract above and produce the same named artifacts defined by the referenced prompt.

