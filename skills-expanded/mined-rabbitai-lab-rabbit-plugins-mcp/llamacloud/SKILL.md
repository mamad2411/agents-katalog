---
name: llamacloud
description: "LlamaCloud document parsing and indexing. Use when the agent needs this capability via MCP."
---

# llamacloud

LlamaCloud document parsing and indexing

## When to Activate

- Use **llamacloud** from an MCP-aware client
- AI Services tasks that llamacloud supports
- Register llamacloud via `claude mcp add` or `.mcp.json`

## Installation

llamacloud is an MCP server (stdio transport). Register it with Claude Code:

```bash
claude mcp add llamacloud -- npx @llamaindex/mcp-llamacloud
```

Or add to `.mcp.json`:

```json
{
  "mcpServers": {
    "llamacloud": {
      "command": "npx",
      "args": [
        "@llamaindex/mcp-llamacloud"
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

- **Server**: `llamacloud`
- **Maintainer**: LlamaIndex
- **Protocol**: stdio
- **Category**: AI Services
- **Priority**: Recommended
