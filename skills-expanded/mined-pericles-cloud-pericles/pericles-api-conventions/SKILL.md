---
name: pericles-api-conventions
version: 2026.05.0
description: >
  How API endpoints in Pericles validate input, shape responses, and enforce tenant
  scope. Use this WHENEVER you add or change an HTTP endpoint (Express auth-server or a
  Next.js route handler). Encodes the Zod request-validation pattern, the
  {success, data, metadata} response envelope, the canonical 10-risk-type enum, error
  shape, and the rule that organization_id is always validated server-side, never
  trusted from the client.
doctrine_refs: [Security §2; Ops §1]
depends_on: [pericles-tenant-isolation, pericles-mastra-tool, pericles-frontend-foundations]
last_reconciled: 2026-05-28
---

# Pericles API Conventions (build skill)

The frontend, mobile, partner integrations, and the auth-server all talk over the same
API. One shape, one validation discipline, one tenant-scoping rule — codified in
`.claude/rules/09-api.md` and applied here.

## When to use this skill

Adding/changing any HTTP endpoint — Express on the auth-server, Next.js route handlers,
or webhook receivers.

## Request validation (Zod, always)

Every endpoint validates its body with a Zod schema before doing anything else; an
invalid request short-circuits to 400 with the validation error. From the rule:

```ts
import { z } from 'zod';

const TriggerMonitoringSchema = z.object({
  organization_id: z.string().uuid(),
  risk_types: z.array(z.enum([
    'WEATHER', 'POLITICAL', 'CYBER', 'ECONOMIC', 'NEWS',
    'MARITIME', 'LABOR', 'REGULATORY', 'PANDEMIC', 'GEOPOLITICAL',
  ])).optional(),
  location: z.object({
    lat: z.number().min(-90).max(90),
    lon: z.number().min(-180).max(180),
  }).optional(),
});

export async function POST(request: Request) {
  const body = await request.json();
  const validated = TriggerMonitoringSchema.parse(body);
  // ...
}
```

The 10-risk-type enum is canonical (matches the 10 Topical monitor tools,
`pericles-topical-skill`). Reuse the enum, don't redeclare it.

## Response envelope (success/data/metadata)

```ts
return Response.json({
  success: true,
  data: result,
  metadata: { /* request_id, timing, version, etc. */ },
});
```

Errors follow the inverse — `{ success: false, error: { code, message, details? } }`
with the right HTTP status. No bare data blobs; no mixing success/error shapes; clients
parse one envelope.

## Tenant scoping at the API boundary (non-negotiable)

`organization_id` in a request body is **input**, not authorization. The endpoint must
verify the authenticated user has access to that org via `UserOrganization` before
doing any work (`pericles-tenant-isolation` guarantee 1). A client that submits another
tenant's `organization_id` gets 403, not 200. This is the same rule Mastra tools follow
(`pericles-mastra-tool`).

## Error handling

- Validation errors → 400 with the Zod issues.
- Auth failures → 401 / 403, never 404 (don't leak existence).
- Internal errors → 500 with a request id, **never** the stack to the client; log the
  stack with `tool-logger`/Pino (`pericles-observability`).
- Idempotency: writes accept an idempotency key where appropriate; retries don't
  double-act.

## Auth & headers

JWT via the auth-server; Google OAuth + (in Standard/Enterprise) SSO; CORS configured
per environment. The realtime channel is `socket.io` and follows the same tenant rules
(per-tenant rooms).

## What this forbids

Endpoints without Zod validation; trusting a client-supplied `organization_id`; bare
data blobs without the envelope; returning stacks/internal errors to clients; mixing
the success/error shapes; redeclaring the risk-type enum or other domain enums.

## Verification

Every endpoint validates input with Zod; the response envelope is consistent; the
authenticated user is verified to own the `organization_id` before work; errors map to
the right status and don't leak internals; integration tests cover unauthorized
cross-tenant access (returns 403, not 200).

## Existing standards (read alongside)

`.claude/rules/09-api.md`; `backend/src/server/` (auth-server); `pericles-tenant-isolation`,
`pericles-mastra-tool`.

## Open questions

- Whether the Next.js frontend talks to the Express auth-server directly or through
  Next.js route handlers acting as a BFF — decide and document the boundary.
- Versioning (URL `/v1/…` vs header) — choose before public APIs ship.

## Changelog

- 2026.05.0 — Initial draft from `.claude/rules/09-api.md`; consolidated the request/
  response/error/scoping rules.
