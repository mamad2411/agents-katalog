---
name: spec-driven-development-pro
description: Turn vague requirements into clear specifications before implementation. Inspired by production-grade engineering lifecycle skills. Use for new features, significant changes, API behavior, UI flows, acceptance criteria, and when requirements are ambiguous or likely to grow.
---

# Spec Driven Development Pro

## Workflow

1. Define problem, user, goal, and non-goals.
2. Capture current behavior and desired behavior.
3. Specify scope, constraints, data/API needs, UI states, error cases, and security considerations.
4. Define acceptance criteria and verification method.
5. Identify docs that must be updated.
6. Only then plan or implement.

## Spec Shape

```markdown
## Goal
## Non-Goals
## User Flow
## Functional Requirements
## Edge Cases
## Data / API
## Security / Permissions
## Acceptance Criteria
## Verification
## Docs To Update
```

## Rules

- Do not over-spec small fixes.
- Keep specs short enough to guide implementation.
- Turn uncertainty into explicit open questions or assumptions.
- Update `docs/features/` for meaningful feature specs.

## Output

State the spec summary, open questions, and implementation readiness.
