# gobuster

Gobuster Integration for Zen-AI-Pentest

**Category:** scanning — Directory & Content Discovery

## Overview

Gobuster Integration for Zen-AI-Pentest
Directory and file brute-forcing

## Usage in Zen-Ai-Pentest

```python
from tools.gobuster_integration import GobusterScanner


async def main():
    tool = GobusterScanner()
    result = await tool.__init__("target.com")
    print(result)
```

## CLI Equivalent

```bash
gobuster --help
```

## Agent Integration

- CLI: `deep-recon --tool gobuster_integration --target example.com`
- Agent persona: auto-selected from category `scanning`
- MCP: `zen-agents_agent_run agent_type=scanning tool=gobuster_integration`
- API: `POST /tools/execute` with `{"tool_name": "gobuster_integration", "target": "example.com"}`
