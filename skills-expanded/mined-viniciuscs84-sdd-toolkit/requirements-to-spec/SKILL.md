---
name: requirements-to-spec
description: turn rough ideas, issues, notes or feature requests into clear specification-driven development specs with scope, acceptance criteria, constraints, risks and implementation planning notes. use when working from vague requirements, github issues, product notes or stakeholder requests before coding starts.
---

# Requirements to Spec

Use this skill to convert rough input into a clear SDD specification.

## Input

Accept any of these:

- rough idea
- GitHub issue
- stakeholder note
- bug report
- feature request
- product requirement
- technical improvement request

## Process

1. Identify the problem.
2. Identify affected users or systems.
3. Define expected value.
4. Separate in-scope and out-of-scope items.
5. Convert vague statements into testable acceptance criteria.
6. Identify constraints and assumptions.
7. List risks and open questions.
8. Suggest implementation waves only after the spec is clear.

## Output format

Return:

```md
# Specification: <title>

## Problem

## Goal

## Users or systems affected

## Scope

### In scope

### Out of scope

## Acceptance criteria

- Given ...
  When ...
  Then ...

## Constraints

## Assumptions

## Risks

## Open questions

## Suggested waves

## Review checklist
```

## Rules

- Do not jump to implementation details too early.
- Do not invent business rules without marking them as assumptions.
- Keep acceptance criteria testable.
- Prefer small waves and reviewable tasks.
- Make uncertainty explicit.
