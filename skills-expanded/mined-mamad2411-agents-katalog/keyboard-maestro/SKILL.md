---
name: keyboard-maestro
description: "Keyboard Maestro macro automation. Use when the agent needs this capability via MCP."
---

# keyboard-maestro

Keyboard Maestro macro automation

## When to Activate

- Use **keyboard-maestro** from an MCP-aware client
- System Automation tasks that keyboard-maestro supports
- Register keyboard-maestro via `claude mcp add` or `.mcp.json`

## Installation

keyboard-maestro is an MCP server (stdio transport). Register it with Claude Code:

```bash
claude mcp add keyboard-maestro -- npx mcp-keyboard-maestro
```

Or add to `.mcp.json`:

```json
{
  "mcpServers": {
    "keyboard-maestro": {
      "command": "npx",
      "args": [
        "mcp-keyboard-maestro"
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

- **Server**: `keyboard-maestro`
- **Maintainer**: 社区
- **Protocol**: stdio
- **Category**: System Automation
- **Priority**: Optional
