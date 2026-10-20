---
name: homelab-network-auditor
description: Audit homelab network topology, scan for open ports and exposed services, review firewall rules, and generate network security reports.
---

# homelab-network-auditor

## Purpose
Provide systematic network security auditing for the homelab. Discovers active hosts, scans for open ports and services, checks firewall rule consistency, identifies unintended exposures, and produces actionable security reports. Feeds findings into `homelab-logbook` and `homelab-change-planner`.

## Invocation
- "Scan homelab network for open ports"
- "Audit firewall rules on [host/VLAN]"
- "Find exposed services on the homelab network"
- "Generate a network security report"
- "Check what ports are open on [IP]"
- "Verify only expected services are accessible externally"

## Workflow Steps
1. **Scope:** Define target IP range, VLAN, or specific hosts; confirm scope is limited to owned infrastructure.
2. **Discover:** Run host discovery (ping sweep or ARP scan) to enumerate active hosts.
3. **Scan:** Execute port scan (nmap or equivalent) against discovered hosts; record open ports and service banners.
4. **Firewall review:** Compare open ports against documented firewall rules; flag discrepancies.
5. **Exposure check:** Identify any services reachable from external/WAN interface that should not be.
6. **Report:** Generate summary: hosts scanned, open ports, unexpected exposures, recommended remediations.
7. **Log:** Record audit results in `homelab-logbook`.
8. **Plan:** Create remediation tasks in `homelab-change-planner` for any critical findings.

## Safety
- ONLY scan infrastructure you own or have explicit permission to audit.
- Never run aggressive scan profiles against production or shared networks.
- Do not expose raw scan data or IP maps in unsecured outputs.
- Alert user before scanning any subnet outside the documented homelab range.
- Confirm scope with user before any scan begins.

## MCP
- No dedicated MCP; orchestrates nmap CLI and firewall API calls via agent subprocess.
- May integrate with Proxmox MCP (`mcp/proxmox-mcp.json`) for VM network inspection.

## References
- nmap: https://nmap.org/
- nmap reference guide: https://nmap.org/book/man.html
- Proxmox networking: https://pve.proxmox.com/wiki/Network_Configuration

## Companion Skills
- `homelab-topology-mapper` — consumes audit data for topology updates
- `homelab-safe-ops` — safety gates for all network changes
- `homelab-change-planner` — tracks remediation tasks from audit findings
- `homelab-logbook` — stores audit reports
- `reverse-proxy-and-tunnel` — validates external exposure config
