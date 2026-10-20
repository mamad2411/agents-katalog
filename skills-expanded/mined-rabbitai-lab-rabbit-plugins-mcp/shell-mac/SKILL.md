---
name: shell-mac
description: "macOS shell command execution. Use when the agent needs this capability via MCP."
---

# shell-mac

macOS shell command execution

## When to Activate

- Use **shell-mac** from an MCP-aware client
- System Automation tasks that shell-mac supports
- Register shell-mac via `claude mcp add` or `.mcp.json`

## Installation

shell-mac is an MCP server (stdio transport). Register it with Claude Code:

```bash
claude mcp add shell-mac -- npx mcp-server-shell-mac
```

Or add to `.mcp.json`:

```json
{
  "mcpServers": {
    "shell-mac": {
      "command": "npx",
      "args": [
        "mcp-server-shell-mac"
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

- **Server**: `shell-mac`
- **Maintainer**: 社区
- **Protocol**: stdio
- **Category**: System Automation
- **Priority**: Essential
