---
name: duckduckgo
description: "DuckDuckGo privacy-focused search engine. Use when the agent needs this capability via MCP."
---

# duckduckgo

DuckDuckGo privacy-focused search engine

## When to Activate

- Use **duckduckgo** from an MCP-aware client
- Search & Web tasks that duckduckgo supports
- Register duckduckgo via `claude mcp add` or `.mcp.json`

## Installation

duckduckgo is an MCP server (stdio transport). Register it with Claude Code:

```bash
claude mcp add duckduckgo -- npx mcp-duckduckgo
```

Or add to `.mcp.json`:

```json
{
  "mcpServers": {
    "duckduckgo": {
      "command": "npx",
      "args": [
        "mcp-duckduckgo"
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

- **Server**: `duckduckgo`
- **Maintainer**: 社区
- **Protocol**: stdio
- **Category**: Search & Web
- **Priority**: Optional
