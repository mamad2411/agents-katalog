---
name: api-webhooks
description: "Implement signatures, retries, replay handling, and delivery tracking. Use for authenticated durable event receipt or signed outbound delivery; integrate wires the provider itself and backend-jobs handles deferred processing."
---

# api-webhooks

Implement signatures, retries, replay handling, and delivery tracking.

## Choose this workflow

Use for authenticated durable event receipt or signed outbound delivery; integrate wires the provider itself and backend-jobs handles deferred processing.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [APIs methods](../../references/packs/api.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **apply**. Apply; inbound/outbound direction, provider contract, signing method, events, and environment.

**Pack prerequisites:** Interface definitions, producer/consumer source, authentication model, versioning constraints, and isolated test endpoints. External API calls must respect environment, credentials, rate limits, and side-effect scope.

- **Infer from evidence:** Read producer/consumer schemas, error contracts, auth conventions and known supported client versions.
- **Reasonable default:** Keep compatible response and pagination semantics where the brief does not request a breaking change.
- **Ask only when needed:** Ask when contract sources disagree or an unknown consumer changes compatibility; do not require live credentials to write or test an isolated client.

Declared evidence requirements: `project.read`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Verification, delivery/retry, replay handling, event ordering, and tracking for the specified integration.

Apply: only the requested local changes and relevant isolated verification. Inspect/plan requests remain inspection/planning. External actions require their exact action and target in session authorization.

## Execute

1. Verify signatures over the provider-specified raw bytes and time rules, comparing in constant time and accepting current and previous secrets during a bounded rotation period.
2. Persist receipt identity before acknowledgment, and separate durable deduplication from business processing.
3. Test invalid, duplicate, delayed and reordered messages.

## Technical method

- **Inspect:** Read the provider's signature contract, raw-body handling, timestamp tolerance, event IDs and retry/order semantics.
- **Method:** Verify authentic bytes before side effects with a constant-time comparison (for example crypto.timingSafeEqual or hmac.compare_digest), accepting current and previous secrets during a bounded rotation period; durably deduplicate delivery and business effects, and handle out-of-order versions deliberately.
- **Avoid misdiagnosis:** Re-serialized JSON changes signed bytes; a valid signature does not prevent replay or duplicate processing.
- **Check the result:** Test altered body, invalid/stale signature, a delivery signed with the previous secret during rotation, concurrent duplicate, reversed event order and a crash before acknowledgment with synthetic fixtures.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [APIs worked example](../../references/examples/api.md).
- Identity, ownership, tenant isolation, replay or privilege changes affect the task: [Identity and authorization](../../references/security/identity.md).
- The affected project uses Django / DRF: [Django / DRF](../../references/frameworks/django.md).
- The affected project uses FastAPI: [FastAPI](../../references/frameworks/fastapi.md).
- The affected project uses Spring Boot: [Spring Boot](../../references/frameworks/spring-boot.md).

## Decision branches

- **When valid events arrive out of order or concurrently:** Apply version/ordering policy and durable effect deduplication rather than assuming arrival order.
- **When sending webhooks to customer-supplied URLs:** Validate destinations after DNS resolution (block private, loopback and link-local ranges; limit redirects), sign id.timestamp.body with a per-endpoint rotatable secret, give each event a stable ID, retry with bounded exponential backoff and jitter, record every attempt, and disable persistently failing endpoints. Test against a private-IP target and a redirecting endpoint.

## Deliver and verify

- Webhook implementation and configuration names, a receipt/processing state machine, and invalid, replayed, duplicate and reordered checks.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- Invalid signatures cause no business effect; retried events do not duplicate the intended effect.

## Stop and recover

- Never log signing secrets or send real business events without authorization. Provider uncertainty must be resolved before relying on delivery guarantees.

## Example requests

- **Normal (apply):** Implement signed webhook validation and durable duplicate handling in the sandbox.
- **Edge (apply):** Handle two concurrent copies of a signed payment event.
- **Blocked (inspect):** Review webhook handling without live signing keys or sending real business events.
