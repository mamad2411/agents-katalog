---
name: api-openapi
description: "Create or reconcile OpenAPI documentation with implementation. Use to maintain an OpenAPI contract; api-breaking assesses compatibility between versions, and client or SDK generation belongs to api-client."
---

# api-openapi

Create or reconcile OpenAPI documentation with implementation.

## Choose this workflow

Use to maintain an OpenAPI contract; api-breaking assesses compatibility between versions, and client or SDK generation belongs to api-client.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [APIs methods](../../references/packs/api.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **apply**. Apply; existing OpenAPI/schema, implementation, and source-of-truth convention.

**Pack prerequisites:** Interface definitions, producer/consumer source, authentication model, versioning constraints, and isolated test endpoints. External API calls must respect environment, credentials, rate limits, and side-effect scope.

- **Infer from evidence:** Read producer/consumer schemas, error contracts, auth conventions and known supported client versions.
- **Reasonable default:** Keep compatible response and pagination semantics where the brief does not request a breaking change.
- **Ask only when needed:** Ask when contract sources disagree or an unknown consumer changes compatibility; do not require live credentials to write or test an isolated client.

Declared evidence requirements: `project.read`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Reconcile documented paths, schemas, authentication, responses, and examples with actual intended behavior.

Apply: only the requested local changes and relevant isolated verification. Inspect/plan requests remain inspection/planning. External actions require their exact action and target in session authorization.

## Execute

1. Identify the authoritative schema source, then compare its coverage with routes, serializers and route validators.
2. Resolve documentation-versus-code discrepancies in the authoritative source.
3. Validate references, required/null distinctions and representative examples.

## Technical method

- **Inspect:** Identify OpenAPI version, source-of-truth convention, generators, serializers and client usage.
- **Method:** Reconcile path parameters, required/null semantics, security schemes and error responses; regenerate derived artifacts from their source.
- **Avoid misdiagnosis:** OpenAPI 3.0 and 3.1 null/schema semantics differ; a valid schema can still document behavior the server never emits.
- **Check the result:** Validate references/examples with the supported tooling and compare representative real requests/responses against the contract.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [APIs worked example](../../references/examples/api.md).
- The affected project uses Django / DRF: [Django / DRF](../../references/frameworks/django.md).
- The affected project uses FastAPI: [FastAPI](../../references/frameworks/fastapi.md).
- The affected project uses Spring Boot: [Spring Boot](../../references/frameworks/spring-boot.md).

## Decision branches

- **When generated schema disagrees with runtime behavior:** Correct the source of generation or document a deliberate contract change; do not patch generated output alone.

## Deliver and verify

- Validated specification with covered routes and schema/example validation, and a list of remaining runtime discrepancies.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- Examples conform to declared schemas; missing error responses are represented accurately.

## Stop and recover

- Do not silently change runtime behavior to match stale documentation or overwrite generated files without updating their source.

## Example requests

- **Normal (apply):** Reconcile the existing specification with actual request and error schemas.
- **Edge (apply):** Document nullable fields and a rate-limit response omitted from generated output.
- **Blocked (inspect):** Review supplied schema without running the provider; do not claim runtime conformance.
