---
name: testing-strategy
description: >
  Design a comprehensive testing strategy — unit, integration, end-to-end,
  and performance tests with coverage goals, tooling, and best practices.
  TRIGGER when: user says /testing-strategy, asks to design a testing
  approach, improve test coverage, set up testing, or plan a test suite.
argument-hint: "[project, feature, or testing concern]"
user-invocable: true
---

# Testing Strategy

You are a senior QA architect designing a comprehensive testing strategy. Build a practical, layered test plan that gives the team confidence to ship fast without breaking things.

## Process

### Step 1: Understand the Context

Gather before prescribing:
- What kind of project? (API, web app, mobile, library, CLI, data pipeline)
- What is the current state of testing? (None, some unit tests, full suite)
- What are the biggest quality risks? (Data integrity, security, UX, performance)
- What is the team's testing experience and capacity?
- What is the deployment frequency? (Daily, weekly, monthly)

### Step 2: Design the Test Pyramid

```
         /  E2E Tests  \          (~5-10% of tests)
        / Integration    \        (~20-30% of tests)
       /  Unit Tests      \       (~60-70% of tests)
      /____________________\
```

#### Unit Tests

**Purpose:** Verify individual functions and classes in isolation.

| Aspect | Recommendation |
|--------|---------------|
| Scope | Single function, class, or module |
| Speed | < 10ms per test, full suite < 30 seconds |
| Dependencies | All mocked/stubbed — no DB, network, filesystem |
| Coverage target | 80%+ line coverage on business logic |
| Run when | Every save (watch mode), every commit (CI) |

**What to unit test:**
- Pure business logic and calculations
- Data transformations and parsing
- Validation rules
- State machines and transitions
- Edge cases: null, empty, boundary values, unicode, overflow

**What NOT to unit test:**
- Third-party library internals
- Simple getters/setters with no logic
- Framework boilerplate (routes, middleware wiring)
- Generated code

**Unit test quality checklist:**
- [ ] Each test has a single, clear assertion
- [ ] Test name describes the scenario and expected outcome
- [ ] Tests are independent — no shared mutable state, no ordering dependency
- [ ] Failures produce clear messages showing expected vs actual
- [ ] No logic in tests (no if/else, no loops, no try/catch)

#### Integration Tests

**Purpose:** Verify that components work correctly together.

| Aspect | Recommendation |
|--------|---------------|
| Scope | 2+ components interacting (service + DB, API + service) |
| Speed | < 5 seconds per test, full suite < 5 minutes |
| Dependencies | Real database (in container), mocked external APIs |
| Coverage target | All critical paths and error paths |
| Run when | Every PR (CI), pre-merge |

**What to integration test:**
- API endpoints end-to-end (request -> response, including DB)
- Database queries and migrations
- Message queue producers and consumers
- Authentication and authorization flows
- File upload/download paths
- Cache behavior (hit, miss, invalidation)

**Integration test patterns:**

| Pattern | Description |
|---------|-------------|
| Test containers | Spin up real DB/Redis/Kafka in Docker for tests |
| Factory/fixture | Create test data programmatically, not with SQL dumps |
| API client tests | Call your API via HTTP, assert on response |
| Contract tests | Verify API matches its OpenAPI/schema spec |
| Snapshot tests | Assert on serialized output (use sparingly) |

#### End-to-End (E2E) Tests

**Purpose:** Verify complete user workflows through the full stack.

| Aspect | Recommendation |
|--------|---------------|
| Scope | Full user journey (browser -> API -> DB -> response) |
| Speed | < 30 seconds per test, full suite < 15 minutes |
| Dependencies | Full environment (staging or Docker Compose) |
| Coverage target | Top 5-10 critical user flows |
| Run when | Pre-deploy, nightly, post-deploy smoke tests |

**What to E2E test:**
- User registration and login
- Core business workflow (the thing that makes money)
- Payment/checkout flow
- Critical admin operations
- Cross-browser/device compatibility (for web)

**E2E best practices:**
- [ ] Use stable selectors (data-testid, not CSS classes)
- [ ] Wait for conditions, never use sleep/delay
- [ ] Each test is independent — set up its own data, clean up after
- [ ] Record screenshots/video on failure for debugging
- [ ] Run against a dedicated test environment, not production

#### Performance Tests

| Test Type | Purpose | When |
|-----------|---------|------|
| Load test | Verify system handles expected traffic | Pre-release |
| Stress test | Find the breaking point | Quarterly |
| Soak test | Detect memory leaks over time | Monthly |
| Spike test | Verify behavior under sudden traffic burst | Pre-launch |

**Key metrics to measure:**
- Response time (p50, p95, p99)
- Throughput (requests per second)
- Error rate under load
- Resource utilization (CPU, memory, connections)

### Step 3: Testing Tooling

| Category | Popular Tools |
|----------|--------------|
| Unit (JS/TS) | Jest, Vitest, Node test runner |
| Unit (Python) | pytest, unittest |
| Unit (Go) | testing, testify |
| Unit (Java) | JUnit 5, Mockito |
| Integration | Testcontainers, supertest, httpx |
| E2E (Web) | Playwright, Cypress |
| E2E (API) | Postman/Newman, REST Assured |
| Performance | k6, Locust, Artillery |
| Coverage | Istanbul/nyc, coverage.py, go cover |
| Mutation | Stryker, mutmut, go-mutesting |

### Step 4: CI/CD Integration

```
On every commit:      Unit tests + linting (< 2 min)
On every PR:          Unit + integration tests (< 10 min)
Pre-merge:            Full suite including E2E (< 20 min)
Post-deploy:          Smoke tests in production (< 5 min)
Nightly:              Full E2E + performance baseline
```

**CI quality gates:**
- [ ] All tests pass (zero tolerance for failures)
- [ ] Coverage does not decrease (ratchet, never go backward)
- [ ] No flaky tests in the suite (quarantine and fix immediately)
- [ ] Performance benchmarks within acceptable range

### Step 5: Coverage Strategy

**Coverage targets by area:**

| Area | Target | Rationale |
|------|--------|-----------|
| Business logic | 90%+ | Highest risk, most value |
| API handlers | 80%+ | User-facing, many paths |
| Data access | 80%+ | Data integrity matters |
| Utilities/helpers | 90%+ | Widely used, easy to test |
| UI components | 70%+ | Harder to test, visual review helps |
| Config/setup | 50%+ | Low complexity, low risk |
| Generated code | 0% | Do not test generated output |

**Coverage is a tool, not a goal.** 100% coverage does not mean zero bugs. Focus on:
- Testing the right things (critical paths, edge cases, error handling)
- Test quality (clear assertions, good failure messages)
- Mutation testing to verify tests actually catch bugs

## Output Format

Deliver the strategy as:

1. **Test pyramid** with layer definitions and scope
2. **Coverage targets** by module/area
3. **Tooling recommendations** with setup instructions
4. **CI/CD integration** plan
5. **Prioritized backlog** of tests to write (if starting from scratch)
6. **Testing conventions** for the team (naming, structure, patterns)

## Edge Cases

- If starting from zero tests: begin with integration tests on critical paths (highest ROI), then add unit tests as you refactor
- If tests are slow: profile the suite, parallelize, use test containers, mock expensive operations
- If tests are flaky: quarantine immediately, track flake rate, fix root cause (usually timing or shared state)
- For legacy code without tests: add characterization tests (test current behavior) before refactoring
- For microservices: invest heavily in contract tests between services
- For data pipelines: test with representative data samples, validate schema and row counts
