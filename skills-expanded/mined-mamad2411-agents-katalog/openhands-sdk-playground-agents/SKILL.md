# OpenHands Lab - Agent Memory

## Project Overview

**OpenHands Lab** is a local-first playground for exploring the OpenHands SDK. It provides a configuration-driven architecture for swapping agent "Personalities" (prompts), "Capabilities" (custom tools), and "Environments" (Local vs. Docker).

## Project Status: ✅ COMPLETE

All build phases implemented and tested (59 tests passing):
- Phase 1: Core Orchestrator (SessionManager, ConfigLoader, CLI)
- Phase 2: Dynamic Tool Registry (BaseLabTool, ToolLoader, Hot-reload)
- Phase 3: Multi-Tenant UI (Streamlit dashboard)
- Phase 4: Enterprise Safety (RuntimeFactory, SandboxGuard)
- Integration Tests: Blind agent, Safety loop, Context drift, Agent validation

## Quick Commands

```bash
# Install dependencies
uv sync

# Run tests
uv run python -m pytest tests/ -v

# CLI commands
uv run python -m lab --help
uv run python -m lab list
uv run python -m lab config
uv run python -m lab run --agent debug-cli --task "list files"

# Launch Streamlit UI
uv run streamlit run src/lab/ui/main.py
```

## Core Tech Stack
- **Language:** Python 3.12+
- **Package Manager:** `uv`
- **Agent SDK:** `openhands-sdk` v1.16.0+
- **Configuration:** YAML
- **Monitoring:** `watchdog`
- **Visualization:** Streamlit

## SDK Reference
- GitHub: https://github.com/OpenHands/software-agent-sdk
- Documentation: https://docs.openhands.dev/sdk
- Getting Started: https://docs.openhands.dev/sdk/getting-started

## Project Directory Structure
```
openhands-lab/
├── .oh-lab/                    # Session logs and traces
├── config/
│   ├── agents.yaml             # Agent definitions (personas + tools)
│   └── settings.yaml           # Global settings
├── examples/sdk/               # SDK examples imported via sdk-playground agent
├── src/lab/
│   ├── __init__.py
│   ├── __main__.py             # CLI entry point
│   ├── core/
│   │   ├── config.py           # ConfigLoader, LabConfig, AgentConfig
│   │   ├── session.py          # SessionManager, LabSession
│   │   ├── runtime.py          # RuntimeFactory
│   │   └── sandbox.py          # SandboxGuard
│   ├── tools/
│   │   ├── base.py             # BaseLabTool abstract class
│   │   ├── loader.py           # ToolLoader for dynamic imports
│   │   ├── word_count.py       # Example custom tool
│   │   └── sdk_examples.py     # SDK example importer tool
│   ├── ui/
│   │   └── main.py             # Streamlit dashboard
│   └── utils/
│       ├── events.py           # EventFormatter
│       └── watcher.py          # ToolWatcher for hot-reload
├── tests/
│   ├── test_config.py          # Config loading tests
│   ├── test_integration.py     # End-to-end integration tests
│   ├── test_sandbox.py         # Safety guard tests
│   ├── test_sdk_examples.py    # SDK example tool tests
│   ├── test_tools.py           # Tool loading tests
│   └── fixtures/               # Test fixtures for agent validation
│       ├── insecure_app/       # Auditor test app
│       └── js_project/         # Modernizer test project
├── CONTRIBUTING.md             # Contribution guidelines
├── LICENSE                     # MIT License
└── pyproject.toml
```

## Key Components

### Core Module (`lab.core`)
- `ConfigLoader` - Loads YAML configuration files
- `LabConfig` - Global settings model
- `AgentConfig` - Agent definition model (name, prompt, tools)
- `SessionManager` - Manages multiple agent sessions
- `LabSession` - Single agent session wrapper
- `RuntimeFactory` - Creates Local/Docker workspaces
- `SandboxGuard` - Command filtering middleware

### Tools Module (`lab.tools`)
- `BaseLabTool` - Abstract base class for custom tools
- `ToolLoader` - Dynamic tool discovery and loading

### Utils Module (`lab.utils`)
- `EventFormatter` - Formats SDK events for UI display
- `ToolWatcher` - File watcher for hot-reloading

## Available Agents

Defined in `config/agents.yaml`:
- **debug-cli** - Debug and troubleshoot CLI applications
- **code-reviewer** - Review code for quality and security
- **auditor** - Find hardcoded secrets and vulnerabilities
- **modernizer** - Convert JS to TS, add types
- **minimal** - Minimal agent with basic tools
- **sdk-playground** - Run OpenHands SDK examples

## Configuration Priority

Model selection follows this priority order:
1. `LLM_MODEL` environment variable (highest)
2. Per-agent `model` field in agents.yaml
3. `settings.yaml` default model (lowest)

## Creating Custom Tools

```python
from lab.tools.base import BaseLabTool
from openhands.sdk import Action, Observation, TextContent

class MyAction(Action):
    param: str

class MyObservation(Observation):
    result: str
    
    @property
    def to_llm_content(self):
        return [TextContent(text=self.result)]

class MyTool(BaseLabTool[MyAction, MyObservation]):
    tool_name = "my_tool"
    tool_description = "Does something"

    @classmethod
    def create(cls, conv_state, **params):
        return [cls(
            description=cls.tool_description,
            action_type=MyAction,
            observation_type=MyObservation,
            executor=MyExecutor(),
        )]
```

## Configuration Files

### settings.yaml
```yaml
llm:
  model: "anthropic/claude-sonnet-4-5-20250929"
  api_key_env: "LLM_API_KEY"
runtime:
  environment: "local"  # or "docker"
  command_blacklist:
    - "rm -rf /"
session_log_dir: ".oh-lab"
```

### agents.yaml
```yaml
agents:
  my-agent:
    description: "Description"
    system_prompt: "You are..."
    tools:
      - terminal
      - file_editor
    model: null  # Optional per-agent override
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `LLM_API_KEY` | Yes | API key for LLM provider |
| `LLM_MODEL` | No | Override model (e.g., `openhands/claude-sonnet-4-5-20250929`) |
| `LLM_BASE_URL` | No | Custom API endpoint |
| `OPENHANDS_SUPPRESS_BANNER` | No | Set to `1` to hide SDK banner |
