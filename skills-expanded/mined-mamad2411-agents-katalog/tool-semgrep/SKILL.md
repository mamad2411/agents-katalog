# semgrep

Semgrep Integration - Static Analysis for Code Security for Zen-AI-Pentest

**Category:** scanning — Security Code & Container Scanning

## Overview

Semgrep Integration - Static Analysis for Code Security for Zen-AI-Pentest

This module provides a comprehensive Semgrep wrapper with:
- Custom rule support
- OWASP/CWE coverage
- Multiple language support
- CI/CD integration
- Rule configuration
- JSON output parsing
- Finding categorization
- False positive handling

Author: Zen-AI-Pentest Team
License: MIT

## Usage in Zen-Ai-Pentest

```python
# Auto-registered in tool_registry under "scanning"
result = await tool_orchestrator.execute("semgrep_integration", target="example.com")
```

## CLI Equivalent

```bash
semgrep --help
```

## Agent Integration

- CLI: `deep-recon --tool semgrep_integration --target example.com`
- Agent persona: auto-selected from category `scanning`
- MCP: `zen-agents_agent_run agent_type=scanning tool=semgrep_integration`
- API: `POST /tools/execute` with `{"tool_name": "semgrep_integration", "target": "example.com"}`
