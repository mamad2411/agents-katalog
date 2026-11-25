---
name: nestjs-testing
description: NestJS testing best practices (unit and e2e). Use when writing or reviewing NestJS tests — Test.createTestingModule, mocking providers, controller/service unit tests, or e2e with supertest. Triggers on TestingModule, createTestingModule, overrideProvider, or supertest.
license: MIT
metadata:
  author: nestjs
  version: "1.0.0"
---

# NestJS Testing

Best practices for testing NestJS applications, following the official testing docs
(https://docs.nestjs.com/fundamentals/testing). Covers isolated unit tests built with
`Test.createTestingModule` and full-stack e2e tests driven through supertest. Each rule
pairs an antipattern with the idiomatic Jest pattern.

## When to Apply

Reference these guidelines when:
- Writing unit tests for a controller or service with `Test.createTestingModule`
- Mocking a unit's dependencies (repositories, HTTP clients, other services)
- Writing e2e tests that hit the real HTTP server via supertest
- Bypassing guards/auth or swapping providers in e2e
- Managing test data, fixtures, and teardown between tests
- Reviewing or refactoring an existing NestJS test suite

## Rules

- `test-createtestingmodule` (CRITICAL) — build the unit under test with `Test.createTestingModule(...).compile()`
- `mock-dependencies` (CRITICAL) — provide mock providers (`useValue`) for every dependency of the unit
- `unit-test-services` (HIGH) — test service logic against mocked repos/clients, never a real DB
- `e2e-with-supertest` (HIGH) — exercise the whole app over HTTP with `createNestApplication` + supertest
- `override-guards-in-e2e` (HIGH) — bypass auth in e2e with `overrideGuard` / `overrideProvider`
- `isolated-test-data` (HIGH) — fresh fixtures per test; reset mocks and tear down the app/DB between tests
- `test-behavior-not-implementation` (MEDIUM) — assert returned values and HTTP contracts, not internal call shapes

## How to Use

Read the individual rule file for the explanation and before/after example:

```
rules/test-createtestingmodule.md
rules/mock-dependencies.md
rules/unit-test-services.md
rules/e2e-with-supertest.md
rules/override-guards-in-e2e.md
rules/isolated-test-data.md
rules/test-behavior-not-implementation.md
```

Each rule file contains:
- A short explanation of why it matters, tied to the official docs
- An **Incorrect** example (the antipattern)
- A **Correct** example (the idiomatic NestJS + Jest pattern)

All examples target NestJS v10/v11 with the `@nestjs/testing` package and `supertest`.
