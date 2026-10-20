---
name: enterprise-test-suites
description: Comprehensive testing matrix spanning Unit, Integration, E2E (Playwright), Contract (Pact), Chaos/Fault-Injection, Mutation, Load/Stress (k6), and Security Fuzz testing.
version: 1.0.0
---

# Enterprise Multi-Tier Test Suite Engineering Skill

This skill defines industry standards for implementing a resilient, multi-tiered test pyramid for mission-critical enterprise applications.

---

## 1. The Enterprise Testing Matrix

```
                      / \
                     /   \
                    / E2E \       → Playwright / Cypress UI workflows
                   /-------\
                  / Contract\     → Pact / OpenAPI Consumer-Provider validation
                 /-----------\
                / Integration \   → Testcontainers (Postgres, Redis, Kafka)
               /---------------\
              /      Unit       \ → Vitest / Jest / PyTest (>80% branch coverage)
             /-------------------\
            / Specialized Suites  \
           /-----------------------\
          • Chaos & Fault Injection (Simulate network drop, latency, node crash)
          • Load & Performance (k6 / Artillery latency & concurrency benchmarks)
          • Security & Property Fuzzing (Malformed payload injection)
          • Mutation Testing (Stryker / mutmut test-quality validation)
```

---

## 2. Test Suite Specifications

### A. Unit Test Suite (`*.spec.ts` / `*_test.go`)
- **Focus**: Pure business logic, domain models, mathematical formulas, and validators.
- **Rules**: Fast (<5ms per test), zero external I/O, deterministic mocking.
- **Coverage**: Target >80% line and branch coverage.

### B. Integration Test Suite (`*.integration.spec.ts`)
- **Focus**: Database repositories, ORM queries, cache layers, external API clients, and queue consumers.
- **Standard**: Use ephemeral real dependencies with **Testcontainers** (Postgres, Redis, Kafka, LocalStack).
- **Invariants**: Test database transactions, rollback on failure, connection pools, and migration compatibility.

### C. Consumer-Driven Contract Test Suite (`*.contract.spec.ts`)
- **Focus**: Microservices API boundaries and webhook contracts.
- **Tooling**: Pact / MSW.
- **Invariants**: Assert request/response schemas, error codes, and headers without deploying the full fleet.

### D. End-to-End (E2E) Test Suite (`tests/e2e/*.spec.ts`)
- **Focus**: Critical user journeys (e.g. User Signup -> Policy Selection -> Payout -> Invoice Generation).
- **Tooling**: Playwright headless browser runners with parallel workers and video/trace capture on failure.

### E. Load & Stress Test Suite (`tests/perf/*.js`)
- **Tooling**: **k6** or **Artillery**.
- **Scenarios**:
  - *Load Test*: Target expected average RPS (e.g. 500 RPS) for 10 minutes; assert p95 latency < 150ms.
  - *Spike Test*: 10x instant burst to verify auto-scaling and rate-limiting resilience.
  - *Soak Test*: Sustained traffic for 2 hours to detect memory leaks and connection exhaustion.

### F. Chaos & Fault Injection Test Suite (`tests/chaos/*.ts`)
- **Focus**: Distributed resilience and graceful degradation.
- **Simulations**:
  - Database primary failover mid-transaction.
  - 500ms artificial network latency on Redis/Kafka.
  - External third-party payment gateway 503 outage (verify circuit breaker and fallback queue).

### G. Security & Property-Based Fuzzing (`tests/fuzz/*.ts`)
- **Tooling**: Fast-check / Atheris.
- **Focus**: Property-based invariance testing with randomized edge-case inputs (overflow numbers, null bytes, unicode emojis, SQL fragments).

---

## 3. Test Suite Organization Standard

```
tests/
├── unit/                 ← Fast isolated unit tests
├── integration/          ← Testcontainers-backed DB & API integration tests
├── contract/             ← Pact consumer/provider verification
├── e2e/                  ← Playwright browser journeys
├── perf/                 ← k6 load, spike, and soak test scripts
├── chaos/                ← Circuit breaker & fault-injection simulations
└── fuzz/                 ← Property-based fuzzing harnesses
```
