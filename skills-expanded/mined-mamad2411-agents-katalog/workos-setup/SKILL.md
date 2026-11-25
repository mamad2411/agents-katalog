---
name: workos-setup
description: WorkOS API keys, environments, redirect URIs, webhook signature verification, and the docs MCP server. Use on first-time setup or when requests fail with auth or signature errors.
---

# WorkOS setup

## Keys and environments

Every WorkOS environment (Staging and Production out of the box) has its own:

- **API key** (`sk_...`): server-only secret, passed to SDK constructors or
  `WORKOS_API_KEY`. Create named keys per system so revocation is surgical.
- **Client ID** (`client_...`): public identifier used in OAuth/AuthKit flows,
  `WORKOS_CLIENT_ID`.

```bash
WORKOS_API_KEY=sk_example_123
WORKOS_CLIENT_ID=client_example_123
WORKOS_COOKIE_PASSWORD=<openssl rand -base64 32>   # AuthKit session encryption
NEXT_PUBLIC_WORKOS_REDIRECT_URI=https://app.example.com/auth/callback
```

Rules:

- Staging and production keys are unrelated; configure redirect URIs,
  webhooks, and roles in each environment separately.
- Never ship `sk_` keys to a browser bundle or repo; if one leaks, roll it in
  Dashboard > API Keys (create new, deploy, revoke old).
- The API key grants management access to users and orgs: scope who on the
  team can see production keys.

## Redirect URIs

Dashboard > Redirects: register every callback exactly (scheme, host, port,
path). Add `http://localhost:3000/auth/callback` in staging for local dev and
the deployed URLs per environment. Mismatches are the top cause of
`invalid_redirect_uri` errors.

## Webhooks

Dashboard > Webhooks: add your endpoint per environment and subscribe to the
events you handle (`user.created`, `dsync.*`, `connection.*`, ...). Each
endpoint has a signing secret. Verify every delivery:

```ts
// Express-style: use the RAW body, not parsed JSON
const event = await workos.webhooks.constructEvent({
  payload: req.body,                       // raw string/bytes
  sigHeader: req.headers["workos-signature"],
  secret: process.env.WORKOS_WEBHOOK_SECRET,
  tolerance: 180_000,                      // ms, rejects stale/replayed events
});
```

- Reject on any verification failure with 4xx; respond 2xx fast and process
  async.
- Handlers idempotent (WorkOS retries).
- Exclude the webhook route from auth middleware; the signature is its auth.
- One secret per endpoint per environment; store in the secret manager.

## SDK install matrix

```bash
npm i @workos-inc/node                 # backend (v9 line)
npm i @workos-inc/authkit-nextjs       # Next.js App Router helpers
pip install workos                     # Python
gem install workos                     # Ruby
```

## Docs MCP server

This plugin ships the official WorkOS documentation MCP server:

```bash
npx -y @workos/mcp-docs-server
```

It exposes search-then-read tools (`workos_search`, then `workos_docs`,
`workos_examples`, `workos_changelogs`) over current WorkOS docs, examples,
and changelogs. It is read-only documentation access: it needs no API key and
cannot touch your WorkOS data, so it is safe to run before any setup.

## Troubleshooting

- `401 Unauthorized`: wrong environment's API key, or key revoked.
- `invalid_redirect_uri`: URI not registered in this environment.
- Signature verification fails: parsed body instead of raw, wrong endpoint
  secret, or clock skew beyond tolerance.
- AuthKit cookie errors: `WORKOS_COOKIE_PASSWORD` shorter than 32 chars or
  differs across instances behind a load balancer.
