---
name: astral
description: >
  Local-first natal charts, transits, synastry and moon phases. No API key.
  Prefer MCP tools if connected; otherwise the package CLI.
---

# Astral — skill or MCP

Same binary. Prefer MCP tools if connected.

```bash
npx -y astral-mcp call astral_connection_status --json '{}'
```

If MCP tools named `astral_*` are already available, use them. Do not invent env flags.
