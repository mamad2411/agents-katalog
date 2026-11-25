---
name: mcp-server-registry
description: Instructions for discovery and usage of servers through the official MCP registry. Use when discovering new integrations. For building custom servers, see mcp-reference-servers.
---

# MCP Server Registry Skill

## When to Use

- When the user wants to find new MCP servers to extend agent capabilities.
- When researching available integrations for specific tools (e.g., Slack, GitHub, Postgres).
- To verify the official status or source of an MCP server.

## Reference

[Official MCP Registry](https://registry.modelcontextprotocol.io/)

## Instructions

### 1. Browse Registry

- Visit the registry to search for servers by category or keyword.
- Prioritize "Official" or "Verified" servers for production environments.

### 2. Integration Pattern

When adding a server from the registry:
- Check the `README` of the specific server for configuration requirements (API keys, environment variables).
- Use the `mcp_config` pattern if using a desktop client (Cursor, Claude Desktop).
- For agentic usage (like Antigravity), ensure the server is added to the active MCP server list.

### 3. Verification

- Ensure the server URL is correct.
- Validate that the server supports the versions of the tools you are using.
- Connection test passes after configuration.

## Quality Gates

- Server URL is valid and reachable.
- Required environment variables are identified and documented in `.env`.
- Connection test passes after configuration.
