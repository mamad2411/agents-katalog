---
name: mcp-integration
description: Use when configuring, connecting, or troubleshooting Model Context Protocol (MCP) servers and external tool integrations.
tags: mcp, integration, external-tools, protocol
---

# MCP Integration Skill

Use this skill when working with MCP servers and external tool integrations.

## Workflow

1. Discover available MCP servers in the project
2. Configure connections (stdio, HTTP, SSE transports)
3. Verify tool availability and permissions
4. Handle OAuth/authentication flows
5. Debug connection issues

## MCP Concepts

- **Server**: External service exposing tools via MCP protocol
- **Tools**: Functions exposed by MCP servers for agent use
- **Resources**: File-like data sources from MCP servers
- **Prompts**: Reusable prompt templates
- **Transport**: Communication method (stdio, HTTP, SSE)

## Key Tools

- `mcp_client` - Connect to MCP servers
- `mcp_list_tools` - List available MCP tools
- `mcp_invoke` - Call MCP tools
- `mcp_resources` - Access MCP resources

## Transport Types

| Type | Use Case | Configuration |
|------|----------|---------------|
| stdio | Local processes | Command + args |
| HTTP | REST APIs | URL + headers |
| SSE | Server-sent events | URL + event endpoint |

## Common MCP Servers

- Filesystem access
- GitHub integration
- Database connections
- Search services
- Custom internal APIs

## Configuration

MCP servers are configured via:
- Project: `.teaagent/mcp.json`
- User: `~/.config/teaagent/mcp.json`
- Environment variables

## Rules

- Always verify MCP server availability before invoking tools
- Handle OAuth flows properly (use tokens, not hardcoded credentials)
- Filter tools appropriately using allow/block lists
- Implement proper timeout for long-running operations
- Log MCP tool calls in audit trail

## Debugging

- Check server logs for errors
- Verify network connectivity (for HTTP transports)
- Validate configuration syntax
- Test with `--debug` flag for verbose output

## References

- See the MCP concepts, transport types, and debugging sections above for advanced MCP patterns and troubleshooting.