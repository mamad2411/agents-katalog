---
name: delx-mcp-server
description: >
  Delx MCP Server. Prefer MCP tools if connected; otherwise the package CLI.
---

# Delx MCP Server — skill or MCP

Same package, two doors.

```bash
npx -y delx-mcp-server call health --json '{}'
```

If MCP tools are already connected, use them. Do not invent mutation flags.
This package is a stdio bridge to api.delx.ai. Local CLI tool `call health` maps to `--health --json`.
