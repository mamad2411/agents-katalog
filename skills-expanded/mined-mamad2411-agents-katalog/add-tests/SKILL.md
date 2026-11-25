---
name: add-tests
description: "Design, implement, and maintain automated unit and integration tests that validate system behavior, prevent regressions, and ensure long-term reliability of the codebase."
---

# Add Tests

## Purpose

Design, implement, and maintain automated unit and integration tests that validate system behavior, prevent regressions, and ensure long-term reliability of the codebase.

This skill provides operational guidance for Add Tests, including tool usage patterns, workflows, and quality expectations aligned with Syncolab skill standards.

## When to Use

- Use when the user needs help with Add Tests.
- When integrations for this domain are available and the task matches the workflows below.

## When NOT to Use

- When the task is unrelated to Add Tests or covered by a more specific skill.
- When required integrations or credentials are unavailable.

## Expected Outcome

- Correct use of domain tools with verified results (not fabricated).
- Clear summary of actions taken, data returned, and recommended next steps.
- Errors and missing permissions reported explicitly.

## Inputs to Gather

- User goal, constraints, and any identifiers (URLs, IDs, project keys).
- Available tool sets and connection status.
- Relevant context from related systems before destructive writes.

## Workflow

1. Confirm the request maps to Add Tests and required tools are available.
2. Gather identifiers and scope (project, channel, repo, date range, etc.).
3. Follow the domain guidance below; prefer list/search before get/update when applicable.
4. Execute tool calls using schemas from the integration; never invent tool output.
5. Summarize results and offer logical follow-ups.

# Skill: Add Tests

## Description
Design, implement, and maintain automated unit and integration tests that validate system behavior, prevent regressions, and ensure long-term reliability of the codebase.

---

## Purpose
This skill ensures that the system is continuously verifiable and safe to evolve. It focuses on creating meaningful, maintainable tests that validate both expected behavior and critical edge cases, enabling confident development and refactoring.

---

## Responsibilities

- Translate requirements and code behavior into effective test coverage
- Write clear, deterministic unit and integration tests
- Maintain and improve existing test suites
- Ensure tests reflect real system behavior, not just implementation details
- Identify gaps in coverage and potential risk areas
- Support other agents (e.g., Feature, Refactor) by validating their work

---

## Workflow

### 1. Understand the Context (Jira + GitHub)
- Review the Jira ticket to identify:
  - Expected behavior
  - Acceptance criteria
  - Edge cases and failure scenarios
- Explore the relevant code in GitHub:
  - Understand logic, data flow, and dependencies
  - Identify what should be tested and at what level (unit vs integration)

---

### 2. Define Test Strategy
- Decide:
  - What to test (core logic, edge cases, failure paths)
  - Test type (unit, integration, or both)
- Prioritize:
  - Business-critical flows
  - Complex or error-prone logic
- Avoid testing trivial or implementation-specific details

---

### 3. Implement Unit Tests
- Write focused tests for isolated logic
- Use mocks/stubs only when appropriate
- Ensure:
  - Clear inputs and expected outputs
  - Fast and deterministic execution
- Cover:
  - Happy paths
  - Edge cases
  - Invalid inputs

---

### 4. Implement Integration Tests
- Validate interactions between components:
  - APIs
  - Databases
  - Services
- Prefer realistic setups over excessive mocking
- Ensure tests reflect real usage scenarios

---

### 5. Align with Existing Test Patterns
- Follow:
  - Project structure and conventions
  - Naming patterns
  - Fixtures and setup styles
- Reuse existing utilities and helpers when possible

---

### 6. Validate and Stabilize
- Run the test suite (when possible)
- Ensure:
  - All new tests pass
  - No existing tests are broken unintentionally
- Fix flaky or unstable tests if encountered

---

### 7. Identify Gaps and Risks
- Highlight:
  - Areas that cannot be tested easily
  - Missing infrastructure or dependencies
  - Potential blind spots in coverage
- Document these clearly in Jira

---

### 8. Maintain Test Quality
- Refactor tests when needed for clarity and maintainability
- Remove redundant or obsolete tests
- Ensure tests remain readable and meaningful over time

---

### 9. Update Jira
- Provide a concise summary including:
  - What tests were added or updated
  - What behaviors are covered
  - Any uncovered risks or limitations
- Mark the task appropriately (e.g., ready for review)

---

## GitHub Usage Guidelines

- Read existing tests before adding new ones
- Keep tests close to the code they validate
- Maintain consistency with project standards
- Avoid large, noisy test changes without clear purpose
- Ensure test files are clean, readable, and well-structured

---

## Jira Usage Guidelines

- Use Jira to understand test intent and expected behavior
- Document:
  - Coverage decisions
  - Assumptions made
  - Known gaps or blockers
- Keep the ticket aligned with actual test coverage

---

## Best Practices

- Test behavior, not implementation
- Keep tests simple, focused, and readable
- Prefer deterministic tests over complex setups
- Cover edge cases that are easy to overlook
- Use integration tests to validate real-world flows
- Treat tests as first-class code

---

## Anti-Patterns to Avoid

- Over-mocking critical logic
- Writing brittle tests tied to implementation details
- Ignoring failing or flaky tests
- Duplicating test logic unnecessarily
- Testing trivial code with no real value
- Leaving gaps in critical paths

---

## Output Expectations

- High-quality unit and integration tests
- Improved test coverage of critical behavior
- Stable and maintainable test suite
- Clear Jira summary of coverage and gaps
- Tests ready for continuous integration and review

## Tool Availability Rules

| Access | Behavior |
|--------|----------|
| Full tool access | Execute workflows, verify outputs, report errors. |
| Read-only | Inspect and plan; provide exact commands or dispatch request for writes. |
| No integration | State limitation; do not fabricate API results. |

### Related tool sets

- `cypress`
- `playwright`
- `selenium`



## Review / Decision / Execution Criteria

- Prefer smallest safe change; confirm destructive actions with the user.
- Use evidence from tool responses; cite IDs and links when present.
- Match integration-specific conventions (JQL, RFC3339, A1 notation, etc.).

## Output Format

Report:

1. What was requested and what was done.
2. Key results (tables or bullets).
3. Errors, blockers, or missing permissions.
4. Suggested next steps.

## Quality Bar

- Specific, actionable, and grounded in tool output.
- Concise unless the user asked for detail.
- Respect rate limits, pagination, and API semantics.

## Safety and Boundaries

- Do not commit secrets, tokens, or PII into skills or user-visible logs.
- Do not fabricate validation, send, or write confirmations.
- Confirm destructive operations (delete, destroy, mass update) when appropriate.

## Escalation / Dispatch Rules

- If the task spans multiple domains, use or suggest related skills via `relationships.skills`.
- If write access is required but unavailable, dispatch or ask the user to enable tools.

## References

- Legacy content migrated from `skills/old_skills.json` (`add-tests`).
- `skills/skill.instruction.md`, `skills/meta.instructions.md`
