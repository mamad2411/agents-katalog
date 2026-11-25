---
name: wireshark-mcp
description: >-
  Use the wireshark MCP server for authorized packet capture and analysis with
  TShark. Apply when investigating live traffic, reading pcap/pcapng files,
  debugging DNS/HTTP/TLS, or working on the wireshark-mcp codebase itself.
---

# Wireshark MCP

Works with any stdio MCP host (Cursor, Claude, VS Code, custom agents).

## When to use

- Live or offline packet analysis via the `wireshark` MCP server
- Choosing the right tool (`quick_capture`, DNS/HTTP analysis, expert info, etc.)
- Editing this repository’s MCP tools/prompts

## Hard rules

1. Call `list_interfaces` first; pass an **exact** returned interface name.
2. Prefer short captures (`duration` 3–10s, modest `packet_limit`).
3. **Never invent traffic.** If a tool returns `Error: ...`, report that failure.
4. Only capture traffic you are authorized to inspect.
5. Treat pcaps and verbose dumps as sensitive; redact secrets before sharing.

## Setup / online status

Hosts show the MCP online only after the process starts. This server **exits if TShark is missing**. If offline:

1. `python -m wireshark_mcp doctor`
2. `python -m wireshark_mcp setup` (prompts for TShark path; writes/prints `mcpServers` JSON)
3. Reload/restart MCP in the host

In-session: `check_environment`, `configure_tshark`. See `docs/Setup.md`.

## Tool cheat-sheet

| Goal | Tool |
|------|------|
| Deps / path | `check_environment`, `configure_tshark` |
| List NICs | `list_interfaces` |
| Quick sample | `quick_capture` |
| Quick insights | `quick_traffic_analysis` |
| Deep tabular | `deep_packet_analysis` |
| Protocol tree | `protocol_hierarchy_statistics` |
| DNS | `analyze_dns_traffic` |
| HTTP/TLS tables | `analyze_http_traffic_tabular` |
| Offline summary | `read_pcap_file` |
| HTTP from file | `analyze_http_traffic` |
| Display filter | `filtered_packet_display` |
| Expert warnings | `expert_information` |
| Save pcap | `save_capture_to_file` |

## MCP prompts

- `investigate_live_traffic`
- `analyze_pcap_file`
- `security_traffic_review`
- `safe_capture_rules`
- `packet_capture_help`

## Local run

```text
python -m wireshark_mcp setup
python -m wireshark_mcp
```

Requires TShark (`PATH` or `TSHARK_PATH`) and Npcap (Windows) / libpcap (Unix) for live capture.
