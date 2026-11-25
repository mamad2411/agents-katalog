---
name: les-frontend-verification
description: Verify completed frontend work across design, UI states, boundary data, supported viewports, accessibility, performance, and critical browser journeys.
invocation: model
maturity: stable
route: frontend-verification
profile: frontend
bootstrap: skills/les-bootstrap/SKILL.md
loads: ["../les-bootstrap/SKILL.md","../../policies/workflows/verification.md","../../profiles/frontend/rules/ui-completeness.md","../../profiles/frontend/rules/api-integration.md","../../profiles/frontend/rules/accessibility.md","../../profiles/frontend/rules/interaction-responsive.md","../../profiles/frontend/rules/performance.md","../../profiles/frontend/rules/browser-evidence.md","../../profiles/frontend/rules/frontend-verification.md","../../profiles/frontend/references/design-quality-bar.md","../../profiles/frontend/references/browser-review-protocol.md"]
---

# Frontend Verification

## Invoke

Inherit `../les-bootstrap/SKILL.md` with the active frontend profile.

## Inputs

Changed UI, relevant states, viewport support, and API boundary.

## Procedure

1. Map acceptance to direction, journeys, states, viewports, and boundary data. Done when: every applicable condition has a check and a review surface.
2. Check design quality, responsive interaction, keyboard/focus, accessibility, boundary, and performance conditions. Done when: evidence types remain separate and React/Next guidance is used only for matching projects.
3. Run the critical browser journey when the UI boundary requires it. Done when: action, viewport, console/network result, and observed result are recorded. If the journey cannot be reached, stop with `BLOCKED`.
4. Report residual uncertainty and terminal status. Done when: unavailable evidence is named and never converted into pass.

## Output

Frontend verification record with state/viewport matrix, evidence categories,
measurements, residual risk, and terminal status.

## Guardrails

Do not weaken universal rules or claim unavailable visual, keyboard, accessibility,
responsive, performance, or browser checks passed.

Use `BLOCKED` when a required browser journey cannot be safely reached or
verified, even when the owner can supply access. Use `SKIPPED` only when a
verification category does not apply to the change and the alternative evidence
is named. Mark unavailable checks `unavailable`; never mark them passed.

## Verification

Return focused UI evidence, exact commands or journey steps, measurements where
relevant, and the next safe action for failures.

Bootstrap LES and require the frontend profile. Map acceptance to design, state,
viewport, keyboard, boundary-data, performance, and browser checks that apply.
Output actual pass, fail, skipped, and unavailable evidence by category. Stop after
proof; do not implement new behavior under verification authority.
