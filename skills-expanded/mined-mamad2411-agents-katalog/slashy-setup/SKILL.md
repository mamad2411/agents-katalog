---
name: slashy-setup
description: Connect, authenticate, verify, reconnect, or troubleshoot the Slashy MCP server in Caeros. Use when Slashy tools are unavailable, OAuth does not open, tools are missing, the wrong Google or Slashy account is connected, a token expired, or the server is not responding.
---

# Slashy setup

Slashy is a hosted MCP server at exactly
`https://slashy.ctrlcenter.ai/mcp`. Authentication is OAuth 2.1 with PKCE;
never ask for or store an API key or static access token.

## Connect

1. Open Settings → MCP in Caeros.
2. Find the Slashy server contributed by the installed plugin and click Connect.
3. Complete browser sign-in with the intended Google account and approve the
   requested Slashy permissions.
4. Return to Settings → MCP and verify that Slashy is connected and its tools
   are visible.

The client stores a short-lived OAuth token and refreshes it automatically.
Do not expose, copy, or commit the cached token.

## Troubleshoot

- **OAuth window did not open:** fully restart Caeros, verify a default browser
  is configured, and allow popups for `slashy.ctrlcenter.ai`; then reconnect.
- **Tools are missing:** disconnect and reconnect Slashy, finish OAuth, then
  start a fresh task so the tool catalog is reloaded.
- **Wrong account:** sign out of Slashy in the browser, reconnect, and choose the
  correct Google account. Confirm with the server's account-info tool.
- **Expired or revoked token:** reconnect to issue a fresh token. Do not delete
  auth caches unless the user explicitly approves that destructive fallback.
- **Server unavailable:** verify the endpoint has no trailing slash, check
  `https://status.slashy.com`, and test network/TLS reachability. Do not replace
  the server with a similarly named or unofficial endpoint.
- **Permission error:** surface the authorization link returned by Slashy and
  ask the user to grant that scope; do not retry writes repeatedly.

If reconnection still fails, report the exact client error and direct the user
to `support@slashy.com` with that error and the Caeros client name.
