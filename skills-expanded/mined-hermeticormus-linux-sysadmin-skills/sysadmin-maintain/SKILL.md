---
name: sysadmin-maintain
description: Routine maintenance pass on a Debian/Ubuntu Linux machine that updates and upgrades packages, autoremoves, cleans cache, scans logs, checks disk and services, and verifies backups. Asks before destructive steps. Use for regular upkeep.
license: MIT
---

# System maintenance

Perform routine maintenance on a Debian/Ubuntu Linux machine. Run each step carefully and report findings. Ask before any potentially destructive operation.

## Maintenance checklist

1. Updates: check and install updates (`apt update && apt upgrade`).
2. Cleanup: remove unused packages (`apt autoremove`).
3. Cache: clean the package cache if needed (`apt clean`).
4. Logs: check system logs for issues (`journalctl -p 3 -b`).
5. Disk space: check disk usage (`df -h`).
6. Services: verify critical services are running (`systemctl is-active <service>`).
7. Security: check for security updates.
8. Backup: verify backup systems are working and have a recent successful run.

Run each step carefully and report findings. Ask before performing potentially destructive operations such as package removal, cache clearing, or anything that deletes or replaces files.

---

See full content at https://github.com/HermeticOrmus/linux-sysadmin-skills.
