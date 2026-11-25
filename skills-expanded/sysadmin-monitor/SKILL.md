---
name: sysadmin-monitor
description: Read-only health sweep of a Debian/Ubuntu Linux machine covering CPU, memory, disk, network, processes, critical services, temperatures, and recent log errors, ending in a summary that flags concerns. Use for an on-demand snapshot of system health.
license: MIT
---

# System monitoring

Check the overall health of a Debian/Ubuntu Linux machine. This is a read-only sweep: it observes and reports, it does not change anything.

## Monitoring checklist

1. CPU usage: check load and top processes.
2. Memory: RAM and swap usage (`free -h`).
3. Disk: free space and I/O (`df -h`).
4. Network: traffic and connectivity.
5. Processes: running processes and resource consumption.
6. Services: status of critical units (`systemctl --failed`, `systemctl is-active <service>`).
7. Temperatures: system temperatures if sensors are available.
8. Logs: recent errors or warnings (`journalctl -p 3 -b`).

Provide a summary of system health and flag any concerns. Suggest follow-up if issues are found; for a routine fix-up, the maintenance workflow is the next step.

---

See full content at https://github.com/HermeticOrmus/linux-sysadmin-skills.
