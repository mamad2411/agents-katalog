---
name: auth0-setup
description: Auth0 tenants, applications, callback URLs, the auth0 CLI, and the official MCP server with device-flow auth and read-only mode. Use for first-time setup, tenant hygiene, or MCP connection issues.
---

# Auth0 setup

## Tenants

- A tenant is an isolated Auth0 environment with its own domain
  (`your-tenant.us.auth0.com`), users, applications, and Actions.
- Use separate tenants for dev, staging, and production; tag them with the
  environment in Settings so dashboards and CLI targets are unambiguous.
- Production tenants: enable a custom domain, review attack protection
  (brute force, breached password detection), and restrict dashboard admin
  membership.

## Applications

Create one application per client, with the correct type:

- **Single Page Application**: SPA with PKCE, no secret.
- **Regular Web Application**: server-rendered app with client secret
  (Next.js, Express, Rails).
- **Machine to Machine**: backend services calling APIs via client
  credentials.
- **Native**: mobile/desktop.

Per application, configure exactly:

- Allowed Callback URLs (for Next.js v4: `https://app.example.com/auth/callback`,
  plus the localhost equivalent in dev tenants only)
- Allowed Logout URLs and Allowed Web Origins
- Grant types: leave only what the app uses (disable password grants).

APIs (resource servers): register each API with an identifier (the `audience`),
define scopes/permissions there, and enable RBAC + "Add Permissions in the
Access Token" if you enforce permissions from claims.

## Auth0 CLI

```bash
brew install auth0/auth0-cli/auth0     # macOS; releases exist for all platforms
auth0 login                            # device flow into a tenant
auth0 tenants list
auth0 apps list
auth0 apps create --name "Web App" --type regular
auth0 test login                       # end-to-end login test from the terminal
auth0 logs tail                        # live tenant logs while debugging
auth0 actions deploy <id>
```

The CLI stores tenant credentials locally; `auth0 logout <tenant>` removes
them. Use a dedicated M2M application with least-privilege Management API
scopes for CI automation rather than personal CLI sessions.

## Official MCP server

This plugin ships Auth0's official server:

```bash
npx -y @auth0/auth0-mcp-server run
```

- First run opens a browser device-authorization flow to your tenant;
  credentials are stored in the OS keychain, not in files. No secrets go in
  the MCP config.
- Scope it down: `run --read-only` for audit-style sessions, or
  `run --tools 'auth0_list_*,auth0_get_*'` to allowlist tools
  (`--read-only` wins when both are set). Prefer read-only unless you are
  actively creating apps or deploying Actions.
- It is beta software operating on your real tenant: point it at a dev tenant
  for experimentation, production only with read-only mode and intent.
- Requires Node.js 18+.

## Tenant hygiene checklist

- No wildcard callback URLs in production applications.
- Rotate client secrets on leak suspicion (Dashboard > application >
  Credentials); update deployed env vars in the same window.
- Default and custom connections reviewed: disable sign-up on connections
  that should be invite-only.
- Monitoring > Logs streamed to your SIEM for failed logins, anomaly events,
  and Action errors.
- Verify email templates and the custom domain before launch so verification
  mail does not land in spam.
