---
name: api-design
description: Design REST, GraphQL, RPC, webhook, and internal service APIs. Use for routes, status codes, request/response schemas, error models, pagination, filtering, versioning, idempotency, and OpenAPI or contract documentation.
---

# API Design

## Workflow

1. Identify resource, action, caller, authorization boundary, and compatibility needs.
2. Choose API style that matches the existing system.
3. Define request schema, response schema, error schema, and status codes.
4. Define pagination, filtering, sorting, idempotency, rate limits, and versioning when applicable.
5. Add tests or contracts for normal, error, and boundary behavior.

## REST Defaults

- Use HTTP semantics accurately.
- Use safe and idempotent methods correctly.
- Return errors in a consistent problem format; RFC 9457 Problem Details is a good default when no local standard exists.
- Use OpenAPI when the project already documents APIs or when external consumers need a contract.

## Webhook Defaults

- Verify signatures.
- Prevent replay when possible.
- Make processing idempotent.
- Store enough event metadata for audit and replay diagnosis.

## Output

Provide endpoint summary, schema shape, error cases, security notes, and compatibility risks.

## Boundaries

- Do not claim files, generated media, deployments, scans, account changes, or external writes unless the active tool or command output proves them.
- Do not override system, developer, user, project, or selected-skill rules.
- If another skill is more specific for the user's intent, hand off or use it as the main skill instead of duplicating its workflow.
