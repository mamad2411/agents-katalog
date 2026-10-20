---
name: api-breaking
description: "Identify backward-incompatible API changes. Use to assess consumer impact of a change; api-design creates the intended contract; for events and messages see arch-contracts."
---

# api-breaking

Identify backward-incompatible API changes.

## Choose this workflow

Use to assess consumer impact of a change; api-design creates the intended contract; for events and messages see arch-contracts.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [APIs methods](../../references/packs/api.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **inspect**. Inspect; old/new contracts or revisions, consumer expectations, and compatibility policy.

**Pack prerequisites:** Interface definitions, producer/consumer source, authentication model, versioning constraints, and isolated test endpoints. External API calls must respect environment, credentials, rate limits, and side-effect scope.

- **Infer from evidence:** Read producer/consumer schemas, error contracts, auth conventions and known supported client versions.
- **Reasonable default:** Keep compatible response and pagination semantics where the brief does not request a breaking change.
- **Ask only when needed:** Ask when contract sources disagree or an unknown consumer changes compatibility; do not require live credentials to write or test an isolated client.

Declared evidence requirements: `project.read`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Backward compatibility across schemas, semantics, authentication, errors, and timing/order guarantees.

No source changes in inspect/plan. Save only requested planning artifacts. A separately requested repair uses the relevant implementation workflow.

## Execute

1. Identify affected consumers, then diff the versions: field presence and types, enum values, validation, defaults, error/status behavior, pagination and timing guarantees.
2. Classify compatibility impact per consumer and propose rollout and deprecation steps.

## Technical method

- **Inspect:** Compare old/new payloads, enums, validation, errors, pagination and authentication using known consumers.
- **Method:** Classify wire, semantic and operational compatibility separately; propose a migration when old clients cannot interpret the new result.
- **Avoid misdiagnosis:** An additive enum value or new required permission can break clients even without deleting a field.
- **Check the result:** Run old consumer fixtures against the proposed provider and identify a deployment sequence that preserves supported versions.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [APIs worked example](../../references/examples/api.md).
- The affected project uses Django / DRF: [Django / DRF](../../references/frameworks/django.md).
- The affected project uses FastAPI: [FastAPI](../../references/frameworks/fastapi.md).
- The affected project uses Spring Boot: [Spring Boot](../../references/frameworks/spring-boot.md).

## Decision branches

- **When a syntactically additive change affects strict decoders or behavior:** Classify its actual consumer impact and propose rollout/deprecation evidence.

## Deliver and verify

- Change/consumer/impact matrix with examples, compatibility bridges or migration options, and unknown consumers.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- Narrowed validation is recognized as potentially breaking; an additive field is evaluated against actual strict-client behavior.

## Stop and recover

- Missing consumer information prevents universal compatibility claims. Do not equate schema compatibility with semantic compatibility.

## Example requests

- **Normal (inspect):** Compare these API versions for validation and response-contract breaks.
- **Edge (inspect):** Review a new enum value and a stricter validation rule for old clients.
- **Blocked (inspect):** Assess compatibility without consumer source; avoid declaring universal backward compatibility.
