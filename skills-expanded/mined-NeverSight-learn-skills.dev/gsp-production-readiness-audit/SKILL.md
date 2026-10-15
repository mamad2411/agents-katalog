---
name: gsp-production-readiness-audit
description: "Use when auditing whether a game project meets production-grade standards for release or continued iteration."
---

# Game Production Readiness Audit

## Goal
Audit whether the codebase is ready for sustained development rather than only demo survival.

## Outputs

Follow the `gsp-orchestrator` output strategy:
- **inline** (default): present findings in conversation.
- **minimal** or **full**: write to `docs/game-studio/audit/audit-summary.md`, `docs/game-studio/audit/scorecard.json`, `docs/game-studio/audit/repair-roadmap.md`.

Use:
- `../../shared/checklists/production-readiness-audit-checklist.md`
- `../../shared/checklists/production-code-checklist.md`

## Evaluate
- code organization and ownership boundaries
- clarity of state and event flow
- dead prototypes vs durable systems
- naming and consistency
- whether future AI-driven changes will be easy or destabilizing

