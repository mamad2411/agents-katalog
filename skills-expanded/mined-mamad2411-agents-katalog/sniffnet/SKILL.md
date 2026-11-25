---
name: sniffnet
description: "Inspect network traffic with Sniffnet, configure packet filters and bandwidth alerts, and troubleshoot capture drivers."
category: cross-platform
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["sniffnet", "pcap", "npcap", "network-monitoring", "packet-capture", "rust", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Sniffnet Network Traffic Monitor AI Skill Guide (Claude)

## Overview & Engine Architecture
Sniffnet is a multi-platform, open-source network traffic analyzer written in **Rust**, powered by the `pcap` / `npcap` packet capture driver and the `iced` GUI framework. Claude operates as a Senior Network Security Analyst and Systems Engineer, specializing in **zero-copy packet sniffing**, **Berkeley Packet Filter (BPF) syntax**, **IP ASN and Geolocation lookup mechanics**, and **network interface permission auditing (`CAP_NET_RAW`)**.

### Sniffnet Capture Architecture & Rust Stack

```
┌─────────────────────────────────────────────────────────────┐
│                 Sniffnet Engine Architecture                │
│                                                             │
│  Kernel Packet Ingestion Layer                              │
│  ├── Npcap Driver (Windows) / libpcap (Linux & macOS)       │
│  ├── Promiscuous & Monitor Mode Network Adapter Hook        │
│  └── Kernel-Level Berkeley Packet Filter (BPF) Virtual Mach.│
│                                                             │
│  Rust Processing & Analytics Layer                          │
│  ├── `pnet` & `etherparse` Zero-Copy Protocol Parsing       │
│  ├── MaxMind GeoLite2 ASN / Geolocation Enrichment Engine   │
│  └── Ring Buffer Aggregator & Iced Reactive UI Graphs       │
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **Packet Capture Driver Remediation**: Diagnose missing adapter enumeration and packet capture failures across Windows (Npcap driver installation with WinPcap API compatibility) and Linux (`setcap cap_net_raw,cap_net_admin=eip`).
2. **BPF Filter Rule Formulation**: Construct high-performance capture filters (`tcp and port 443 and not src host 192.168.1.1`) to isolate target network conversations without overwhelming CPU buffers.
3. **Bandwidth Alert Thresholding**: Configure custom byte and packet rate thresholds to detect port scanning, DDoS volumetric spikes, and unauthorized external data exfiltration.
4. **Network Protocol Auditing**: Identify unencrypted legacy protocol leaks (HTTP, Telnet, FTP, DNS over plaintext) and inspect TLS SNI headers.

---

## Production Python Automation: Automated BPF Packet Sniffer & Flow Inspector

Save this script as `packet_flow_inspector.py` (requires `pip install scapy`) to verify network interface capture rules and analyze packet bandwidth distributions programmatically:

```python
"""
Network Traffic & BPF Filter Verification Tool
Captures and classifies packets across local adapters using Scapy/pcap.
"""

import sys
import time
from collections import defaultdict
from scapy.all import sniff, IP, TCP, UDP

traffic_by_protocol = defaultdict(int)
traffic_by_ip = defaultdict(int)
total_bytes = 0

def packet_callback(packet):
    global total_bytes
    if IP in packet:
        src = packet[IP].src
        dst = packet[IP].dst
        proto = "TCP" if TCP in packet else "UDP" if UDP in packet else "OTHER"
        pkt_len = len(packet)
        
        total_bytes += pkt_len
        traffic_by_protocol[proto] += pkt_len
        traffic_by_ip[f"{src} -> {dst}"] += pkt_len

def start_capture(interface: str = None, bpf_filter: str = "", duration_sec: int = 10):
    print(f"Starting Packet Capture [Duration: {duration_sec}s | Filter: '{bpf_filter or 'ALL'}']...")
    
    sniff(
        iface=interface,
        filter=bpf_filter if bpf_filter else None,
        prn=packet_callback,
        timeout=duration_sec,
        store=False
    )

    print("\n--- [CAPTURE ANALYSIS SUMMARY] ---")
    print(f"Total Traffic Captured: {total_bytes / 1024:.2f} KB")
    print("\nBandwidth by Protocol:")
    for proto, b in traffic_by_protocol.items():
        print(f"  • {proto:<6}: {b / 1024:.2f} KB ({(b / max(total_bytes, 1))*100:.1f}%)")

    print("\nTop 5 Active Network Flows:")
    sorted_flows = sorted(traffic_by_ip.items(), key=lambda x: x[1], reverse=True)[:5]
    for flow, b in sorted_flows:
        print(f"  • {flow:<35}: {b / 1024:.2f} KB")

if __name__ == "__main__":
    # Example: Sniff HTTPS and DNS traffic for 5 seconds
    start_capture(bpf_filter="tcp port 443 or udp port 53", duration_sec=5)
```

---

## Technical Troubleshooting Matrix

| Issue & Failure Signature | Root Cause Analysis | Diagnostic & Resolution Pathway |
| :--- | :--- | :--- |
| **`No network adapters found` (Windows)** | Npcap is not installed, or installed without WinPcap API compatibility mode. | 1. Download and install latest **Npcap**.<br>2. Check **Install Npcap in WinPcap API-compatible Mode** during setup.<br>3. Ensure service is active: `net start npcap`. |
| **`Permission Denied` during Packet Capture (Linux)** | Binary lacks Linux raw socket privileges (`CAP_NET_RAW` / `CAP_NET_ADMIN`). | 1. Grant Linux capabilities: `sudo setcap cap_net_raw,cap_net_admin=eip $(which sniffnet)`.<br>2. Alternatively, run with `sudo sniffnet`. |
| **High Packet Drop Rate on High-Throughput (>1Gbps) Interfaces** | Kernel packet buffer overrun before the user-space process can drain packets. | 1. In Sniffnet, specify tighter BPF filters to discard unwanted traffic at the kernel level.<br>2. Increase socket buffer sizes: `sysctl -w net.core.rmem_max=16777216`. |
| **IP Geolocation / Country Flags Show 'Unknown'** | MaxMind GeoLite2 mmdb database failed to download on startup or local offline mode enabled. | 1. Ensure internet connection during initial launch to fetch geolocation database.<br>2. Check `%APPDATA%\sniffnet` or `~/.config/sniffnet/` for database files. |

---

## Command Line Syntax & Permissions

```bash
# Windows CLI: Verify Npcap Service Status via PowerShell
Get-Service -Name npcap

# Linux: Set Persistent Raw Socket Capabilities on Sniffnet Binary
sudo setcap cap_net_raw,cap_net_admin=eip /usr/local/bin/sniffnet

# Launch Sniffnet Application
sniffnet
```

### Essential File Locations
- **Windows User Settings**: `%APPDATA%\sniffnet`
- **Linux User Settings**: `~/.config/sniffnet`
- **macOS User Settings**: `~/Library/Application Support/sniffnet`
- **Npcap Driver Root**: `C:\Program Files\Npcap\`

---

## Agent Operational Directive
> **MANDATORY**: On Linux, execute `setcap cap_net_raw,cap_net_admin=eip` rather than recommending unrestricted `sudo` execution. On Windows, verify Npcap WinPcap API compatibility mode before running packet captures.
