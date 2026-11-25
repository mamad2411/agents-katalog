---
name: testing-strategy
description: Comprehensive testing strategy covering unit, integration, E2E, and property-based testing.
---

# Testing Strategy

Multi-layer testing for robust, maintainable code.

## Test Pyramid
1. **Unit Tests** (70%): Fast, isolated, test individual functions/modules
2. **Integration Tests** (20%): Test component interactions, real databases
3. **E2E Tests** (10%): Full user flows, browser/API level

## Unit Testing
- **JavaScript/TypeScript**: Vitest, Jest, bun:test
- **Python**: pytest, unittest, hypothesis
- **Go**: testing, testify, table-driven tests
- **Rust**: cargo test, proptest, insta for snapshots

## Integration Testing
- **API**: Supertest, httpx, testcontainers
- **Database**: Testcontainers, in-memory DB, transaction rollback
- **Message Queue**: Embedded Kafka/RabbitMQ, test events
- **External Services**: Mock servers, WireMock, Pact contracts

## E2E Testing
- **Browser**: Playwright, Cypress, Selenium
- **API**: Postman/Newman, k6, Karate
- **Mobile**: Appium, Detox, XCUITest

## Advanced Testing
- **Property-Based**: Hypothesis, fast-check, quickcheck — generate test cases
- **Mutation Testing**: Stryker, mutmut — verify test quality
- **Snapshot Testing**: Jest snapshots, Insta — catch unintended changes
- **Fuzzing**: libFuzzer, AFL, cargo-fuzz — find crashes
- **Load Testing**: k6, Gatling, Locust — performance under load
- **Chaos Testing**: Chaos Monkey, Litmus — resilience testing

## Test Best Practices
1. AAA pattern: Arrange, Act, Assert
2. One assertion per test (or one concept per test)
3. Test behavior, not implementation
4. Name tests descriptively: `should_X_when_Y`
5. Use fixtures/builders for test data
6. Clean up after tests (no shared state)
7. Test edge cases: null, empty, boundary, concurrent

## Coverage
- Statement coverage: lines executed
- Branch coverage: branches taken
- Function coverage: functions called
- Aim for meaningful coverage, not 100%
