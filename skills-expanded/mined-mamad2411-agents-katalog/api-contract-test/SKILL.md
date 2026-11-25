---
name: api-contract-test
description: "Verify provider and consumer expectations. Use to implement consumer/provider contract checks; test-integration exercises broader dependency behavior."
---

# api-contract-test

Verify provider and consumer expectations.

## Choose this workflow

Use to implement consumer/provider contract checks; test-integration exercises broader dependency behavior.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [APIs methods](../../references/packs/api.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **apply**. Apply; provider/consumer expectations, versions, fixtures, and test environment.

**Pack prerequisites:** Interface definitions, producer/consumer source, authentication model, versioning constraints, and isolated test endpoints. External API calls must respect environment, credentials, rate limits, and side-effect scope.

- **Infer from evidence:** Read producer/consumer schemas, error contracts, auth conventions and known supported client versions.
- **Reasonable default:** Keep compatible response and pagination semantics where the brief does not request a breaking change.
- **Ask only when needed:** Ask when contract sources disagree or an unknown consumer changes compatibility; do not require live credentials to write or test an isolated client.

Declared evidence requirements: `project.read`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Observable cross-boundary contracts; no reliance on live production state.

Apply: only the requested local changes and relevant isolated verification. Inspect/plan requests remain inspection/planning. External actions require their exact action and target in session authorization.

## Execute

1. Derive assertions from actual consumer assumptions, and control fixture identity and provenance.
2. Verify valid and invalid exchanges, including the real provider boundary when a safe environment exists, and integrate the cases with the relevant checks.

## Technical method

- **Inspect:** Identify independently owned provider/consumer expectations and representative boundary fixtures.
- **Method:** Exercise real serialization and decoding with valid, absent, null, unknown-field and error cases; keep mocks scoped to what they establish.
- **Avoid misdiagnosis:** A provider-generated mock validating itself is circular evidence of compatibility.
- **Check the result:** Run a known incompatible response through the consumer and a valid control; record which real boundary and version were exercised.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [APIs worked example](../../references/examples/api.md).
- The affected project uses Django / DRF: [Django / DRF](../../references/frameworks/django.md).
- The affected project uses FastAPI: [FastAPI](../../references/frameworks/fastapi.md).
- The affected project uses Spring Boot: [Spring Boot](../../references/frameworks/spring-boot.md).

## Decision branches

- **When only mocks can run:** Report consumer behavior and mocked assumptions separately from provider conformance.

## Deliver and verify

- Contract cases with schema and semantic assertions, fixture provenance, provider verification coverage and execution results.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- Removing a required response field fails; implementation changes preserving the contract remain valid.

## Stop and recover

- Do not make mocks the sole evidence that the real provider conforms. Missing provider execution is a stated coverage gap.

## Example requests

- **Normal (apply):** Test invoice producer and consumer contracts against isolated fixtures.
- **Edge (apply):** Test an API returning an optional field as null versus omitting it.
- **Blocked (inspect):** Design contract checks with no provider runtime; do not equate a mock pass with compatibility.
