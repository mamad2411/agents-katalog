---
name: api-errors
description: "Standardize useful error responses and propagation. Use to standardize error behavior without changing business policy; api-design defines a new contract."
---

# api-errors

Standardize useful error responses and propagation.

## Choose this workflow

Use to standardize error behavior without changing business policy; api-design defines a new contract.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [APIs methods](../../references/packs/api.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **apply**. Apply; API scope, current error format, consumers, and logging requirements.

**Pack prerequisites:** Interface definitions, producer/consumer source, authentication model, versioning constraints, and isolated test endpoints. External API calls must respect environment, credentials, rate limits, and side-effect scope.

- **Infer from evidence:** Read producer/consumer schemas, error contracts, auth conventions and known supported client versions.
- **Reasonable default:** Keep compatible response and pagination semantics where the brief does not request a breaking change.
- **Ask only when needed:** Ask when contract sources disagree or an unknown consumer changes compatibility; do not require live credentials to write or test an isolated client.

Declared evidence requirements: `project.read`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Error status, machine-readable codes, safe messages, propagation, and trace correlation.

Apply: only the requested local changes and relevant isolated verification. Inspect/plan requests remain inspection/planning. External actions require their exact action and target in session authorization.

## Execute

1. Inventory existing client-visible codes and shapes and the compatibility they must preserve.
2. Map domain failures to stable public errors deliberately, redacting internal details while preserving safe correlation IDs.
3. Test representative client and server failures: validation, authorization, dependency and unexpected errors.

## Technical method

- **Inspect:** Inventory exception sources, status semantics, domain codes, request IDs and retry behavior.
- **Method:** Map expected domain failures to stable public errors; redact internal details while retaining correlated server diagnostics.
- **Avoid misdiagnosis:** Returning 200 with an error-shaped body or retryable status for a permanent denial misleads clients.
- **Check the result:** Exercise invalid input, forbidden resource, dependency timeout and unexpected exception; verify public redaction and useful internal correlation.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [APIs worked example](../../references/examples/api.md).
- The affected project uses Django / DRF: [Django / DRF](../../references/frameworks/django.md).
- The affected project uses FastAPI: [FastAPI](../../references/frameworks/fastapi.md).
- The affected project uses Spring Boot: [Spring Boot](../../references/frameworks/spring-boot.md).

## Decision branches

- **When changing a code would break a known consumer:** Add a compatibility path or a versioned transition instead of silently normalizing it.
- **When no published error contract exists:** Prefer RFC 9457 Problem Details (application/problem+json) with stable type URIs and extension members for field errors; never break an existing published shape.

## Deliver and verify

- Error taxonomy and documented contract, the mapping locations, and checks for validation, authorization and dependency failures.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- Validation errors identify usable field problems; unexpected failures do not leak stack traces or credentials.

## Stop and recover

- Do not turn all failures into success responses or change public codes silently. Unknown consumer reliance needs compatibility handling.

## Example requests

- **Normal (apply):** Standardize safe API errors while preserving published machine-readable codes.
- **Edge (apply):** Standardize errors while preserving a client's retry behavior on conflict.
- **Blocked (inspect):** Review errors from source without provoking real service failures.
