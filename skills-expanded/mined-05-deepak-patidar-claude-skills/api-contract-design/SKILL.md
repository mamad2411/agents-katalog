---
name: api-contract-design
description: Designing HTTP/REST APIs, request/response shapes, error formats, versioning, pagination, idempotency, and webhooks. Use when adding or changing endpoints, integrating a frontend with a backend, designing public or partner APIs, or when the user says "API design", "endpoint", "REST", "contract", "breaking change", or "webhook".
---

# API Contract Design

An API is a promise. Clients — your own frontend, partners, and AI models writing integrations — build on exactly what you return, including your mistakes. Design every endpoint as if you can never change it, because for practical purposes you can't (only add).

## Contract-first, always

Before writing the handler, write the contract: method, path, auth, request shape, response shape, every error case with its code. Five minutes of contract prevents the frontend and backend from building two different APIs. Keep it wherever it's enforceable — OpenAPI, typed schemas (Pydantic/zod), or at minimum a markdown table — the schema layer IS the documentation if you make it one.

## Shape rules

- **Resources and predictability over cleverness**: plural nouns (`/invoices/{id}`), nesting only one level deep when ownership is intrinsic (`/invoices/{id}/payments`); verbs only for true actions (`/invoices/{id}/cancel`). A developer should guess the next endpoint correctly.
- **Response envelopes are uniform across the whole API**: pick one success shape and ONE error shape (`{"error": {"code", "message"}}`-style) and never deviate. Machine-readable `code` (stable, documented, for programs) + human `message` (for humans, changeable). Clients that parse message strings are a bug you caused.
- **Every list endpoint, from day one**: pagination (limit + cursor/offset), a deterministic default sort, and filters as query params. Retrofitting pagination onto a client that assumes "all rows" is a breaking change.
- Field conventions fixed project-wide: one case style, ISO-8601 timestamps in UTC, money as string-decimal or integer minor units (never JSON floats), booleans not 0/1 strings, `null` vs absent given meaning consistently.
- Return the resource state after mutation (the created/updated object), so clients don't need a follow-up GET.

## Status codes — the short honest set

`200` read/update ok · `201` created · `204` deleted/no body · `400` malformed/validation · `401` who are you · `403` you can't do that (but see threat-model-security: prefer `404` when existence itself is private) · `404` not found *or hidden* · `409` state conflict (duplicate, already-cancelled) · `422` semantic validation if you distinguish it · `429` rate limited · `5xx` our fault, never leaks internals. Don't return `200 {"success": false}` — that lies to every HTTP-aware layer between you and the client.

## Idempotency — the rule everyone skips until it costs money

- GET/PUT/DELETE are naturally idempotent; keep them so.
- Any POST that creates something valuable or moves money accepts an **idempotency key** (client-generated, stored unique): the retry after a timeout must not create a second payment. Networks fail *after* the server succeeds; without this, your client's only options are "maybe duplicate" or "maybe lose it".
- Everything a queue/webhook/cron touches follows the same rule (see system-design).

## Evolution without breakage

Safe: adding optional request fields, adding response fields, adding endpoints/enum-values *clients were told to tolerate*. Breaking: removing/renaming fields, type changes, semantics changes, tightening validation, changing defaults, changing error codes. 

- Clients must ignore unknown response fields (say this in the contract); servers must reject unknown fields only where security demands it.
- When you must break: new field alongside old → dual-write/dual-read → migrate clients → deprecate with a date → remove. Version (`/v2`) only when the surface change is too broad for field-level evolution.
- Your own frontend counts as a client: deploys aren't atomic across app and API; the old frontend will talk to the new API for a while (and cached bundles make "a while" longer than you think).

## Webhooks you emit

Sign payloads (HMAC + timestamp), retry with backoff on non-2xx, provide a redelivery/reconciliation path, and document that consumers must be idempotent. Send a thin event (`type`, `id`, minimal data) and let consumers fetch fresh state — fat payloads go stale in retry queues.

## Review checklist

- Can every error the handler can produce be triggered deliberately, and does each map to the documented envelope + code?
- Does any endpoint return different shapes for the same status? (Fix it.)
- Walk a slow-network retry through every POST: what duplicates?
- Diff against the previous contract: is every change in the "safe" list? If not, where's the migration plan?
- Auth on every route confirmed server-side — including the "internal" ones that are one leaked URL away from public (threat-model-security Gate 2).
