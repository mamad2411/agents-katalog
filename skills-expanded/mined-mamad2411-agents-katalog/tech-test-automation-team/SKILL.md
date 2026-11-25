---
name: tech-test-automation-team
description: End-to-end software test automation workflow. Use when the user wants a complete testing expert workflow covering TDD strategy, test case generation, unit/integration/E2E testing, API test automation, coverage, performance, QA test plans, release readiness, or quality dashboards. Coordinates superpowers-tdd, test-case-generator, test-patterns, e2e-testing-patterns, api-test-automation, and afrexai-qa-test-plan.
metadata:
  short-description: Complete software test automation workflow
---

# Tech Test Automation

Use this skill as the workflow entry point for a complete automated testing package. It coordinates the companion skills in this bundle instead of replacing them.

## Workflow

1. Use `superpowers-tdd` when implementing a feature or bug fix. Start with a failing test, verify it fails for the right reason, write minimal code, then refactor.
2. Use `test-case-generator` to generate unit test files from source code, including imports, mocks, assertions, normal paths, edge cases, and error paths.
3. Use `test-patterns` to write, run, and debug unit/integration tests across Node.js, Python, Go, Rust, and Bash, including coverage and dependency mocking.
4. Use `e2e-testing-patterns` for Playwright/Cypress E2E suites, critical user journeys, stable selectors, CI integration, flaky-test reduction, and visual/accessibility checks.
5. Use `api-test-automation` for REST/GraphQL testing, contract tests, mock services, performance tests, and API test reports.
6. Use `afrexai-qa-test-plan` to create QA test plans, coverage matrices, bug severity rules, automation ROI, release readiness checklists, and quality dashboards.

## Routing

- If the task is implementation work, start with `superpowers-tdd` unless the user explicitly says not to use TDD.
- If the user provides code and asks for tests, use `test-case-generator` first, then `test-patterns` to align with the project’s real test framework and run commands.
- If the task is browser workflow testing, use `e2e-testing-patterns`.
- If the task is endpoint, contract, mock, REST, GraphQL, or performance testing, use `api-test-automation`.
- If the task is planning, release quality, coverage strategy, or QA reporting, use `afrexai-qa-test-plan`.
- For full test automation requests, run the workflow in phases and keep each artifact actionable.

## Project-First Rules

When working in a local codebase:

1. Inspect the project’s existing test framework, scripts, package files, CI config, and test naming conventions before generating tests.
2. Prefer existing project helpers, fixtures, mock patterns, factories, and data builders.
3. Run the narrowest relevant test command first, then broaden only when risk warrants it.
4. Keep generated tests deterministic. Avoid real network calls, time-dependent assertions, shared mutable state, and brittle selectors.
5. Report exact commands run, pass/fail results, coverage evidence when available, and any skipped verification.

## Output Package

For a full automated testing package, produce:

1. Test strategy: layers, risk areas, coverage targets, and priorities.
2. Test code: unit, integration, E2E, and API tests where applicable.
3. Execution report: commands, pass/fail summary, failures, coverage, and performance baseline.
4. QA plan: coverage matrix, severity framework, release checklist, automation ROI, and metrics dashboard.

## Operating Notes

- Prefer behavior-focused tests over implementation-detail tests.
- Use stable selectors such as roles, labels, and explicit test IDs for E2E tests.
- Keep assumptions explicit.
- Do not claim test success without running or clearly stating the verification limit.
