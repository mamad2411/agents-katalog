---
name: clerk-backend
description: Use the Clerk backend SDK, verify session JWTs networklessly, authenticate requests outside Next.js, and verify webhook signatures. Use when the user builds APIs or backend services against Clerk.
---

# Clerk backend

Package: `@clerk/backend` (framework-agnostic; the Next.js SDK re-exports most
of it). Needs `CLERK_SECRET_KEY` server-side.

## Backend client (management API)

```ts
import { createClerkClient } from "@clerk/backend";

const clerk = createClerkClient({ secretKey: process.env.CLERK_SECRET_KEY });

const user = await clerk.users.getUser(userId);
const list = await clerk.users.getUserList({ emailAddress: ["a@b.com"] });
await clerk.users.updateUserMetadata(userId, { publicMetadata: { plan: "pro" } });
const orgs = await clerk.organizations.getOrganizationList();
```

Metadata rules: `publicMetadata` is readable client-side (never store
secrets), `privateMetadata` is backend-only, `unsafeMetadata` is
client-writable (treat as untrusted input, validate before use).

## Authenticating requests in any backend

```ts
import { createClerkClient } from "@clerk/backend";

const clerk = createClerkClient({
  secretKey: process.env.CLERK_SECRET_KEY,
  publishableKey: process.env.CLERK_PUBLISHABLE_KEY,
});

const { isAuthenticated, toAuth } = await clerk.authenticateRequest(request, {
  authorizedParties: ["https://yourapp.com"],   // set this: blocks CSRF via subdomain tokens
});
if (!isAuthenticated) return unauthorized();
const { userId, sessionClaims } = toAuth();
```

`authenticateRequest` handles both cookie-based sessions (same-origin) and
`Authorization: Bearer <token>` (cross-origin/native) and verifies
networklessly using the instance JWKS.

## Manual JWT verification

```ts
import { verifyToken } from "@clerk/backend";

const payload = await verifyToken(token, {
  secretKey: process.env.CLERK_SECRET_KEY,   // fetches + caches JWKS
  authorizedParties: ["https://yourapp.com"],
});
// payload.sub = userId; payload.exp/nbf already enforced
```

Verify, in order: signature (JWKS), `exp` and `nbf`, `azp` against your
origins. Session tokens are short-lived (60s) and auto-refreshed by
Clerk's frontend; do not cache them server-side.

## Webhook verification (svix signatures)

Clerk signs webhooks with svix. Verify before trusting any payload:

```ts
// Next.js route handler, with @clerk/nextjs installed
import { verifyWebhook } from "@clerk/nextjs/webhooks";

export async function POST(req: Request) {
  try {
    const evt = await verifyWebhook(req);   // uses CLERK_WEBHOOK_SIGNING_SECRET
    switch (evt.type) {
      case "user.created": /* provision */ break;
      case "user.deleted": /* clean up */ break;
    }
    return new Response("ok");
  } catch {
    return new Response("invalid signature", { status: 400 });
  }
}
```

Outside Next.js, verify with the `svix` library and the endpoint's signing
secret (`svix-id`, `svix-timestamp`, `svix-signature` headers over the raw
body). Always verify against the raw body bytes, not a re-serialized parse.

Webhook rules:

- The webhook route must be public (exclude it from auth middleware).
- Handlers must be idempotent; svix retries on non-2xx.
- Treat webhook data as eventually consistent; fetch the current object via
  the backend client when you need authoritative state.

## Hardening checklist

- Secret key only in server env; separate keys per environment.
- Set `authorizedParties` everywhere tokens are verified.
- Rate limit and log auth failures on custom endpoints.
- Never mint your own long-lived tokens from Clerk sessions; use short-lived
  session tokens or JWT templates with minimal claims.
