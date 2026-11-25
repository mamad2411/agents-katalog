---
name: replicate-api-key
description: Create a Replicate API token and configure it for the hosted MCP server, REST calls, and client libraries. Use when Replicate access fails with auth errors or the user is setting up.
---

# Replicate API token setup

## Get a token

1. Create an account at https://replicate.com (GitHub sign-in supported).
2. Generate a token at https://replicate.com/account/api-tokens. Name
   tokens per environment or per app so you can revoke one without breaking
   everything.
3. Billing: add a payment method for real usage; you pay per run (per
   output for official models, per hardware time otherwise).

## Hosted MCP server auth (this plugin)

The connector points at `https://mcp.replicate.com/sse`. On first connect a
web authentication flow opens and asks for your Replicate API token there,
in the browser. The token is stored server-side for your MCP session and is
never exposed to the agent or the chat transcript. If tools start failing
with auth errors, re-run the connect flow and paste a current token.

Do not paste the token into chat; the browser flow is the only place it
belongs.

## Direct API and SDKs

- REST: `Authorization: Bearer $REPLICATE_API_TOKEN` on
  `https://api.replicate.com/v1/...`.
- Python (`pip install replicate`) and JS (`npm install replicate`) clients
  read `REPLICATE_API_TOKEN` from the environment automatically.

```bash
export REPLICATE_API_TOKEN="r8_..."
```

Keep the export in your shell profile or a secrets manager; never commit it
or bake it into images.

## Troubleshooting

- 401 Unauthorized: token revoked, misspelled env var, or a stale token in
  a different environment (check `echo ${REPLICATE_API_TOKEN:0:6}` matches
  the dashboard's token prefix).
- 402 or billing errors: no payment method on file for paid usage.
- 422 on creation is an input problem, not auth; check the model's input
  schema.
- MCP tools failing after months of working: tokens do not expire on their
  own, but re-authing through mcp.replicate.com fixes stored-credential
  drift.

## Hygiene

Rotate immediately if a token leaks (revoke at the same dashboard page),
use separate tokens for CI, local dev, and production, and scope spend by
watching https://replicate.com/account usage pages before and after large
batch jobs.
