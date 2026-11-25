# subdomain-enum

Subdomain Enumeration Tool - CLI Interface

**Category:** reconnaissance — Subdomain Discovery & DNS Enumeration

## Overview

Subdomain Enumeration Tool - CLI Interface
Unified interface for basic and advanced subdomain scanning

## Usage in Zen-Ai-Pentest

```python
# Auto-registered in tool_registry under "reconnaissance"
result = await tool_orchestrator.execute("subdomain_enum", target="example.com")
```

## CLI Equivalent

```bash
subdomain-enum --help
```

## Agent Integration

- CLI: `deep-recon --tool subdomain_enum --target example.com`
- Agent persona: auto-selected from category `reconnaissance`
- MCP: `zen-agents_agent_run agent_type=reconnaissance tool=subdomain_enum`
- API: `POST /tools/execute` with `{"tool_name": "subdomain_enum", "target": "example.com"}`
