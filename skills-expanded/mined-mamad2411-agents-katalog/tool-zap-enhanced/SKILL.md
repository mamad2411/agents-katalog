# zap-enhanced

OWASP ZAP Enhanced Integration - Complete Web Application Security Scanner

**Category:** scanning — Web Vulnerability Scanning

## Overview

OWASP ZAP Enhanced Integration - Complete Web Application Security Scanner

This module provides a comprehensive OWASP ZAP integration with:
- ZAP API Client with full authentication support
- Multiple scan policies (Default, API, Full, Quick)
- Complete authentication support (Form, JWT, API Key, Basic Auth, OAuth2)
- Spider, AJAX Spider, Active and Passive scanning
- Context management with scope definition
- Report generation (HTML, XML, JSON, Markdown)
- Alert filtering and risk scoring
- ReAct Agent integration
- Async operations throughout

Author: Zen-AI-Pentest Team
License: MIT
Versio

## Usage in Zen-Ai-Pentest

```python
# Auto-registered in tool_registry under "scanning"
result = await tool_orchestrator.execute("zap_integration_enhanced", target="example.com")
```

## CLI Equivalent

```bash
zap-enhanced --help
```

## Agent Integration

- CLI: `deep-recon --tool zap_integration_enhanced --target example.com`
- Agent persona: auto-selected from category `scanning`
- MCP: `zen-agents_agent_run agent_type=scanning tool=zap_integration_enhanced`
- API: `POST /tools/execute` with `{"tool_name": "zap_integration_enhanced", "target": "example.com"}`
