---
name: win-cli
description: "Windows command-line operations. Use when the agent needs this capability via MCP."
---

# win-cli

Windows command-line operations

## When to Activate

- Use **win-cli** from an MCP-aware client
- System Automation tasks that win-cli supports
- Register win-cli via `claude mcp add` or `.mcp.json`

## Installation

win-cli is an MCP server (stdio transport). Register it with Claude Code:

```bash
claude mcp add win-cli -- npx mcp-server-win-cli
```

Or add to `.mcp.json`:

```json
{
  "mcpServers": {
    "win-cli": {
      "command": "npx",
      "args": [
        "mcp-server-win-cli"
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

- **Server**: `win-cli`
- **Maintainer**: 社区
- **Protocol**: stdio
- **Category**: System Automation
- **Priority**: Optional
