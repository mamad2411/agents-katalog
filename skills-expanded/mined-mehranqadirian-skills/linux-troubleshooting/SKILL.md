---
name: linux-troubleshooting
description: Diagnoses problems on Linux machines in a structured, read-only-first way. Use whenever the user reports a slow or frozen system, full disk, out-of-memory kills, a service that will not start, a port that is not reachable, DNS or network failures, permission denied or SELinux errors, or asks to check the health of a server or laptop, even if they only say "my Fedora is acting weird". Starts with a read-only snapshot script and never suggests destructive commands as a first step.
---

# linux-troubleshooting

Find the cause before changing anything. A read-only snapshot gives facts in seconds; the playbooks turn symptoms into the next command.

```
linux-troubleshooting/
├── SKILL.md
├── scripts/
│   └── sysdiag.sh           load, memory, swap, disk and inodes, failed units, journal errors, network, ports
└── references/
    └── playbooks.md         slow machine, disk full, services, ports, DNS, permissions, SELinux, logs, safety
```

## When to use

- Slow, frozen or overheating machine
- Disk or inode exhaustion, memory pressure, OOM kills
- A systemd service fails or keeps restarting
- Something cannot connect, or a port does not answer
- Permission or SELinux denials
- A routine health check of a server or workstation

## Workflow

1. **Get the facts**: run `bash scripts/sysdiag.sh` (use `--brief` for warnings only). It never uses sudo and never changes anything. Thresholds can be adjusted with `DISK_WARN`, `INODE_WARN`, `MEM_WARN`, `SWAP_WARN`, `LOAD_FACTOR`.
2. **Read the verdict**: each warning names the subsystem. Pick the matching playbook in `references/playbooks.md`.
3. **State a hypothesis and the command that would disprove it**, then run only read-only commands first. Ask the user for the output and wait; do not guess results.
4. **Check logs before restarting**: `journalctl -u NAME -b`, `journalctl -b -p err`. A restart can destroy the evidence.
5. **Change one thing at a time**, with a backup (`cp file file.bak`) and a way to undo. Explain what the command does and the risk before the user runs it.
6. **Verify the fix** with the same observation that showed the problem, and say what else to watch.

## Rules

- Read-only commands first; confirm before `rm`, `kill -9`, `chmod -R`, `dd`, `mkfs`, firewall or SELinux changes
- Never recommend `chmod -R 777`, disabling SELinux or turning off the firewall as a diagnostic shortcut
- Match the distribution: Fedora and RHEL use `dnf`, `firewalld`, SELinux; Debian and Ubuntu use `apt`, `ufw`, AppArmor
- Do not run commands for the user; give them, with expected output and what it means
- Say what you could not see (no sudo, no journal access) instead of guessing
- Remote servers: warn before any command that could cut the SSH session (network, firewall, sshd)

## What to report back

| Field | Content |
|-------|---------|
| Symptom | what was observed, with the numbers |
| Evidence | commands and the lines that matter |
| Cause | the most likely one, and how sure |
| Fix | steps in order, with undo for each |
| Verification | how to confirm, and what to monitor |

## Related skills

- `systematic-debugging`: the general reproduce, isolate, prove method
- `docker-basics`: container disk usage, ports and permissions
- `shell-scripting`: write the checks you will run repeatedly as safe scripts
- `termux-setup`: Android specific problems
