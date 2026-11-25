# Testing — AI-Driven TDD Strategy

## When to Use
- Starting a new feature or module
- Refactoring existing code to prevent regressions
- Debugging complex issues by reproducing with a failing test
- When confidence in AI-generated code is critical

## Core Principle
Write tests before code. Use Claude to brainstorm edge cases, generate test skeletons, and validate coverage — but always verify assertions manually.

## Process
1. **Clarify requirements** — Break the feature into testable units. Ask Claude to enumerate edge cases and acceptance criteria.
2. **Write failing tests** — Generate minimal tests that fail initially, one behavior per test. Use the project's testing framework.
3. **Implement minimal code** — Write just enough to make tests pass. No over-engineering.
4. **Refactor with confidence** — Clean up code while tests stay green. Use Claude for optimization suggestions.
5. **Validate coverage** — Run coverage tools. Have Claude identify gaps. Target 80-90%.
6. **Document test strategy** — Summarize key tests, edge cases handled, and any gaps.

## Output Format
- Test suite summary (bullet list with pass/fail)
- Code changes (diff-style snippets)
- Coverage metrics
- Edge cases handled (3-5 non-obvious scenarios)

## Rules
- Red-green-refactor cycle. No skipping refactor.
- One assertion per test when possible.
- Tests describe WHAT, not HOW — test behavior, not implementation.
- Claude generates, human verifies. Never trust assertions blindly.
- Integration tests complement unit tests — don't skip either.

## Anti-Patterns
- Writing tests after code (defeats TDD purpose)
- Testing implementation details (breaks on refactor)
- Ignoring failing tests to "move forward" (accumulates debt)
- Over-relying on Claude for test logic without reviewing assertions
- Testing trivial getters/setters (inflates count, adds no value)
