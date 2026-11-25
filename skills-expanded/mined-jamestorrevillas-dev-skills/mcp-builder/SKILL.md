---
name: mcp-builder
description: Use this skill when building Model Context Protocol (MCP) servers, creating AI tool integrations, designing agent-accessible tools, or making external services accessible to AI agents. Trigger on keywords: MCP, Model Context Protocol, MCP server, AI tool, tool integration, agent tools, connect AI to, build MCP, FastMCP.
---

# MCP Builder

## What is MCP

Model Context Protocol is the open standard for connecting AI agents to external tools and data sources. Think of it as USB-C for AI — one standard connector to any tool.

**When to use MCP:** When you want a tool to be reusable across multiple agents or platforms (Claude, Copilot, Cursor, etc.)

**When NOT to use MCP:** For project-specific, one-off integrations where the overhead isn't worth it.

---

## MCP Server Structure

```
my-mcp-server/
├── server.py (Python) or index.ts (TypeScript)
├── tools/
│   ├── tool_one.py
│   └── tool_two.py
├── resources/       # Optional: expose data sources
├── prompts/         # Optional: expose prompt templates
├── requirements.txt or package.json
└── README.md
```

---

## Python (FastMCP) — Recommended

```python
from fastmcp import FastMCP

mcp = FastMCP("my-server-name")

@mcp.tool()
def get_user(user_id: str) -> dict:
    """
    Retrieve a user by their ID.
    
    Args:
        user_id: The unique identifier of the user
    
    Returns:
        User object with id, name, email
    """
    # implementation
    return {"id": user_id, "name": "James", "email": "james@example.com"}

@mcp.tool()
def create_task(title: str, description: str, assignee: str = None) -> dict:
    """Create a new task in the project management system."""
    # implementation
    return {"id": "task_123", "title": title, "status": "created"}

if __name__ == "__main__":
    mcp.run()
```

---

## TypeScript (MCP SDK)

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js"
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js"
import { z } from "zod"

const server = new McpServer({ name: "my-server", version: "1.0.0" })

server.tool(
  "get_user",
  "Retrieve a user by their ID",
  { userId: z.string().describe("The user's unique ID") },
  async ({ userId }) => ({
    content: [{ type: "text", text: JSON.stringify({ id: userId, name: "James" }) }]
  })
)

const transport = new StdioServerTransport()
await server.connect(transport)
```

---

## Tool Design Principles

### Tool Definition Checklist
- [ ] Name is descriptive and action-oriented (`get_user`, not `user`)
- [ ] Description clearly states when to use this tool
- [ ] Parameters have clear names and descriptions
- [ ] Returns are documented
- [ ] Error cases are handled and return meaningful messages
- [ ] Side effects are documented (if tool writes/deletes data)

### Tool Design Rules
- **One tool = one action** — don't combine multiple operations
- **Idempotent where possible** — safe to call multiple times
- **Validate inputs** — don't trust that the AI passes valid data
- **Return structured data** — JSON is better than plain text for programmatic use
- **Include context in errors** — "User 'abc' not found" not just "Not found"

---

## Resources (Exposing Data)

```python
@mcp.resource("users://list")
def list_users() -> str:
    """Returns all users as a JSON string"""
    users = db.get_all_users()
    return json.dumps(users)

@mcp.resource("user://{user_id}")
def get_user_resource(user_id: str) -> str:
    """Returns a specific user's data"""
    user = db.get_user(user_id)
    return json.dumps(user)
```

---

## Connecting to Claude Desktop

In `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "my-server": {
      "command": "python",
      "args": ["/path/to/server.py"],
      "env": {
        "API_KEY": "your-key-here"
      }
    }
  }
}
```

---

## Security Checklist

- [ ] Never expose credentials in tool definitions
- [ ] Validate and sanitize all inputs before using in DB queries or file operations
- [ ] Rate limit expensive operations
- [ ] Log all tool invocations for auditing
- [ ] Implement timeouts for external calls
- [ ] Don't give the tool more permissions than it needs
