---
name: fullstack-shared-types-contract
description: "Use this skill to keep frontend, backend, API, validation, and database types aligned."
---

# Shared Types Contract Skill

## Purpose

Use this skill to keep frontend, backend, API, validation, and database types aligned.

This skill is the operational workflow that supports the related Cursor rule:

```text
.cursor/rules/fullstack/shared-types-contract.mdc
```

Rules decide when behavior should apply. Skills define how the agent should execute the workflow when the task calls for it.

## When To Use

Use this skill when the user request, changed files, or related rule indicates that keep frontend, backend, API, validation, and database types aligned.

Also use it when the user manually invokes the skill by name:

```text
/fullstack-shared-types-contract
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

1. Trace the feature from UI to API to database to deployment behavior.
2. Keep shared types, validation schemas, and API contracts aligned.
3. Verify auth and authorization at the server boundary.
4. Update tests, docs, environment examples, and user-facing states as needed.
5. Run frontend, backend, database, and integration checks when available.

## Safety Rules

- Do not update the UI without the matching API and data path.
- Do not assume auth is handled elsewhere.
- Do not change environment variables without updating examples and docs.
- Do not hide uncertainty. Report unclear assumptions and unresolved risk.
- Do not make broad unrelated edits while executing this skill.
- Do not mark the task complete if the core workflow was skipped.

## Verification Checklist

Run or consider these checks based on the project tooling:

- `frontend build`
- `backend tests`
- `database validation`
- `API contract verification`
- `auth flow test`


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
