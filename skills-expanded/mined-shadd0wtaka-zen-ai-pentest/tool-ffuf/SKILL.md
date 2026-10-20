# ffuf

FFUF Integration - Stub for testing

**Category:** scanning — Directory & Content Discovery

## Overview

FFUF Integration - Stub for testing
Full implementation needed for production

## Usage in Zen-Ai-Pentest

```python
from tools.ffuf_integration import FfufTool


async def main():
    tool = FfufTool()
    result = await tool.__init__("target.com")
    print(result)
```
```python
from tools.ffuf_integration import FfufFuzzer


async def main():
    tool = FfufFuzzer()
    result = await tool.__init__("target.com")
    print(result)
```

## CLI Equivalent

```bash
ffuf --help
```

## Agent Integration

- CLI: `deep-recon --tool ffuf_integration --target example.com`
- Agent persona: auto-selected from category `scanning`
- MCP: `zen-agents_agent_run agent_type=scanning tool=ffuf_integration`
- API: `POST /tools/execute` with `{"tool_name": "ffuf_integration", "target": "example.com"}`
