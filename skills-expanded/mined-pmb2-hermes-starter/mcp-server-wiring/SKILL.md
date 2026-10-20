---
name: mcp-server-wiring
description: >-
  Wire existing Python business-logic modules as MCP tools consumed by Hermes
  Agent. Covers FastMCP wrapping, Pydantic input schemas, registration in
  .mcp.json and ~/.hermes/config.yaml, and env-var passthrough for API keys.
  Not about building MCP servers from scratch — that is building-mcp-servers.
version: 1.0.0
license: MIT
metadata:
  hermes:
    tags: [mcp, tools, python, fastapi, pydantic, hermes]
    triggers:
      - "make this an MCP server"
      - "expose as tools for Hermes"
      - "register as MCP server"
      - "create MCP tools from my CLI"
      - "set up as tooling for AI agent"
      - "connect it to Hermes"
      - "ensure everything is set up as MCP server and tooling"
    related_skills: [building-mcp-servers, native-mcp, fastapi-mcp-bridge, mcp-fleet-audit]
---

# MCP Server Wiring — Hermes Tool Layer

Wrap existing Python business-logic modules as MCP tools callable by Hermes
Agent and any MCP-compatible client.

## Pattern

Two approaches; prefer FastMCP for simple toolsets (< 5 tools), raw protocol for complex multi-tool servers that need fine-grained descriptions and dispatch control.

### Approach A: FastMCP (preferred for simple toolsets)

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("my-tools")

@mcp.tool()
def my_tool(param: str) -> str:
    """Description shown to the agent."""
    # Call existing business logic
    return result
```

Use Pydantic `BaseModel` for tools with many parameters:

```python
from pydantic import BaseModel, Field

class InputSchema(BaseModel):
    niche: str = Field(..., description="Service type")
    location: str = Field(..., description="City, State")

@mcp.tool()
def search_businesses(input: InputSchema) -> str:
    import json
    return json.dumps(run_search(input.niche, input.location))
```

### Approach B: Raw `mcp.server.Server` protocol (for 5+ tools, complex descriptions)

When you need fine-grained control over tool descriptions, namespacing, or dispatch, use the lower-level protocol directly:

```python
from mcp.server import Server, stdio_server
from mcp.types import Tool, TextContent

server = Server("my-service")

@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="my_service__tool_name",
            description="Complete sentence describing what this tool does.",
            inputSchema={
                "type": "object",
                "properties": {
                    "param": {"type": "string", "description": "What the param means"},
                },
                "required": ["param"],
            },
        ),
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    match name:
        case "my_service__tool_name":
            result = domain_function(arguments["param"])
            return [TextContent(type="text", text=result)]
        case _:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]

def cli():
    import anyio
    async def run():
        async with stdio_server() as (read, write):
            await server.run(read, write, server.create_initialization_options())
    anyio.run(run)
```

Use a `match` statement (Python 3.10+) for clean tool dispatch. Tool handlers must be **thin wrappers** — call the existing domain functions; no business logic in the MCP layer.

**Tool naming convention:** double-underscore namespace (`deal_finder__find_deals`) so tools are identifiable by source in combined agent tool lists.

**Common pitfalls (raw protocol):**
- `TextContent(type="text", text=...)` — the `type` field is a string, not a Python type object
- f-strings without placeholders on long continuation lines — `ruff check --fix` catches these automatically
- You must call `server.create_initialization_options()` — don't omit it

### 2. Run and test

```bash
python -m my_package.mcp_server          # stdio transport (default)
python -m my_package.mcp_server --sse    # SSE for HTTP clients
```

Test tool registration before wiring to Hermes:

```python
from my_package.mcp_server import mcp
tools = mcp._tool_manager.list_tools()
for t in tools:
    print(f"  {t.name}: {t.description}")
```

### 3. Register in `.mcp.json` (project-local)

```json
{
  "mcpServers": {
    "my-tools": {
      "command": "python",
      "args": ["-m", "my_package.mcp_server"],
      "env": {
        "PYTHONPATH": "src"
      }
    }
  }
}
```

### 4. Register in `~/.hermes/config.yaml` (user-level profile)

```yaml
mcp_servers:
  my-tools:
    command: python
    args: ["-m", "my_package.mcp_server"]
    workdir: "E:/path/to/project"
    timeout: 300
    connect_timeout: 30
    env:
      PYTHONPATH: "E:/path/to/project/src"
      API_KEY: "${API_KEY}"  # inherits from shell env
```

### 5. Environment variable passthrough

MCP servers run as child processes. API keys must be explicitly forwarded:

```yaml
env:
  SERPER_API_KEY: "${SERPER_API_KEY}"
  GITHUB_TOKEN: "${GITHUB_TOKEN}"
  NAMECHEAP_API_KEY: "${NAMECHEAP_API_KEY}"
```

For local development, you can hardcode fallbacks or defaults:

```yaml
env:
  FALLBACK_URL: "https://example.com"
  TIMEOUT: "60"
```

## Common pitfalls

- **FastMCP `description` param**: older `mcp` library versions do not accept
  `description=` in the constructor. Omit it; use the docstring instead.
- **Path resolution**: MCP servers run from `workdir`. Use absolute paths for
  `PYTHONPATH`, `cwd`, and any referenced directories to avoid ambiguity.
- **Stdio vs SSE**: stdio is the default and matches Hermes's subprocess model.
  SSE is for external HTTP consumers; Hermes does not use it.
- **Import errors at startup**: the entire MCP server module is imported when
  Hermes connects. A missing dependency will fail silently — test with
  `python -c "from my_package.mcp_server import mcp"` first.
- **Name collisions**: If the skill name collides across external_dir and local
  dirs, Hermes refuses to load it. Rename one, or use the categorized path.
- **Security-sensitive edits**: `~/AppData/Local/hermes/config.yaml` is protected from
  direct file writes by the agent. Use `~/.hermes/config.yaml` (profile-level)
  or the `hermes mcp add` command instead. There are TWO config files — always
  update the `~/.hermes/config.yaml` profile copy; the `AppData/Local` one is
  system-level and blocked from modification.

## Verification checklist

- [ ] `python -c "from x.mcp_server import mcp; print(len(mcp._tool_manager.list_tools()))"` shows N tools
- [ ] `.mcp.json` is in project root with correct command + args
- [ ] `~/.hermes/config.yaml` has an `mcp_servers.` entry for the server
- [ ] Env vars for API keys are listed under `env:` (not relying on shell inheritance)
- [ ] Tool descriptions are written as complete sentences the agent can understand
- [ ] Python path (`PYTHONPATH`, `workdir`) uses absolute Windows paths or stable relative paths

## Reference

- `landlord.lead_capture.mcp_server` (website-landlord project) — example of wrapping a full business workflow as 5 MCP tools
- `building-mcp-servers` skill — for building MCP servers from scratch (protocol, discovery, lifecycle)
