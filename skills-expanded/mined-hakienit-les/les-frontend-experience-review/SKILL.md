---
name: les-frontend-experience-review
description: Review a frontend journey for visual hierarchy, interaction feedback, responsive behavior, state completeness, and user-facing coherence.
invocation: user
maturity: stable
route: frontend-experience
profile: frontend
bootstrap: skills/les-bootstrap/SKILL.md
loads: ["../les-bootstrap/SKILL.md","../../policies/workflows/review.md","../../profiles/frontend/rules/visual-system.md","../../profiles/frontend/rules/interaction-responsive.md","../../profiles/frontend/rules/ui-completeness.md","../../profiles/frontend/rules/browser-evidence.md","../../profiles/frontend/references/design-quality-bar.md","../../profiles/frontend/references/browser-review-protocol.md"]
---

# Frontend Experience Review

## Invoke

Bootstrap LES and require the frontend profile. Review the named journey or
working-tree change without modifying implementation.

## Inputs

Journey objective, affected states, viewport evidence, rendered UI, project visual
decisions, and any available browser or interaction trace.

## Procedure

1. Resolve the review identity, URL, environment, and journey. Done when: base, dirty paths, safe target, viewport, and evidence source are recorded.
2. Walk the affected journey at applicable 375px, 768px, and 1440px surfaces, including loading, empty, success, error, retry, disabled, permission, focus, and keyboard paths. Done when: each applicable experience boundary has a result.
3. Inspect hierarchy, typography, color, spacing, icons, forms, navigation, states, touch behavior, responsive layout, motion, console, and network. Done when: user-visible and runtime evidence are separated and each applicable risk has a result.
4. Report findings by severity and evidence type. Done when: each finding has location, user impact, reproduction, safe next action, and any approved or skipped mutation.

## Output

Browser-backed experience findings or an evidence-qualified no-finding report,
including unavailable browser lanes when the target cannot be safely reached.

## Guardrails

Read-only. Do not substitute personal taste for product intent or project design
decisions. A screenshot alone cannot prove interaction, accessibility, or browser
behavior.

## Verification

Record the evidence actually inspected, skipped categories, unavailable browser
checks, and terminal status.
