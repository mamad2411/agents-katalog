---
name: recon-nmap
description: Network reconnaissance and security auditing using Nmap for port scanning, service enumeration, and vulnerability detection.
metadata:
  version: 0.2.0
  category: offsec
  tags:
  - reconnaissance
  - nmap
  - port-scanning
---
# Nmap Network Reconnaissance

## Quick Start
```bash
# Comprehensive scan (OS, versions, default scripts)
nmap -A <target-ip>

# Fast discovery of live hosts in a network
nmap -sn <network>/24 -oG - | awk '/Up$/{print $2}' > live_hosts.txt
```

## Workflow
1. **Verify Authorization**: Confirm written permission before scanning.
2. **Discover Hosts**: Identify live targets using `-sn` (ping sweep) or `-Pn` (assume up).
3. **Scan Ports**: Identify open ports on live hosts (e.g., `-F` for fast, `-p-` for all).
4. **Enumerate Services**: Use `-sV` for versions and `-O` for OS detection.
5. **Run Scripts**: Use NSE scripts (`--script=vuln,discovery`) for deep analysis.
6. **Report**: Output results using `-oA` for all formats.

## Rules & Constraints
- **RULE-1**: MUST have explicit authorization before any scanning activity.
- **RULE-2**: Use rate limiting (`--max-rate 100`) on fragile or production networks.
- **RULE-3**: Do NOT run intrusive or DOS scripts unless specifically requested.

## When to Use
- Authorized network asset discovery and service enumeration.
- Identifying versions of running services for vulnerability mapping.
- Validating firewall rules and network segmentation.

## When NOT to Use
- Scanning networks or hosts without explicit permission.
- Detailed web application fuzzing (use `dast-ffuf` or `webapp-sqlmap`).

## References
- [Nmap cheatsheet](references/nmap-cheatsheet.md)
- [Nmap Manual (Flags, Patterns, Evasion)](references/nmap-manual.md)
- [Official Nmap Book](https://nmap.org/book/)
- [NSE Script Documentation](https://nmap.org/nsedoc/)
