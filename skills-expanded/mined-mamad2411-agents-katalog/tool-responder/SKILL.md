# responder

Responder Integration - LLMNR/NBT-NS/mDNS Poisoning

**Category:** reconnaissance — Active Directory Enumeration

## Overview

Responder Integration - LLMNR/NBT-NS/mDNS Poisoning

## Usage in Zen-Ai-Pentest

```python
from tools.responder_integration import ResponderPoisoner


async def main():
    tool = ResponderPoisoner()
    result = await tool.__init__("target.com")
    print(result)
```

## CLI Equivalent

```bash
responder --help
```

## Agent Integration

- CLI: `deep-recon --tool responder_integration --target example.com`
- Agent persona: auto-selected from category `reconnaissance`
- MCP: `zen-agents_agent_run agent_type=reconnaissance tool=responder_integration`
- API: `POST /tools/execute` with `{"tool_name": "responder_integration", "target": "example.com"}`
