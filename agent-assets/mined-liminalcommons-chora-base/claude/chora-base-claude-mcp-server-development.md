# MCP Server Development - Claude-Specific Awareness (SAP-014)

**SAP ID**: SAP-014
**Version**: 1.0.0
**Status**: ⚠️ **DEPRECATED** (as of 2025-11-12)
**Last Updated**: 2025-11-12

---

## ⚠️ DEPRECATION NOTICE

**SAP-014 is deprecated. Use SAP-047 (Capability Server Template) for new projects.**

**Quick migration**: `python scripts/create-capability-server.py --enable-mcp`

See [SAP-047 Documentation](../capability-server-template/) for details.

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

This CLAUDE.md provides: Claude Code workflows (Bash mcp commands, Write/Edit tool implementation, Read test logs).

---

## Progressive Context Loading

```yaml
phase_1_quick_reference:
  target_audience: "Claude (first-time orientation)"
  estimated_tokens: 5000
  estimated_time_minutes: 3
  sections:
    - "1. Quick Start for Claude"
    - "2. When to Use MCP Server Development"
    - "3. Tool Integration Patterns"

phase_2_implementation:
  target_audience: "Claude implementing MCP servers"
  estimated_tokens: 15000
  estimated_time_minutes: 10
  sections:
    - "4. Key Workflows (Claude Code)"
    - "5. Integration with Other SAPs"

phase_3_deep_dive:
  target_audience: "Claude debugging MCP servers"
  estimated_tokens: 30000
  estimated_time_minutes: 20
  files_to_read:
    - "protocol-spec.md (complete MCP specification)"
    - "capability-charter.md (design rationale)"
    - "static-template/mcp-templates/ (templates)"
```

---

## 1. Quick Start for Claude

### What is MCP Server Development? (Claude perspective)

**MCP Server Development (SAP-014)** provides **rapid MCP server scaffolding** using FastMCP and Chora MCP Conventions.

**Claude's Role**:
- Scaffold servers using **Bash tool** (scaffolding scripts)
- Create tools/resources using **Write/Edit tool** (Python code)
- Configure clients using **Edit tool** (JSON config files)
- Test servers using **Bash tool** (pytest)

---

### When Should Claude Use This?

**Use MCP Server Development when**:
- User asks "create an MCP server"
- Need to expose tools to Claude Desktop/Cursor/Cline
- Building data source integrations for AI assistants
- User mentions "FastMCP" or "Model Context Protocol"

**Don't use when**:
- User wants RESTful API (different protocol)
- Non-Python project (MCP available in other languages)
- User wants different protocol (GraphQL, gRPC)

---

### Tool Integration Patterns

**Bash tool** (scaffold, test):
```bash
# Scaffold new MCP server
python scripts/scaffold_mcp_server.py --namespace myserver --name "My Server"

# Run MCP server
python -m myserver.server

# Test MCP server
pytest tests/test_server.py -v
```

**Write tool** (new server):
```bash
# Create new server.py
Write myserver/server.py
# Content: FastMCP server with tools/resources
```

**Edit tool** (add tools, configure):
```bash
# Add new tool to existing server
Edit myserver/server.py
# Add @mcp.tool() function

# Configure Claude Desktop
Edit ~/Library/Application Support/Claude/claude_desktop_config.json
# Add mcpServers entry
```

**Read tool** (templates, config):
```bash
# Read template for reference
Read docs/skilled-awareness/mcp-server-development/static-template/server.py.template

# Read existing config
Read ~/.config/claude/claude_desktop_config.json
```

---

## 2. When to Use MCP Server Development

### User Signal Detection

| User Statement | Claude Action | Tools Used |
|----------------|---------------|------------|
| "Create an MCP server" | Scaffold from templates | Bash (scaffold) + Write (files) |
| "Add tool to MCP server" | Implement @mcp.tool() function | Edit (server.py) |
| "Configure Claude Desktop for MCP" | Update config JSON | Edit (claude_desktop_config.json) |
| "Test MCP tools" | Run pytest tests | Bash (pytest) |
| "Deploy MCP server" | Create Dockerfile | Write (Dockerfile) + Bash (docker build) |

---

## 3. Tool Integration Patterns

### Pattern 1: Scaffold-Configure-Test

**Always follow this sequence**:

```markdown
Step 1: Scaffold server
Bash: python scripts/scaffold_mcp_server.py --namespace myserver

Step 2: Configure Claude Desktop
Edit ~/Library/Application Support/Claude/claude_desktop_config.json

Step 3: Test server
Bash: pytest tests/test_server.py -v
```

---

### Pattern 2: Read-Template-Write

**Use templates as reference**:

```markdown
Step 1: Read template
Read static-template/mcp-templates/server.py.template

Step 2: Customize for user needs
[Modify tool functions, resource URIs]

Step 3: Write customized server
Write myserver/server.py
```

---

### Pattern 3: Edit-Test-Restart

**When adding new tools**:

```markdown
Step 1: Add tool to server.py
Edit myserver/server.py
# Add @mcp.tool() function

Step 2: Test new tool
Bash: pytest tests/test_server.py::test_new_tool -v

Step 3: Restart if server running
# User must restart Claude Desktop to load new tool
```

---

## 4. Key Workflows (Claude Code)

### Workflow 1: Create MCP Server from Templates

**Goal**: Scaffold new MCP server using SAP-014 templates

**Tools**: Bash (scaffold), Read (verify), Write (customize)

**Steps**:

1. **Read scaffolding script** to understand options:
   ```bash
   Read scripts/scaffold_mcp_server.py
   # Check available options: --namespace, --name, --output
   ```

2. **Scaffold MCP server**:
   ```bash
   Bash: python scripts/scaffold_mcp_server.py \
     --namespace taskmgr \
     --name "Task Manager MCP Server" \
     --enable-namespacing true \
     --output /path/to/output
   ```

3. **Verify generated files**:
   ```bash
   Bash: ls -R taskmgr/
   # Should show: server.py, mcp/__init__.py, tests/, pyproject.toml
   ```

4. **Install dependencies**:
   ```bash
   Bash: cd taskmgr && pip install -e .
   ```

5. **Test server runs**:
   ```bash
   Bash: python -m taskmgr.server
   # Should start MCP server on stdio (Ctrl+C to stop)
   ```

**Expected Outcome**: Working MCP server scaffold

**Time Estimate**: 10-15 minutes

---

### Workflow 2: Add Tools to Existing Server

**Goal**: Implement new tool in existing MCP server

**Tools**: Read (existing code), Edit (add tool), Bash (test)

**Steps**:

1. **Read existing server.py** to understand structure:
   ```bash
   Read myserver/server.py
   # Check existing tools, import statements
   ```

2. **Add new tool function** using Edit:
   ```bash
   Edit myserver/server.py
   ```

   Add this code:
   ```python
   @mcp.tool()
   async def analyze_data(source: str, metric: str) -> dict:
       """Analyze data and calculate metric.

       Args:
           source: Data source path
           metric: Metric to calculate (mean, median, sum)

       Returns:
           Analysis results
       """
       if metric not in ["mean", "median", "sum"]:
           raise ValueError(f"Invalid metric: {metric}")

       data = load_data(source)
       value = calculate_metric(data, metric)

       return {
           "metric": metric,
           "value": value,
           "data_points": len(data)
       }
   ```

3. **Add test for new tool**:
   ```bash
   Edit tests/test_server.py
   ```

   Add:
   ```python
   @pytest.mark.asyncio
   async def test_analyze_data():
       result = await analyze_data("test.csv", "mean")
       assert result["metric"] == "mean"
       assert "value" in result
   ```

4. **Run tests**:
   ```bash
   Bash: pytest tests/test_server.py::test_analyze_data -v
   ```

5. **If tests pass, inform user** that server needs restart in Claude Desktop

**Expected Outcome**: New tool added and tested

**Time Estimate**: 15-30 minutes

---

### Workflow 3: Configure and Test MCP Client

**Goal**: Set up Claude Desktop to use MCP server

**Tools**: Edit (config), Bash (test), Read (verify)

**Steps**:

1. **Locate Claude Desktop config file**:
   ```bash
   # macOS
   config_path="~/Library/Application Support/Claude/claude_desktop_config.json"

   # Check if exists
   Bash: ls "$config_path"
   ```

2. **Read existing config** (if exists):
   ```bash
   Read ~/Library/Application Support/Claude/claude_desktop_config.json
   # Check existing mcpServers
   ```

3. **Edit config to add MCP server**:
   ```bash
   Edit ~/Library/Application Support/Claude/claude_desktop_config.json
   ```

   Add:
   ```json
   {
     "mcpServers": {
       "taskmgr": {
         "command": "python",
         "args": ["-m", "taskmgr.server"],
         "cwd": "/absolute/path/to/taskmgr"
       }
     }
   }
   ```

4. **Validate JSON syntax**:
   ```bash
   Bash: python -c "import json; json.load(open('$config_path'))"
   # Should print nothing if valid, error if invalid
   ```

5. **Inform user to restart Claude Desktop**:
   ```
   Please restart Claude Desktop to load the new MCP server.
   After restart, you can test by asking me to "list tasks" or "create a task".
   ```

6. **Verify server appears**:
   ```
   After restart, ask user to check if "taskmgr" tools appear when they type "@"
   ```

**Expected Outcome**: MCP server configured and working in Claude Desktop

**Time Estimate**: 10-20 minutes

**Common Issues**:
- **Trailing commas in JSON**: Remove them
- **Relative paths**: Use absolute paths for "cwd"
- **Wrong Python command**: May need "python3" instead of "python"

---

## 5. Integration with Other SAPs

### SAP-004 (testing-framework)

**Integration**: pytest patterns for MCP testing

**Claude workflow**:
1. Use pytest for tool tests
2. Use pytest-asyncio for async tools
3. Mock external dependencies

### SAP-011 (docker-operations)

**Integration**: Docker deployment

**Claude workflow**:
1. Create Dockerfile:
   ```bash
   Write Dockerfile
   # FROM python:3.11-slim, install FastMCP
   ```
2. Build and test:
   ```bash
   Bash: docker build -t myserver .
   Bash: docker run -i myserver
   ```

---

## 6. Claude-Specific Tips

### Tip 1: Read Templates Before Writing

**Pattern**:
```markdown
Step 1: Read template
Read static-template/mcp-templates/server.py.template

Step 2: Customize
[Modify for user needs]

Step 3: Write
Write myserver/server.py
```

**Why**: Templates provide battle-tested patterns

---

### Tip 2: Always Use Absolute Paths in Configs

**Pattern**:
```json
{
  "cwd": "/Users/username/projects/myserver"  // Correct
  "cwd": "./myserver"  // Wrong - will fail
}
```

**Why**: Relative paths cause "module not found" errors

---

### Tip 3: Test Before Configuring Client

**Pattern**:
```markdown
Step 1: Run pytest
Bash: pytest tests/ -v

Step 2: Only if tests pass, configure client
Edit claude_desktop_config.json
```

**Why**: Catch errors before Claude Desktop integration

---

### Tip 4: Validate JSON After Editing

**Pattern**:
```bash
Bash: python -c "import json; json.load(open('config.json'))"
```

**Why**: Invalid JSON breaks Claude Desktop

---

### Tip 5: Inform User to Restart Claude

**Pattern**:
```
After configuration changes, please restart Claude Desktop to load the MCP server.
```

**Why**: Changes don't take effect without restart

---

## 7. Common Pitfalls

### Pitfall 1: Relative Paths in Config

**Problem**: "cwd": "./myserver" fails

**Fix**: Use absolute paths

### Pitfall 2: Missing Docstrings

**Problem**: AI can't understand tool purpose

**Fix**: Write comprehensive docstrings for all tools

### Pitfall 3: Not Restarting Claude

**Problem**: Changes don't appear

**Fix**: Always restart Claude Desktop after config changes

### Pitfall 4: Trailing Commas in JSON

**Problem**: JSON parse error

**Fix**: Remove trailing commas (JSON doesn't allow them)

### Pitfall 5: Sync Tools Blocking

**Problem**: Long-running sync tools block server

**Fix**: Use `async def` for tools with I/O

---

## 8. Quick Reference

### Common Bash Commands

```bash
# Scaffold server
python scripts/scaffold_mcp_server.py --namespace myserver

# Run server
python -m myserver.server

# Test server
pytest tests/test_server.py -v

# Build Docker image
docker build -t myserver .

# Validate JSON
python -c "import json; json.load(open('config.json'))"
```

---

### Claude Desktop Config Template

```json
{
  "mcpServers": {
    "server-name": {
      "command": "python",
      "args": ["-m", "package.server"],
      "cwd": "/absolute/path/to/project"
    }
  }
}
```

---

## 9. Version History

**1.0.0** (2025-11-05):
- Initial CLAUDE.md for SAP-014 (mcp-server-development)
- 3 workflows: create server, add tools, configure client
- Integration with SAP-004, SAP-011
- 5 Claude-specific tips, 5 common pitfalls
- Tool usage patterns (Bash, Read, Write, Edit)

---

## Quick Links

- **AGENTS.md**: [AGENTS.md](AGENTS.md) - Generic agent patterns (5 workflows)
- **Protocol Spec**: [protocol-spec.md](protocol-spec.md) - Complete MCP specification
- **Capability Charter**: [capability-charter.md](capability-charter.md) - Design rationale
- **MCP Templates**: [../../../static-template/mcp-templates/](../../../static-template/mcp-templates/)
- **Chora MCP Conventions**: [../../../docs/standards/CHORA_MCP_CONVENTIONS_v1.0.md](../../../docs/standards/CHORA_MCP_CONVENTIONS_v1.0.md)

---

**Next Steps**:
1. Read [AGENTS.md](AGENTS.md) for comprehensive workflow details
2. Read [protocol-spec.md](protocol-spec.md) for complete MCP specification
3. Read [adoption-blueprint.md](adoption-blueprint.md) for installation steps
4. See [../AGENTS.md](../AGENTS.md) for SAP catalog navigation
