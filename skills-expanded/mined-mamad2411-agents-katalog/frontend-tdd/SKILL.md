---
name: frontend-tdd
description: Use when a frontend change should begin with a colocated spec.md, produce reviewable test-scenarios.md, and wait for review before writing Vitest and React Testing Library tests plus the implementation.
license: MIT
---

# Frontend TDD

Use this skill when the user wants a spec-first, document-driven frontend workflow:

- clarify the requested behavior
- choose a local working directory for the spec documents
- write or update `spec.md`
- derive `test-scenarios.md` from the spec
- wait for approval
- write Vitest and React Testing Library tests
- implement the minimum code needed to pass

## When to Use

- The user says they want to use TDD for a frontend feature
- The user wants a spec-first or scenario-first workflow before implementation
- The user wants `spec.md` or `test-scenarios.md` drafted before tests are written
- The user wants test scenarios reviewed before implementation
- The task involves frontend components, hooks, view models, forms, routing UI, pages, or client-side state
- The expected tests should be written with Vitest

## What This Skill Covers

- Integration-first frontend testing with Vitest and React Testing Library
- Unit tests for pure functions, mappers, validators, and small logic helpers
- A document workflow where `spec.md` is the source of truth and `test-scenarios.md` is a reviewable derived artifact
- A collaboration workflow where test scenarios are reviewed before test files or implementation are written
- Minimal implementation after failing tests are in place

## What This Skill Does Not Cover

- E2E testing
- Playwright, Cypress, or browser automation workflows
- Backend, API, or infrastructure testing
- Writing implementation before the user approves the test direction

## Default Test Strategy

- Prefer integration tests for user-visible behavior
- Use unit tests only for logic that is meaningfully testable without rendering
- Do not default to E2E in this skill
- Test observable behavior, not implementation details
- Prefer a small number of high-signal tests over many brittle ones

Read [references/test-strategy.md](references/test-strategy.md) when deciding between integration and unit coverage.

## Source Documents

Treat these markdown files as the default working set for a feature:

- `spec.md`: the source of truth for requirements, constraints, acceptance criteria, and open questions
- `test-scenarios.md`: the reviewable scenario list derived from `spec.md`
- `implementation-notes.md`: optional notes for decisions, follow-up work, or tradeoffs discovered during implementation

If the spec changes:

- update `spec.md` first
- then update `test-scenarios.md`
- only then update tests or implementation

## Document Placement

Place the working markdown documents in the closest stable location to the code being changed.

Default preference order:

1. the feature or component directory being changed
2. a local sibling `docs/` directory near that feature area
3. a higher-level shared directory only when the change spans multiple distant areas

Use a repository-root `docs/` directory only for cross-cutting work that truly spans unrelated parts of the codebase.

When choosing a location:

- optimize for reviewability by the engineer changing the code
- keep the documents near the files that will be updated together
- avoid scattering multiple copies of the same feature spec across the repository

## Workflow

1. Restate the requested behavior in plain language
2. Choose the working document location closest to the primary implementation target
3. Write or update `spec.md`
4. Separate confirmed requirements from assumptions and open questions inside the spec
5. Derive `test-scenarios.md` from the current spec
6. Wait for user review or approval
7. After approval, write failing tests with Vitest and React Testing Library
8. Implement the minimum code needed to pass
9. Refactor while keeping tests green
10. Run relevant verification commands and summarize the result

Read [references/workflow.md](references/workflow.md) for the detailed execution rules.

## Output Contract

Before implementation, create or update the markdown documents first.

When answering inline, structure the response in this order:

1. `Spec Summary`
2. `Assumptions / Open Questions`
3. `Test Scenarios`
4. `Out of Scope`
5. `Implementation Notes`

## Implementation Guardrails

- Do not write test files before the scenario list is reviewed when the user explicitly wants that approval step
- Keep implementation small and directly tied to the failing test
- Prefer existing patterns in the target codebase over introducing a new abstraction
- Avoid coupling tests to private internals when a user-facing assertion is possible
- If dedicated testing, framework, or code-quality skills are available in the environment, use them as companion guidance

Read [references/implementation-guardrails.md](references/implementation-guardrails.md) before implementation.

## References

- [references/workflow.md](references/workflow.md)
- [references/spec-template.md](references/spec-template.md)
- [references/test-scenarios-template.md](references/test-scenarios-template.md)
- [references/test-strategy.md](references/test-strategy.md)
- [references/implementation-guardrails.md](references/implementation-guardrails.md)
