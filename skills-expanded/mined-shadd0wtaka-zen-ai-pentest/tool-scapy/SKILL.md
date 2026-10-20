# scapy

Scapy Integration für Zen-AI-Pentest

**Category:** network — Network & Wireless Analysis

## Overview

Scapy Integration für Zen-AI-Pentest

## Usage in Zen-Ai-Pentest

```python
from tools.scapy_integration import ScapyScanner


async def main():
    tool = ScapyScanner()
    result = await tool.__init__("target.com")
    print(result)
```

## CLI Equivalent

```bash
scapy --help
```

## Agent Integration

- CLI: `deep-recon --tool scapy_integration --target example.com`
- Agent persona: auto-selected from category `network`
- MCP: `zen-agents_agent_run agent_type=network tool=scapy_integration`
- API: `POST /tools/execute` with `{"tool_name": "scapy_integration", "target": "example.com"}`
