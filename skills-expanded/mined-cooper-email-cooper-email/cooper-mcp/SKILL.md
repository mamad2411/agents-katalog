---
name: cooper-mcp
description: Connect or troubleshoot the hosted Cooper Email MCP server (https://cooperemail.com/mcp) in Cursor, Claude Code, Claude.ai, ChatGPT, VS Code, Windsurf, Codex, or any Streamable HTTP MCP client. Use for installation, OAuth sign-in, Bearer API-key headers, 401 errors, or missing tools. Do not use when the connection already works and the user just wants to send, read, or manage mail; use the sibling Cooper skills for that.
license: MIT
metadata:
  version: "1"
  homepage: https://cooperemail.com/docs/mcp
---

# Cooper Email MCP

Hosted Streamable HTTP server (no local process):

```text
https://cooperemail.com/mcp
```

`/api/mcp` is an alias. The server publishes 61 tools today; clients read the
live catalog, so do not depend on a copied count.

## Cursor (this plugin)

The plugin registers the server with the bare URL. No key goes in the config.
Finish OAuth 2.1 + PKCE before creating an inbox. Create the inbox after
sign-in with `cooper_create_inbox`, or with the create option on Cooper's
consent screen. That inbox is the OAuth account.

`cooper_onboard` with no token does not sign this connector in. It creates a
separate account, returns an API key once, and stops there. Approving OAuth
later does not attach that key. The next signed-in tool uses the OAuth
account and can list a different inbox. The first inbox remains available
only when requests send `Authorization: Bearer` with the saved key.

To use a saved API key instead of OAuth, add the server to `.cursor/mcp.json`
or `~/.cursor/mcp.json` with a header. Do not also approve OAuth for that
same entry and expect both accounts to be one inbox:

```json
{
  "mcpServers": {
    "cooper-email": {
      "url": "https://cooperemail.com/mcp",
      "headers": { "Authorization": "Bearer ${env:COOPER_API_KEY}" }
    }
  }
}
```

Keys start with `coop_live_`. Keep them in an environment variable or secret
store, never in a committed file or in chat.

## Other clients

- Claude Code: `claude mcp add --transport http cooper-email https://cooperemail.com/mcp`,
  then finish OAuth in `/mcp` before creating an inbox. Add
  `--header "Authorization: Bearer $COOPER_API_KEY"` only when you already have
  a key and want that key's account instead of OAuth. Plugin:
  `/plugin marketplace add cooper-email/cooper-email`, then
  `/plugin install cooper-email@cooper-email` (plugin version 1.2.2).
- Claude.ai and Claude Desktop: Settings, Connectors, Add custom connector.
  Name `Cooper Email`, URL `https://cooperemail.com/mcp`, then connect with
  OAuth before creating an inbox.
- ChatGPT and Grok Bot: add the MCP URL and finish OAuth before creating an
  inbox. The anonymous key is not picked up by that approval.
- VS Code, Windsurf, Codex, Goose: copy-paste configs at
  https://cooperemail.com/integrations

## Which account you are on

OAuth clients (this plugin, Claude, Claude Code, ChatGPT, Grok Bot): connect
`https://cooperemail.com/mcp`, finish OAuth, then create the inbox. Do not
call `cooper_onboard` first.

HTTP and clients with no OAuth: `POST https://cooperemail.com/api/v1/onboard`
or `cooper_onboard` on a request that has no credentials. Store the one-time
`api_key` and send it as `Authorization: Bearer` on later calls. That key
does not attach itself to an OAuth session.

## Verify

1. Reload Cursor (Developer: Reload Window) or start a new session.
2. Check the MCP status in Cursor settings and finish sign-in before any
   create call.
3. Call `cooper_whoami` (shows `auth_type` oauth or api_key) and
   `cooper_list_inboxes`. If you onboarded anonymously and then approved
   OAuth, the list can omit the anonymous inbox. That is a different account,
   not a failed install. Use the saved Bearer key to reach the first inbox.

## Troubleshoot

- 404: the URL is missing `/mcp`.
- 401 with "needs an OAuth access token or Authorization: Bearer": the
  connection is not signed in. Finish OAuth, or set the Bearer header to a
  key you already saved. `cooper_onboard` mints another key; it does not
  apply that key to this connection.
- "API key or OAuth access token is not recognized": the key is wrong,
  revoked, or expired, or `COOPER_API_KEY` was not visible to the client
  process. Finish OAuth only if you mean to use the OAuth account (it is not
  the rejected key's inbox), or mint a new key from a working session over
  HTTP (`POST /api/v1/keys`) so the secret stays out of the chat.
- 403 `permission_denied`: the key is limited to one inbox or a permission
  list; `cooper_whoami` shows the scope.
- Discovery: `/.well-known/oauth-protected-resource`,
  `/.well-known/oauth-authorization-server`, `/.well-known/mcp.json`, and the
  catalog at `/api/v1/mcp/tools`.

Docs: https://cooperemail.com/docs/mcp · https://cooperemail.com/llms.txt
