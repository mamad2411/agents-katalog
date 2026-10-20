---
name: zenml
description: "ZenML ML pipeline management. Use when the agent needs this capability via MCP."
---

# zenml

ZenML ML pipeline management

## When to Activate

- Use **zenml** from an MCP-aware client
- AI Services tasks that zenml supports
- Register zenml via `claude mcp add` or `.mcp.json`

## Installation

zenml is an MCP server (stdio transport). Register it with Claude Code:

```bash
claude mcp add zenml -- npx @zenml/mcp
```

Or add to `.mcp.json`:

```json
{
  "mcpServers": {
    "zenml": {
      "command": "npx",
      "args": [
        "@zenml/mcp"
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

- **Server**: `zenml`
- **Maintainer**: ZenML
- **Protocol**: stdio
- **Category**: AI Services
- **Priority**: Optional
