---
name: ad-initial-access
description: "Turn enumeration/OSINT into a first valid credential: lockout-aware password spraying, credential validation, AS-REP roasting. Active, lockout-risky, approval-gated per the engagement autonomy.mode."
version: "1.0.0"
author: redteam-ops
license: Apache-2.0
allowed-tools: Bash Read Write
---

# AD Initial Access

> **Runtime: Claude Code.** Helper scripts are in this skill's `scripts/` directory; in commands below, `<skill-dir>` is the absolute skill path provided when the skill loads. `<active-engagement>` is the engagement folder path recorded in `~/.claude/engagements/active` (set by the engagement-setup skill) — read it before resolving paths. Active scope: `<active-engagement>/scope.yaml`. Write outputs to the engagement's numbered subfolders (01-recon, 03-evidence, 04-findings, 05-changes, 07-reports, logs/ — see that folder's CLAUDE.md). Tools are restricted to `Bash Read Write`; irreversible actions are governed by the F0RT1KA permission wall (`~/.claude/hooks/offensive-gate.py`) per the engagement's `autonomy.mode` — `gated` forces a Bash permission prompt, `supervised-auto` allows after a stage briefing. **This skill performs irreversible actions** — post a stage briefing (blast radius + revert plan) before each step; the permission wall enforces the gate per the engagement's `autonomy.mode`.


INITIAL ACCESS phase. Turn enumeration/OSINT into a first valid credential or unauthenticated
foothold — lockout-aware password spraying, validating recovered credentials, and AS-REP
roasting against accounts without pre-auth. Active and lockout-risky: **approval-gated**, manual
invocation only.

## When to Use

- Between enumeration and escalation, when you need a first credential.
- When asked to "spray the domain", "validate these creds", or "AS-REP roast".

## Quick Reference

| Step                    | Tool                      | Notes |
| ----------------------- | ------------------------- | ----- |
| Lockout-aware spray     | `netexec` (nxc)           | one well-chosen password across users, paced under the lockout policy |
| Credential validation   | `netexec` / impacket      | confirm a recovered cred without burning attempts |
| AS-REP roast (no cred)  | impacket `GetNPUsers`     | accounts without pre-auth; crack offline |

Budget the spray safely first:
```bash
python3 <skill-dir>/scripts/spray_budget.py --threshold 5 --window-min 30 --users 800
```

## Procedure

1. **Scope + approval.** `scope_check` the target with `--action exploitation` → `GATED`; get explicit approval before spraying. Spraying can lock accounts — confirm the lockout policy and client sign-off.
2. **Read the policy first.** Get the lockout threshold and observation window (from `ad-enumerate`). Compute a safe budget with `spray_budget.py` and leave margin.
3. **Spray carefully.** One password per account per window across the user list; pace by the computed budget; stop at the first sign of lockout risk.
4. **Validate.** Confirm any hit without burning attempts; note where it is valid (SMB/LDAP/WinRM).
5. **AS-REP roast.** Extract hashes for pre-auth-disabled accounts and crack them offline (`ad-harvest`) — don't spray those.
6. **Hand off.** Valid credential(s) → `ad-enumerate` (authenticated) and `ad-attack-paths`. Evidence to `<active-engagement>`, secrets redacted.

## Pitfalls

- **Lockouts cause real outages** and breach the RoE — always policy-aware, budgeted, and approved.
- **Spraying is noisy** and alerts the SOC — coordinate timing and deconfliction.
- **One password per account per window** — never queue multiple passwords per account per round.
- **Don't blind-spray service/admin accounts** — higher blast radius.

## Verification

- Every spray had approval and a computed safe budget; no lockouts were triggered.
- Valid credentials are recorded with secrets redacted.
