# sherlock

Sherlock Integration - Social Media OSINT

**Category:** reconnaissance — OSINT & Information Gathering

## Overview

Sherlock Integration - Social Media OSINT
Findet Benutzernamen auf über 400 Social Media Plattformen

## Usage in Zen-Ai-Pentest

```python
from tools.sherlock_integration import SherlockIntegration


async def main():
    tool = SherlockIntegration()
    result = await tool.__init__("target.com")
    print(result)
```

## CLI Equivalent

```bash
sherlock --help
```

## Agent Integration

- CLI: `deep-recon --tool sherlock_integration --target example.com`
- Agent persona: auto-selected from category `reconnaissance`
- MCP: `zen-agents_agent_run agent_type=reconnaissance tool=sherlock_integration`
- API: `POST /tools/execute` with `{"tool_name": "sherlock_integration", "target": "example.com"}`
