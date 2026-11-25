---
name: ad-harvest
description: "Collect and crack approved, in-scope credential material \u2014 domain secrets via DCSync-style replication (impacket secretsdump) and offline cracking (hashcat/john). Credential access, approval-gated. Gated at runtime by the F0RT1KA permission wall per the engagement autonomy.mode."
version: "1.0.0"
author: redteam-ops
license: Apache-2.0
allowed-tools: Bash Read Write
---

# AD Harvest

> **Runtime: Claude Code.** Helper scripts are in this skill's `scripts/` directory; in commands below, `<skill-dir>` is the absolute skill path provided when the skill loads. `<active-engagement>` is the engagement folder path recorded in `~/.claude/engagements/active` (set by the engagement-setup skill) — read it before resolving paths. Active scope: `<active-engagement>/scope.yaml`. Write outputs to the engagement's numbered subfolders (01-recon, 03-evidence, 04-findings, 05-changes, 07-reports, logs/ — see that folder's CLAUDE.md). Tools are restricted to `Bash Read Write`; irreversible actions are governed by the F0RT1KA permission wall (`~/.claude/hooks/offensive-gate.py`) per the engagement's `autonomy.mode` — `gated` forces a Bash permission prompt, `supervised-auto` allows after a stage briefing. **This skill performs irreversible actions** — post a stage briefing (blast radius + revert plan) before each step; the permission wall enforces the gate per the engagement's `autonomy.mode`.


HARVEST phase. Collect and crack credential material from **approved, in-scope** sources —
domain secrets via DCSync-style replication, and offline cracking of extracted hashes. This is
credential access and is **approval-gated**; manual invocation only.

## When to Use

- After access/escalation yields sufficient privilege, with approval to harvest.
- Deliberate, manual invocation only.

## Quick Reference

| Step                     | Tool                              | Notes |
| ------------------------ | --------------------------------- | ----- |
| Domain secrets (DCSync)  | impacket `secretsdump -just-dc`   | replicates secrets from a DC — high impact, gated |
| Local SAM/LSA secrets    | impacket `secretsdump` (local)    | from an approved host |
| Offline cracking         | `hashcat` / `john`                | non-destructive, runs on the operator box |

## Procedure

1. **Scope + approval.** `scope_check` the target with `--action exploitation` → `GATED`; get explicit approval before any DCSync/secrets extraction. DCSync against a DC is high-impact — confirm sign-off and timing with the client.
2. **Extract from the approved source only.** Run `secretsdump` against the in-scope DC/host you are authorized for; capture output securely.
3. **Crack offline.** Feed hashes to `hashcat`/`john` on the operator machine — no target interaction, non-destructive.
4. **Handle secrets carefully.** Store recovered material encrypted in `<active-engagement>`. Never paste plaintext secrets into logs or reports — reference counts and severity instead.
5. **Hand off.** Recovered/used credentials inform the chain narrative in `ad-report`. Do not expand their use beyond the approved scope.

## Pitfalls

- **DCSync is sensitive and monitored** and replicates real secrets — treat as high-impact, gate it, and time it with the client.
- **Secret sprawl.** Recovered hashes/passwords are sensitive data: encrypt at rest, redact in deliverables, destroy per RoE.
- **Off-box cracking** (cloud/shared rigs) may breach data-handling rules — keep material on the authorized operator box.
- **Reusing harvested creds on new hosts is a new action** — re-gate it.

## Verification

- DCSync/secrets extraction had explicit approval and passed `scope_check`.
- Recovered material is stored encrypted; no plaintext secrets appear in logs or reports.
