---
name: longport
description: "Longport HK/US stock trading API. Use when the agent needs this capability via MCP."
---

# longport

Longport HK/US stock trading API

## ⚠️ Caution

This server is marked **Use with Caution**. It may require API keys, credentials, or paid access; review the maintainer's docs and handle secrets carefully before registering.

## When to Activate

- Use **longport** from an MCP-aware client
- Payments & Finance tasks that longport supports
- Register longport via `claude mcp add` or `.mcp.json`

## Installation

longport is an MCP server (stdio transport). Register it with Claude Code:

```bash
claude mcp add longport -- npx @longport/mcp
```

Or add to `.mcp.json`:

```json
{
  "mcpServers": {
    "longport": {
      "command": "npx",
      "args": [
        "@longport/mcp"
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

- **Server**: `longport`
- **Maintainer**: Longport
- **Protocol**: stdio
- **Category**: Payments & Finance
- **Priority**: Use with Caution
