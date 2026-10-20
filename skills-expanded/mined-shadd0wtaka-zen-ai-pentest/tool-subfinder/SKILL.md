# subfinder

Subfinder Integration - Subdomain Discovery

**Category:** reconnaissance — Subdomain Discovery & DNS Enumeration

## Overview

Subfinder Integration - Subdomain Discovery
Schnelle Subdomain-Enumeration mit Subfinder

## Usage in Zen-Ai-Pentest

```python
from tools.subfinder_integration import SubfinderIntegration


async def main():
    tool = SubfinderIntegration()
    result = await tool.__init__("target.com")
    print(result)
```

## CLI Equivalent

```bash
subfinder --help
```

## Agent Integration

- CLI: `deep-recon --tool subfinder_integration --target example.com`
- Agent persona: auto-selected from category `reconnaissance`
- MCP: `zen-agents_agent_run agent_type=reconnaissance tool=subfinder_integration`
- API: `POST /tools/execute` with `{"tool_name": "subfinder_integration", "target": "example.com"}`
