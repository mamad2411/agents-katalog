---
name: testing-strategy
description: >-
  Test strategy framework covering the test pyramid, test ratios, shift-left
  practices, and quality gates. Provides actionable guidance on unit, integration,
  and E2E test design with anti-patterns to avoid.
when-to-use: >-
  Invoke when designing a testing approach for a new project, reviewing test
  coverage, setting up CI/CD quality gates, or evaluating an existing test suite.
  Also invoke when arguing for testing investment or fixing a broken test culture.
categories:
  - testing
  - quality-assurance
  - ci-cd
---

# Testing Strategy

Every system needs a testing strategy that balances speed, confidence, and cost. More tests at the base (fast, cheap) and fewer at the top (slow, expensive).

## The Test Pyramid

```
    /  E2E  \        10% — Full system, slowest, most brittle
   /----------\
  / Integration \    20% — Real dependencies, moderate speed
 /----------------\
/    Unit Tests    \ 70% — Fast, isolated, mock dependencies
--------------------
```

| Level | Target | Speed | Dependencies | When to Run |
|---|---|---|---|---|
| **Unit** | 70% | < 100ms per test | All mocked | Every commit, every PR |
| **Integration** | 20% | Seconds | Real (DB, APIs) | CI before merge |
| **E2E** | 10% | Minutes | Full system | Staging after deployment |

---

## Unit Tests

- Test a single unit of logic in isolation
- Mock all external dependencies (databases, APIs, file systems)
- Should run in milliseconds — if slow, it's not a unit test
- Focus on business rules, edge cases, error handling
- Use AAA pattern: **Arrange**, **Act**, **Assert**
- One logical assertion per test — test one behavior
- Name descriptively: `MethodName_Scenario_ExpectedResult`

## Integration Tests

- Use real dependencies where possible (real DB, real queue)
- Test component boundaries and interaction contracts
- Slower than unit tests — accept seconds, not minutes
- Use test containers or ephemeral environments
- Validate serialization, network calls, auth flows
- Clean up state between tests to prevent cross-test contamination

## E2E Tests

- Test complete user workflows through the full stack
- Reserve for critical business paths only (login, checkout, core transactions)
- Accept that these are slower and more brittle
- Run in a production-like environment with realistic data
- Invest in stability over coverage — few reliable tests beat many flaky ones
- Use retry logic for infrastructure flakiness, not logic errors

---

## Quality Gate Configuration

| Stage | Required Tests | Failure Action |
|---|---|---|
| **PR validation** | Lint, static analysis, unit tests (L0/L1) | Block merge |
| **CI build** | Unit + integration tests (L2), security scanning | Block merge |
| **Staging deploy** | Smoke tests, functional tests (L3), load tests | Block promotion |
| **Production deploy** | Smoke tests, synthetic monitoring | Auto-rollback |
| **Post-deploy** | Integration tests (L4), chaos testing, compliance | Alert + investigate |

---

## Shift Left — Test Early

- Run unit tests on every commit and pull request
- Run integration tests in CI before merge
- Run E2E tests in staging after deployment
- Static analysis and linting are the earliest quality gate
- Cost of fixing grows exponentially with time — catch early

## Test in CI, Not Just Locally

- [ ] CI is the single source of truth for test results
- [ ] CI test environments match production configuration
- [ ] Pipeline fails fast — run fastest tests first
- [ ] Parallelize test execution for short feedback loops
- [ ] Tests that pass locally but fail in CI indicate environment coupling

---

## Anti-Patterns (What NOT to Do)

| Anti-Pattern | Problem | Fix |
|---|---|---|
| **Testing theater** | High coverage on trivial code (getters, DTOs) | Cover complex logic and failure modes |
| **Ice cream cone** | More E2E tests than unit tests | Invert the pyramid |
| **Testing implementation** | Tests break on refactor without behavior change | Test behavior, not internals |
| **Shared mutable state** | Tests depend on order or other tests' side effects | Isolate test data |
| **Ignoring test failures** | "Known failures" instead of fixing | Fix or delete — no middle ground |
| **100% coverage worship** | Covering getters/setters while ignoring edge cases | Cover what matters |
| **Flaky test tolerance** | "It'll pass on retry" | Fix immediately — flaky tests erode trust |

---

## Test Naming Convention

```
MethodName_Scenario_ExpectedResult

Examples:
- CalculateDiscount_WhenOrderOver100_Returns10Percent
- ValidateInput_NullEmail_ThrowsArgumentException
- CreateUser_DuplicateEmail_ReturnsConflict
```

## Related Skills

- `infrastructure-testing` — Terraform, Bicep, and policy testing specifics
- `pipeline-quality-gates` — CI/CD pipeline quality gate configuration
