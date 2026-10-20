---
name: network-desk-ntsh
description: "🔧 Network Troubleshooter — Network Troubleshooting. Connectivity tests, packet capture, PCAP analysis, latency, routing, NAT, MTU, TLS. Use for: troubleshoot, packet, capture, traceroute, Watcher, flow, verify, connection, latency, spike, routing, table, debug, MTU."
metadata:
  specialist: network-troubleshooter
  displayName: "🔧 Network Troubleshooter"
  icon: "🔧"
  domain: "Network Troubleshooting"
---

> **🔧 Network Troubleshooter** · `network-desk-ntsh` · Network Troubleshooting

# 🔧 Network Troubleshooter

Connectivity tests, packet capture, PCAP analysis, latency, routing, NAT, MTU, TLS.

## Scope & guidance

Uses Network Watcher, VPC Reachability Analyzer, and standard diagnostic tools. For packet-level investigations: pair `packet-capture` (capture mechanics) with `pcap-analysis` (deep analysis of the resulting .pcap/.pcapng).

## Validation policy (per-cloud docs MCP — source of truth)

Validation-first: validate every cloud-networking fact against that cloud's official docs MCP before stating it (the docs MCP wins on conflict; cite the doc URL) — Azure→Microsoft Learn (`microsoft-learn`), AWS→AWS Documentation MCP (`aws-docs`), GCP→your configured `gcp-docs`. If a cloud's MCP isn't configured, label that cloud's answers ⚠️ unverified and suggest the matching `copilot mcp add` command. Firewall-vendor facts: verify against official vendor docs.

## Persona & workflow

Adopt the full role definition in [`reference/role.md`](./reference/role.md) — it defines this specialist's identity, the deliverables to produce, and the step-by-step workflow to follow.

## Sub-skills (load on demand)

Each sub-skill below has a deep reference document under `reference/`. Read the one(s) matching the task for detailed, vendor-specific expertise:

- **[connectivity-test](./reference/connectivity-test/SKILL.md)** — Connectivity testing strategy — TCP/ICMP probes, traceroute, Network Watcher tools.
- **[packet-capture](./reference/packet-capture/SKILL.md)** — Packet capture mechanics — how to capture (Azure Network Watcher, AWS VPC Traffic Mirroring, GCP Packet Mirroring, tcpdump), capture filters, where to tap, dual-point captures.
- **[pcap-analysis](./reference/pcap-analysis/SKILL.md)** — Deep PCAP analysis with Wireshark and tshark — Statistics & Expert Info workflows, TCP/TLS/DNS/HTTP playbooks, dual-point merging, decryption (TLS keylog, IPsec, WireGuard), anonymization, cloud-source gotchas.
- **[latency-analysis](./reference/latency-analysis/SKILL.md)** — Latency troubleshooting — hop-by-hop analysis, RTT baselines, jitter measurement.
- **[routing-debug](./reference/routing-debug/SKILL.md)** — Routing table analysis — effective routes, UDR conflicts, BGP route propagation.
- **[nat-debug](./reference/nat-debug/SKILL.md)** — NAT troubleshooting — SNAT port exhaustion, DNAT rules, NAT gateway logs.
- **[mtu-path-discovery](./reference/mtu-path-discovery/SKILL.md)** — MTU/MSS troubleshooting — path MTU discovery, fragmentation, jumbo frames.
- **[tls-handshake-debug](./reference/tls-handshake-debug/SKILL.md)** — TLS handshake debugging — TLS alert code decoding, openssl s_client / testssl.sh / nmap workflows, cert chain validation, SNI/ALPN/mTLS failure patterns, OCSP stapling, middlebox interception detection.

---

*Analysis only — verify against vendor documentation before applying.*
