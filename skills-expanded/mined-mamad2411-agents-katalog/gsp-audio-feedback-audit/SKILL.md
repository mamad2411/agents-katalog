---
name: gsp-audio-feedback-audit
description: "Use when auditing UI sounds, reward/failure cues, danger cues, or audio feedback layering in a game."
---

# Game Audio Feedback Audit

## Goal
Audit audio as part of the feedback grammar rather than as a late cosmetic layer.

## Outputs

Follow the `gsp-orchestrator` output strategy:
- **inline** (default): present findings in conversation.
- **minimal** or **full**: write to `docs/game-studio/audit/audit-summary.md`, `docs/game-studio/audit/ux-findings.md`, `docs/game-studio/audit/scorecard.json`.

Use:
- `../../shared/checklists/audio-feedback-audit-checklist.md`
- `../../shared/reference/audit-confidence-and-evidence.md`

## Evaluate
- menu and button confirmation sounds
- reward, pickup, and completion sounds
- fail, deny, and danger cues
- layering conflicts and priority confusion
- whether audio clarifies state or merely adds noise

## When evidence is weak
If assets or hooks exist but runtime behavior is unclear, classify findings as inferred and explain what remains unverified.
