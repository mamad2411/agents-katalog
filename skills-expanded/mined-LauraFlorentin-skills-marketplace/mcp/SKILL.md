---
name: mcp
description: An interoperability standard that allows AI models to connect to external data and tools securely and consistently, decoupling the tool implementation from the agent. Use when user asks about "MCP servers", "model context protocol", "connect tools to my agent", or mentions MCP integration, tool servers, or context protocol.
---

# Model Context Protocol (MCP)

The Model Context Protocol (MCP) forces a separation between the *definition* of a tool (the server) and the *consumption* of a tool (the client/agent). Instead of hardcoding API integrations inside your agent's codebase, you build an MCP Server that exposes resources (data) and tools (functions). Any MCP-compliant agent can then discover and use these tools without custom glue code.

## Use Cases

-   **Database Access**: An MCP server that exposes safe SQL queries as tools.
-   **File System**: An MCP server that allows an agent to read/write files in a sandboxed directory.
-   **API Wrapper**: An MCP server that wraps the GitHub API, exposing actions like `create_issue` or `list_prs`.

## Implementation Pattern

```python
# MCP Server Implementation (Conceptual)
from fastmcp import FastMCP, tool

# Create a server
mcp = FastMCP("MyTools")

# Expose a tool
@mcp.tool()
def calculate_vat(amount: float, country: str) -> float:
    """Calculates VAT for a given country."""
    rate = get_rate(country)
    return amount * rate

# The Agent (Client) simply connects to this server
# and automatically "sees" the calculate_vat tool available for use.
# client.connect(mcp_server)
# response = client.chat("How much VAT for 100 EUR in Germany?")
```


## Examples

**Input**: "Connect my agent to a database MCP server."

```json
// .claude/settings.json
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": { "DATABASE_URL": "postgresql://localhost/mydb" }
    }
  }
}
```

Agent can now call `mcp__postgres__query` to run SQL and `mcp__postgres__schema` to inspect tables.

---

**Input**: "Build a multi-MCP workflow: search the web, then save results to Notion."

**Pattern**: Phase 1 calls `mcp__brave__search`, collects results. Phase 2 calls `mcp__notion__createPage` with formatted output. Each phase validates data before proceeding.


## Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| MCP server not found | Binary not installed | Run `npx -y @modelcontextprotocol/server-name` to install |
| Tool calls return auth errors | Missing API key in env | Add key to `env` block in `mcpServers` config |
| Agent can't find MCP tools | Server not registered | Check `.claude/settings.json`; restart Claude Code after changes |
| Tool call times out | MCP server unresponsive | Test server independently: `npx @modelcontextprotocol/inspector` |
| Data format mismatch between MCPs | Different schemas | Add a transformation step between phases to normalize formats |
