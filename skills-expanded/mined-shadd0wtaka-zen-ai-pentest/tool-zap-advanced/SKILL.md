# zap-advanced

OWASP ZAP Advanced Integration - Enterprise Web Application Security Scanner

**Category:** scanning — Web Vulnerability Scanning

## Overview

OWASP ZAP Advanced Integration - Enterprise Web Application Security Scanner

This module provides a comprehensive OWASP ZAP integration with:
- Full ZAP API Client with authentication
- Multiple scan types (Spider, Active, Passive, AJAX Spider, OpenAPI)
- Context and scope management
- Technology detection
- Policy management (Low/Medium/High/Insane)
- Authentication handling (Form-based, Script-based)
- Advanced reporting (JSON, HTML, risk-based filtering)
- False positive management
- ReActAgent integration

Author: Zen-AI-Pentest Team
License: MIT
Version: 2.0.0

## Usage in Zen-Ai-Pentest

```python
# Auto-registered in tool_registry under "scanning"
result = await tool_orchestrator.execute("zap_integration_advanced", target="example.com")
```

## CLI Equivalent

```bash
zap-advanced --help
```

## Agent Integration

- CLI: `deep-recon --tool zap_integration_advanced --target example.com`
- Agent persona: auto-selected from category `scanning`
- MCP: `zen-agents_agent_run agent_type=scanning tool=zap_integration_advanced`
- API: `POST /tools/execute` with `{"tool_name": "zap_integration_advanced", "target": "example.com"}`
