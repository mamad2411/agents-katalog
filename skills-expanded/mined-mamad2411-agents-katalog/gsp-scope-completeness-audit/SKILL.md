---
name: gsp-scope-completeness-audit
description: "Use when auditing whether delivered features actually match the promised scope and quality target."
---

# Game Scope Completeness Audit

## Goal
Audit what the project is supposed to be, what it currently is, and where scope or completeness assumptions are misleading.

## Outputs

Follow the `gsp-orchestrator` output strategy:
- **inline** (default): present findings in conversation.
- **minimal** or **full**: write to `docs/game-studio/audit/audit-summary.md`, `docs/game-studio/audit/scorecard.json`, `docs/game-studio/audit/repair-roadmap.md`.

Use:
- `../../shared/checklists/scope-completeness-audit-checklist.md`
- `../../shared/reference/scope-tiers.md`
- `../../shared/reference/quality-targets.md`

## Evaluate
- claimed target vs actual target (`first-playable`, `polished-prototype`, `production-feature`, `live-patch`)
- must-have features complete vs partial vs placeholder
- surface-level completeness hiding missing loop closure
- scope creep and low-value complexity
- where to cut, where to finish, and where to stop pretending something is done

