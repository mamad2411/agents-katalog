---
name: agentic-code-review
description: Use to review a diff against repository contracts, specs, docs, tests, and architecture boundaries.
---

# Agentic Code Review

## Review Stance

Lead with findings. Prioritize:

- correctness bugs
- security or permission issues
- missing tests
- stale docs/specs
- broken architecture boundaries
- hidden prompt-only enforcement
- UI regressions against `DESIGN.md`

## Process

1. Read `AGENTS.md`, `DESIGN.md`, and affected specs/docs.
2. Inspect the diff.
3. Identify findings with file and line references.
4. For each finding, explain impact and suggested fix.
5. If there are no findings, state residual risk and validation gaps.

## Review Loop

Valid findings should become:

- a code fix
- a test
- a docs/spec update
- a new or updated skill/rule

## Output

Lead with findings ordered by severity. Include file references, the behavioral risk, and the smallest useful fix. Keep summaries secondary to actionable issues.
