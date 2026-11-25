---
name: integration-review
description: Catch defects that appear where two or more layers meet, which per-layer review misses. Use when a change crosses boundaries such as frontend to API, API to service, service to database, auth to route authorization, webhook to database, worker to API, payment provider to frontend, or any external provider to internal state.
---
# Integration Review

## Purpose

Each layer can look correct alone and still disagree at the seam. Trace the real contracts and data across boundaries instead of reviewing only the changed lines.

## Boundaries to Trace

- Frontend to API, including the request the client actually sends.
- API to service and service to service.
- Service to database and database back to caller.
- Authentication to route authorization.
- Webhook sender to internal handler and persistence.
- Worker or queue producer to consumer and API.
- External provider to internal state.

## Checks

- Type and shape mismatches across the boundary.
- Naming mismatches, including casing and pluralization differences.
- Nullable and missing-value behavior on each side.
- Serialization and deserialization: dates, times, timezones, numbers, precision, and encoding.
- Identifier formats, ownership, and tenant or user scoping across the boundary.
- Transaction boundaries: partial writes, work outside the transaction, and non-atomic multi-step operations.
- Stale state and cache invalidation after a mutation.
- Duplicate events, duplicate deliveries, and repeated requests.
- Error and fallback propagation: does a failure on one side produce a correct response on the other?
- Frontend expectations versus actual backend behavior, including loading, empty, and failure states.
- Ordering assumptions and eventual consistency.

## Rules

- Read the real implementation on both sides; do not infer behavior from names.
- Prefer confirming end-to-end flow with a safe test or dry run when one exists.
- Do not duplicate `frontend-review`, `database-review`, `security-review`, or `backend-review`; use this skill for the seams between them.
