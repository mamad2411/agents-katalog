---
name: tdd-implementation-loop
description: Use when implementing behavior from an approved plan with test-first or regression-test-first development.
---

# TDD Implementation Loop

## Workflow

1. Read `AGENTS.md`, the active plan, and the relevant spec.
2. Identify the smallest behavior that can be proven by a test.
3. Add or update the failing test first when practical.
4. Implement the minimal code needed to pass.
5. Run the focused test.
6. Repeat until the planned behavior is covered.
7. Run the full required validation before handoff.

## Rules

- Keep tests tied to user-visible behavior or durable service contracts.
- Prefer deterministic tests over broad snapshot or prompt-output assertions.
- When test-first is not practical, explain why and add the strongest regression coverage available.
- Update docs/specs if implementation changes current behavior or accepted scope.

## Output

Return changed files, tests added, validation commands, and any behavior that remains untested.
