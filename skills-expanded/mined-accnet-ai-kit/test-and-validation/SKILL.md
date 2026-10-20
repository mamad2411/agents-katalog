---
name: test-and-validation
description: How to design and run tests — test pyramid, mocking boundaries, mutation checks, and mapping tests to acceptance criteria. Use when writing tests or validating a change. Test CODE lives in the project; commands come from kit.yaml verification.
version: 0.2.0
tier: core
stack: [any]
owner: qa
gates: [G2]
related: [.ai/modules/testing.md, .ai/templates/test-case.md]
---

# Skill: test-and-validation

## Purpose
Define how tests are written and validated so quality is enforced by the repo (Gate G2 + CI), not by whichever skill happened to run. Rules only — the actual test files live in the project (e.g. `src/**/*.test.ts`) and the runner comes from `.ai-config/kit.yaml` `verification.test_command`.

## When to use
Writing tests for any task, or validating a change before marking a task done (G2).

## Test pyramid
- **Unit (most)**: pure logic with dependencies mocked at the boundary. Mock the DB client (e.g. `pool.query`) for repositories; mock repositories for services; mock the transaction + peer services for creation flows.
- **Integration (some)**: real wiring across a couple of layers.
- **E2E (few)**: critical paths only.

## Rules
1. **One behavior per test**, named for the behavior. Every decision/fallback branch gets its own case (primary path, each fallback, constraint isolation, no-candidate error).
2. **Assert the boundary**: verify the right query filter / the right args passed down (e.g. that the authenticated identity reaches the service), not just the return value.
3. **Acceptance mapping**: each acceptance criterion in `tasks.md` maps to at least one test; a task isn't done (G2) until its criteria have passing tests.
4. **Mutation check**: after green, invert a key condition and confirm a test fails; if nothing fails, strengthen the tests. Revert the mutation.
5. **Focused first, full before done**: run focused while iterating, then the full suite (`test_command`) before G2; record the result (e.g. "N suites, M tests passed") in the task note.

## Checklist
- [ ] Each acceptance criterion covered by a passing test
- [ ] Every decision/fallback/error branch has its own case
- [ ] Boundary asserted (args/filters), not just return value
- [ ] Mutation check performed and reverted
- [ ] Full suite green; result recorded in the task note

## Anti-patterns
- Testing implementation details instead of behavior
- Only the happy path covered
- Over-mocking so the test passes even when logic is wrong (caught by the mutation check)

## Commands (from kit.yaml, not hardcoded here)
Tests `verification.test_command`, typecheck `verification.typecheck_command`, lint `verification.lint_command`. CI runs these via `.github/workflows/gates.yml`; `doctor.sh` checks they exist. Draft cases with `.ai/templates/test-case.md`.

## Output
Test files in the project + a task note recording the suite result; failures become tasks, never silent skips.
