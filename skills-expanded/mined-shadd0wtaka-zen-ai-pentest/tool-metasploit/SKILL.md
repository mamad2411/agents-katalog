# metasploit

Metasploit Framework Integration

**Category:** exploitation — Exploitation & Credential Attacks

## Overview

Metasploit Framework Integration

## Usage in Zen-Ai-Pentest

```python
from tools.metasploit_integration import MetasploitManager


async def main():
    tool = MetasploitManager()
    result = await tool.__init__("target.com")
    print(result)
```
```python
from tools.metasploit_integration import MetasploitCLI


async def main():
    tool = MetasploitCLI()
    result = await tool.run_command("target.com")
    print(result)
```

## CLI Equivalent

```bash
metasploit --help
```

## Agent Integration

- CLI: `deep-recon --tool metasploit_integration --target example.com`
- Agent persona: auto-selected from category `exploitation`
- MCP: `zen-agents_agent_run agent_type=exploitation tool=metasploit_integration`
- API: `POST /tools/execute` with `{"tool_name": "metasploit_integration", "target": "example.com"}`
