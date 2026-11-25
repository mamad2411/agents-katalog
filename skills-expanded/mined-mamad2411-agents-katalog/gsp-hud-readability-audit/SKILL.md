---
name: gsp-hud-readability-audit
description: "Use when auditing HUD hierarchy, readability, controls discoverability, or mobile thumb-zone pressure."
---

# Game HUD Readability Audit

## Goal
Audit the heads-up display and overlay layer for readability, hierarchy, and actionable clarity.

## Outputs

Follow the `gsp-orchestrator` output strategy:
- **inline** (default): present findings in conversation.
- **minimal** or **full**: write to `docs/game-studio/audit/ux-findings.md`, `docs/game-studio/audit/audit-summary.md`, `docs/game-studio/audit/scorecard.json`.

Use:
- `../../shared/checklists/hud-readability-audit-checklist.md`
- `../../shared/checklists/ui-ux-hard-rules.md`
- `../../shared/reference/audit-confidence-and-evidence.md`

## Evaluate
- information priority and hierarchy
- readability of numbers, labels, and state cues
- button affordance and control discoverability
- text density and clutter
- overlap between HUD and playfield
- persistent HUD budget discipline
- mobile thumb-zone or one-handed pressure
- whether essential state is hidden, delayed, or over-explained
- whether menu / pause / overlay states fight gameplay readability

## Important
If screenshots are unavailable, state which claims are inferred from code or layout structure rather than observed directly.
Call out explicit hard-rule violations when the playfield, focus, or safe-area behavior is likely wrong.
