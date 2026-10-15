---
name: gsp-live-risk-audit
description: "Use when auditing rollback, compatibility, corruption, or operational risks in a shipped or live-risky game."
---

# Game Live Risk Audit

## Goal
Audit shipped or high-risk projects before changes are proposed or applied.

## Outputs

Follow the `gsp-orchestrator` output strategy:
- **inline** (default): present findings in conversation.
- **minimal** or **full**: write to `docs/game-studio/audit/audit-summary.md`, `docs/game-studio/audit/risk-register.md`, `docs/game-studio/audit/scorecard.json`.

Use:
- `../../shared/checklists/live-risk-audit-checklist.md`
- `../../shared/reference/project-state-and-risk.md`

## Evaluate
- save or state compatibility risk
- blast radius of likely edits
- rollback difficulty
- hidden production dependencies
- unsafe assumptions in seemingly small changes
- what should not be touched without a release plan

## Important
When risk is high, recommendations should bias toward small, reversible, well-isolated fixes.
