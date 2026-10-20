---
name: currents
description: "Currents test execution and reporting. Use when the agent needs this capability via MCP."
---

# currents

Currents test execution and reporting

## When to Activate

- Use **currents** from an MCP-aware client
- Developer Tools tasks that currents supports
- Register currents via `claude mcp add` or `.mcp.json`

## Installation

currents is an MCP server (stdio transport). Register it with Claude Code:

```bash
claude mcp add currents -- npx @currents/mcp
```

Or add to `.mcp.json`:

```json
{
  "mcpServers": {
    "currents": {
      "command": "npx",
      "args": [
        "@currents/mcp"
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

- **Server**: `currents`
- **Maintainer**: Currents
- **Protocol**: stdio
- **Category**: Developer Tools
- **Priority**: Optional
