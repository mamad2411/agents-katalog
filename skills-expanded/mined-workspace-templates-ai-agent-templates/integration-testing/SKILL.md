---
name: integration-testing
description: Writes integration tests that use real databases and services, each with isolated data and fixed setup, so they are trustworthy and repeatable.
---

# Integration testing

Test the seams: your code against the real database, queue, cache or HTTP service.

## Steps

1. Pick the seams worth covering: repositories and migrations, HTTP routes with the real middleware, message consumers, clients of external APIs. Leave pure logic to unit tests.
2. Provide real dependencies. Use Testcontainers or docker compose with pinned image versions that match production. For third-party HTTP services use a local fake server or recorded fixtures (WireMock, nock, MSW), never the live service.
3. Setup once per run: start containers, apply real migrations, wait for readiness by health check, not by sleep.
4. Isolate each test: wrap it in a transaction that rolls back, or truncate touched tables, or give each worker its own schema. Create the data the test needs inside the test with small factory helpers. No shared fixtures that tests mutate.
5. Make time and randomness deterministic: inject a clock, seed generators, fix the time zone and locale.
6. Assert on observable results: rows stored, response status and body, messages published. Avoid asserting on SQL text or call counts.
7. Test failure paths too: unique violation, timeout, a 500 from the fake service, a retry.
8. Keep it quick: reuse the container, run files in parallel when data is isolated, and tag slow tests so they run in CI.

## Rules

- No `sleep` for synchronization; poll with a timeout.
- Tests must pass in any order and when run alone.
- Never point a test at a shared or production database.

## Report

Seams covered, the setup used, how isolation works, run time, and flakiness checks (run the suite three times).
