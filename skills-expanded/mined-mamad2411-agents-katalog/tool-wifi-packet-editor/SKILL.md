# wifi-packet-editor

WiFi Packet Editor für Zen-AI-Pentest

**Category:** network — Network & Wireless Analysis

## Overview

WiFi Packet Editor für Zen-AI-Pentest
======================================

802.11 WiFi Frame Analyse und Modifikation.

⚠️  WICHTIGE SICHERHEITSHINWEISE:
    - NUR in eigenen Netzwerken oder mit EXPLIZITER schriftlicher Genehmigung verwenden
    - Das Abhören/Manipulieren fremder Netzwerke ist ILLEGAL (§ 202a StGB, CFAA, etc.)
    - Benutzer ist ALLEINIG VERANTWORTLICH für ihre Handlungen

Unterstützte Funktionen:
    - 802.11 Frame Parsing (Beacon, Probe, Data, Management)
    - MAC-Adress-Spoofing
    - Frame Injection (mit kompatiblem Adapter)
    - Deauthentication Frame-Erkennung
    -

## Usage in Zen-Ai-Pentest

```python
# Auto-registered in tool_registry under "network"
result = await tool_orchestrator.execute("wifi_packet_editor", target="example.com")
```

## CLI Equivalent

```bash
wifi-packet-editor --help
```

## Agent Integration

- CLI: `deep-recon --tool wifi_packet_editor --target example.com`
- Agent persona: auto-selected from category `network`
- MCP: `zen-agents_agent_run agent_type=network tool=wifi_packet_editor`
- API: `POST /tools/execute` with `{"tool_name": "wifi_packet_editor", "target": "example.com"}`
