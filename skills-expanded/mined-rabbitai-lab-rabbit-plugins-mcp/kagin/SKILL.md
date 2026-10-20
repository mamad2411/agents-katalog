---
name: kagin
description: "Kagi Search API integration. Use when the agent needs this capability via MCP."
---

# kagin

Kagi Search API integration

## When to Activate

- Use **kagin** from an MCP-aware client
- Search & Web tasks that kagin supports
- Register kagin via `claude mcp add` or `.mcp.json`

## Installation

kagin is an MCP server (stdio transport). Register it with Claude Code:

```bash
claude mcp add kagin -- npx @kagi/mcp-server
```

Or add to `.mcp.json`:

```json
{
  "mcpServers": {
    "kagin": {
      "command": "npx",
      "args": [
        "@kagi/mcp-server"
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

- **Server**: `kagin`
- **Maintainer**: Kagi
- **Protocol**: stdio
- **Category**: Search & Web
- **Priority**: Optional
