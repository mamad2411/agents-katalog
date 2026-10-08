---
name: python-python-type-safety
description: "Use this skill to use annotations, typed models, protocols, and static checks where valuable."
---

# Python Type Safety Skill

## Purpose

Use this skill to use annotations, typed models, protocols, and static checks where valuable.

This skill is the operational workflow that supports the related Cursor rule:

```text
.cursor/rules/python/python-type-safety.mdc
```

Rules decide when behavior should apply. Skills define how the agent should execute the workflow when the task calls for it.

## When To Use

Use this skill when the user request, changed files, or related rule indicates that use annotations, typed models, protocols, and static checks where valuable.

Also use it when the user manually invokes the skill by name:

```text
/python-python-type-safety
```

## Inputs To Inspect

Before making changes, inspect the most relevant available inputs:

- The related rule file, if present
- Current repository structure
- Existing implementation patterns
- Relevant config files
- Relevant tests
- Recent diffs
- Project documentation
- Project connection metadata when deployment or external services are involved

## Required Workflow

1. Inspect package layout, dependency files, config, tests, and entry points.
2. Use typed, modular functions and clear boundaries.
3. Handle errors explicitly and log useful context.
4. Use pytest, ruff, mypy, or project checks when available.
5. Keep scripts reproducible and avoid local machine assumptions.

## Safety Rules

- Do not rely on local absolute paths.
- Do not hide exceptions with broad bare except blocks.
- Do not add heavy dependencies when the standard library is enough.
- Do not hide uncertainty. Report unclear assumptions and unresolved risk.
- Do not make broad unrelated edits while executing this skill.
- Do not mark the task complete if the core workflow was skipped.

## Verification Checklist

Run or consider these checks based on the project tooling:

- `python -m pytest`
- `python -m ruff check .`
- `python -m mypy .`
- `python -m build when packaged`


Also verify:

- The implementation matches the related rule.
- The diff is limited to the requested work.
- User-facing behavior is correct.
- Tests or checks were run, or skipped with a clear reason.
- No secrets, credentials, or sensitive data were introduced.

## Output Expectations

When finished, report:

- What changed
- What files or areas were affected
- What checks were run
- What checks were skipped and why
- Any risks, assumptions, or follow-up items

## Failure Handling

If the workflow cannot be completed:

1. Stop before making unsafe changes.
2. Explain the blocker clearly.
3. Preserve any useful partial work if it is safe.
4. Suggest the smallest next safe action.

Do not continue by guessing when the missing information affects safety, data integrity, deployment, security, or production behavior.
