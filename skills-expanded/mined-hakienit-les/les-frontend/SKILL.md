---
name: les-frontend
description: Route frontend work through the FE-first LES contract for design, component structure, state, integrations, accessibility, responsive interaction, performance, experience, and verification.
invocation: model
maturity: stable
route: frontend-ui
profile: frontend
bootstrap: skills/les-bootstrap/SKILL.md
loads: ["../les-bootstrap/SKILL.md","../../profiles/frontend/rules/component-design.md","../../profiles/frontend/rules/state-management.md","../../profiles/frontend/rules/ui-completeness.md","../../profiles/frontend/rules/api-integration.md","../../profiles/frontend/rules/accessibility.md","../../profiles/frontend/rules/interaction-responsive.md","../../profiles/frontend/rules/visual-system.md","../../profiles/frontend/rules/performance.md","../../profiles/frontend/rules/browser-evidence.md","../../profiles/frontend/rules/frontend-verification.md"]
---

# Frontend Router

## Invoke

Inherit `../les-bootstrap/SKILL.md` only when the frontend profile activates.

## Inputs

UI task, affected journey, active profile triggers, and project conventions.

## Procedure

1. Confirm profile activation, user journey, affected states, and relevant touchpoints. Done when: backend-only work is excluded and the UI boundary is named.
2. Load only relevant frontend rules and specialist skills. Done when: accessibility, interaction, and verification remain active for every UI change.
3. Define design, state, viewport, keyboard, performance, and browser evidence. Done when: each acceptance condition has an owner and proof type.
4. Route implementation and verification. Done when: the primary skill, specialist skills, and fallback are recorded.

## Output

Frontend route plan with activated rules, specialist ownership, state/viewport matrix,
evidence categories, and verification path.

## Guardrails

Do not choose framework, design tool, or component library for the project. Do not
let visual inspection replace keyboard, accessibility, responsive, or browser proof.

## Verification

Report profile activation, selected specialist skills, all skipped irrelevant rules,
and unavailable evidence separately from passed evidence.

First run `../les-bootstrap/SKILL.md`. Load only activated files from
`../../profiles/frontend/rules/`: component design and state for UI structure;
visual system and interaction-responsive for design and interaction; completeness
and API integration for journeys; accessibility for every interface change;
performance for measured cost or responsiveness; browser evidence for rendered
boundaries; frontend verification before completion. Project ADRs own framework
and library choices.
