# wafw00f

WAFW00F Integration - Web Application Firewall Detection

**Category:** scanning — Web Vulnerability Scanning

## Overview

WAFW00F Integration - Web Application Firewall Detection
Erkennt WAFs (Cloudflare, AWS WAF, ModSecurity, etc.)

## Usage in Zen-Ai-Pentest

```python
# Auto-registered in tool_registry under "scanning"
result = await tool_orchestrator.execute("wafw00f_integration", target="example.com")
```

## CLI Equivalent

```bash
wafw00f --help
```

## Agent Integration

- CLI: `deep-recon --tool wafw00f_integration --target example.com`
- Agent persona: auto-selected from category `scanning`
- MCP: `zen-agents_agent_run agent_type=scanning tool=wafw00f_integration`
- API: `POST /tools/execute` with `{"tool_name": "wafw00f_integration", "target": "example.com"}`
