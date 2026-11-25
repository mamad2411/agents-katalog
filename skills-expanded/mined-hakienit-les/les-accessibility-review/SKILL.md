---
name: les-accessibility-review
description: Review a frontend journey for semantic, keyboard, focus, naming, contrast, responsive, and dynamic-status accessibility.
invocation: user
maturity: stable
route: accessibility
profile: frontend
bootstrap: skills/les-bootstrap/SKILL.md
loads: ["../les-bootstrap/SKILL.md","../../policies/workflows/review.md","../../profiles/frontend/rules/accessibility.md","../../profiles/frontend/rules/interaction-responsive.md","../../profiles/frontend/rules/browser-evidence.md","../../profiles/frontend/rules/frontend-verification.md"]
---

# Accessibility Review

## Invoke

Inherit `../les-bootstrap/SKILL.md` with the active frontend profile.

## Inputs

Affected UI journey, supported states, and rendered interface evidence.

## Procedure

1. Resolve the journey, rendered states, viewports, and evidence source. Done when: coverage and unavailable evidence are explicit.
2. Inspect semantic structure, names, keyboard, focus, contrast, target size, responsive behavior, and dynamic status. Done when: each applicable boundary is evidenced.
3. Report impact, severity, reproduction, and verification path. Done when: findings are actionable and read-only.

## Output

Accessibility findings or no-finding result with terminal status.

## Guardrails

Read-only unless a fix is separately requested; do not treat visual review as
keyboard, accessibility-tree, responsive, or browser proof.

## Verification

Each finding identifies user impact, location, evidence type, severity, and safe
next action. A no-finding result names the checks actually run.

Bootstrap LES and require the frontend profile. Inspect affected journeys with
semantic structure, keyboard-only operation, focus order, accessible names,
contrast, target size, responsive behavior, and status announcements. Output
severity-ordered findings with user impact, evidence type, and verification path.
Review stays read-only unless fixes are requested.
