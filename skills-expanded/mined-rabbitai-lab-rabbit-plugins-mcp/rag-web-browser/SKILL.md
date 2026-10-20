---
name: rag-web-browser
description: "RAG web browser for content extraction and vectorization. Use when the agent needs this capability via MCP."
---

# rag-web-browser

RAG web browser for content extraction and vectorization

## When to Activate

- Use **rag-web-browser** from an MCP-aware client
- Browser Automation tasks that rag-web-browser supports
- Register rag-web-browser via `claude mcp add` or `.mcp.json`

## Installation

rag-web-browser is an MCP server (stdio transport). Register it with Claude Code:

```bash
claude mcp add rag-web-browser -- npx rag-web-browser-mcp
```

Or add to `.mcp.json`:

```json
{
  "mcpServers": {
    "rag-web-browser": {
      "command": "npx",
      "args": [
        "rag-web-browser-mcp"
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

- **Server**: `rag-web-browser`
- **Maintainer**: 社区
- **Protocol**: stdio
- **Category**: Browser Automation
- **Priority**: Optional
