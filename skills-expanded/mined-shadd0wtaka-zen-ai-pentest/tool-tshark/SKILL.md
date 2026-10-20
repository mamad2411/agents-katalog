# tshark

TShark Integration - Network Traffic Analysis

**Category:** network — Network & Wireless Analysis

## Overview

TShark Integration - Network Traffic Analysis
Wireshark CLI für automatisierte Netzwerk-Analyse

## Usage in Zen-Ai-Pentest

```python
# Auto-registered in tool_registry under "network"
result = await tool_orchestrator.execute("tshark_integration", target="example.com")
```

## CLI Equivalent

```bash
tshark --help
```

## Agent Integration

- CLI: `deep-recon --tool tshark_integration --target example.com`
- Agent persona: auto-selected from category `network`
- MCP: `zen-agents_agent_run agent_type=network tool=tshark_integration`
- API: `POST /tools/execute` with `{"tool_name": "tshark_integration", "target": "example.com"}`
