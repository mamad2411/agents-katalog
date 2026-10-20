# scout

ScoutSuite Integration - Cloud Security Posture Assessment for Zen-AI-Pentest

**Category:** reconnaissance — OSINT & Information Gathering

## Overview

ScoutSuite Integration - Cloud Security Posture Assessment for Zen-AI-Pentest

This module provides a comprehensive ScoutSuite wrapper with:
- AWS, Azure, GCP support
- Compliance checking
- Security rule evaluation
- Report parsing
- Finding normalization
- Risk scoring integration

Author: Zen-AI-Pentest Team
License: MIT

## Usage in Zen-Ai-Pentest

```python
# Auto-registered in tool_registry under "reconnaissance"
result = await tool_orchestrator.execute("scout_integration", target="example.com")
```

## CLI Equivalent

```bash
scout --help
```

## Agent Integration

- CLI: `deep-recon --tool scout_integration --target example.com`
- Agent persona: auto-selected from category `reconnaissance`
- MCP: `zen-agents_agent_run agent_type=reconnaissance tool=scout_integration`
- API: `POST /tools/execute` with `{"tool_name": "scout_integration", "target": "example.com"}`
