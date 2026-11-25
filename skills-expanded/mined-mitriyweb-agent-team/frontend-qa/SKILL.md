---
name: frontend-qa
description: Write and execute tests for UI components and views.
compatibility: Requires bash, Claude Code
metadata:
  team: frontend
  role: qa
  version: "1.0"
---

The Frontend QA (Automated) is responsible for ensuring the reliability and quality of the user interface through comprehensive automated test suites.

## Procedure

1. **Discover project rules** — follow the Project Rules Discovery procedure from the team PROTOCOL. Read lint config and test config before writing any tests.
2. **Design End-to-End User Flows**: Based on `UI_SPEC.md`, identify critical paths and user journeys.
3. **Implement lint-compliant tests**: Write E2E, visual regression, and performance tests. Tests MUST pass the project's linter.
4. **Functional Verification**: Ensure all user interactions, form submissions, and navigations work as expected.
5. **Run all quality gates**: Run tests, lint, and build. All three must pass.
6. **Performance Auditing**: Monitor Core Web Vitals (LCP, FID, CLS) and identify bottlenecks.
7. **Bug Reporting**: Report failures (including lint errors) back to the developer with detailed traces, screenshots, and logs.
8. **Fix Verification**: Re-run ALL quality gates to verify fixes provided by the developer.

## Gotchas

- **Lint compliance**: Read the project's lint rules BEFORE writing tests.
  Common violations in test files: `testing-library/no-node-access`,
  `no-unused-vars`, `no-container`. Know the rules, write compliant code.

- **Headless Environment**: Ensure all E2E tests pass in a headless environment for CI/CD compatibility.

- **Viewports**: Test across multiple responsive viewports (mobile, tablet, desktop).

- **Flakiness**: Use stable selectors (e.g., `data-testid`) to minimize test flakiness.

## Validation loop

The QA role ensures that the UI implementation passes all quality gates: tests, lint, and build.
A test that breaks lint is not a passing test.
The loop is complete when all three gates pass and all reported bugs are verified as fixed.
