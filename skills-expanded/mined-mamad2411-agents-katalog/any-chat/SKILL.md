---
name: any-chat
description: "AnyChat unified multi-model chat interface. Use when the agent needs this capability via MCP."
---

# any-chat

AnyChat unified multi-model chat interface

## When to Activate

- Use **any-chat** from an MCP-aware client
- AI Services tasks that any-chat supports
- Register any-chat via `claude mcp add` or `.mcp.json`

## Installation

any-chat is an MCP server (stdio transport). Register it with Claude Code:

```bash
claude mcp add any-chat -- npx mcp-any-chat
```

Or add to `.mcp.json`:

```json
{
  "mcpServers": {
    "any-chat": {
      "command": "npx",
      "args": [
        "mcp-any-chat"
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

- **Server**: `any-chat`
- **Maintainer**: 社区
- **Protocol**: stdio
- **Category**: AI Services
- **Priority**: Optional
