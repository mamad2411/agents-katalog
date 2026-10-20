---
name: ad-report
description: "Turn the executed kill chain into a scored narrative report \u2014 foothold to domain impact, with evidence, CVSS scoring, environment-change/revert status, and remediation. Documentation only."
version: "1.0.0"
author: redteam-ops
license: Apache-2.0
allowed-tools: Bash Read Write
---

# AD Report

> **Runtime: Claude Code.** Helper scripts are in this skill's `scripts/` directory; in commands below, `<skill-dir>` is the absolute skill path provided when the skill loads. `<active-engagement>` is the engagement folder path recorded in `~/.claude/engagements/active` (set by the engagement-setup skill) — read it before resolving paths. Active scope: `<active-engagement>/scope.yaml`. Write outputs to the engagement's numbered subfolders (01-recon, 03-evidence, 04-findings, 05-changes, 07-reports, logs/ — see that folder's CLAUDE.md). Tools are restricted to `Bash Read Write`; irreversible actions are governed by the F0RT1KA permission wall (`~/.claude/hooks/offensive-gate.py`) per the engagement's `autonomy.mode` — `gated` forces a Bash permission prompt, `supervised-auto` allows after a stage briefing.


SHIP phase. Turn the executed kill chain into a clear, scored narrative: how access went from
initial foothold to domain impact, backed by evidence, with remediation and the status of any
changes made. Documentation only.

## When to Use

- After the kill chain is executed and evidence captured.
- When asked to "write up the chain", "score these AD findings", or "DA via certipy ESC from the initial cred".

## Quick Reference

Chain narrative skeleton: initial access → enumeration insight → escalation step(s) → harvest → domain impact.

Score notable findings (CVSS v3.1):
```bash
python3 <skill-dir>/scripts/cvss.py "CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H"
```

Per finding: title, affected object(s), severity, summary, impact, reproduction (minimal, secret-free), evidence refs, remediation.

## Procedure

1. **Assemble.** Pull the path plan, executed steps, and evidence from `<active-engagement>`.
2. **Write the chain narrative.** Tell it end-to-end (e.g., initial OWA cred → roast → ACL → DA via AD CS ESC), each step tied to evidence.
3. **Score findings.** Build defensible CVSS vectors, compute with `cvss.py`, and note the assumptions behind each vector.
4. **Remediation.** Concrete fixes: certificate-template hardening, SMB signing / channel binding (EPA), admin tiering, delegation cleanup, and KRBTGT rotation where relevant.
5. **Context.** Executive summary, scope and `authorization_ref`, methodology, and any environment changes made with their revert status.
6. **Deliver.** Write a Markdown report to `<active-engagement>`. For a high-resolution BloodHound path screenshot, append `[[as_document]]` on its own line so it is delivered as a file.

## Pitfalls

- **Plaintext secrets in the report.** Reference counts and severity — never dump credentials or hashes.
- **Unreverted changes.** Document every write and its revert status.
- **Inflated scores.** Match the CVSS vector to demonstrated reality.
- **Vague remediation.** Name the template, ACL, or setting to change.

## Verification

- An end-to-end chain narrative is tied to evidence; findings are scored.
- Environment changes and revert status are documented; no secrets are leaked.
