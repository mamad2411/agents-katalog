# gobuster-robust-parser

Robuster Gobuster Parser mit Deduplizierung und Soft-404-Erkennung

**Category:** scanning — Directory & Content Discovery

## Overview

Robuster Gobuster Parser mit Deduplizierung und Soft-404-Erkennung
Zukünftige Version - wird aktiviert sobald Smart-Test Rot zeigt

## Usage in Zen-Ai-Pentest

```python
from tools.gobuster_robust_parser import RobustGobusterScanner


async def main():
    tool = RobustGobusterScanner()
    result = await tool.__init__("target.com")
    print(result)
```

## CLI Equivalent

```bash
gobuster-robust-parser --help
```

## Agent Integration

- CLI: `deep-recon --tool gobuster_robust_parser --target example.com`
- Agent persona: auto-selected from category `scanning`
- MCP: `zen-agents_agent_run agent_type=scanning tool=gobuster_robust_parser`
- API: `POST /tools/execute` with `{"tool_name": "gobuster_robust_parser", "target": "example.com"}`
