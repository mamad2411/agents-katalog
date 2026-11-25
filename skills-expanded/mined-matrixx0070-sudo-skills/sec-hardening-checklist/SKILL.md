---
name: sec-hardening-checklist
version: 1.0.0
description: Produce a CIS-style server and application hardening checklist with evidence and prioritized, exposure-ranked fixes.
author: matrixx0070
tags: [security, hardening, cis, baseline, configuration, defensive]
capabilities: []
---

## When to use

Use this when standing up a new server or service, preparing for an audit, or reducing attack surface on existing infrastructure. It maps configuration to a defensive baseline and ranks the fixes by impact.

**Not for:** scanning for exploitable vulnerabilities on someone else's systems; reviewing application source (use `sec-code-audit`); or applying changes to production without approval. Assess and recommend — the operator applies changes.

## Method

1. **Identify the target.** Note the OS, runtime, exposed services, and network position (internet-facing vs. internal). *Decision point:* internet-facing systems get the stricter baseline and jump the priority queue.
2. **OS & accounts.** Check patch level, disabled root SSH login, key-only auth, minimal sudoers, no default/shared accounts, and password/lockout policy.
3. **Network & services.** Verify firewall default-deny, only required ports open, no unneeded daemons, and TLS with modern ciphers on every listener.
4. **Application config.** Confirm secure headers, disabled debug/verbose errors, least-privilege service accounts, resource limits, and secrets sourced from a vault.
5. **Logging & monitoring.** Ensure audit logging is on, logs ship off-host, and alerts exist for auth failures and privilege changes.
6. **Prioritize.** Rank each gap by exposure and exploitability; internet-facing and privilege-related gaps first.

## Example

Target: an internet-facing Ubuntu web host. Check: `PermitRootLogin` in `sshd_config`. Evidence: currently `yes`. Status: Fail. Category: OS & accounts. Fix: set `PermitRootLogin no` and `PasswordAuthentication no`, use key-only auth, reload sshd. Priority: Critical — remote root exposure on an internet-facing host.

## Pitfalls

- **Copying a baseline verbatim.** A CIS profile for a database host misfits a web server; tailor controls to the actual role.
- **Marking Pass without evidence.** "Firewall looks fine" is not an audit. Record the config value or command output that proves it.
- **Ranking by category, not exposure.** A weak internal cron matters less than an open internet-facing port; sort by blast radius.
- **One-and-done.** Baselines drift as software updates and people make changes; schedule re-checks.

## Output format

```
## Target profile
OS: <>. Services: <>. Exposure: <internet/internal>. Baseline: <CIS / vendor guide>.

## Checklist
| Control | Category | Status (Pass/Fail/N-A) | Evidence | Fix |
|---------|----------|------------------------|----------|-----|

## Prioritized fixes
| Fix | Priority (Critical→Low) | Effort |
|-----|-------------------------|--------|

## Baseline drift note
- <what to re-check and how often>
```
