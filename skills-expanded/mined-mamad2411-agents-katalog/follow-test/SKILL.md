---
name: follow-test
description: Set up and use end-to-end testing strategies including regression testing per standard
argument-hint: "[config-test-env] [scope]"
related:
  - deep-review-codebase
  - follow-math-concepts
  - follow-monorepo

---

## Goal

Set up and use complete testing strategies following the test pyramid principle

## Scope

Use to set up and run testing for every project type and ecosystem

## Execute

### 1. Check Prerequisites

> Goal: Check Prerequisites

- check `package.json` or `Cargo.toml`
- check the testing framework used per ecosystem
- check for a monorepo (multiple `package.json`, workspace config)
- if it is a monorepo, run `/follow-monorepo` first

### 2. Select Test Strategy Level

> Goal: Select Test Strategy Level

Choose the level per Rules section 1

### 3. Setup Test Configurations

> Goal: Setup Test Configurations

- run `/follow-tool-vitest` for the testing framework
- run `/follow-tool-playwright` for E2E testing
- run `/follow-tasks` for test scripts
- set up config files per the tech stack

### 4. Apply Test Scripts

> Goal: Apply Test Scripts

- run `/use-scripts` per the tech stack from Rules section 3
- add test scripts in `package.json` or `Cargo.toml`
- single workspace: edit directly
- multiple workspaces: run `/follow-monorepo` first

### 5. Setup Test Directories

> Goal: Setup Test Directories

- create the directory structure per Rules section 4
- organize test files per conventions
- set up test fixtures and helpers

### 6. Write Tests

> Goal: Write Tests

- run `/update-tests` to write unit tests and coverage
- run `/run-test all` to run every test type (unit, integration, e2e, component)
- run `/run-test` for API tests and contract tests if the project has an API

### 7. Validate

> Goal: Validate

- run the test scripts at the chosen level
- check coverage against the targets
- check test quality against best practices

### Workflows

> Goal: dispatch to the workflow by topic/argument

| Topic/Argument | Workflow |
|----------------|----------|
| `config-test-env`, `test-env`, `env`, `fixtures`, `test-db` | `workflows/config-test-env/SKILL.md` — test env vars, fixtures, test db, CI test env |

1. if the argument matches a topic → read `workflows/<name>/SKILL.md` and follow the flow there — do not execute directly from this table
2. if not specified → follow steps 1-7 in order

## Rules

### 1. Test Strategy Levels

Choose the level by project size and complexity:
- Minimal (Default): unit tests, basic coverage (70%) - suits small-medium projects
- Standard: Minimal + integration tests, component tests, coverage (85%) - suits projects needing higher confidence
- Complete: Standard + e2e tests, performance tests, visual tests, contract tests, coverage (100%) - suits production systems

### 2. Test Pyramid Principle

Use the test pyramid to balance between test types:
- 70% Unit Tests: test individual units in isolation - fast, cheap, maintainable
- 20% Integration Tests: test interactions between components - moderate speed, cost
- 10% E2E Tests: test complete user flows - slow, expensive, critical paths only

### 3. Test Scripts

Scripts for testing per ecosystem:

| Task | Bun/Node | Rust | Python | Go |
|------|----------|------|--------|----|
| test | vitest run | cargo nextest run | pytest | go test ./... |
| test:watch | vitest | cargo nextest run --watch | pytest-watch | go test ./... -watch |
| test:coverage | vitest run --coverage | cargo llvm-cov --html | pytest --cov | go test -coverprofile=coverage.out |
| test:integration | vitest run --config vitest.integration.config.ts | cargo nextest run --test-dir integration | pytest tests/integration | go test ./tests/integration |
| test:e2e | vitest run --config vitest.e2e.config.ts | cargo nextest run --test-dir e2e | pytest tests/e2e | go test ./tests/e2e |
| test:component | vitest run --config vitest.component.config.ts | - | - | - |

### 4. Test Structure

Directory structure for test files:

```
tests/
├── unit/                    # Unit tests
│   ├── modules/
│   └── shared/
├── integration/             # Integration tests
│   ├── adapters/
│   └── api/
├── e2e/                     # End-to-end tests
│   ├── flows/
│   └── pages/
├── component/               # Component tests
├── fixtures/                # Test fixtures
└── helpers/                 # Test helpers
```

### 5. Coverage Targets

Coverage targets per level:

| Level | Unit | Integration | E2E | Overall |
|-------|------|-------------|-----|---------|
| Minimal | 70% | - | - | 70% |
| Standard | 85% | 60% | - | 80% |
| Complete | 95% | 80% | 50% | 90% |

### 6. Test Best Practices

Follow the best practices for writing tests:
- AAA pattern: arrange, act, assert for test structure
- Descriptive names: test names should say what is being tested
- One assertion per test: test one thing in each test
- Independent tests: tests should not depend on each other
- Fast feedback: unit tests should be fast (< 100ms per test)
- Mock external dependencies: mock services, databases, APIs
- Test edge cases: boundary values, null, undefined, empty
- Use fixtures: reuse test data and setup code
- CI integration: run tests in the CI pipeline
- Test documentation: tests are documentation of the code

### 7. Regression Testing

> Goal: verify new changes did not break existing features

1. identify the changed files and modules with `git diff`
2. analyze dependencies and downstream effects; identify critical paths and integration points
3. select test cases covering the changed code, critical paths, and relevant edge cases
4. run unit tests for the changed modules, integration tests for affected flows, e2e tests for critical user journeys
5. analyze failures: group them by error pattern, separate regressions from pre-existing bugs, check for flaky tests
6. run smoke tests for critical functionality and the tests covering changed lines first — use CI/CD for automated regression in a near-production environment
7. fix regressions, add new test cases where needed, re-run tests until all pass — never skip regression testing to save time

### 8. Advanced Testing (Optional)

For the Complete level, add advanced testing:
- Mutation testing: verify test quality via code mutation
- Performance testing: benchmark critical paths and bottlenecks
- Visual testing: detect UI regressions via screenshot comparison
- Contract testing: verify API contracts between services
- Security testing: scan for vulnerabilities in dependencies and code
- Load testing: test the system under high-load scenarios

- Use /follow-math-concepts if needed

## Expected Outcome

- test scripts fully set up in `package.json`
- test directory structure organized correctly
- test configurations set per the tech stack
- coverage meets the target for the chosen level
- tests run in the CI pipeline
- regression testing covers the changed code and critical paths
