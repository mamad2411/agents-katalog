# httpx

HTTPX Integration - Fast HTTP Prober

**Category:** scanning — Web Vulnerability Scanning

## Overview

HTTPX Integration - Fast HTTP Prober
Schneller HTTP/HTTPS Prober für Subdomains und URLs

## Usage in Zen-Ai-Pentest

```python
# Auto-registered in tool_registry under "scanning"
result = await tool_orchestrator.execute("httpx_integration", target="example.com")
```

## CLI Equivalent

```bash
httpx --help
```

## Agent Integration

- CLI: `deep-recon --tool httpx_integration --target example.com`
- Agent persona: auto-selected from category `scanning`
- MCP: `zen-agents_agent_run agent_type=scanning tool=httpx_integration`
- API: `POST /tools/execute` with `{"tool_name": "httpx_integration", "target": "example.com"}`
