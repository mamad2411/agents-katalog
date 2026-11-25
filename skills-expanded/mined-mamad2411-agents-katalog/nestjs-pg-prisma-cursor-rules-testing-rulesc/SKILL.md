---
description: Testing rules for NestJS Prisma backend
globs:
  - "src/**/*.spec.ts"
  - "test/**/*.ts"
  - "jest.config.js"
  - "package.json"
alwaysApply: true
---

# Testing Rules

This project uses unit tests and e2e tests.

## Test Types

- Unit tests live near source files as `*.spec.ts`.
- E2E tests live in `test/e2e` as `*.e2e-spec.ts`.
- Unit tests must not connect to the real database.
- E2E tests must use a dedicated test database.

## Safety Rules

- Never run tests against production database.
- Never run destructive migration reset commands automatically.
- Use `deleteMany` cleanup on the test database only.
- Do not print secrets in test logs.
- Use unique emails for user tests.

## Unit Test Rules

- Mock PrismaService.
- Mock external services.
- Test services, guards, interceptors, filters, and utilities.
- Keep tests fast and deterministic.

## E2E Test Rules

- Use Supertest.
- Use real HTTP requests.
- Use common response assertions.
- Clean database before test files or tests.
- Do not rely on test execution order.

## Common Response Assertions

Success response must include:

- success: true
- statusCode
- message
- data
- timestamp
- path

Error response must include:

- success: false
- statusCode
- message
- error
- timestamp
- path

## Auth Testing Rules

Test:
- signup
- login
- refresh token
- logout
- change password
- profile
- RBAC permissions

## Coverage

Initial coverage target:
- statements: 70
- branches: 60
- functions: 70
- lines: 70

Do not make coverage unrealistically strict in the first implementation.