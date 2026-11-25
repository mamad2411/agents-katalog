---
name: gsp-architecture-maintainability-audit
description: "Use when auditing structure, boundaries, coupling, or state-management risks in an existing game project."
---

# Game Architecture Maintainability Audit

## Goal
Audit technical structure and changeability, especially where future iteration will become painful.

## Outputs

Follow the `gsp-orchestrator` output strategy:
- **inline** (default): present findings in conversation.
- **minimal** or **full**: write to `docs/game-studio/audit/audit-summary.md`, `docs/game-studio/audit/scorecard.json`, `docs/game-studio/audit/risk-register.md`.

Use:
- `../../shared/checklists/architecture-maintainability-audit-checklist.md`
- `../../shared/reference/game-dev-abstractions.md`

## Evaluate
- state management clarity
- coupling between UI, gameplay, systems, and content
- module boundaries and change surfaces
- hidden complexity and implicit contracts
- where future AI edits are likely to rot the codebase

