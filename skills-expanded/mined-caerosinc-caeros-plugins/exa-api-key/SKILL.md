---
name: exa-api-key
description: Set up Exa credentials, the EXA_API_KEY environment variable, and the plugin's MCP connection modes (keyless vs authenticated). Use when the user needs to create, configure, or debug Exa authentication.
---

# Exa API Key Setup

## Get a key

Create keys in the Exa dashboard at https://exa.ai (sign in, open API
keys). Never commit a key and never paste one into chat history.

## Use it

- **Direct API**: header `x-api-key: <key>` (or
  `Authorization: Bearer <key>`) on `https://api.exa.ai/...` requests.
- **Environment**: `export EXA_API_KEY=...` for the official SDKs
  (`pip install exa-py` / `npm install exa-js`) and the local MCP server.

## MCP connection modes

This plugin ships Exa's hosted server `https://mcp.exa.ai/mcp`.

- **Keyless** (plugin default): the hosted server responds without a key,
  rate limited. Good for light interactive use.
- **Authenticated hosted**: pass the key as the `x-api-key` header. The key
  never belongs in the URL.
- **Tool selection**: the hosted server enables `web_search_exa` and
  `web_fetch_exa` by default; append
  `?tools=web_search_exa,web_fetch_exa,web_search_advanced_exa` (or the
  `agent_tools` alias) to the server URL to change the set.
- **Local stdio server** for full quota control:

```json
{
  "mcpServers": {
    "exa": {
      "transport": "stdio",
      "command": "npx",
      "args": ["-y", "exa-mcp-server"],
      "env": {"EXA_API_KEY": "..."}
    }
  }
}
```

Keep that config out of version control, or source the env var from your
shell profile instead of inlining it.

## Verify

```bash
curl -s https://api.exa.ai/search \
  -H "x-api-key: $EXA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "test", "numResults": 1}'
```

`401` means missing or invalid key. Success returns a `results` array and a
`costDollars` block you can use to sanity-check pricing.

## Hygiene

- One key per environment; rotate on any suspected exposure.
- Deep research types and large `contents` requests cost more per call;
  watch usage in the dashboard before automating them.
