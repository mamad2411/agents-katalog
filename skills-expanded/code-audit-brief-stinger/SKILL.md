---
name: code-audit-brief-stinger
description: Render the Audit My Code brief, one self-contained Field Guide styled HTML file per run, from the workspace only. Escapes repo text, merges duplicates, prints cleanly to PDF.
license: AGPL-3.0-or-later
compatibility: Claude Code 2.1 or newer, Cursor 2.4 or newer, Codex, Cowork. The renderer needs Python 3.11 standard library only.
metadata:
  author: Legion Code Inc.
  hive-drone: code-audit-brief-wasp-drone
  pair-drone: code-audit-brief-wasp-drone
  domain: audit brief rendering
  version: 1.0.0
  research-window: 2026-03-30 to 2026-09-30
---

# Code Audit Brief Stinger

Designed and built by Legion Code Inc.

## Where this skill's files are

Every path below (`guides/`, `references/`, `scripts/`) is relative to the folder that contains this `SKILL.md`. In Claude Code that folder is `${CLAUDE_SKILL_DIR}`. If that text was not replaced with a real path, find the folder with Glob for `**/code-audit-brief-stinger/SKILL.md` and use it in every command.

## Purpose

Turn a finished `/audit-my-code` run workspace into one HTML brief at `<workspace>/brief/brief.html` that a founder can read on a phone or save as a PDF. The brief covers exactly the dimensions of the tier that ran, in the Legion Code Inc. Field Guide style: cover, the whole audit in one paragraph, a verdict scorecard, one part per dimension (measures, charts, findings, spot checks, tool limits), fix these first, coverage and caps, and the method and evidence index. It renders; it never invents, edits, or re-scores a finding.

## When to use

- "Render the brief", "build the audit report", "make the HTML for this audit run"
- The last step of `/audit-my-code` after every dimension Drone has written its output
- Re-rendering after a Drone fixes its `findings.jsonl` or `metrics.json`
- Changing the brief's branding (palette, fonts, logos, footer) in one place

## When not to use

- Running any audit dimension: the foundation, bloat, security, quality, and remediation Drones own that
- Website audit reports from crawled sites: `audit-reporting-stinger`
- Scoring or weighting findings into a number: this brief uses the contract verdict scale only
- Writing anything into the audited repository: this skill writes only `brief/brief.html` in the workspace

## Procedure

1. Read `guides/00-inputs-and-contract.md` and the contract it links. Confirm the workspace path and that `intake.json` exists.
2. Run the contract checker if installed and note its failures for the orchestrator (guide 00).
3. Render: `python3 scripts/render_brief.py <workspace>` (guide 02). Keep the summary line it prints.
4. Check the brief against `guides/04-verification-before-handoff.md` and `references/verification-checklist.md`: tier coverage, not-run reasons, caps, escaping, phone width, print.
5. Report the brief path, overall verdict, counts by severity, and every data check, naming the Drone that owns each problem. Never patch workspace files yourself.
6. Branding change requested: follow `guides/03-branding-system.md`, edit only `references/brand/brand.json` and the logo files, re-render a fixture, and run `python3 scripts/test_render_brief.py`.

## References map

| Path | Load when |
| --- | --- |
| `guides/00-inputs-and-contract.md` | First, on every task |
| `guides/01-section-map-per-tier.md` | Checking which sections a tier gets or where a section's content comes from |
| `guides/02-rendering-and-escaping.md` | Running or editing the renderer; any question about untrusted text |
| `guides/03-branding-system.md` | Changing palette, fonts, logos, footer, theme, or print look |
| `guides/04-verification-before-handoff.md` | Before handing the brief to anyone |
| `references/REFERENCE.md` | Script options, files read, function contracts, fixtures |
| `references/verification-checklist.md` | The tick list for guide 04 |
| `references/brand/brand.json` | The single place to change branding |
| `references/brand/*.svg` | Logo, symbol, and favicon inlined into the brief |
| `references/fixtures/sample-*/` | Fictional workspaces and their rendered briefs, for testing changes |
| `scripts/render_brief.py` | Run to render; `rollup_verdict` sits near the top |
| `scripts/test_render_brief.py` | Run after any change to the script or the brand file |
| `references/research/distilled-brief-rendering.md` | Verifying a claim about print, tables, escaping, fonts, or the design sources |
| Source research archive (not shipped with the plugin) | Source-repository only; the shipped distillation summarizes it, do not require it |

## Related drones and stingers

- [audit-my-code-stinger](../audit-my-code-stinger) - The orchestrating skill and the run contract this renderer reads.
- [remediation-planning-stinger](../remediation-planning-stinger) - Owns `plan.json` and `roadmap.md`, which the mario-tier part renders.
- [code-audit-brief-wasp-drone](../../agents/code-audit-brief-wasp-drone.md) - The paired agent; delegate the render and verification to it.

## Critical Directive

- You must read all files and context contained within your skill.
- In the event your core knowledge does not provide sufficient guidance you must make every attempt to search the internet, related knowledge base documentation files, and other available resources to supplement your knowledge prior to proceeding with your task.
- Additional related skills can be found here:
  - [audit-my-code-stinger](../audit-my-code-stinger) - Run contract, tiers, and the orchestration of every Audit My Code dimension.
  - [remediation-planning-stinger](../remediation-planning-stinger) - The plan and roadmap formats rendered in the mario tier.

<!-- Ship Gate removed: research-only stinger, produces no committable code. It writes one HTML file into the audit workspace and never changes the audited repository. -->

---

Designed and built by Legion Code Inc. Licensed under AGPL-3.0-or-later.
