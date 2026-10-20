# MCP Server Development - Agent Awareness (SAP-014)

**SAP ID**: SAP-014
**Version**: 1.0.0
**Status**: ⚠️ **DEPRECATED** (as of 2025-11-12)
**Last Updated**: 2025-11-12

---

## ⚠️ DEPRECATION NOTICE

**SAP-014 is deprecated as of 2025-11-12. Use SAP-047 (Capability Server Template) for new projects.**

**Why deprecated?**
- SAP-047 provides multi-interface support (CLI, REST, MCP) vs MCP-only
- SAP-047 includes architectural patterns (SAP-042-047: registry, bootstrap, composition)
- SAP-047 reduces setup time from 40-60h to 5 minutes (2,271% ROI)

**Migration path**: See [SAP-047 Adoption Blueprint](../capability-server-template/adoption-blueprint.md)

**Quick start**:
```bash
python scripts/create-capability-server.py \
    --name "YourCapability" \
    --namespace yournamespace \
    --enable-mcp \
    --output ~/projects/your-capability
```

**Support timeline**: SAP-014 supported until 2025-12-31 for existing projects only.

---

## 📖 Quick Reference

**New to SAP-014?** → Read **[README.md](README.md)** first (8-min read)

The README provides:
- 🚀 **Quick Start** - 6-step MCP development workflow (create → implement → test → configure → restart → use)
- 📚 **Time Savings** - 80% faster setup (fast-setup vs manual), 100% protocol compliance (FastMCP), 90% namespace consistency
- 🎯 **MCP Core Concepts** - Tools (functions AI calls), Resources (data AI reads), Prompts (interaction templates)
- 🔧 **CLI Commands** - create-mcp-server, mcp-validate-namespace, mcp-claude-config, mcp-test for streamlined development
- 📊 **Chora MCP Conventions v1.0** - namespace:tool_name pattern, namespace://type/id URIs for composability
- 🔗 **Integration** - Works with SAP-003 (Bootstrap), SAP-004 (Testing), SAP-005 (CI/CD), SAP-011 (Docker)

This AGENTS.md provides: Agent-specific patterns for MCP server development, tool/resource implementation, and client integration.

---

## Progressive Context Loading

```yaml
phase_1_quick_reference:
  target_audience: "All agents (first-time orientation)"
  estimated_tokens: 8000
  estimated_time_minutes: 5
  sections:
    - "1. Quick Start for Agents"
    - "2. What You Can Do"
    - "3. When to Use This Capability"
    - "4. Common User Signals"

phase_2_implementation:
  target_audience: "Agents implementing MCP servers"
  estimated_tokens: 25000
  estimated_time_minutes: 15
  sections:
    - "5. How It Works"
    - "6. Key Workflows"
    - "7. Integration with Other SAPs"

phase_3_deep_dive:
  target_audience: "Agents debugging or customizing MCP servers"
  estimated_tokens: 50000
  estimated_time_minutes: 30
  files_to_read:
    - "protocol-spec.md (complete MCP specification)"
    - "capability-charter.md (design rationale)"
    - "static-template/mcp-templates/ (templates)"
    - "docs/standards/CHORA_MCP_CONVENTIONS_v1.0.md (conventions)"
```

---

## 1. Quick Start for Agents

### What is MCP Server Development? (60-second overview)

**MCP Server Development (SAP-014)** provides **rapid MCP server scaffolding** for connecting AI assistants to tools, data, and resources:

- **FastMCP-based**: Uses official FastMCP Python library
- **Chora MCP Conventions**: Standardized naming, namespacing, URI patterns
- **Complete Templates**: Server, tests, client configs, documentation
- **Tool/Resource/Prompt Patterns**: Battle-tested implementations
- **Client Configuration**: Claude Desktop, Cursor, Cline ready

**Purpose**: Build production-ready MCP servers in 30-60 minutes instead of 8-16 hours.

**Key Benefits**:
- **Fast Scaffolding**: Templates for all MCP server components
- **Protocol Compliance**: Guaranteed MCP specification adherence
- **Consistent Conventions**: Interoperable across MCP ecosystem
- **Testing Included**: pytest patterns for MCP tool/resource testing

---

### When Should You Use This?

**Use MCP Server Development when**:
- User asks "create an MCP server"
- Need to expose tools/functions to Claude/GPT-4
- Building data source integrations for AI assistants
- Developing computational resource exposures
- User mentions "FastMCP", "Model Context Protocol", or "MCP"

**Don't use MCP Server Development when**:
- User wants RESTful API (MCP is JSON-RPC over stdio/SSE/WebSocket)
- Non-Python project (MCP available in other languages, different SAP)
- Quick prototyping without MCP client (overhead not justified)
- User explicitly wants different protocol (GraphQL, gRPC, etc.)

---

### Quick Command Reference

```bash
# Scaffold new MCP server from templates
python scripts/scaffold_mcp_server.py --namespace myserver --name "My Server"

# Run MCP server (stdio transport)
python -m myserver.server

# Test MCP server
pytest tests/test_server.py

# Configure Claude Desktop
# Edit: ~/Library/Application Support/Claude/claude_desktop_config.json
```

---

## 2. What You Can Do

### Core Capabilities

1. **Scaffold MCP Server**
   - FastMCP server entry point
   - Chora MCP Conventions implementation
   - Tool/resource/prompt patterns
   - Testing infrastructure

2. **Implement Tools** (functions AI can call)
   - Define tool functions with type hints
   - Implement request/response patterns
   - Handle errors gracefully
   - Use namespaced naming (e.g., "myserver:create_task")

3. **Implement Resources** (data AI can read)
   - Define resource URIs (e.g., "myserver://templates/daily.md")
   - Provide read access to data sources
   - Support dynamic resource lists

4. **Implement Prompts** (pre-defined interactions)
   - Create prompt templates for common tasks
   - Provide contextual guidance to AI
   - Include dynamic prompt parameters

5. **Configure MCP Clients**
   - Claude Desktop JSON configuration
   - Cursor settings
   - Cline integration
   - Test with multiple clients

---

### Integration Points

**SAP-004 (testing-framework)**:
- MCP server testing patterns (pytest)
- Tool/resource mocking
- Integration tests

**SAP-011 (docker-operations)**:
- Docker-based MCP server deployment
- Containerized testing
- Production deployment patterns

**SAP-003 (project-bootstrap)**:
- MCP server as project template option
- Integrated with chora-base scaffolding

---

## 3. When to Use This Capability

### User Signal Pattern: MCP Server Creation

| User Statement | Interpretation | Recommended Action |
|----------------|----------------|---------------------|
| "Create an MCP server" | New MCP server needed | Scaffold from SAP-014 templates |
| "Add FastMCP to project" | Existing project, add MCP | Install FastMCP, add server.py |
| "Expose tools to Claude" | Tool integration needed | Implement @mcp.tool() functions |
| "Connect data source to AI" | Resource integration | Implement @mcp.resource() endpoints |
| "Configure Claude Desktop for MCP" | Client configuration | Update claude_desktop_config.json |

---

### User Signal Pattern: MCP Development

| User Statement | Interpretation | Recommended Action |
|----------------|----------------|---------------------|
| "How do I add a new tool?" | Tool implementation | Use @mcp.tool() decorator pattern |
| "How to test MCP tools?" | Testing guidance | Use pytest with MCP mocking |
| "MCP server not showing in Claude" | Client config issue | Check claude_desktop_config.json |
| "Tool names not following conventions" | Naming issue | Use make_tool_name() helper |
| "How to deploy MCP server?" | Deployment question | Provide Docker/production patterns |

---

## 4. Common User Signals

### Signal 1: "Create an MCP server for task management"

**Context**: User wants new MCP server with custom tools

**Agent Response**:
1. Scaffold MCP server from templates:
   ```bash
   python scripts/scaffold_mcp_server.py \
     --namespace taskmgr \
     --name "Task Manager MCP Server" \
     --enable-namespacing true
   ```

2. Implement task management tools:
   ```python
   from fastmcp import FastMCP
   from .mcp import make_tool_name

   mcp = FastMCP("Task Manager")

   @mcp.tool()
   def create_task(title: str, description: str, priority: int = 0) -> dict:
       """Create a new task."""
       # Implementation
       return {"status": "created", "task_id": "123"}

   @mcp.tool()
   def list_tasks(status: str = "open") -> list[dict]:
       """List tasks by status."""
       # Implementation
       return [{"id": "123", "title": "Example", "status": "open"}]
   ```

3. Configure Claude Desktop:
   ```json
   {
     "mcpServers": {
       "taskmgr": {
         "command": "python",
         "args": ["-m", "taskmgr.server"],
         "cwd": "/path/to/taskmgr"
       }
     }
   }
   ```

4. Test MCP server:
   ```bash
   pytest tests/test_server.py -v
   ```

**Expected Outcome**: Working MCP server with task management tools

---

### Signal 2: "How do I add a new tool to my MCP server?"

**Context**: Existing MCP server, user wants to add functionality

**Agent Response**:
1. Open server.py and add tool function:
   ```python
   @mcp.tool()
   def new_tool_function(param1: str, param2: int) -> dict:
       """Tool description (shown to AI)."""
       # Validate inputs
       if not param1:
           raise ValueError("param1 is required")

       # Implement logic
       result = do_something(param1, param2)

       # Return result
       return {"status": "success", "result": result}
   ```

2. Add tests for new tool:
   ```python
   # tests/test_server.py
   def test_new_tool_function():
       result = new_tool_function("test", 42)
       assert result["status"] == "success"
   ```

3. Run tests:
   ```bash
   pytest tests/test_server.py::test_new_tool_function -v
   ```

4. Restart MCP server (if running) to load new tool

**Expected Outcome**: New tool added and tested

---

### Signal 3: "MCP server not showing up in Claude Desktop"

**Context**: Configuration issue preventing Claude from discovering server

**Agent Response**:
1. Check Claude Desktop config file location:
   ```bash
   # macOS
   ~/Library/Application Support/Claude/claude_desktop_config.json

   # Windows
   %APPDATA%/Claude/claude_desktop_config.json

   # Linux
   ~/.config/claude/claude_desktop_config.json
   ```

2. Verify JSON syntax:
   ```json
   {
     "mcpServers": {
       "server-name": {
         "command": "python",
         "args": ["-m", "package_name.server"],
         "cwd": "/absolute/path/to/project"
       }
     }
   }
   ```

3. Common issues to check:
   - **Trailing commas**: Remove trailing commas in JSON
   - **Absolute paths**: Use full paths for "cwd"
   - **Python path**: Ensure "python" is correct (may need "python3")
   - **Module name**: Verify "-m package_name.server" matches structure

4. Restart Claude Desktop after config changes

5. Check Claude's developer console for errors:
   - View → Developer → Toggle Developer Tools

**Expected Outcome**: MCP server appears in Claude Desktop

---

### Signal 4: "How do I test MCP tools?"

**Context**: User needs testing patterns for MCP server

**Agent Response**:
1. Create test file with pytest:
   ```python
   # tests/test_server.py
   import pytest
   from myserver.server import create_task, list_tasks

   def test_create_task():
       """Test task creation."""
       result = create_task(title="Test Task", description="Test")
       assert result["status"] == "created"
       assert "task_id" in result

   def test_list_tasks():
       """Test task listing."""
       tasks = list_tasks(status="open")
       assert isinstance(tasks, list)

   def test_create_task_validation():
       """Test input validation."""
       with pytest.raises(ValueError):
           create_task(title="", description="Test")
   ```

2. Run tests:
   ```bash
   pytest tests/test_server.py -v
   ```

3. For integration testing with MCP client:
   ```python
   # tests/test_integration.py
   from mcp import ClientSession, StdioServerParameters
   from mcp.client.stdio import stdio_client

   async def test_mcp_tool_call():
       """Test tool via MCP protocol."""
       server_params = StdioServerParameters(
           command="python",
           args=["-m", "myserver.server"]
       )

       async with stdio_client(server_params) as (read, write):
           async with ClientSession(read, write) as session:
               await session.initialize()

               # Call tool via MCP
               result = await session.call_tool(
                   "create_task",
                   arguments={"title": "Test", "description": "Integration test"}
               )

               assert result["status"] == "created"
   ```

**Expected Outcome**: Comprehensive test coverage for MCP tools

---

### Signal 5: "How do I deploy my MCP server?"

**Context**: User ready to deploy MCP server to production

**Agent Response**:
1. **Local Development** (already set up):
   ```json
   {
     "mcpServers": {
       "myserver": {
         "command": "python",
         "args": ["-m", "myserver.server"],
         "cwd": "/path/to/myserver"
       }
     }
   }
   ```

2. **Docker Deployment**:
   ```dockerfile
   # Dockerfile
   FROM python:3.11-slim

   WORKDIR /app
   COPY . /app

   RUN pip install -e .

   CMD ["python", "-m", "myserver.server"]
   ```

   Build and run:
   ```bash
   docker build -t myserver .
   docker run -i myserver
   ```

3. **Production Deployment** (with monitoring):
   ```python
   # Add logging
   import logging
   logging.basicConfig(level=logging.INFO)

   # Add error handling
   @mcp.tool()
   def safe_tool(param: str) -> dict:
       try:
           result = do_something(param)
           return {"status": "success", "result": result}
       except Exception as e:
           logging.error(f"Tool error: {e}")
           return {"status": "error", "message": str(e)}
   ```

4. **Client Configuration** (production):
   ```json
   {
     "mcpServers": {
       "myserver": {
         "command": "docker",
         "args": ["run", "-i", "myserver:latest"]
       }
     }
   }
   ```

**Expected Outcome**: MCP server deployed and accessible to clients

---

## 5. How It Works

### MCP Protocol Overview

**MCP (Model Context Protocol)** enables AI assistants to interact with:
- **Tools**: Functions AI can call (like API endpoints)
- **Resources**: Data AI can read (like files or databases)
- **Prompts**: Pre-defined templates for AI interactions

**Transport**: JSON-RPC 2.0 over stdio, SSE, or WebSocket

**Example Tool Call Flow**:
```
Claude Desktop → MCP Client → JSON-RPC Request → MCP Server (stdio)
                                                         ↓
                                                   Tool Function
                                                         ↓
Claude Desktop ← MCP Client ← JSON-RPC Response ← Result
```

---

### Chora MCP Conventions v1.0

**Tool Naming**:
```
Pattern: namespace:tool_name
Example: taskmgr:create_task
Rules:
- Namespace: 3-20 chars, lowercase alphanumeric, starts with letter
- Tool name: lowercase, snake_case
```

**Resource URIs**:
```
Pattern: namespace://type/id
Example: taskmgr://templates/daily.md
Rules:
- Same namespace rules as tools
- Type and id: lowercase, alphanumeric with _/-/.
```

**Benefits**:
- **Discoverability**: AI can infer capabilities from namespace
- **Composability**: Servers can reference each other
- **Consistency**: Predictable patterns across ecosystem

---

### FastMCP Server Structure

```python
from fastmcp import FastMCP

# Initialize server
mcp = FastMCP("Server Name")

# Tool (function AI can call)
@mcp.tool()
def tool_name(param: str) -> dict:
    """Tool description."""
    return {"result": "value"}

# Resource (data AI can read)
@mcp.resource(uri="namespace://type/id")
def resource_name() -> str:
    """Resource description."""
    return "Resource content"

# Prompt (pre-defined interaction)
@mcp.prompt()
def prompt_name() -> str:
    """Prompt description."""
    return "Prompt template"

# Run server (stdio transport)
if __name__ == "__main__":
    mcp.run()
```

---

## 6. Key Workflows

### Workflow 1: Scaffold New MCP Server

**Goal**: Create new MCP server from SAP-014 templates

**Steps**:

1. Run scaffolding script:
   ```bash
   python scripts/scaffold_mcp_server.py \
     --namespace myserver \
     --name "My MCP Server" \
     --enable-namespacing true \
     --output /path/to/output
   ```

2. Review generated files:
   ```
   myserver/
   ├── server.py              # FastMCP server entry point
   ├── mcp/__init__.py        # Namespace helpers
   ├── pyproject.toml         # FastMCP dependency
   ├── tests/test_server.py   # pytest tests
   ├── AGENTS.md              # Agent guidance
   ├── CLAUDE.md              # Claude Desktop config
   └── README.md              # Documentation
   ```

3. Install dependencies:
   ```bash
   cd myserver
   pip install -e .
   ```

4. Run server:
   ```bash
   python -m myserver.server
   ```

5. Configure Claude Desktop:
   ```json
   {
     "mcpServers": {
       "myserver": {
         "command": "python",
         "args": ["-m", "myserver.server"],
         "cwd": "/absolute/path/to/myserver"
       }
     }
   }
   ```

6. Restart Claude Desktop and verify server appears

**Expected Outcome**: Working MCP server scaffold ready for customization

**Time Estimate**: 10-15 minutes

---

### Workflow 2: Implement Custom Tool

**Goal**: Add new tool to existing MCP server

**Steps**:

1. Open server.py and add tool function:
   ```python
   @mcp.tool()
   async def analyze_data(data_source: str, metric: str) -> dict:
       """Analyze data from source and calculate metric.

       Args:
           data_source: Path to data file or database
           metric: Metric to calculate (mean, median, sum)

       Returns:
           Analysis results with metric value and metadata
       """
       # Validate inputs
       if metric not in ["mean", "median", "sum"]:
           raise ValueError(f"Invalid metric: {metric}")

       # Load data
       data = load_data(data_source)

       # Calculate metric
       if metric == "mean":
           value = sum(data) / len(data)
       elif metric == "median":
           value = sorted(data)[len(data) // 2]
       else:
           value = sum(data)

       return {
           "metric": metric,
           "value": value,
           "data_points": len(data),
           "source": data_source
       }
   ```

2. Add helper functions:
   ```python
   def load_data(source: str) -> list[float]:
       """Load data from source."""
       # Implementation
       pass
   ```

3. Add tests:
   ```python
   # tests/test_server.py
   import pytest

   @pytest.mark.asyncio
   async def test_analyze_data():
       result = await analyze_data("test.csv", "mean")
       assert result["metric"] == "mean"
       assert "value" in result

   @pytest.mark.asyncio
   async def test_analyze_data_invalid_metric():
       with pytest.raises(ValueError):
           await analyze_data("test.csv", "invalid")
   ```

4. Run tests:
   ```bash
   pytest tests/test_server.py -v
   ```

5. Restart MCP server to load new tool

**Expected Outcome**: New tool available in Claude Desktop

**Time Estimate**: 15-30 minutes

---

### Workflow 3: Implement Resource with Dynamic URI

**Goal**: Expose data as MCP resource with dynamic URIs

**Steps**:

1. Define resource with URI pattern:
   ```python
   @mcp.resource(uri="myserver://reports/{report_id}")
   async def get_report(uri: str) -> str:
       """Get report by ID.

       Args:
           uri: Resource URI (e.g., "myserver://reports/2025-11-05")

       Returns:
           Report content in markdown format
       """
       # Extract report_id from URI
       report_id = uri.split("/")[-1]

       # Load report
       report = load_report(report_id)

       # Return as markdown
       return f"# Report {report_id}\n\n{report}"
   ```

2. Implement list_resources (for resource discovery):
   ```python
   @mcp.list_resources()
   async def list_reports() -> list[dict]:
       """List available reports."""
       reports = get_all_reports()
       return [
           {
               "uri": f"myserver://reports/{r['id']}",
               "name": r["title"],
               "description": r["summary"]
           }
           for r in reports
       ]
   ```

3. Add tests:
   ```python
   @pytest.mark.asyncio
   async def test_get_report():
       content = await get_report("myserver://reports/2025-11-05")
       assert "# Report 2025-11-05" in content

   @pytest.mark.asyncio
   async def test_list_reports():
       reports = await list_reports()
       assert len(reports) > 0
       assert "uri" in reports[0]
   ```

4. Test in Claude Desktop:
   - Ask Claude to "read report 2025-11-05"
   - Claude should use resource to fetch content

**Expected Outcome**: Dynamic resources accessible to Claude

**Time Estimate**: 20-30 minutes

---

### Workflow 4: Configure Multiple MCP Clients

**Goal**: Make MCP server work with Claude Desktop, Cursor, and Cline

**Steps**:

1. **Claude Desktop** configuration:
   ```json
   // ~/Library/Application Support/Claude/claude_desktop_config.json
   {
     "mcpServers": {
       "myserver": {
         "command": "python",
         "args": ["-m", "myserver.server"],
         "cwd": "/path/to/myserver"
       }
     }
   }
   ```

2. **Cursor** configuration:
   ```json
   // Cursor settings
   {
     "mcp.servers": {
       "myserver": {
         "command": "python",
         "args": ["-m", "myserver.server"],
         "cwd": "/path/to/myserver"
       }
     }
   }
   ```

3. **Cline** configuration:
   ```json
   // Cline settings
   {
     "mcpServers": {
       "myserver": {
         "command": "python",
         "args": ["-m", "myserver.server"],
         "cwd": "/path/to/myserver"
       }
     }
   }
   ```

4. Test with each client:
   - Claude Desktop: Ask Claude to use your tools
   - Cursor: Use Composer to call tools
   - Cline: Verify tools appear in tool list

**Expected Outcome**: MCP server works across all clients

**Time Estimate**: 10-20 minutes

---

### Workflow 5: Deploy MCP Server with Docker

**Goal**: Containerize MCP server for production deployment

**Steps**:

1. Create Dockerfile:
   ```dockerfile
   FROM python:3.11-slim

   WORKDIR /app
   COPY . /app

   RUN pip install --no-cache-dir -e .

   # Run MCP server on stdio
   CMD ["python", "-m", "myserver.server"]
   ```

2. Create .dockerignore:
   ```
   __pycache__/
   *.pyc
   .pytest_cache/
   .venv/
   *.egg-info/
   ```

3. Build Docker image:
   ```bash
   docker build -t myserver:latest .
   ```

4. Test locally:
   ```bash
   docker run -i myserver:latest
   # Should start MCP server on stdio
   ```

5. Update client configuration:
   ```json
   {
     "mcpServers": {
       "myserver": {
         "command": "docker",
         "args": ["run", "-i", "myserver:latest"]
       }
     }
   }
   ```

6. Deploy to production:
   ```bash
   # Push to registry
   docker tag myserver:latest registry.example.com/myserver:latest
   docker push registry.example.com/myserver:latest

   # Pull and run on production
   docker pull registry.example.com/myserver:latest
   docker run -d -i registry.example.com/myserver:latest
   ```

**Expected Outcome**: Dockerized MCP server ready for production

**Time Estimate**: 20-40 minutes

---

## 7. Integration with Other SAPs

### SAP-004 (testing-framework)

**Integration**: pytest patterns for MCP testing

**Agent workflow**:
1. Use pytest for unit tests (tool functions)
2. Use pytest-asyncio for async tool tests
3. Mock external dependencies in tests

### SAP-011 (docker-operations)

**Integration**: Docker deployment patterns

**Agent workflow**:
1. Use Docker for containerized MCP servers
2. Deploy to production with Docker
3. Integrate with CI/CD for automated builds

### SAP-003 (project-bootstrap)

**Integration**: MCP server as project template option

**Agent workflow**:
1. Include MCP server option in project scaffolding
2. Pre-configure FastMCP dependencies
3. Include MCP-specific documentation

---

## 8. Best Practices

### Best Practice 1: Follow Chora MCP Conventions

**Why**: Interoperability, discoverability, consistency

**How**: Use make_tool_name() and make_resource_uri() helpers

### Best Practice 2: Comprehensive Tool Descriptions

**Why**: AI needs clear descriptions to use tools correctly

**How**: Write detailed docstrings with Args, Returns, Examples

### Best Practice 3: Validate Tool Inputs

**Why**: Prevent errors, provide clear feedback

**How**: Check inputs, raise ValueError with clear messages

### Best Practice 4: Test All Tools and Resources

**Why**: Ensure reliability, catch regressions

**How**: pytest with 100% tool coverage

### Best Practice 5: Use Absolute Paths in Client Configs

**Why**: Avoid "module not found" errors

**How**: Always use full paths for "cwd" in client configs

---

## 9. Common Pitfalls

### Pitfall 1: Relative Paths in Client Config

**Problem**: "cwd": "./myserver" fails to find module

**Fix**: Use absolute paths: "cwd": "/full/path/to/myserver"

### Pitfall 2: Missing Tool Descriptions

**Problem**: AI can't understand what tool does

**Fix**: Write comprehensive docstrings for all tools

### Pitfall 3: Not Restarting Claude After Config Changes

**Problem**: Changes don't take effect

**Fix**: Always restart Claude Desktop after config changes

### Pitfall 4: Synchronous Tools Blocking Server

**Problem**: Long-running sync tools block other requests

**Fix**: Use async def for tools with I/O or long operations

### Pitfall 5: Not Following Naming Conventions

**Problem**: Tool names inconsistent, hard to discover

**Fix**: Use namespace:tool_name pattern consistently

---

## 10. Self-Evaluation

### Workflow Coverage Analysis

**Protocol Spec Workflows**: 5 (specified in protocol-spec.md)
1. Scaffold MCP server (templates)
2. Implement tools (FastMCP @mcp.tool())
3. Implement resources (@mcp.resource())
4. Configure clients (Claude Desktop, Cursor, Cline)
5. Deploy server (local, Docker, production)

**AGENTS.md Workflows**: 5 (implemented above)
1. Scaffold New MCP Server
2. Implement Custom Tool
3. Implement Resource with Dynamic URI
4. Configure Multiple MCP Clients
5. Deploy MCP Server with Docker

**CLAUDE.md Workflows**: 3 (to be implemented in CLAUDE.md)
1. Create MCP Server from Templates (Bash + Write tools)
2. Add Tools to Existing Server (Read + Edit tools)
3. Configure and Test MCP Client (Edit + Bash tools)

**Coverage**: 5/5 = 100% (all protocol-spec workflows covered)

**Variance**: 40% (5 generic workflows vs 3 Claude-specific workflows)

**Rationale**: CLAUDE.md focuses on tool-specific patterns (Bash/Read/Write/Edit), while AGENTS.md provides comprehensive guidance applicable to all agents. Both provide equivalent support for SAP-014 adoption.

**Conclusion**: ✅ Equivalent support across agent types

---

## 11. Version History

**1.0.0** (2025-11-05):
- Initial AGENTS.md for SAP-014 (mcp-server-development)
- 5 workflows: scaffold, implement tool, implement resource, configure clients, deploy
- Integration with SAP-004, SAP-011, SAP-003
- 5 best practices, 5 common pitfalls
- Progressive context loading frontmatter

---

## Quick Links

- **Protocol Spec**: [protocol-spec.md](protocol-spec.md) - Complete MCP specification
- **Capability Charter**: [capability-charter.md](capability-charter.md) - Design rationale
- **Adoption Blueprint**: [adoption-blueprint.md](adoption-blueprint.md) - Installation guide
- **MCP Templates**: [../../../static-template/mcp-templates/](../../../static-template/mcp-templates/)
- **Chora MCP Conventions**: [../../../docs/standards/CHORA_MCP_CONVENTIONS_v1.0.md](../../../docs/standards/CHORA_MCP_CONVENTIONS_v1.0.md)

---

**Next Steps**:
1. Read [CLAUDE.md](CLAUDE.md) for Claude Code tool patterns
2. Read [protocol-spec.md](protocol-spec.md) for complete MCP specification
3. Read [adoption-blueprint.md](adoption-blueprint.md) for installation steps
4. See [../AGENTS.md](../AGENTS.md) for SAP catalog navigation
