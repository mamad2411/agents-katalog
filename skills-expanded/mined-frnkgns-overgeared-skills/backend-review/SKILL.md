---
name: backend-review
description: Review server-side logic that is not purely database or security work. Use for API handlers, server functions, services, jobs, workers, event processing, webhooks, background tasks, external-service integrations, and business-logic changes.
---
# Backend Review

Review the server-side behavior of the change: correctness of logic, service boundaries, and asynchronous behavior.

## Boundaries and Logic

- Request validation at the entry point, and trust assumptions between internal modules.
- Business rules enforced in one canonical place rather than duplicated per caller.
- Clear service boundaries: no duplicated logic across handlers, and no hidden coupling.
- Correct use of server-side state instead of client-provided values.

## Asynchronous Behavior

- Concurrency and race conditions on shared state.
- Retries: what is retried, backoff, and what is not safe to retry.
- Idempotency for create, payment, and webhook style operations.
- Timeouts on every external call, including connect and total time budgets.
- Error propagation: preserve the real cause while keeping internals out of user-facing output.
- Resource cleanup for connections, file handles, locks, and temporary files.
- Duplicate processing from replays, redelivery, and at-least-once queues.

## External Services

- Failure and partial-failure handling for third-party calls.
- Rate limits, quotas, and backpressure.
- Payload or response size limits and unexpected response shapes.
- No secrets or sensitive payloads sent to, or logged by, external providers.

## Rules

- Delegate query, schema, and migration concerns to `database-review`.
- Delegate authentication, authorization, and secret-handling concerns to `security-review`.
- Do not duplicate the workflows in those skills; use them for those concerns instead.
