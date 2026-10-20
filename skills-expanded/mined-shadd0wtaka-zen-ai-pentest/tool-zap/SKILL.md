# zap

OWASP ZAP Integration - Web Application Security Scanner for Zen-AI-Pentest

**Category:** scanning — Web Vulnerability Scanning

## Overview

OWASP ZAP Integration - Web Application Security Scanner for Zen-AI-Pentest

This module provides a comprehensive OWASP ZAP wrapper with:
- REST API Wrapper für ZAP
- Authentifizierte Scans (Form, JWT, OAuth2, API Key, Session Cookie)
- Context Management
- Session Handling
- Spider/Crawling (Standard & AJAX)
- Active Scan (Vulnerability Detection)
- OpenAPI Scan (API Endpoints)
- GraphQL Scan
- Alert Management (High/Medium/Low/Informational)
- CWE/WASC Mapping
- Evidence Collection
- Report Generation (HTML, JSON, SARIF)
- Docker Support (Headless Mode)
- Automation Framework Integration

Au

## Usage in Zen-Ai-Pentest

```python
# Auto-registered in tool_registry under "scanning"
result = await tool_orchestrator.execute("zap_integration", target="example.com")
```

## CLI Equivalent

```bash
zap --help
```

## Agent Integration

- CLI: `deep-recon --tool zap_integration --target example.com`
- Agent persona: auto-selected from category `scanning`
- MCP: `zen-agents_agent_run agent_type=scanning tool=zap_integration`
- API: `POST /tools/execute` with `{"tool_name": "zap_integration", "target": "example.com"}`
