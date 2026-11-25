---
name: "leeway-mcp-server"
description: "Run, configure, debug, or integrate the Leeway Skills MCP server that exposes Leeway capabilities as callable tools, including Agent Lee integration and proof badge installation. Use when Codex needs to build the server, start it, connect agents, inspect MCP behavior, or generate proof-backed badge bundles."
---

# Leeway MCP Server

Use this skill when Leeway needs to be exposed as callable tools through MCP.

## Quick start

- Read `references/mcp-readme.md` for server startup, tool format, and MCP behavior.
- Read `references/agent-lee-integration.md` when integrating the MCP server into another agent runtime.
- Read `references/badge-integration.md` when installing a proof-backed Leeway badge bundle into another app.
- Check `references/mcp-package.json` for the server package commands and entry points before changing runtime behavior.
- Pair this skill with `$leeway-agent-skills-platform` for broader architecture work and `$leeway-standards` for governed code changes.

## Reference map

- `references/mcp-readme.md` -> MCP server setup, execution, and tool contract
- `references/agent-lee-integration.md` -> example agent integration and config
- `references/badge-integration.md` -> proof-backed badge installation flow
- `references/mcp-package.json` -> build and start commands for the server package
