---
name: papers-with-code
description: "Papers with Code paper and code search. Use when the agent needs this capability via MCP."
---

# papers-with-code

Papers with Code paper and code search

## When to Activate

- Use **papers-with-code** from an MCP-aware client
- Search & Web tasks that papers-with-code supports
- Register papers-with-code via `claude mcp add` or `.mcp.json`

## Installation

papers-with-code is an MCP server (stdio transport). Register it with Claude Code:

```bash
claude mcp add papers-with-code -- npx mcp-paperswithcode
```

Or add to `.mcp.json`:

```json
{
  "mcpServers": {
    "papers-with-code": {
      "command": "npx",
      "args": [
        "mcp-paperswithcode"
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

- **Server**: `papers-with-code`
- **Maintainer**: 社区
- **Protocol**: stdio
- **Category**: Search & Web
- **Priority**: Recommended
