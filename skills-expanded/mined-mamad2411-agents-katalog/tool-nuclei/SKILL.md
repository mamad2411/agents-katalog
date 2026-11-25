# nuclei

Nuclei Integration - Stub for testing

**Category:** scanning — Web Vulnerability Scanning

## Overview

Nuclei Integration - Stub for testing
Full implementation needed for production

## Usage in Zen-Ai-Pentest

```python
from tools.nuclei_integration import NucleiTool


async def main():
    tool = NucleiTool()
    result = await tool.__init__("target.com")
    print(result)
```
```python
from tools.nuclei_integration import NucleiScanner


async def main():
    tool = NucleiScanner()
    result = await tool.__init__("target.com")
    print(result)
```

## CLI Equivalent

```bash
nuclei --help
```

## Agent Integration

- CLI: `deep-recon --tool nuclei_integration --target example.com`
- Agent persona: auto-selected from category `scanning`
- MCP: `zen-agents_agent_run agent_type=scanning tool=nuclei_integration`
- API: `POST /tools/execute` with `{"tool_name": "nuclei_integration", "target": "example.com"}`
