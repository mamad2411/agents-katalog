# dnsenum

DNSenum Integration for Zen-AI-Pentest

**Category:** reconnaissance — Subdomain Discovery & DNS Enumeration

## Overview

DNSenum Integration for Zen-AI-Pentest
DNS enumeration and zone transfer testing

## Usage in Zen-Ai-Pentest

```python
from tools.dnsenum_integration import DNSenumScanner


async def main():
    tool = DNSenumScanner()
    result = await tool.__init__("target.com")
    print(result)
```

## CLI Equivalent

```bash
dnsenum --help
```

## Agent Integration

- CLI: `deep-recon --tool dnsenum_integration --target example.com`
- Agent persona: auto-selected from category `reconnaissance`
- MCP: `zen-agents_agent_run agent_type=reconnaissance tool=dnsenum_integration`
- API: `POST /tools/execute` with `{"tool_name": "dnsenum_integration", "target": "example.com"}`
