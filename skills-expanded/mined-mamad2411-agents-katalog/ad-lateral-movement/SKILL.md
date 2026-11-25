---
name: ad-lateral-movement
description: "Use validated credentials or hashes to move host-to-host within the in-scope estate \u2014 remote execution over SMB/WMI/WinRM and pivoting to segmented targets. Every remote-exec or pivot is approval-gated. Gated at runtime by the F0RT1KA permission wall per the engagement autonomy.mode."
version: "1.0.0"
author: redteam-ops
license: Apache-2.0
allowed-tools: Bash Read Write
---

# AD Lateral Movement

> **Runtime: Claude Code.** Helper scripts are in this skill's `scripts/` directory; in commands below, `<skill-dir>` is the absolute skill path provided when the skill loads. `<active-engagement>` is the engagement folder path recorded in `~/.claude/engagements/active` (set by the engagement-setup skill) — read it before resolving paths. Active scope: `<active-engagement>/scope.yaml`. Write outputs to the engagement's numbered subfolders (01-recon, 03-evidence, 04-findings, 05-changes, 07-reports, logs/ — see that folder's CLAUDE.md). Tools are restricted to `Bash Read Write`; irreversible actions are governed by the F0RT1KA permission wall (`~/.claude/hooks/offensive-gate.py`) per the engagement's `autonomy.mode` — `gated` forces a Bash permission prompt, `supervised-auto` allows after a stage briefing. **This skill performs irreversible actions** — post a stage briefing (blast radius + revert plan) before each step; the permission wall enforces the gate per the engagement's `autonomy.mode`.


LATERAL MOVEMENT phase. Use validated credentials or hashes to move host-to-host within the
in-scope estate — remote execution over SMB/WMI/WinRM and pivoting to reach segmented targets.
Every remote-exec or pivot uses/changes a target and is **approval-gated**; manual invocation only.

## When to Use

- After a valid credential/hash, with a reason to reach another in-scope host.
- When asked to "move to host X", "exec on these hosts", or "pivot to the DB subnet".

## Quick Reference (orchestration of existing tools)

| Step                          | Tool                                       | Notes |
| ----------------------------- | ------------------------------------------ | ----- |
| Remote exec (SMB/WMI/WinRM)   | `netexec`, impacket (psexec/wmiexec/atexec)| runs commands on the target — gated |
| Pass-the-hash / -ticket       | `netexec` / impacket                       | reuse creds without plaintext |
| Pivoting / tunneling          | ssh / proxychains / chisel-style           | reach segmented in-scope hosts only |

## Procedure

1. **Scope + approval.** `scope_check` **each destination host** with `--action exploitation` → `GATED` + explicit approval. Lateral movement crosses hosts; re-gate every hop.
2. **Choose the least-invasive exec.** Prefer WinRM/WMI over service-creating psexec where possible (fewer artifacts).
3. **Execute one approved hop.** Run the planned remote-exec against the in-scope host; capture output.
4. **Pivot only within scope.** Tunnels must reach only authorized hosts/subnets — never bridge to out-of-scope networks.
5. **Record artifacts + revert.** Note any services/files created; clean them up; capture evidence (redact secrets).
6. **Stop conditions.** An out-of-scope host, an availability risk, or DC/critical-system exec without explicit sign-off → stop and report.

## Pitfalls

- **Every hop is a new authorization decision** — re-gate; the chain does not inherit scope.
- **psexec-style exec leaves services/artifacts** — prefer cleaner methods, track and clean up.
- **Tunnels can accidentally bridge out-of-scope networks** — constrain and document them.
- **Cred-reuse blast radius** — a reused admin hash can hit many hosts; move deliberately.

## Verification

- Each hop had approval and passed `scope_check` on the destination host.
- Artifacts are tracked and reverted; evidence is logged with secrets redacted.
