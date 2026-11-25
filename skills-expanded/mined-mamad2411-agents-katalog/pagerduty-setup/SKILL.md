---
name: pagerduty-setup
description: Set up PagerDuty access, including user API tokens, account keys, scoped OAuth, region hosts, and the official MCP server (hosted and local). Use when connecting Caeros or scripts to PagerDuty.
---

# PagerDuty Setup

## Choose a credential

- **User API token**: acts as one user with that user's permissions. Created
  under User Settings (or user icon) > API Access > Create API User Token.
  Required by the MCP server; good default for personal automation.
- **Account-level REST API key** (General Access): admin-created, acts with
  account-wide access, read-only variant available. For service-to-service
  integrations, not for the MCP server.
- **Scoped OAuth app**: register an app in Integrations > App Registration,
  request granular scopes (e.g. `incidents.read`, `services.write`,
  `oncalls.read`), and use the OAuth flow to obtain tokens. Best for
  multi-user or distributed integrations: least privilege plus per-user
  identity.

REST auth header format differs by credential: API tokens use
`Authorization: Token token=<key>`; OAuth access tokens use
`Authorization: Bearer <token>`. Store any of them in a secret manager or
untracked `.env`, never in code or chat.

Regions: US `https://api.pagerduty.com`, EU `https://api.eu.pagerduty.com`.
Match the region to your account or every call 401s.

## Official MCP server: hosted

This plugin connects to PagerDuty's hosted MCP service:

- US: `https://mcp.pagerduty.com/mcp`
- EU: `https://mcp.eu.pagerduty.com/mcp` (edit `.mcp.json` if your account is
  EU)

Requirements: a PagerDuty account with Advanced Permissions and a User API
token; authentication is supplied through your MCP client's auth flow (the
MCP API accepts the same credentials as the REST API, token or OAuth). The
hosted server exposes 60+ read and write tools across incidents, services,
on-call, escalation, event orchestration, incident workflows, and status
pages; what you can actually call follows your plan and user permissions.

## Official MCP server: local (self-hosted)

Open source at https://github.com/PagerDuty/pagerduty-mcp-server, package
`pagerduty-mcp`:

```bash
export PAGERDUTY_USER_API_KEY="<user api token>"
export PAGERDUTY_API_HOST="https://api.pagerduty.com"   # EU: api.eu.pagerduty.com
uvx pagerduty-mcp                       # read-only by default
uvx pagerduty-mcp --enable-write-tools  # opt in to write tools
```

Docker is also supported (`docker run -i --rm -e PAGERDUTY_USER_API_KEY
pagerduty-mcp:latest`). The local server is read-only out of the box; write
tools (acknowledge, resolve, create) require the explicit flag. Prefer local
read-only mode for reporting agents, hosted for full interactive ops.

## Verify

1. `curl -H "Authorization: Token token=$KEY" https://api.pagerduty.com/users/me`
   returns your user.
2. Ask the MCP server to list open incidents.

## Troubleshooting

- 401: wrong region host, revoked token, or Bearer/Token format mixed up.
- 403 on write tools: user role lacks permission, or the local server was
  started without `--enable-write-tools`.
- Empty tool list on hosted MCP: plan lacks Advanced Permissions.
