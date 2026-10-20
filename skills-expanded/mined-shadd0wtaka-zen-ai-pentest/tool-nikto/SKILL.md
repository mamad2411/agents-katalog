# nikto

Nikto Integration - Web Vulnerability Scanner

**Category:** scanning — Web Vulnerability Scanning

## Overview

Nikto Integration - Web Vulnerability Scanner
Klassischer Web-Security-Scanner

## Usage in Zen-Ai-Pentest

```python
# Auto-registered in tool_registry under "scanning"
result = await tool_orchestrator.execute("nikto_integration", target="example.com")
```

## CLI Equivalent

```bash
nikto --help
```

## Agent Integration

- CLI: `deep-recon --tool nikto_integration --target example.com`
- Agent persona: auto-selected from category `scanning`
- MCP: `zen-agents_agent_run agent_type=scanning tool=nikto_integration`
- API: `POST /tools/execute` with `{"tool_name": "nikto_integration", "target": "example.com"}`
