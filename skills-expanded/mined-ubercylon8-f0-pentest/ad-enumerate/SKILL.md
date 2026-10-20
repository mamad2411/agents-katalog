---
name: ad-enumerate
description: "Read the directory with available access \u2014 users, groups, computers, ACLs, delegation, shares, and AD CS templates \u2014 plus a BloodHound collection for path analysis. Read-only enumeration."
version: "1.0.0"
author: redteam-ops
license: Apache-2.0
allowed-tools: Bash Read Write
---

# AD Enumerate

> **Runtime: Claude Code.** Helper scripts are in this skill's `scripts/` directory; in commands below, `<skill-dir>` is the absolute skill path provided when the skill loads. `<active-engagement>` is the engagement folder path recorded in `~/.claude/engagements/active` (set by the engagement-setup skill) — read it before resolving paths. Active scope: `<active-engagement>/scope.yaml`. Write outputs to the engagement's numbered subfolders (01-recon, 03-evidence, 04-findings, 05-changes, 07-reports, logs/ — see that folder's CLAUDE.md). Tools are restricted to `Bash Read Write`; irreversible actions are governed by the F0RT1KA permission wall (`~/.claude/hooks/offensive-gate.py`) per the engagement's `autonomy.mode` — `gated` forces a Bash permission prompt, `supervised-auto` allows after a stage briefing.


ENUMERATE phase. With whatever access is permitted (a low-priv credential, or anonymous/guest
where allowed), read the directory — users, groups, computers, ACLs, delegation, shares, and
certificate services — and run a BloodHound collection for later path analysis. Read-only.

## When to Use

- After `ad-discover`, or when handed a DC/domain and (optionally) a low-priv credential.
- When asked to "enumerate the domain", "run a BloodHound collection", or "list users/groups/shares".

## Quick Reference

| Tool                          | Role |
| ----------------------------- | ---- |
| `netexec` (nxc)               | SMB/LDAP enum: users, shares, password policy, signing |
| `ldapdomaindump`              | offline-browsable LDAP dump |
| `bloodhound-python` / SharpHound | collect graph data (read-only LDAP/SMB) |
| `certipy find`                | enumerate AD CS CAs and templates (read-only) |
| `smbclient`                   | list/inspect in-scope shares |

Collection example: `bloodhound-python -u <user> -p <pass> -d <domain> -c All -ns <dc-ip> --zip`

## Procedure

1. **Scope first.** Run `scope_check` on the DC/targets with `--action active_scan`.
2. **Baseline.** `nxc` SMB/LDAP for users, password policy, share list, and signing posture.
3. **Directory dump.** `ldapdomaindump` for an offline view; `smbclient` to inventory readable shares. Reading share *contents* can expose sensitive data — stay within RoE and redact in evidence.
4. **Graph collection.** Run a BloodHound collection (`-c All`) with the lowest-privilege credential available; keep the zip in evidence. These are read-only LDAP/SMB queries.
5. **AD CS inventory.** `certipy find` to list CAs and templates (read-only) for path analysis.
6. **Hand off.** Collected data goes to `ad-attack-paths`. Write artifacts to `<active-engagement>`.

## Pitfalls

- **LDAP queries are logged**; bulk collection is noisy. Expected in TLPT, but coordinate timing.
- **No credential brute-forcing here.** Guessing/spraying is an active step — gate it, don't fold it into enumeration.
- **Share contents may hold PII/secrets.** Handle per RoE; redact in stored evidence.
- **Clock skew breaks Kerberos.** Sync to the DC clock before authenticated queries.

## Verification

- A BloodHound zip is collected and ingestible; an LDAP dump exists.
- Password policy, signing posture, and the CA/template list are recorded.
- Every enumerated target is in scope.
