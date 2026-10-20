---
name: k8m
description: "K8m Kubernetes AI ops assistant. Use when the agent needs this capability via MCP."
---

# k8m

K8m Kubernetes AI ops assistant

## When to Activate

- Use **k8m** from an MCP-aware client
- Cloud & DevOps tasks that k8m supports
- Register k8m via `claude mcp add` or `.mcp.json`

## Installation

k8m is an MCP server (stdio transport). Register it with Claude Code:

```bash
claude mcp add k8m -- npx @k8m/mcp
```

Or add to `.mcp.json`:

```json
{
  "mcpServers": {
    "k8m": {
      "command": "npx",
      "args": [
        "@k8m/mcp"
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

- **Server**: `k8m`
- **Maintainer**: K8m
- **Protocol**: stdio
- **Category**: Cloud & DevOps
- **Priority**: Recommended
