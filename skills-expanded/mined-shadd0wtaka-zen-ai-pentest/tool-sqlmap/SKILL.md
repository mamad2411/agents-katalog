# sqlmap

SQLMap Integration für automatisierte SQL Injection Tests

**Category:** scanning — Web Vulnerability Scanning

## Overview

SQLMap Integration für automatisierte SQL Injection Tests

## Usage in Zen-Ai-Pentest

```python
from tools.sqlmap_integration import SQLMapScanner


async def main():
    tool = SQLMapScanner()
    result = await tool.__init__("target.com")
    print(result)
```
```python
from tools.sqlmap_integration import _FunctionTool


async def main():
    tool = _FunctionTool()
    result = await tool.__init__("target.com")
    print(result)
```

## CLI Equivalent

```bash
sqlmap --help
```

## Agent Integration

- CLI: `deep-recon --tool sqlmap_integration --target example.com`
- Agent persona: auto-selected from category `scanning`
- MCP: `zen-agents_agent_run agent_type=scanning tool=sqlmap_integration`
- API: `POST /tools/execute` with `{"tool_name": "sqlmap_integration", "target": "example.com"}`
