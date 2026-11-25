---
name: dexpaprika
description: "DEX Paprika decentralized exchange data. Use when the agent needs this capability via MCP."
---

# dexpaprika

DEX Paprika decentralized exchange data

## ⚠️ Caution

This server is marked **Use with Caution**. It may require API keys, credentials, or paid access; review the maintainer's docs and handle secrets carefully before registering.

## When to Activate

- Use **dexpaprika** from an MCP-aware client
- Payments & Finance tasks that dexpaprika supports
- Register dexpaprika via `claude mcp add` or `.mcp.json`

## Installation

dexpaprika is an MCP server (stdio transport). Register it with Claude Code:

```bash
claude mcp add dexpaprika -- npx mcp-dexpaprika
```

Or add to `.mcp.json`:

```json
{
  "mcpServers": {
    "dexpaprika": {
      "command": "npx",
      "args": [
        "mcp-dexpaprika"
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

- **Server**: `dexpaprika`
- **Maintainer**: 社区
- **Protocol**: stdio
- **Category**: Payments & Finance
- **Priority**: Use with Caution
