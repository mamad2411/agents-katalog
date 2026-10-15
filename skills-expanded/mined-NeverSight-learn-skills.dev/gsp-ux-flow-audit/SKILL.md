---
name: gsp-ux-flow-audit
description: "Use when auditing first-minute onboarding, menus, fail/retry flow, or player comprehension in a game."
---

# Game UX Flow Audit

## Goal
Audit the player journey and moment-to-moment experience flow, especially the first 30 seconds.

## Outputs

Follow the `gsp-orchestrator` output strategy:
- **inline** (default): present findings in conversation.
- **minimal** or **full**: write to `docs/game-studio/audit/ux-findings.md`, `docs/game-studio/audit/audit-summary.md`, `docs/game-studio/audit/scorecard.json`.

Use:
- `../../shared/checklists/ux-flow-audit-checklist.md`
- `../../shared/reference/first-30-seconds.md`
- `../../shared/reference/audit-confidence-and-evidence.md`

## Evaluate
- first actionable screen clarity
- onboarding length and interruption cost
- main verb discoverability
- fail / retry / pause / resume flow
- menu-to-play transitions
- whether the UI or setup blocks the core loop

## Evidence discipline
Tag each important finding with:
- confidence: `high`, `medium`, or `low`
- evidence: `code`, `config`, `asset`, `screenshot`, or `inferred`

## Output style
Write findings in game-language, such as:
- what the player understands too late
- what the player is asked to do too early
- where friction kills momentum

