---
name: metoro
description: "Metoro eBPF observability. Use when the agent needs this capability via MCP."
---

# metoro

Metoro eBPF observability

## When to Activate

- Use **metoro** from an MCP-aware client
- Monitoring tasks that metoro supports
- Register metoro via `claude mcp add` or `.mcp.json`

## Installation

metoro is an MCP server (stdio transport). Register it with Claude Code:

```bash
claude mcp add metoro -- npx @metoro/mcp
```

Or add to `.mcp.json`:

```json
{
  "mcpServers": {
    "metoro": {
      "command": "npx",
      "args": [
        "@metoro/mcp"
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

- **Server**: `metoro`
- **Maintainer**: Metoro
- **Protocol**: stdio
- **Category**: Monitoring
- **Priority**: Optional
