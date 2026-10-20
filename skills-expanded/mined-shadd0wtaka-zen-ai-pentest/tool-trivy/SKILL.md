# trivy

Trivy Integration - Container and Filesystem Vulnerability Scanner for Zen-AI-Pentest

**Category:** scanning — Security Code & Container Scanning

## Overview

Trivy Integration - Container and Filesystem Vulnerability Scanner for Zen-AI-Pentest

This module provides a comprehensive Trivy wrapper with:
- Container image scanning
- Filesystem scanning
- SBOM generation
- CVE detection
- Misconfiguration detection
- JSON output parsing
- Severity filtering
- Cache integration

Author: Zen-AI-Pentest Team
License: MIT

## Usage in Zen-Ai-Pentest

```python
# Auto-registered in tool_registry under "scanning"
result = await tool_orchestrator.execute("trivy_integration", target="example.com")
```

## CLI Equivalent

```bash
trivy --help
```

## Agent Integration

- CLI: `deep-recon --tool trivy_integration --target example.com`
- Agent persona: auto-selected from category `scanning`
- MCP: `zen-agents_agent_run agent_type=scanning tool=trivy_integration`
- API: `POST /tools/execute` with `{"tool_name": "trivy_integration", "target": "example.com"}`
