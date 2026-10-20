---
name: apify-actors
description: "Apify Actors scraping and automation platform. Use when the agent needs this capability via MCP."
---

# apify-actors

Apify Actors scraping and automation platform

## When to Activate

- Use **apify-actors** from an MCP-aware client
- Browser Automation tasks that apify-actors supports
- Register apify-actors via `claude mcp add` or `.mcp.json`

## Installation

apify-actors is an MCP server (stdio transport). Register it with Claude Code:

```bash
claude mcp add apify-actors -- npx apify-mcp-server
```

Or add to `.mcp.json`:

```json
{
  "mcpServers": {
    "apify-actors": {
      "command": "npx",
      "args": [
        "apify-mcp-server"
      ]
    }
  }
}
```

A guided installer is at `scripts/install.sh`.

## Verification

```bash
claude mcp list
```

## Details

- **Server**: `apify-actors`
- **Maintainer**: Apify
- **Protocol**: stdio
- **Category**: Browser Automation
- **Priority**: Optional
