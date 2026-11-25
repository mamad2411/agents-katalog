# ffuf-enhanced

FFuF Integration - Fast Web Fuzzer

**Category:** scanning — Directory & Content Discovery

## Overview

FFuF Integration - Fast Web Fuzzer
Erweiterte Integration für Zen-AI-Pentest

Supports:
- Directory bruteforcing
- Parameter fuzzing
- Virtual host discovery
- POST data fuzzing
- Filter & Matcher rules

## Usage in Zen-Ai-Pentest

```python
# Auto-registered in tool_registry under "scanning"
result = await tool_orchestrator.execute("ffuf_integration_enhanced", target="example.com")
```

## CLI Equivalent

```bash
ffuf-enhanced --help
```

## Agent Integration

- CLI: `deep-recon --tool ffuf_integration_enhanced --target example.com`
- Agent persona: auto-selected from category `scanning`
- MCP: `zen-agents_agent_run agent_type=scanning tool=ffuf_integration_enhanced`
- API: `POST /tools/execute` with `{"tool_name": "ffuf_integration_enhanced", "target": "example.com"}`
