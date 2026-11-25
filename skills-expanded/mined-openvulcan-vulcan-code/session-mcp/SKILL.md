---
name: session-mcp
description: "Create, inspect, or close a temporary MCP server connection for this conversation."
---

# Temporary MCP connections

Read this skill before managing a temporary MCP connection. Use `tool_call` with `skill: "session-mcp"`, `action: "mcp_connect"`, and the matching JSON arguments from the action schema.

- Use the inner action `connect` to create a connection when the task needs a specific MCP server. Reading this skill alone does not open a connection.
- Use the inner action `status` to inspect existing connections or `disconnect` to close one.
- The root conversation owns each connection. After connecting, use the returned connection ID with `mcp_tools` and `mcp_call`.
- Reference credentials by their configured environment variable names. Connection parameters are temporary and do not modify user settings.
