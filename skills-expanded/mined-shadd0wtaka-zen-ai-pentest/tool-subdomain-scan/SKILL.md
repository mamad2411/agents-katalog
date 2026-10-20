# subdomain-scan

Subdomain Scanner CLI Tool

**Category:** reconnaissance — Subdomain Discovery & DNS Enumeration

## Overview

Subdomain Scanner CLI Tool
Quick subdomain enumeration for target.com

## Usage in Zen-Ai-Pentest

```python
# Auto-registered in tool_registry under "reconnaissance"
result = await tool_orchestrator.execute("subdomain_scan", target="example.com")
```

## CLI Equivalent

```bash
subdomain-scan --help
```

## Agent Integration

- CLI: `deep-recon --tool subdomain_scan --target example.com`
- Agent persona: auto-selected from category `reconnaissance`
- MCP: `zen-agents_agent_run agent_type=reconnaissance tool=subdomain_scan`
- API: `POST /tools/execute` with `{"tool_name": "subdomain_scan", "target": "example.com"}`
