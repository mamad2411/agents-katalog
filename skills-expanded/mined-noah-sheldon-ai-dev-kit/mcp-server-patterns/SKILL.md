---
name: mcp-server-patterns
description: MCP server patterns — server configuration, tool definition, resource exposure, prompt template integration, server security, multi-server orchestration, context passing, error handling, MCP protocol basics.
origin: AI Dev Kit
---

# MCP Server Patterns

Build, configure, and operate Model Context Protocol (MCP) servers that expose tools,
resources, and prompts to LLM clients. Covers protocol basics, security, multi-server
orchestration, and production patterns.

## When to Use

- Building a custom MCP server to expose internal tools or APIs to an LLM client.
- Defining tools with structured input schemas for function calling.
- Exposing resources (files, data, API responses) through the MCP protocol.
- Integrating multiple MCP servers and routing tool calls between them.
- Securing MCP servers with provenance verification and permission scopes.
- Debugging MCP tool execution, context passing, and error handling.

## Core Concepts

### 1. MCP Protocol Basics

MCP is a protocol that allows LLM clients to interact with servers that expose:
- **Tools** — Executable functions the LLM can call (like function calling)
- **Resources** — Data sources the LLM can read (files, APIs, databases)
- **Prompts** — Reusable prompt templates the LLM can invoke

```
┌──────────────┐         ┌──────────────┐
│  LLM Client  │ ←───→   │  MCP Server  │
│  (Claude,    │  JSON   │  (Python,    │
│   GPT, etc.) │  RPC    │   Node, etc.)│
└──────────────┘         └──────────────┘
       │                          │
  tools/call               tools/list
  resources/read    ←───→   resources/list
  prompts/get              prompts/list
```

**Transport:** Stdio (default) or SSE/HTTP for remote servers.

### 2. Server Configuration

**Python MCP SDK:**

```python
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent


app = Server("my-tools-server")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """Return the list of available tools."""
    return [
        Tool(
            name="search_database",
            description="Search the internal database for records matching a query.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of results",
                        "default": 10,
                    },
                },
                "required": ["query"],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Execute a tool and return results."""
    if name == "search_database":
        query = arguments["query"]
        limit = arguments.get("limit", 10)
        results = await execute_search(query, limit)
        return [TextContent(type="text", text=str(results))]

    raise ValueError(f"Unknown tool: {name}")


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

**MCP Client Configuration (`.mcp.json`):**

```json
{
  "mcpServers": {
    "my-tools": {
      "command": "python",
      "args": ["path/to/server.py"],
      "env": {
        "DATABASE_URL": "postgresql://...",
        "API_KEY": "${API_KEY}"
      }
    },
    "exa": {
      "command": "npx",
      "args": ["-y", "exa-mcp-server"],
      "env": {
        "EXA_API_KEY": "${EXA_API_KEY}"
      }
    }
  }
}
```

### 3. Tool Definition

```python
from mcp.types import Tool, TextContent, EmbeddedResource
from pydantic import BaseModel, Field


class SearchArgs(BaseModel):
    """Structured input validation for the search tool."""
    query: str = Field(..., min_length=1, max_length=500, description="Search query")
    limit: int = Field(default=10, ge=1, le=100, description="Max results")
    filters: dict[str, str] = Field(default_factory=dict, description="Key-value filters")


def validate_tool_args(name: str, arguments: dict) -> BaseModel:
    """Validate tool arguments against schema."""
    validators = {
        "search_database": SearchArgs,
        "create_record": CreateRecordArgs,
        "update_config": UpdateConfigArgs,
    }
    validator = validators.get(name)
    if not validator:
        raise ValueError(f"Unknown tool: {name}")
    return validator.model_validate(arguments)


def format_tool_result(result: any) -> list[TextContent]:
    """Format tool output for MCP response."""
    if isinstance(result, str):
        return [TextContent(type="text", text=result)]
    return [TextContent(type="text", text=str(result))]
```

### 4. Resource Exposure

```python
from mcp.types import Resource, TextResourceContents


@app.list_resources()
async def list_resources() -> list[Resource]:
    """Expose readable resources to the LLM."""
    return [
        Resource(
            uri="config://app/settings",
            name="Application Settings",
            description="Current application configuration",
            mimeType="application/json",
        ),
        Resource(
            uri="docs://api/reference",
            name="API Reference",
            description="Full API documentation",
            mimeType="text/markdown",
        ),
    ]


@app.read_resource()
async def read_resource(uri: str) -> TextResourceContents:
    """Read a resource by URI."""
    if uri == "config://app/settings":
        return TextResourceContents(
            uri=uri,
            mimeType="application/json",
            text=settings.model_dump_json(indent=2),
        )
    elif uri == "docs://api/reference":
        content = await load_api_docs()
        return TextResourceContents(
            uri=uri,
            mimeType="text/markdown",
            text=content,
        )

    raise ValueError(f"Resource not found: {uri}")
```

### 5. Prompt Template Integration

```python
from mcp.types import Prompt, PromptArgument, PromptMessage, TextContent


@app.list_prompts()
async def list_prompts() -> list[Prompt]:
    """Expose reusable prompt templates."""
    return [
        Prompt(
            name="code_review",
            description="Review code for quality, security, and performance.",
            arguments=[
                PromptArgument(
                    name="code",
                    description="The code to review",
                    required=True,
                ),
                PromptArgument(
                    name="focus",
                    description="Focus area: security, performance, style",
                    required=False,
                ),
            ],
        ),
    ]


@app.get_prompt()
async def get_prompt(name: str, arguments: dict) -> list[PromptMessage]:
    """Generate a prompt from a template."""
    if name == "code_review":
        code = arguments.get("code", "")
        focus = arguments.get("focus", "all")

        return [
            PromptMessage(
                role="system",
                content=TextContent(
                    type="text",
                    text=f"You are a senior code reviewer. Focus on: {focus}.\n\n"
                         "Review the code and provide specific, actionable feedback.\n"
                         "Cite file paths and line numbers. Rate severity as BLOCKER/SUGGESTION/NIT.",
                ),
            ),
            PromptMessage(
                role="user",
                content=TextContent(type="text", text=code),
            ),
        ]

    raise ValueError(f"Unknown prompt: {name}")
```

### 6. Server Security

```python
# Provenance verification — only allow calls from trusted servers
TRUSTED_SERVERS = {"my-tools", "exa", "context7"}


def verify_provenance(server_name: str) -> bool:
    if server_name not in TRUSTED_SERVERS:
        raise PermissionError(f"Untrusted server: {server_name}")
    return True


# Permission scopes — restrict what tools can access
TOOL_PERMISSIONS = {
    "search_database": {"scopes": ["read"]},
    "create_record": {"scopes": ["read", "write"]},
    "delete_record": {"scopes": ["read", "write", "delete"]},
    "run_migration": {"scopes": ["admin"], "require_approval": True},
}


def check_tool_permission(tool_name: str, requested_scopes: list[str]) -> bool:
    perms = TOOL_PERMISSIONS.get(tool_name, {})
    allowed = set(perms.get("scopes", []))
    return all(s in allowed for s in requested_scopes)


# Require approval for dangerous operations
async def require_approval(tool_name: str, arguments: dict) -> bool:
    """Gate for high-risk tools."""
    perms = TOOL_PERMISSIONS.get(tool_name, {})
    if perms.get("require_approval"):
        # Return False to block; client must re-invoke with approval
        return False
    return True
```

### 7. Multi-Server Orchestration

```python
class MultiServerRouter:
    """Route tool calls to the appropriate MCP server."""

    def __init__(self):
        self.servers: dict[str, MCPServerClient] = {}
        self.tool_registry: dict[str, str] = {}  # tool_name → server_name

    def register_server(self, name: str, client: MCPServerClient) -> None:
        self.servers[name] = client
        tools = client.list_tools()
        for tool in tools:
            self.tool_registry[tool.name] = name

    async def call_tool(self, tool_name: str, arguments: dict) -> any:
        server_name = self.tool_registry.get(tool_name)
        if not server_name:
            raise ValueError(f"No server provides tool: {tool_name}")

        server = self.servers[server_name]
        return await server.call_tool(tool_name, arguments)

    async def list_all_tools(self) -> list[dict]:
        """Aggregate tools from all registered servers."""
        all_tools = []
        for server_name, server in self.servers.items():
            for tool in server.list_tools():
                all_tools.append({
                    "name": tool.name,
                    "description": tool.description,
                    "server": server_name,
                    "schema": tool.inputSchema,
                })
        return all_tools
```

### 8. Context Passing Between Servers

```python
from dataclasses import dataclass


@dataclass
class MCPContext:
    """Shared context passed between MCP server calls."""
    session_id: str
    user_id: str
    request_id: str
    metadata: dict


class ContextAwareServer:
    """Server that propagates context to tool executions."""

    def __init__(self, context: MCPContext):
        self.context = context

    async def call_tool(self, name: str, arguments: dict) -> list[TextContent]:
        # Inject context into tool execution
        arguments["_context"] = {
            "session_id": self.context.session_id,
            "user_id": self.context.user_id,
            "request_id": self.context.request_id,
        }

        # Execute with audit logging
        result = await self._execute_tool(name, arguments)
        await self._log_execution(name, arguments, result, self.context)

        return format_tool_result(result)
```

### 9. Error Handling

```python
from mcp.types import Error


async def safe_tool_call(name: str, arguments: dict) -> list[TextContent] | Error:
    """Safely execute a tool with comprehensive error handling."""
    try:
        # Validate inputs
        args = validate_tool_args(name, arguments)

        # Execute
        result = await execute_tool(name, args.model_dump())

        # Format
        return format_tool_result(result)

    except ValueError as e:
        return Error(code=-32602, message=f"Invalid arguments: {e}")
    except PermissionError as e:
        return Error(code=-32603, message=f"Permission denied: {e}")
    except TimeoutError as e:
        return Error(code=-32603, message=f"Tool timed out: {e}")
    except Exception as e:
        # Log full traceback internally; return safe message to client
        logger.exception(f"Tool {name} failed with arguments {arguments}")
        return Error(code=-32603, message=f"Internal error in {name}: {type(e).__name__}")
```

## Anti-Patterns

- **No input validation** — trusting raw tool arguments leads to injection and crashes
- **Exposing destructive tools without approval gates** — delete/drop/migrate operations need confirmation
- **Hardcoded credentials in server config** — use environment variables with `${VAR}` syntax
- **No error categorization** — returning generic "error" messages instead of structured MCP Error types
- **Single-server monolith** — split tools by domain into separate servers for isolation
- **No audit logging** — every tool call should be logged with context, args, and result

## Best Practices

1. **Validate all tool inputs with Pydantic/Zod** — never trust raw arguments.
2. **Define clear tool schemas** — explicit `inputSchema` with descriptions for every field.
3. **Use resources for static data** — config, docs, reference material that the LLM reads.
4. **Implement permission scopes** — restrict tools to read/write/delete as appropriate.
5. **Require approval for dangerous operations** — gate deletions, migrations, and admin actions.
6. **Route multi-server calls through a router** — aggregate tools and delegate to the right server.
7. **Pass context with every call** — session_id, user_id, request_id for tracing.
8. **Return structured errors** — use MCP Error types with codes, not raw exceptions.
9. **Log every tool execution** — tool name, arguments, result, duration, and context.
10. **Keep servers focused** — one server per domain (e.g., exa for search, context7 for docs).

## Related Skills

- `agentic-engineering` — Agent orchestration that uses MCP tools for delegation
- `exa-search` — Example MCP server for web search
- `api-integrations` — Connecting MCP servers to third-party APIs
- `security-review` — Security review of MCP tool exposure and permissions
