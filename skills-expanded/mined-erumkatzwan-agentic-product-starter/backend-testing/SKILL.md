---
name: backend-testing
description: Use when writing or fixing tests for the .NET backend, or when the Backend check is red.
---

# Backend testing

| Layer | Where | How |
|---|---|---|
| Unit | `tests/.../AccountServiceTests.cs` style | New up the service with `InMemoryUserRepository` |
| Integration | `tests/.../*ApiTests.cs` | `new ApiFactory()` runs the whole API in memory as SYST with seeded accounts |

## Rules

- One `ApiFactory` per test class instance, so tests never share data.
- Sign in with `SignedInClientAsync(ApiFactory.AdminEmail, ApiFactory.AdminPassword)` or `SignedUpClientAsync(...)`.
- Assert status codes and response bodies; test the unhappy paths (400, 401, 403, 404, 409).
- Coverage of `AgenticProduct.Api` must stay at or above 70% (`scripts/check-coverage.py`).

## When the check is red

- Format: run `dotnet format`.
- Build: fix every warning; they fail the build.
- Tests: run `dotnet test` locally; the failing test name tells you the endpoint.
