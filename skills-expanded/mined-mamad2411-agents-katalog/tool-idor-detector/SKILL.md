# idor-detector

IDOR Detector - Insecure Direct Object Reference Detection

**Category:** scanning — Web Application Testing

## Overview

IDOR Detector - Insecure Direct Object Reference Detection
Phase 8.3: Business-Logic Testing - IDOR Detection

Dieses Modul implementiert IDOR-Vulnerability-Detection durch
Testen von sequentiellen IDs und verschiedenen Benutzer-Sessions.

## Usage in Zen-Ai-Pentest

```python
# Auto-registered in tool_registry under "scanning"
result = await tool_orchestrator.execute("idor_detector", target="example.com")
```

## CLI Equivalent

```bash
idor-detector --help
```

## Agent Integration

- CLI: `deep-recon --tool idor_detector --target example.com`
- Agent persona: auto-selected from category `scanning`
- MCP: `zen-agents_agent_run agent_type=scanning tool=idor_detector`
- API: `POST /tools/execute` with `{"tool_name": "idor_detector", "target": "example.com"}`
