---
name: cmd-exec
description: "General command execution MCP server. Use when the agent needs this capability via MCP."
---

# cmd-exec

General command execution MCP server

## ⚠️ Caution

This server is marked **Use with Caution**. It may require API keys, credentials, or paid access; review the maintainer's docs and handle secrets carefully before registering.

## When to Activate

- Use **cmd-exec** from an MCP-aware client
- System Automation tasks that cmd-exec supports
- Register cmd-exec via `claude mcp add` or `.mcp.json`

## Installation

cmd-exec is an MCP server (stdio transport). Register it with Claude Code:

```bash
claude mcp add cmd-exec -- npx mcp-cmd-exec
```

Or add to `.mcp.json`:

```json
{
  "mcpServers": {
    "cmd-exec": {
      "command": "npx",
      "args": [
        "mcp-cmd-exec"
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

- **Server**: `cmd-exec`
- **Maintainer**: 社区
- **Protocol**: stdio
- **Category**: System Automation
- **Priority**: Use with Caution
