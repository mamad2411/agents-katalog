---
name: sysadmin-diagnose
description: Diagnose a failing service or system issue on a Debian/Ubuntu Linux machine with a hypothesis-driven loop that gathers evidence from journalctl and systemctl, finds patterns, tests a hypothesis, fixes, and verifies. Use when something is broken and you need root cause, not a guess.
license: MIT
---

# System diagnosis

A system issue is happening. Diagnose and fix it on a Debian/Ubuntu Linux machine using a systematic, hypothesis-driven loop. Gather evidence before changing anything; confirm before applying a fix.

## Diagnostic steps

1. Describe the problem: what is happening, and when did it start?
2. Gather information:
   - System logs: `journalctl -xe`
   - Specific service logs: `systemctl status <service>` and `journalctl -u <service> -xe`
   - Resource usage: `top`, `htop`, `df -h`
   - Network: `ip addr`, `ping`, `ss -tlnp`
3. Identify patterns: is it consistent or intermittent?
4. Check recent changes: what changed before the issue appeared?
5. Research: look for known issues.
6. Test hypotheses: verify the likely cause before acting.
7. Implement the fix: apply the solution.
8. Verify: confirm the issue is resolved (`systemctl is-active <service>`, reproduce the original symptom).

Be systematic and thorough. Form a hypothesis from the evidence rather than guessing, and document findings for future reference.

---

See full content at https://github.com/HermeticOrmus/linux-sysadmin-skills.
