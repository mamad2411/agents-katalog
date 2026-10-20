---
description: "Python coding conventions for agents, tools, MCP servers, validators, and diagram scripts"
applyTo: "**/*.py"
---

# Python Guidelines

Instructions for writing clean, consistent Python in this repository.
Target Python 3.13+ with Ruff for linting and formatting.

## Project Context

Python is used for six purposes in this repo:

1. **Agents** — orchestration and domain logic in `src/agents/`
2. **Tools** — discovery, assessment, deployment, monitoring in `src/tools/`
3. **Configuration** — settings and profiles in `src/config/`
4. **MCP servers** — async servers in `mcp/` (azure-pricing, azure-platform)
5. **Architecture diagrams** — `diagrams` library scripts in `src/tools/python_diagram_generator.py`
6. **Validators & scripts** — security baseline and cost governance in `scripts/validators/`

## Style & Formatting

- **Formatter/Linter**: Ruff (`ruff format`, `ruff check`) — config in `ruff.toml`
- **Lint rules**: `E` (pycodestyle errors), `W` (warnings), `F` (pyflakes), `I` (isort), `B` (bugbear), `C4` (comprehensions), `UP` (pyupgrade), `SIM` (simplify)
- **Line length**: 120 characters
- **Imports**: sorted — stdlib → third-party → first-party (`src.*`)
- **Quotes**: double quotes for strings
- **Type hints**: use for all function signatures
  - Prefer `X | None` over `Optional[X]`
  - Prefer `list[str]` over `List[str]` (modern generics)
  - Use `from __future__ import annotations` only if needed for forward refs

## Package Management

- Dependencies in `requirements.txt` at project root (pinned with `>=`)
- MCP servers may have their own `pyproject.toml`
- Virtual environment: `.venv/` activated via devcontainer
- Install: `pip install -r requirements.txt`

## Naming Conventions

- `snake_case` for functions, variables, and modules
- `PascalCase` for classes
- `UPPER_SNAKE_CASE` for module-level constants
- `_prefixed` for private/internal functions and methods
- Prefix module-level loggers: `logger = logging.getLogger(__name__)`

## Data Models & Configuration

- Use `pydantic.BaseModel` for validated data with external input (API responses, user input)
- Use `pydantic_settings.BaseSettings` for environment-driven config (see `src/config/settings.py`)
- Use `@dataclass` for internal-only data structures without validation needs
- Nest settings classes and compose into a root `Settings` class
- Always use `Field(alias="ENV_VAR_NAME")` for environment variable mapping

```python
from pydantic_settings import BaseSettings
from pydantic import Field

class AzureSettings(BaseSettings):
    subscription_id: str = Field(default="", alias="AZURE_SUBSCRIPTION_ID")
    model_config = {"env_file": ".env", "extra": "ignore"}
```

## Async Patterns

- Use `async def` with `await` — never mix sync and async I/O
- Use `async with` for Azure SDK clients (proper cleanup)
- Use `asyncio.gather()` for parallel independent operations
- Use `aiohttp.ClientSession` for HTTP — create once, reuse across calls
- Handle `azure.identity` credential errors gracefully with fallback

```python
async def discover(self, scope: str) -> DiscoveryResult:
    async with self.credential:
        results = await asyncio.gather(
            self._collect_management_groups(scope),
            self._collect_subscriptions(scope),
            self._collect_resources(scope),
        )
    return DiscoveryResult(...)
```

## Error Handling & Logging

- Use module-level `logger = logging.getLogger(__name__)`
- Never bare `except:` — always catch specific exceptions
- Log at appropriate levels: `logger.info` for flow, `logger.error` for failures
- Use structured context in log messages: `logger.info("Phase %d: %s", num, desc)`
- Raise custom exceptions for domain errors, catch SDK exceptions at boundaries

## Path Handling

- Use `pathlib.Path` exclusively — never string concatenation for paths
- Use `Path.mkdir(parents=True, exist_ok=True)` for directory creation
- Use `Path.write_text(content, encoding="utf-8")` for file writes

## Conventions

- Prefer f-strings over `.format()` or `%` formatting
- Use context managers (`with`/`async with`) for file and network operations
- Limit function arguments — use dataclass/model for 4+ params
- Keep functions under 50 lines; extract helpers for complexity
- Use `| None` return types when a function can fail gracefully

## Testing

- **Framework**: `pytest` with `pytest-asyncio` for async tests
- **Test files**: `tests/test_{module}.py` matching source module names
- **Async**: decorate with `@pytest.mark.asyncio`
- **Fixtures**: use `@pytest.fixture` for shared setup (credentials, mock data)
- **Mocking**: `unittest.mock.patch` or `pytest-mock` for Azure SDK calls
- **Run**: `python -m pytest tests/ -v`
- **Coverage**: `python -m pytest tests/ --cov=src --cov-report=term`

```python
@pytest.fixture
def discovery():
    return DiscoveryResult(scope="test", scope_type=DiscoveryScope.SUBSCRIPTION, ...)

@pytest.mark.asyncio
async def test_assess(discovery):
    engine = WaraEngine(credential=Mock(), settings=Mock())
    result = await engine.assess(discovery, subscriptions=["sub-001"])
    assert result.overall_score >= 0
```

## Azure SDK

- Use `azure-identity` `DefaultAzureCredential` for auth
- Use `azure-mgmt-*` SDKs for resource management
- Use `azure-mgmt-resourcegraph` for Resource Graph queries
- Always pass credentials via constructor injection (testable)
- Close clients in `finally` or use `async with`

## Security

- Never hardcode credentials, subscription IDs, or tenant IDs
- Use environment variables via `pydantic_settings`
- Reference `src/config/settings.py` for the settings pattern
- Never log secrets or tokens — use `repr()` guards on sensitive fields
- Validate all external input at system boundaries

## Diagram Scripts

Follow the pattern in `src/tools/python_diagram_generator.py`:

- Always set `show=False` to prevent auto-opening
- Use `direction="TB"` (top-to-bottom) for consistency
- Group resources in `Cluster` blocks matching Azure resource groups/scopes
- Use the `ICON_MAP` registry pattern for string→icon class mapping
- Set explicit `filename` parameter to control output location
- Set `graph_attr={"bgcolor": "white", "pad": "0.5"}` for clean output

```python
from diagrams import Cluster, Diagram, Edge
from diagrams.azure.network import VirtualNetworks

with Diagram(
    "Hub Network",
    filename=str(output_dir / "hub-network"),
    show=False,
    direction="TB",
    graph_attr={"bgcolor": "white", "pad": "0.5", "ranksep": "0.8"},
):
    with Cluster("Hub Resource Group"):
        hub_vnet = VirtualNetworks("hub-vnet")
```

## CLI Patterns

CLIs use `typer` + `rich` (see `tools/apex-recall/`, `src/tools/assess_cli.py`):

- Use `typer.Typer()` app with `@app.command()` decorators
- Use `rich.console.Console` for formatted output
- Accept `--json` flag for machine-readable output
- Use `typer.Option()` with help text for all parameters
- Entry points defined in `pyproject.toml` `[project.scripts]`

```python
import typer
from rich.console import Console

app = typer.Typer(help="Tool description")
console = Console()

@app.command()
def show(customer: str, json_output: bool = typer.Option(False, "--json")):
    """Show session state for a customer."""
    ...
```

## Module Structure

- Use absolute imports: `from src.tools.discovery import DiscoveryResult`
- `__init__.py` should only re-export public API (keep minimal)
- Private helpers prefixed with `_` (not imported externally)
- One primary class per module; related helpers in same file
- Module-level docstring explains purpose, lists key exports

## Docstrings

Use triple-quote docstrings (Google-ish style):

- Module docstring at top of every file explaining purpose
- Class docstring on public classes
- Function docstrings for public methods (skip obvious one-liners)
- No docstrings required for private `_prefixed` methods

```python
"""
Discovery — read-only Azure environment inventory collectors.

Collects management groups, subscriptions, resources, policies, RBAC,
network topology, logging config, and security posture.
"""

class DiscoveryCollector:
    """Collects Azure environment inventory via Resource Graph and management APIs."""

    async def discover(self, scope: str, scope_type: DiscoveryScope) -> DiscoveryResult:
        """Run all collectors and return aggregated discovery data."""
        ...
```

## Enums

Use `str, Enum` (or `StrEnum` on 3.11+) for string enumerations:

```python
from enum import Enum

class DiscoveryScope(str, Enum):
    """Scope levels for discovery."""
    TENANT = "tenant"
    MANAGEMENT_GROUP = "management_group"
    SUBSCRIPTION = "subscription"
    RESOURCE_GROUP = "resource_group"
```

- Inherit from `str` so values serialize naturally to JSON
- Use `UPPER_SNAKE_CASE` for member names, lowercase string values
- Group related enums near the dataclass/model that uses them

## MCP Server Patterns

MCP servers use the official `mcp` Python SDK (see `mcp/azure-platform/server.py`):

- Define tools as `mcp.types.Tool` with JSON Schema `inputSchema`
- Register tool handlers with `@server.call_tool()`
- Return `list[TextContent]` from handlers
- Use async handlers with Azure SDK clients
- Group related tools (Resource Graph, Policy, Monitor, Deployment)

```python
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

server = Server("azure-platform")

TOOLS: list[Tool] = [
    Tool(
        name="query_resources",
        description="Execute an Azure Resource Graph KQL query",
        inputSchema={
            "type": "object",
            "properties": {"query": {"type": "string"}},
            "required": ["query"],
        },
    ),
]

@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    return TOOLS

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[TextContent]:
    ...
```
