# aircrack

Aircrack-ng Integration - Wireless Security Testing

**Category:** network — Network & Wireless Analysis

## Overview

Aircrack-ng Integration - Wireless Security Testing

## Usage in Zen-Ai-Pentest

```python
from tools.aircrack_integration import AircrackSuite


async def main():
    tool = AircrackSuite()
    result = await tool.__init__("target.com")
    print(result)
```
```python
from tools.aircrack_integration import _FunctionTool


async def main():
    tool = _FunctionTool()
    result = await tool.__init__("target.com")
    print(result)
```

## CLI Equivalent

```bash
aircrack --help
```

## Agent Integration

- CLI: `deep-recon --tool aircrack_integration --target example.com`
- Agent persona: auto-selected from category `network`
- MCP: `zen-agents_agent_run agent_type=network tool=aircrack_integration`
- API: `POST /tools/execute` with `{"tool_name": "aircrack_integration", "target": "example.com"}`
