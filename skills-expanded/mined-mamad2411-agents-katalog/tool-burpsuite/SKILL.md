# burpsuite

BurpSuite Integration

**Category:** scanning — Web Application Testing

## Overview

BurpSuite Integration

## Usage in Zen-Ai-Pentest

```python
from tools.burpsuite_integration import BurpSuiteAPI


async def main():
    tool = BurpSuiteAPI()
    result = await tool.__init__("target.com")
    print(result)
```
```python
from tools.burpsuite_integration import BurpSuiteHeadless


async def main():
    tool = BurpSuiteHeadless()
    result = await tool.__init__("target.com")
    print(result)
```

## CLI Equivalent

```bash
burpsuite --help
```

## Agent Integration

- CLI: `deep-recon --tool burpsuite_integration --target example.com`
- Agent persona: auto-selected from category `scanning`
- MCP: `zen-agents_agent_run agent_type=scanning tool=burpsuite_integration`
- API: `POST /tools/execute` with `{"tool_name": "burpsuite_integration", "target": "example.com"}`
