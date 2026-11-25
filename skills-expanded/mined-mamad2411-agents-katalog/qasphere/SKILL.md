---
name: qasphere
description: "QASphere QA testing platform. Use when the agent needs this capability via MCP."
---

# qasphere

QASphere QA testing platform

## When to Activate

- Use **qasphere** from an MCP-aware client
- Developer Tools tasks that qasphere supports
- Register qasphere via `claude mcp add` or `.mcp.json`

## Installation

qasphere is an MCP server (stdio transport). Register it with Claude Code:

```bash
claude mcp add qasphere -- npx @qasphere/mcp
```

Or add to `.mcp.json`:

```json
{
  "mcpServers": {
    "qasphere": {
      "command": "npx",
      "args": [
        "@qasphere/mcp"
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

- **Server**: `qasphere`
- **Maintainer**: QASphere
- **Protocol**: stdio
- **Category**: Developer Tools
- **Priority**: Optional
