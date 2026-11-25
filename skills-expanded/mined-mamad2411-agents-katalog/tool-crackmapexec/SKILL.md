# crackmapexec

CrackMapExec Integration - SMB/WinRM/LDAP/MSSQL Swiss Army Knife

**Category:** exploitation — Exploitation & Credential Attacks

## Overview

CrackMapExec Integration - SMB/WinRM/LDAP/MSSQL Swiss Army Knife

## Usage in Zen-Ai-Pentest

```python
from tools.crackmapexec_integration import CrackMapExec


async def main():
    tool = CrackMapExec()
    result = await tool.__init__("target.com")
    print(result)
```

## CLI Equivalent

```bash
crackmapexec --help
```

## Agent Integration

- CLI: `deep-recon --tool crackmapexec_integration --target example.com`
- Agent persona: auto-selected from category `exploitation`
- MCP: `zen-agents_agent_run agent_type=exploitation tool=crackmapexec_integration`
- API: `POST /tools/execute` with `{"tool_name": "crackmapexec_integration", "target": "example.com"}`
