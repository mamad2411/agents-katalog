---
name: ramp-setup
description: Set up Ramp developer access, create a developer app, pick grant types and scopes, mint tokens, use the sandbox, and connect the official Ramp MCP server. Use when configuring Ramp credentials or environments.
---

# Ramp Developer Setup

## Create a developer app

In the Ramp dashboard (admin/owner role required), open the developer
settings (Settings > Developer API) and create an app. You receive a
`client_id` and `client_secret`. Then:

1. Choose grant types: **client_credentials** for internal server-to-server
   work; **authorization_code** for apps acting on behalf of users (add
   redirect URIs; they must be exact https:// hosts or
   localhost/127.0.0.1, no wildcards).
2. Enable only the scopes the integration needs (read scopes first:
   `transactions:read`, `reimbursements:read`, `users:read`,
   `business:read`; add write scopes only with a concrete reason).
3. Store the secret in a secret manager immediately. Never commit it,
   never paste it into chat, rotate it if it ever leaks.

## Environments

Sandbox and production are fully separate: create one app in each.

- Sandbox: `https://demo-api.ramp.com/developer/v1` against a demo
  business with fake data; safe for iteration and CI.
- Production: `https://api.ramp.com/developer/v1`; real corporate
  financial data, so land here only after sandbox flows pass.

Keep base URL + credentials as one config unit (e.g. `RAMP_ENV`,
`RAMP_CLIENT_ID`, `RAMP_CLIENT_SECRET`) so an environment mixup fails auth
instead of silently reading the wrong data.

## Mint a token (client_credentials)

```bash
curl -X POST "$RAMP_BASE/token" \
  -u "$RAMP_CLIENT_ID:$RAMP_CLIENT_SECRET" \
  -d grant_type=client_credentials \
  -d scope="transactions:read users:read"
```

Tokens from this grant last 10 days; cache and reuse. Authorization-code
access tokens last 1 hour with refresh tokens; refresh proactively. Full
details and endpoint shapes in `ramp-api`.

## Connect the official Ramp MCP server

This plugin ships Ramp's hosted server: `https://mcp.ramp.com/mcp`
(exact URL, no trailing slash). Auth is OAuth: sign in with your Ramp
account when the client prompts. Notes:

- Access mirrors your Ramp role; company-wide data (all transactions,
  bills, reimbursements) generally requires admin-level access.
- Admins manage who can use it under Company > Integrations > Ramp MCP >
  Manage Access (by role, department, or user).
- MCP activity is captured in the Ramp audit log.
- Building your own MCP client or gateway instead? Custom redirect URIs
  must be allowlisted by Ramp developer support first.

There is also a legacy self-hosted server (`ramp-public/ramp_mcp` on
GitHub) that runs locally via `uv` with client credentials and
`RAMP_ENV=demo|prd`; prefer the hosted server unless you specifically need
the sandbox-driven local variant.

## Hygiene checklist

- One app per integration, least-privilege scopes, per-environment
  credentials.
- No secrets in code, logs, or terminal history; use env vars injected
  from a secret store.
- Review granted scopes quarterly; delete unused apps.
- Treat any pasted-in-plaintext secret as compromised: rotate it.
