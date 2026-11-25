# amass

Amass Integration - Advanced Subdomain Enumeration

**Category:** reconnaissance — Subdomain Discovery & DNS Enumeration

## Overview

Amass Integration - Advanced Subdomain Enumeration
Die umfassendste Subdomain-Enumeration

## Usage in Zen-Ai-Pentest

```python
from tools.amass_integration import AmassIntegration


async def main():
    tool = AmassIntegration()
    result = await tool.__init__("target.com")
    print(result)
```

## CLI Equivalent

```bash
amass --help
```

## Agent Integration

- CLI: `deep-recon --tool amass_integration --target example.com`
- Agent persona: auto-selected from category `reconnaissance`
- MCP: `zen-agents_agent_run agent_type=reconnaissance tool=amass_integration`
- API: `POST /tools/execute` with `{"tool_name": "amass_integration", "target": "example.com"}`
