# hydra

Hydra Integration - Online Password Brute-Force

**Category:** exploitation — Exploitation & Credential Attacks

## Overview

Hydra Integration - Online Password Brute-Force

## Usage in Zen-Ai-Pentest

```python
from tools.hydra_integration import HydraBruteForcer


async def main():
    tool = HydraBruteForcer()
    result = await tool.__init__("target.com")
    print(result)
```

## CLI Equivalent

```bash
hydra --help
```

## Agent Integration

- CLI: `deep-recon --tool hydra_integration --target example.com`
- Agent persona: auto-selected from category `exploitation`
- MCP: `zen-agents_agent_run agent_type=exploitation tool=hydra_integration`
- API: `POST /tools/execute` with `{"tool_name": "hydra_integration", "target": "example.com"}`
