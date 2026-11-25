# unified-recon

Unified Reconnaissance Scanner

**Category:** reconnaissance — Automated Reconnaissance

## Overview

Unified Reconnaissance Scanner
Kombiniert alle Tools für eine vollständige Enumeration

Usage:
    python unified_recon.py --target example.com
    python unified_recon.py --target example.com --full

## Usage in Zen-Ai-Pentest

```python
from tools.unified_recon import UnifiedReconScanner


async def main():
    tool = UnifiedReconScanner()
    result = await tool.__init__("target.com")
    print(result)
```

## CLI Equivalent

```bash
unified-recon --help
```

## Agent Integration

- CLI: `deep-recon --tool unified_recon --target example.com`
- Agent persona: auto-selected from category `reconnaissance`
- MCP: `zen-agents_agent_run agent_type=reconnaissance tool=unified_recon`
- API: `POST /tools/execute` with `{"tool_name": "unified_recon", "target": "example.com"}`
