---
name: lint-review-skill
description: Run linter and report results for code review
version: "1.0"
---

# Lint Review Skill

Use this skill when the workflow state is **LINT** or **RUN_LINT**.

## Instructions

1. Trigger the **run_lint** action (no body or optional repo path).
2. Wait for the stream or poll until status is no longer `processing`.
3. When the state becomes **REVIEW_RESULTS**, call **submit_results** with:
   - `passed` (boolean): Whether lint passed.
   - `issues` (array or number): Count or list of issues.

## Example

```json
{
  "passed": false,
  "issues": 3
}
```

Use **request_changes** with a `reason` if the agent should block merge.
