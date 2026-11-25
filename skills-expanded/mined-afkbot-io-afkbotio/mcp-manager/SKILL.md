---
name: mcp-manager
description: "Profile MCP management via `mcp.profile.*` tools and `afk mcp`. Use when the user wants to connect, inspect, validate, update, or remove MCP servers by URL for one profile."
aliases:
  - mcp
  - mcp-profile
  - mcp-config
triggers:
  - mcp
  - connect mcp
  - add mcp
  - configure mcp
  - setup mcp
  - подключи mcp
  - добавь mcp
  - настрой mcp
  - mcp сервер
tool_names:
  - mcp.profile.list
  - mcp.profile.get
  - mcp.profile.upsert
  - mcp.profile.validate
  - mcp.profile.delete
  - credentials.list
  - credentials.request
  - credentials.create
  - credentials.update
preferred_tool_order:
  - mcp.profile.list
  - mcp.profile.get
  - mcp.profile.upsert
  - mcp.profile.validate
  - mcp.profile.delete
---
# mcp-manager

Use this skill when the user wants AFKBOT to connect or manage one MCP server for the current profile.

## Workflow
1. Start with `mcp.profile.list` when the request is broad or when you need to avoid duplicates.
2. If the user names one existing MCP server, inspect it with `mcp.profile.get`.
3. If the user provides an MCP endpoint URL, save it with `mcp.profile.upsert`.
4. Run `mcp.profile.validate` after changes unless the user explicitly asked to skip validation.
5. If the MCP server needs secret or credential bindings, use `credentials.*` tools to inspect or request them without exposing plaintext secrets in chat.
6. If the user wants to remove one MCP server, use `mcp.profile.delete`.

## Rules
- Prefer the actual MCP endpoint URL, not a generic product homepage.
- When `server` or `transport` is not provided, let `mcp.profile.upsert` infer them from the URL first.
- Explain the difference between:
  - profile MCP config management: `mcp.profile.*` or `afk mcp`
  - runtime MCP tool usage: `mcp.tools.list` and `mcp.tools.call`
- After a successful connect, tell the user which `server`, `transport`, `env_refs`, and `secret_refs` were stored.
- If validation fails, surface the exact error and do not claim the MCP server is ready.
