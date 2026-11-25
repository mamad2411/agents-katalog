---
name: tavily-api-key
description: Set up Tavily credentials, the TAVILY_API_KEY environment variable, and the plugin's OAuth MCP connection. Use when the user needs to create, configure, or debug Tavily authentication.
---

# Tavily API Key Setup

## Get a key

Create keys in the Tavily dashboard at https://app.tavily.com (sign up,
copy the key from the home screen). Keys look like `tvly-...` and come
with a monthly free credit allowance. Never commit a key and never paste
one into chat history.

## Use it

- **Direct API**: header `Authorization: Bearer tvly-...` on every
  `https://api.tavily.com/...` request.
- **Environment**: `export TAVILY_API_KEY=tvly-...` for the SDKs
  (`pip install tavily-python` / `npm install @tavily/core`) and the local
  MCP server.

## MCP connection

This plugin ships Tavily's hosted server `https://mcp.tavily.com/mcp`,
which authenticates with **OAuth**: on first use Caeros opens a browser
sign-in to your Tavily account, no key handling needed. If the connection
shows unauthorized, reconnect the server from the plugin page to redo the
OAuth flow.

Tavily also documents a `tavilyApiKey` URL query parameter for the hosted
server. Avoid it: secrets in URLs leak into logs and history. Use OAuth
(this plugin's default) or the local stdio server instead:

```json
{
  "mcpServers": {
    "tavily": {
      "transport": "stdio",
      "command": "npx",
      "args": ["-y", "tavily-mcp"],
      "env": {"TAVILY_API_KEY": "tvly-..."}
    }
  }
}
```

Keep that config out of version control, or source the env var from your
shell profile instead of inlining it.

## Verify

```bash
curl -s https://api.tavily.com/search \
  -H "Authorization: Bearer $TAVILY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "test", "max_results": 1}'
```

`401` means missing or malformed key (check the `Bearer ` prefix). Success
returns `results` plus a `usage.credits` field.

## Hygiene

- One key per environment; rotate on any suspected exposure.
- `advanced` search depth and `advanced` extraction cost 2x credits; check
  the dashboard usage page before automating high-volume loops.
