---
name: gsp-feel-audit
description: "Use when auditing control feel, responsiveness, timing, camera reaction, or animation feedback in a game."
---

# Game Feel Audit

## Goal
Audit whether the game seems responsive, readable, and satisfying rather than merely functional.

## Outputs

Follow the `gsp-orchestrator` output strategy:
- **inline** (default): present findings in conversation.
- **minimal** or **full**: write to `docs/game-studio/audit/audit-summary.md`, `docs/game-studio/audit/scorecard.json`, `docs/game-studio/audit/ux-findings.md`.

Use:
- `../../shared/checklists/gsp-feel-audit-checklist.md`
- `../../shared/checklists/game-feel-pillars.md`
- `../../shared/reference/audit-confidence-and-evidence.md`

## Evaluate
- apparent input-to-response latency in the implementation
- camera behavior around motion and impact
- timing support for attacks, movement, traversal, or collection
- feel debt caused by missing polish hooks
- emotionally dead interactions that need stronger juice or pacing

## Important
Without runtime evidence, do not overstate certainty. Identify whether findings are confirmed or probable.

