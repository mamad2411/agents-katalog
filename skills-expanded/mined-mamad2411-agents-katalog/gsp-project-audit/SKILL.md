---
name: gsp-project-audit
description: "Use when running a top-level audit of an existing game project before repair or major changes."
---

# Game Project Audit

## Goal
Audit an existing game project from multiple dimensions **before** making implementation changes.
Default to **read-only first**.

## Default modes
- `audit-only` — produce findings only
- `audit-and-plan` — produce findings and a repair roadmap
- `audit-and-patch` — audit first, then patch only approved high-value issues

## Outputs

Follow the `gsp-orchestrator` output strategy:
- **inline** (default): present all findings, scorecard, and repair directions in conversation. Do not create `docs/` files.
- **minimal**: write only `docs/game-studio/audit/audit-summary.md` for cross-session reference.
- **full**: create and maintain the audit summary, scorecard, UX findings, repair roadmap, and risk register files listed below.

Full output files (when strategy = full):
- `docs/game-studio/audit/audit-summary.md`
- `docs/game-studio/audit/scorecard.json`
- `docs/game-studio/audit/ux-findings.md`
- `docs/game-studio/audit/repair-roadmap.md`
- `docs/game-studio/audit/risk-register.md`

Use:
- `../../shared/templates/audit-summary.md`
- `../../shared/templates/audit-scorecard.md`
- `../../shared/templates/ux-findings.md`
- `../../shared/templates/repair-roadmap.md`
- `../../shared/templates/risk-register.md`
- `../../shared/checklists/project-audit-master-checklist.md`
- `../../shared/checklists/ui-ux-hard-rules.md`
- `../../shared/reference/audit-modes.md`
- `../../shared/reference/audit-confidence-and-evidence.md`

## Audit workflow
1. Assess project state and release risk with `gsp-project-state-assessment`.
2. Determine audit mode and focus dimensions.
3. Run the relevant sub-audits:
   - `gsp-ux-flow-audit`
   - `gsp-hud-readability-audit`
   - `gsp-feedback-audit`
   - `gsp-audio-feedback-audit`
   - `gsp-feel-audit`
   - `gsp-mechanics-systems-audit`
   - `gsp-scope-completeness-audit`
   - `gsp-production-readiness-audit`
   - `gsp-architecture-maintainability-audit`
   - `gsp-live-risk-audit` when the repo is shipped or high-risk
4. Consolidate findings with `gsp-audit-scorecard`.
5. If requested, create a prioritized fix plan with `gsp-repair-roadmap`.
6. Patch only after the audit report exists and the requested mode allows edits.

## Rules
- Never start by changing files when the request is clearly an audit.
- Distinguish between **confirmed issues** and **high-confidence inferred issues**.
- Always include evidence and confidence for important findings.
- Prefer game-native language over frontend jargon.
- Call out hard-rule violations when UI flow, HUD pressure, or input-focus conflicts are likely hurting the player experience.

## Stop condition
You are done when the project has a clear audit summary, a dimensional scorecard, a risk register, and a repair roadmap if requested.
