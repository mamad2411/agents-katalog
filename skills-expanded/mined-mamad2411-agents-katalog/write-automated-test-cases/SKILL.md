---
name: write-automated-test-cases
description: Add or improve executable automated test cases across unit, integration, contract, component, API, and e2e modes. Use when the user asks to add code-level test coverage, regression tests, test files, or verification that can be run by the project test tooling.
---

# Write Automated Test Cases

## Modes

Use the smallest automated test mode that gives useful confidence:

- `unit`: Cover isolated functions, utilities, validation rules, branches, and edge cases.
- `integration`: Cover behavior across modules, services, repositories, integrations, or persistence boundaries.
- `contract`: Cover request/response shapes, canonical values, client/server compatibility, and error contracts.
- `component`: Cover rendered UI behavior, accessibility-visible state, interaction, and frontend state changes.
- `api`: Cover endpoint behavior, auth, validation, errors, and compatibility through API-level tests.
- `e2e`: Cover critical user journeys through the browser or full app surface when lower-level tests are insufficient.

If the user names a specific mode, use that mode. If the user does not specify a mode, choose the smallest mode that covers the behavior and risk.

## Workflow

1. Identify the behavior and risk being covered.
2. Read existing test patterns and setup.
3. Choose the smallest useful automated test mode.
4. Add focused tests for expected behavior, edge cases, and regressions.
5. Avoid brittle implementation-detail assertions where possible.
6. Run the relevant test command and report the exact result.

## Boundaries

- Do not replace focused automated regression coverage with only broad manual notes.
- Do not claim a test passed unless it ran.
- Do not add slow e2e coverage for every small unit-level change.
- Do not use this skill for manual QA test case documents unless the user also asks for executable automated coverage.
- Do not create a separate skill for a test level when a mode in this skill covers it.

## Output

- Relevant files or docs inspected.
- Work completed or plan produced.
- Tests or verification run or recommended.
- Docs updated or skipped with reason.
- Remaining risks, assumptions, and handoffs.
