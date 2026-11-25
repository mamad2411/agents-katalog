---
name: mcp-ops
description: |
  Operate MCP servers, Docker-backed MCP tools, and Serena availability checks.
  Use when discovering, enabling, disabling, troubleshooting, or cleaning up MCP servers, Docker containers, or Serena project activation.
---
# MCP Ops

This is a router skill. Classify the request, choose one lane, then read only the lane reference needed for the current task. Compose lanes only when the user request genuinely crosses responsibilities.

## Intent Routing

| Intent | Load | Use When |
|---|---|---|
| MCP server orchestration | `mcp-manager.md` | Read when loading, unloading, or optimizing MCP servers. |
| Docker container troubleshooting | `docker-ops.md` | Read when MCP containers fail, need logs, or need health checks. |
| Serena activation | `serena-trigger.md` | Read when Serena-backed navigation is expected but unavailable. |

## Loading Protocol

1. Match the user request to the narrowest intent above.
2. Read `references/<lane>.md` for that intent before executing specialized steps.
3. Load scripts or assets from this skill only after the selected reference calls for them.
4. Keep outputs concise and state which lane was used when that matters for handoff or auditability.

## Consolidated Names

Former installable skills now routed here: `mcp-manager`, `docker-ops`, `serena-trigger`.

Related routers: `archive-manager`, `agent-builder`.
