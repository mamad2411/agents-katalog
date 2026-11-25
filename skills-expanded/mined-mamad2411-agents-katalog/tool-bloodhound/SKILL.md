# bloodhound

BloodHound Integration - Active Directory Analysis

**Category:** reconnaissance — Active Directory Enumeration

## Overview

BloodHound Integration - Active Directory Analysis

## Usage in Zen-Ai-Pentest

```python
from tools.bloodhound_integration import BloodHoundAnalyzer


async def main():
    tool = BloodHoundAnalyzer()
    result = await tool.__init__("target.com")
    print(result)
```

## CLI Equivalent

```bash
bloodhound --help
```

## Agent Integration

- CLI: `deep-recon --tool bloodhound_integration --target example.com`
- Agent persona: auto-selected from category `reconnaissance`
- MCP: `zen-agents_agent_run agent_type=reconnaissance tool=bloodhound_integration`
- API: `POST /tools/execute` with `{"tool_name": "bloodhound_integration", "target": "example.com"}`
