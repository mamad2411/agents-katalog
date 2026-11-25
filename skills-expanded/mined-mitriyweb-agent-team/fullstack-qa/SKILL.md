---
name: fullstack-qa
description: >-
  Write and execute tests across frontend and backend.
  Covers UI component tests, API integration tests, and
  end-to-end flows spanning both stacks.
compatibility: Requires bash, Claude Code
metadata:
  team: fullstack
  role: qa
  version: "1.0"
tags:
---

The Fullstack QA ensures reliability across both the UI
and server-side systems.

## Procedure

1. **Discover project rules** -- follow Project Rules
   Discovery from PROTOCOL.md. Read lint and test config.
2. **Classify test scope** -- determine if tests are for
   frontend, backend, or end-to-end integration.
3. **Frontend tests**: Component rendering, user interactions,
   accessibility checks, visual regression.
4. **Backend tests**: API endpoint validation, service logic,
   database operations, error handling, auth flows.
5. **E2E tests**: Full user flows from UI through API to DB.
   Use Playwright for browser automation.
6. **Write lint-compliant tests**: All tests MUST pass the
   project's linter before submission.
7. **Run all quality gates**: Tests, lint, and build must
   all pass.
8. **Bug reporting**: Report UI bugs to fe-dev, API bugs
   to be-dev. Include detailed reproduction steps.
9. **Fix verification**: Re-run ALL quality gates after
   developer fixes.

## Gotchas

- **Lint compliance**: Read lint rules BEFORE writing tests.
- **API mocking**: When testing frontend in isolation, mock
  API responses matching the contract in .claude-loop/reports/task-{id}-spec.md.
- **Database state**: Backend tests should set up and tear
  down their own test data. Never depend on existing state.
- **Flakiness**: Use stable selectors (`data-testid`) for
  UI tests. Use deterministic data for API tests.
- **Auth in tests**: Create test-specific auth tokens or
  use a test user. Never use production credentials.

## Validation Loop

The QA loop is complete when all three quality gates pass
(tests, lint, build), all reported bugs are verified as
fixed, and coverage meets project thresholds.
