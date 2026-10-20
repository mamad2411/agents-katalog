---
name: octagon
description: "Octagon financial data platform. Use when the agent needs this capability via MCP."
---

# octagon

Octagon financial data platform

## When to Activate

- Use **octagon** from an MCP-aware client
- Payments & Finance tasks that octagon supports
- Register octagon via `claude mcp add` or `.mcp.json`

## Installation

octagon is an MCP server (stdio transport). Register it with Claude Code:

```bash
claude mcp add octagon -- npx @octagon/mcp
```

Or add to `.mcp.json`:

```json
{
  "mcpServers": {
    "octagon": {
      "command": "npx",
      "args": [
        "@octagon/mcp"
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

- **Server**: `octagon`
- **Maintainer**: Octagon
- **Protocol**: stdio
- **Category**: Payments & Finance
- **Priority**: Optional
