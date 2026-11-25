# ignorant

Ignorant Integration - Email OSINT

**Category:** reconnaissance — OSINT & Information Gathering

## Overview

Ignorant Integration - Email OSINT
Überprüft Email-Adressen auf 120+ Plattformen

## Usage in Zen-Ai-Pentest

```python
# Auto-registered in tool_registry under "reconnaissance"
result = await tool_orchestrator.execute("ignorant_integration", target="example.com")
```

## CLI Equivalent

```bash
ignorant --help
```

## Agent Integration

- CLI: `deep-recon --tool ignorant_integration --target example.com`
- Agent persona: auto-selected from category `reconnaissance`
- MCP: `zen-agents_agent_run agent_type=reconnaissance tool=ignorant_integration`
- API: `POST /tools/execute` with `{"tool_name": "ignorant_integration", "target": "example.com"}`
