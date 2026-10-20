---
name: sslmon
description: "SSL certificate monitoring and alerting. Use when the agent needs this capability via MCP."
---

# sslmon

SSL certificate monitoring and alerting

## When to Activate

- Use **sslmon** from an MCP-aware client
- Monitoring tasks that sslmon supports
- Register sslmon via `claude mcp add` or `.mcp.json`

## Installation

sslmon is an MCP server (stdio transport). Register it with Claude Code:

```bash
claude mcp add sslmon -- npx mcp-sslmon
```

Or add to `.mcp.json`:

```json
{
  "mcpServers": {
    "sslmon": {
      "command": "npx",
      "args": [
        "mcp-sslmon"
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

- **Server**: `sslmon`
- **Maintainer**: 社区
- **Protocol**: stdio
- **Category**: Monitoring
- **Priority**: Optional
