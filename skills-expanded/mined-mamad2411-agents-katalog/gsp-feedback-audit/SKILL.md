---
name: gsp-feedback-audit
description: "Use when auditing responsiveness, rewards, failures, danger telegraphing, or state-transition feedback in a game."
---

# Game Feedback Audit

## Goal
Audit whether the game clearly responds to the player and communicates consequences.

## Outputs

Follow the `gsp-orchestrator` output strategy:
- **inline** (default): present findings in conversation.
- **minimal** or **full**: write to `docs/game-studio/audit/audit-summary.md`, `docs/game-studio/audit/ux-findings.md`, `docs/game-studio/audit/scorecard.json`.

Use:
- `../../shared/checklists/feedback-audit-checklist.md`
- `../../shared/checklists/game-feel-pillars.md`
- `../../shared/reference/audit-confidence-and-evidence.md`

## Evaluate
- input acknowledgment
- hit / damage / collect / upgrade / deny signals
- reward and success feedback
- fail and error feedback
- danger telegraphing
- state transition clarity
- whether feedback supports understanding or is merely decorative

## Important
A feature that technically works but gives weak or missing feedback should be marked as partially complete, not fully complete.
