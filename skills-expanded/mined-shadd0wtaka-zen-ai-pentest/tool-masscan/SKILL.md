# masscan

Masscan Integration - High-Speed Port Scanner

**Category:** scanning — Port & Service Scanning

## Overview

Masscan Integration - High-Speed Port Scanner
Schneller als Nmap für große Netzwerke

## Usage in Zen-Ai-Pentest

```python
# Auto-registered in tool_registry under "scanning"
result = await tool_orchestrator.execute("masscan_integration", target="example.com")
```

## CLI Equivalent

```bash
masscan --help
```

## Agent Integration

- CLI: `deep-recon --tool masscan_integration --target example.com`
- Agent persona: auto-selected from category `scanning`
- MCP: `zen-agents_agent_run agent_type=scanning tool=masscan_integration`
- API: `POST /tools/execute` with `{"tool_name": "masscan_integration", "target": "example.com"}`
