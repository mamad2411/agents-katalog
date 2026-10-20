---
name: firecrawl-api-key
description: Set up Firecrawl credentials, the FIRECRAWL_API_KEY environment variable, and the plugin's MCP connection modes (keyless free tier vs authenticated). Use when the user needs to create, configure, or debug Firecrawl authentication.
---

# Firecrawl API Key Setup

## Get a key

Create keys in the Firecrawl dashboard (https://firecrawl.dev, sign in and
open the API Keys page). Keys look like `fc-...`. Never commit a key and
never paste one into chat history.

## Use it

- **Direct API**: `Authorization: Bearer fc-...` header on every
  `https://api.firecrawl.dev/v2/...` request.
- **Environment**: `export FIRECRAWL_API_KEY=fc-...` for SDKs
  (`pip install firecrawl-py` / `npm install @mendable/firecrawl-js`) and
  for the local MCP server.

## MCP connection modes

This plugin ships the hosted server `https://mcp.firecrawl.dev/v2/mcp`.

- **Keyless free tier** (plugin default): works with no account, rate
  limited per IP. Fine for trying tools; expect throttling under real load.
- **Authenticated hosted**: the hosted server accepts the key as an
  `Authorization: Bearer fc-...` header. The key never belongs in the URL.
- **Local stdio server**: for full quotas without header plumbing, run the
  official npm package locally with the key in the environment:

```json
{
  "mcpServers": {
    "firecrawl": {
      "transport": "stdio",
      "command": "npx",
      "args": ["-y", "firecrawl-mcp"],
      "env": {"FIRECRAWL_API_KEY": "fc-..."}
    }
  }
}
```

Store that config in a location outside version control, or inject the env
var from your shell profile instead of inlining it.

## Verify

A cheap smoke test:

```bash
curl -s https://api.firecrawl.dev/v2/scrape \
  -H "Authorization: Bearer $FIRECRAWL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "formats": ["markdown"]}'
```

`401` means bad or missing key; `402` means the key is valid but out of
credits (top up in the dashboard); `429` means rate limited.

## Hygiene

- One key per environment; rotate on any suspected exposure.
- Watch credit burn in the dashboard before running large crawls (see the
  `firecrawl-crawl-etiquette` skill).
