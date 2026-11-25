---
name: vps-hardening-check
description: Reports common VPS hardening gaps.
---
# VPS hardening check

1. Check that unattended upgrades and the firewall are on.
2. Read `/etc/ssh/sshd_config` and report whether root login or password login is allowed. Do not change it; recommend `PermitRootLogin no`.
3. Report the checklist with ticks.
