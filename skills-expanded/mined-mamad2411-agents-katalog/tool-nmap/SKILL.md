# nmap

Nmap Integration - Advanced Network Scanner for Zen-AI-Pentest

**Category:** scanning — Port & Service Scanning

## Overview

Nmap Integration - Advanced Network Scanner for Zen-AI-Pentest

This module provides a comprehensive Nmap wrapper with:
- Async/await support
- XML output parsing
- Service detection
- OS detection
- NSE script scanning
- Proper error handling and input validation
- Integration with tool_registry and tool_orchestrator

Author: Zen-AI-Pentest Team
License: MIT

## Usage in Zen-Ai-Pentest

```python
# Auto-registered in tool_registry under "scanning"
result = await tool_orchestrator.execute("nmap_integration", target="example.com")
```

## CLI Equivalent

```bash
nmap --help
```

## Agent Integration

- CLI: `deep-recon --tool nmap_integration --target example.com`
- Agent persona: auto-selected from category `scanning`
- MCP: `zen-agents_agent_run agent_type=scanning tool=nmap_integration`
- API: `POST /tools/execute` with `{"tool_name": "nmap_integration", "target": "example.com"}`
