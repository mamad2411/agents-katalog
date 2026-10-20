# trufflehog

TruffleHog Integration - Secrets Detection for Zen-AI-Pentest

**Category:** scanning — Security Code & Container Scanning

## Overview

TruffleHog Integration - Secrets Detection for Zen-AI-Pentest

This module provides a comprehensive TruffleHog wrapper with:
- Git repository scanning
- File/directory scanning
- Custom regex patterns
- Verified secrets only option
- Multiple output formats
- Result parsing and normalization

Author: Zen-AI-Pentest Team
License: MIT

## Usage in Zen-Ai-Pentest

```python
# Auto-registered in tool_registry under "scanning"
result = await tool_orchestrator.execute("trufflehog_integration", target="example.com")
```

## CLI Equivalent

```bash
trufflehog --help
```

## Agent Integration

- CLI: `deep-recon --tool trufflehog_integration --target example.com`
- Agent persona: auto-selected from category `scanning`
- MCP: `zen-agents_agent_run agent_type=scanning tool=trufflehog_integration`
- API: `POST /tools/execute` with `{"tool_name": "trufflehog_integration", "target": "example.com"}`
