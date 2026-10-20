---
name: win-control
description: "Windows system control automation. Use when the agent needs this capability via MCP."
---

# win-control

Windows system control automation

## When to Activate

- Use **win-control** from an MCP-aware client
- System Automation tasks that win-control supports
- Register win-control via `claude mcp add` or `.mcp.json`

## Installation

win-control is an MCP server (stdio transport). Register it with Claude Code:

```bash
claude mcp add win-control -- npx mcp-win-control
```

Or add to `.mcp.json`:

```json
{
  "mcpServers": {
    "win-control": {
      "command": "npx",
      "args": [
        "mcp-win-control"
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

- **Server**: `win-control`
- **Maintainer**: 社区
- **Protocol**: stdio
- **Category**: System Automation
- **Priority**: Optional
