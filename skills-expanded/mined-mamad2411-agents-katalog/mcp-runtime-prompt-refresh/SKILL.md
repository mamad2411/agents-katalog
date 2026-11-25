---
name: mcp-runtime-prompt-refresh
description: Expose a built-in MCP tool that hot-swaps the server's prompt set at runtime, persists it to disk, and emits notifications/prompts/list_changed so clients pick it up without reconnecting.
category: ai
tags: [mcp, prompts, hot-reload, json-rpc, tool-design]
triggers:
  - "refresh prompts"
  - "update mcp prompts at runtime"
  - "prompts list_changed"
  - "mcp hot reload"
source_project: yamltomcp
version: 0.1.0-draft
---
