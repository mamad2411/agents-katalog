---
name: integration-contract
description: Design integration/contract tests for a service boundary — consumer-driven contracts, stub-vs-hit, fixtures, failure modes. Boundary tests, not unit tests (unit-tests) or the plan (test-strategy).
---

# integration-contract

> Test the seams between components and services — where unit tests can't reach and full e2e is too slow and flaky.

## When to use

- A service talks to another service, a DB, a queue, or an external API and you need confidence at that boundary.
- You want consumer-driven contract tests so a provider change can't silently break a consumer.
- A workflow invokes `polymath-qa:integration-contract`.

This designs *boundary* tests. It is not unit testing (`polymath-qa:unit-tests`), the cross-layer plan (`polymath-qa:test-strategy`), or smell review (`polymath-qa:test-smell`).

## Inputs

- The boundary under test: the components/services and the contract (schema, endpoints, messages).
- Which side you own (consumer, provider, or both).
- Available test doubles / sandboxes / ephemeral environments.

## Procedure

1. **Map the boundary** — list every interaction (request/response, event, query) and its contract.
2. **Stub vs hit** — decide per dependency: stub third-party + nondeterministic; hit owned infra via an ephemeral instance or testcontainer. State the rule you applied.
3. **Contract tests** — for each interaction, pin the schema/shape both sides agree on; consumer-driven where you own the consumer. A provider change that breaks the contract must fail a test.
4. **Failure modes** — cover timeout, 5xx, malformed payload, partial write, retry/idempotency, not just the happy path.
5. **Fixtures/data** — define deterministic setup + teardown; no shared mutable state between tests.
6. List the tests with their boundary, stub/hit decision, and the failure mode each covers.

## Quality bar

- Every owned boundary has a contract test that fails on a breaking change.
- Each test states stub-vs-hit and why; nondeterministic dependencies are stubbed.
- At least the timeout + error + malformed-input failure modes are covered, not only success.
