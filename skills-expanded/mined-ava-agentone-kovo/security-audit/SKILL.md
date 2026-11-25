---
name: security-audit
description: Deep security audit of the VM — network, packages, users, files, processes, malware. Tracks baselines and reports only changes. Escalates suspicious activity via Telegram call.
tools: [shell]
trigger: security, audit, scan, vulnerability, ports, malware, rootkit, packages, suspicious, intrusion, hardening, security check, security report
---

# Security Audit Skill

## Purpose

Perform a comprehensive security audit of the Kovo VM. Maintains a baseline of system state and alerts on unauthorized changes. Escalates suspicious findings via Telegram voice call.

## Audit Categories

### 1. Network — open ports (ss -tlnp), outbound connections, firewall status
### 2. Packages — installed vs baseline, flag unauthorized new packages, pending security updates
### 3. Users & Access — new accounts, sudo grants, SSH config, failed logins
### 4. File System — new SUID binaries, world-writable files, cron job changes, config permissions
### 5. Processes — unknown processes, high resource usage, root processes
### 6. Malware — ClamAV scan, rootkit check (chkrootkit/rkhunter), suspicious files in /tmp /dev/shm

## Baseline

Stored at: /opt/kovo/data/security_baseline.json
- First run creates baseline (no alerts)
- Subsequent runs compare and report changes only
- Reset with: /audit reset

## Escalation

- CALL: new user, new sudo, new SUID, malware, SSH root enabled, unauthorized package, suspicious files, 20+ failed logins
- TEXT WARNING: security updates pending, world-writable files, config permissions, unknown outbound connections
- TEXT CLEAN: no issues found

## Commands

- /audit — run full audit now
- /audit reset — reset baseline
- /audit baseline — show baseline summary
- /audit ports — quick port scan
- /audit packages — quick package diff

## Schedule

Every Sunday at 7:00 AM via heartbeat scheduler.
