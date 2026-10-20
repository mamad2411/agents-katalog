---
name: ad-access-escalate
description: "Execute approved AD attack-path steps (impacket, bloodyAD, krbrelayx, certipy): roasting extraction, ACL abuse, coerce-relay-RBCD, AD CS abuse. Irreversible and approval-gated per the engagement autonomy.mode."
version: "1.0.0"
author: redteam-ops
license: Apache-2.0
allowed-tools: Bash Read Write
---

# AD Access & Escalate

> **Runtime: Claude Code.** Helper scripts are in this skill's `scripts/` directory; in commands below, `<skill-dir>` is the absolute skill path provided when the skill loads. `<active-engagement>` is the engagement folder path recorded in `~/.claude/engagements/active` (set by the engagement-setup skill) — read it before resolving paths. Active scope: `<active-engagement>/scope.yaml`. Write outputs to the engagement's numbered subfolders (01-recon, 03-evidence, 04-findings, 05-changes, 07-reports, logs/ — see that folder's CLAUDE.md). Tools are restricted to `Bash Read Write`; irreversible actions are governed by the F0RT1KA permission wall (`~/.claude/hooks/offensive-gate.py`) per the engagement's `autonomy.mode` — `gated` forces a Bash permission prompt, `supervised-auto` allows after a stage briefing. **This skill performs irreversible actions** — post a stage briefing (blast radius + revert plan) before each step; the permission wall enforces the gate per the engagement's `autonomy.mode`.


ACCESS / ESCALATE phase. Execute the **approved, in-scope** steps from the path plan using the
standard tools. Every step that writes to, coerces, relays to, or issues a certificate on a
target is irreversible and **approval-gated** — one step, one approval, never autonomous.

## When to Use

- After `ad-attack-paths` produces an approved path plan.
- Deliberate, manual invocation only.

## Quick Reference (orchestration of existing tools — do not hand-roll exploitation)

| Step                          | Tool                                   | Reversibility |
| ----------------------------- | -------------------------------------- | ------------- |
| Kerberoast / AS-REP extract   | impacket `GetUserSPNs` / `GetNPUsers`  | read (extract) → crack offline in `ad-harvest` |
| ACL abuse                     | `bloodyAD` (group/attribute changes)   | WRITE — gated, must be reverted |
| Coerce + NTLM relay → RBCD    | `krbrelayx`/`ntlmrelayx` + coercion tool | WRITE/stateful — gated |
| AD CS template abuse          | `certipy` req/auth (per confirmed ESC) | issues a certificate — gated |

## Procedure

1. **Scope + approval.** Ensure `engagement-scope` is loaded; `scope_check` the target with `--action exploitation` — it must return `GATED`. Post the stage briefing and obtain explicit human approval before each writing/relaying/issuing step. This is enforced by the F0RT1KA permission wall (`~/.claude/hooks/offensive-gate.py`) per the engagement's `autonomy.mode` — bloodyAD/dacledit/ntlmrelayx/certipy etc. are recognized as irreversible; in `gated` mode it forces a prompt, in `supervised-auto` it runs after your briefing.
2. **Read/extract before write.** Kerberoast and AS-REP *extraction* are read-only — pull the hashes and pass them to `ad-harvest` for offline cracking before attempting any write-based path.
3. **Execute one approved step.** Run the single planned tool/technique against the in-scope target. Do not chain steps unattended.
4. **Record the change and its revert.** For any write (ACL/group/RBCD/cert), capture the exact change and how to undo it; revert at end of engagement unless the client directs otherwise.
5. **Capture evidence.** Command, target, result, timestamp → `<active-engagement>` (redact secrets).
6. **Stop conditions.** An out-of-scope pivot, a disabled action class, or any DC-impacting/availability-risking action without explicit sign-off → stop and report.

## Pitfalls

- **Writes change the environment.** Always record and plan the revert — uncoordinated changes break production and the RoE.
- **Coercion/relay can hit unintended hosts.** Constrain targets; confirm scope on both ends of a relay.
- **Certificate issuance persists access** and leaves artifacts — track it and clean up.
- **"It worked, let's go further."** Each further step needs its own approval and scope check.

## Verification

- Each executed step has a recorded approval and passed `scope_check` `exploitation`.
- Every write has a captured revert plan; evidence is logged with secrets redacted.
