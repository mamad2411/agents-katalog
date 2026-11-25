---
name: qa-backend-mean
description: "Backend testing for MEAN stack apps. Use when writing and running tests for Express API endpoints, MongoDB operations, authentication flows, and middleware using Jest and Supertest."
---

# Qa Backend Mean

## Purpose

Write and run backend tests for MEAN stack applications. Cover API endpoint testing with Supertest, MongoDB operation testing with in-memory database, authentication flow testing, middleware testing, and integration testing.

## Key Patterns

### Test Structure
- server/__tests__/setup.js — Global test setup (DB connection, cleanup)
- server/__tests__/fixtures/ — Test data factories
- server/__tests__/integration/ — API endpoint tests
- server/__tests__/unit/models/ — Model and utility tests
- server/__tests__/middleware/ — Middleware tests

### Test Setup (MongoDB Memory Server)
- Use MongoMemoryServer for isolated test database
- beforeAll: create memory server, connect mongoose
- afterAll: disconnect, stop server
- afterEach: clear all collections (full isolation between tests)
- Set NODE_ENV=test and JWT_SECRET=test-secret

### Integration Test Pattern (Supertest)
- Import app (not listening server) from server.js
- Use request(app).get/post/put/delete to test endpoints
- Chain .send() for body, .set() for headers, .expect() for status
- Assert: response status, body shape, key field values, side effects (DB state)

### Fixture Factory Pattern
- Default valid data objects for each model
- createX() function that saves to DB and returns document
- getAuthToken() helper: creates user + signs JWT, returns { user, token }
- Override defaults with spread: createUser({ role: 'admin' })

### Auth Testing Pattern
- Test register: success (201), duplicate email (409), validation errors (422)
- Test login: success (200 + token), wrong password (401), non-existent user (404)
- Test protected routes: with valid token (200), without token (401), with invalid token (401)
- Test role-based: authorized role (200), unauthorized role (403)

## Conventions

- Jest as test runner with --detectOpenHandles --forceExit flags
- mongodb-memory-server for isolated test DB — NEVER test against real database
- Supertest for HTTP integration tests — test full request/response cycle
- Test file naming: {name}.test.js
- Each test file: describe block per endpoint, it blocks per scenario
- Test happy path first, then error cases, then edge cases
- Coverage: aim for 80%+ on controllers and middleware, 100% on auth flow
- Export app (not listening server) from server.js for Supertest

## Knowledge Strategy

- **Patterns to capture:** Test patterns for common MEAN features (CRUD, auth, file upload, pagination)
- **Examples to collect:** Complete test files for standard endpoints, fixture factories
- **Update permission:** Agents may freely add/update files in `references/`. Changes to `SKILL.md` or `scripts/` require user approval.
