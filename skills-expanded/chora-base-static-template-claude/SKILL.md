# CLAUDE.md - Example Template

**This is an example CLAUDE.md file** showing how to customize Claude-specific guidance for your project.

**For the canonical CLAUDE.md blueprint, see:** `blueprints/CLAUDE.md.blueprint`

---

## Purpose of This File

This example demonstrates how a generated project's CLAUDE.md should look after customization. When you generate a project from chora-base, you'll get the blueprint version. Customize it with your project-specific details.

---

## Example Project Context

```markdown
# CLAUDE.md - [Your Project Name]

**For [Your Project Name]** - MCP Server for [domain]

Read first: [AGENTS.md](AGENTS.md) for generic AI agent guidance.
This file provides Claude-specific optimizations for this project.

## Quick Start for Claude

### Project Specifics
- **Domain:** [e.g., GitHub integration, database tools, etc.]
- **Key Dependencies:** [FastMCP, specific libraries]
- **Architecture:** [Describe specific architecture]

### Critical Context
Load immediately:
1. AGENTS.md - Project structure and conventions
2. src/[package]/mcp/server.py - MCP server implementation
3. Current task from checkpoint (if resuming)

### Common Patterns in This Project
- **MCP tools:** Defined in src/[package]/mcp/tools.py
- **Error handling:** Use ErrorFormatter from utils/errors.py
- **State management:** StatefulObject for persistence
- **Testing:** pytest with fixtures in tests/conftest.py

### Included Skilled Awareness Packages (SAPs)

This project includes the following SAPs for enhanced development workflows:

- **SAP-053 (Conflict Resolution)**: Pre-merge conflict detection
  - Command: `just conflict-check` - Check for merge conflicts before creating PR
  - Command: `just conflict-check-json` - JSON output for automation
  - Command: `just conflict-check-verbose` - Detailed conflict information
  - Command: `just conflict-status` - Quick status check
  - See: `docs/skilled-awareness/conflict-resolution/` for full documentation

## Domain-Specific Context Management

### Essential Context for This Project (0-10k tokens)
1. **Active MCP tools** you're modifying
2. **Relevant API integration** docs (if external API)
3. **Data models** (if working with specific data structures)
4. **Current task** definition

### Extended Context (10-50k tokens)
1. All MCP tools (src/[package]/mcp/tools.py)
2. Utilities (src/[package]/utils/)
3. Full test suite
4. API documentation for external services

## Project-Specific Patterns

### MCP Tool Implementation
```python
# This project's pattern for MCP tools
from fastmcp import FastMCP

mcp = FastMCP("[server-name]")

@mcp.tool()
async def tool_name(param: str) -> dict:
    """Tool description.

    Args:
        param: Description

    Returns:
        Result dictionary
    """
    # Implementation
```

### Error Handling Pattern
```python
# This project uses ErrorFormatter utility
from [package].utils.errors import ErrorFormatter
from [package].utils.responses import Response

def example():
    if error_condition:
        error_msg = ErrorFormatter.not_found(
            entity_type="resource",
            entity_id=id,
            available=available_ids
        )
        return Response.error(error_code="not_found", message=error_msg)
```

## Testing Patterns for This Project

### Test Structure
```python
# tests/test_tools.py
import pytest
from [package].mcp.server import mcp

def test_tool_name_happy_path():
    """Test tool_name with valid input."""
    result = mcp.call_tool("tool_name", {"param": "value"})
    assert result["status"] == "success"
```

### Fixtures
```python
# tests/conftest.py
@pytest.fixture
def mock_api():
    """Mock external API for testing."""
    # Project-specific mock setup
```

## Development Workflow for This Project

Follow chora-base workflows with these project adaptations:

### DDD (Documentation-Driven Design)
1. Document MCP tool interface in dev-docs/design/
2. Specify input/output schemas
3. List error conditions
4. **Project twist:** Include MCP Inspector screenshots

### BDD (Behavior-Driven Development)
1. Write Gherkin scenarios for tool behaviors
2. Implement as pytest tests
3. **Project twist:** Test via MCP Inspector for integration

### TDD (Test-Driven Development)
1. Write failing test
2. Implement tool
3. Refactor
4. **Project twist:** Run MCP Inspector after each iteration

## Memory System Integration

### Event Log Usage
```bash
# Log MCP tool invocations
[package]-memory query --type tool.invoked --since 24h

# Find failed tool calls
[package]-memory query --type tool.failed --since 7d
```

### Knowledge Graph
```bash
# Search for solutions to API integration issues
[package]-memory knowledge search --tag api-integration

# Store learned patterns
echo "Pattern for [API] rate limiting: [solution]" | \
  [package]-memory knowledge create "API Rate Limiting" \
  --tag api-integration --tag rate-limiting
```

## Common Tasks with Claude

### Add New MCP Tool
```markdown
"Implement new MCP tool: [name]

Specification:
- Purpose: [what it does]
- Input: [schema]
- Output: [schema]
- External API: [if applicable]

Follow pattern in src/[package]/mcp/tools.py
Include comprehensive tests
Add to README tool list
Test with MCP Inspector"
```

### Debug Tool Failure
```markdown
"Debug MCP tool failure:

Tool: [name]
Error: [from logs/inspector]
Input: [what was sent]

Context:
- src/[package]/mcp/tools.py:[line]
- Recent changes: $(git log --oneline -5 tools.py)
- Related: [external API docs if applicable]

Reproduce: [steps]"
```

## Project Metrics

Track Claude effectiveness for this project:

```python
from [package].utils.claude_metrics import ClaudeROICalculator

calculator = ClaudeROICalculator(developer_hourly_rate=100)
# Track sessions specific to MCP tool development
```

## Resources

**Project-Specific:**
- MCP Protocol: https://modelcontextprotocol.io
- FastMCP Docs: https://github.com/jlowin/fastmcp
- [External API]: [link to API docs]

**Chora-Base Patterns:**
- /claude/ - Pattern library in chora-base repo
- dev-docs/workflows/ - DDD, BDD, TDD workflows
- dev-docs/examples/ - Complete feature walkthroughs

**Nested CLAUDE.md Files:**
- [tests/CLAUDE.md](tests/CLAUDE.md) - Test-specific patterns
- [.chora/memory/CLAUDE.md](.chora/memory/CLAUDE.md) - Memory integration
- [docker/CLAUDE.md](docker/CLAUDE.md) - Docker assistance (if applicable)
- [scripts/CLAUDE.md](scripts/CLAUDE.md) - Automation patterns (if applicable)
```

---

## How to Customize This Template

When you create a project from chora-base:

1. **Replace placeholders:**
   - `[Your Project Name]` → Actual project name
   - `[package]` → Your package name
   - `[domain]` → Your specific domain (e.g., "GitHub integration")

2. **Add project specifics:**
   - Key dependencies and versions
   - Domain-specific patterns
   - External API integration details
   - Common data structures

3. **Customize patterns:**
   - Update code examples to match your actual code
   - Add project-specific error handling patterns
   - Document domain-specific edge cases

4. **Integrate with workflows:**
   - Adapt DDD/BDD/TDD to your domain
   - Add domain-specific testing strategies
   - Document integration points

5. **Link resources:**
   - External API documentation
   - Framework-specific guides
   - Domain-specific best practices

---

**This is a template/example file.** The actual CLAUDE.md in generated projects will be created from `blueprints/CLAUDE.md.blueprint` and should be customized for the specific project.
