---
name: api-design
description: Review or design stable API contracts. Use when creating a new API, changing an existing contract, designing server/client interaction, adding pagination, filtering, or sorting, exposing an integration endpoint, or changing webhook and API behavior.
---
# API Design

## Principle

Follow the project's existing API conventions. Do not require REST when the project already uses another valid architecture.

## Contract

- Request shape, types, and validation rules.
- Response shape, types, and stable field meanings.
- Naming consistency with existing endpoints and fields.
- Status codes and error contracts: machine-readable error codes, safe messages, and consistent structure.
- Nullable and optional fields: absence must be unambiguous.

## Operations

- Pagination: default page size, maximum size, cursor or offset, and total counts.
- Filtering and sorting: allowed fields, validation, and stable ordering.
- Versioning and backward compatibility: additive changes by default; never silently change field meaning or remove a field other consumers rely on.
- Idempotency for unsafe operations, and retry semantics that clients can rely on.
- Rate limits and abuse protection where the endpoint is exposed or costly.

## Webhooks and Integrations

- Signature verification and replay protection.
- Ordering assumptions, duplicate delivery tolerance, and versioning of the payload.
- Retry behavior expected from the sender, and terminal failure handling.

## Rules

- Validate at the boundary and trust internal types only after validation.
- Never expose internal errors, stack traces, database details, or secrets in responses.
- Keep contracts consistent with the consumers that actually exist in the repository; verify the real callers instead of assuming.
- When changing a contract, state the impact on every known consumer and update them in the same change or explicitly flag the follow-up.
