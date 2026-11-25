# whatweb

WhatWeb Integration - Web Technology Detection

**Category:** scanning — Web Vulnerability Scanning

## Overview

WhatWeb Integration - Web Technology Detection
Erkennt CMS, Frameworks, Server-Software, etc.

## Usage in Zen-Ai-Pentest

```python
# Auto-registered in tool_registry under "scanning"
result = await tool_orchestrator.execute("whatweb_integration", target="example.com")
```

## CLI Equivalent

```bash
whatweb --help
```

## Agent Integration

- CLI: `deep-recon --tool whatweb_integration --target example.com`
- Agent persona: auto-selected from category `scanning`
- MCP: `zen-agents_agent_run agent_type=scanning tool=whatweb_integration`
- API: `POST /tools/execute` with `{"tool_name": "whatweb_integration", "target": "example.com"}`
