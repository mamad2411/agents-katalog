# Component Integration Test Writing

## Purpose
Tests internal service wiring — UseCase through Repository to real local PostgreSQL — verifying the components assemble correctly.

## Role
Backend Developer

## Phase
Development (after unit tests, before PR)

## Triggered By
Unit tests passing, ready to verify internal integration.

## Inputs
- Passing unit test suite
- Local docker-compose PostgreSQL

## Distinction
Not QA's API integration tests (which test external contract). This tests: does the internal assembly produce correct results with a real database?

## Process

### Mocks (in component integration tests)
- External gRPC services: mock (not available locally)
- Kafka broker: mock (use SIT Kafka only — not local)
- Redis: mock or real (depends on whether Redis is part of the test)

### Real (in component integration tests)
- PostgreSQL: real local docker compose instance
- Business logic: no mocks — real execution

Test location: `apps/servers/{service}/src/test/integration/`

### Steps
1. Set up test database (use separate test database from dev database).
2. Run migrations on test database before tests.
3. Test UseCase → Repository → PostgreSQL full chain.
4. Clean up test data after each test (use `beforeEach`/`afterEach`).
5. Tests must pass with fresh database (no dependency on existing data).

## Outputs
Passing component integration test suite.

## Quality Gates
- [ ] Real PostgreSQL used (not mocked)
- [ ] External services mocked
- [ ] Test database separate from dev database
- [ ] Data cleaned up after each test
- [ ] Tests pass from fresh database state

## References
- `.claude/skills/backend-developer/unit-test-writing/SKILL.md`
- `.claude/skills/qa-engineer/integration-test-case-design/SKILL.md`
