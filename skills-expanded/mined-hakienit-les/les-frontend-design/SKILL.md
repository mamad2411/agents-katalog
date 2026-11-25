---
name: les-frontend-design
description: Define a coherent frontend design direction, component boundary, responsive layout, interaction model, and UI evidence contract before implementation.
invocation: model
maturity: stable
route: frontend-design
profile: frontend
bootstrap: skills/les-bootstrap/SKILL.md
loads: ["../les-bootstrap/SKILL.md","../../policies/workflows/task-lifecycle.md","../../policies/rules/architecture.md","../../policies/rules/definition-of-done.md","../../profiles/frontend/rules/component-design.md","../../profiles/frontend/rules/interaction-responsive.md","../../profiles/frontend/rules/visual-system.md","../../profiles/frontend/rules/ui-completeness.md","../../profiles/frontend/rules/accessibility.md","../../profiles/frontend/references/design-quality-bar.md"]
---

# Frontend Design

## Invoke

Bootstrap LES, require the frontend profile, and load the design rules before
choosing implementation details.

## Inputs

Product outcome, affected journey, project design decisions, supported viewports,
content/data states, and existing component seams.

## Procedure

1. Define the direction, review surface, user journey, information hierarchy, and state matrix. Done when: the direction is one sentence, the review medium is named, and loading, empty, success, error, disabled, retry, and permission states are named where applicable.
2. Choose semantic structure, component ownership, layout, responsive behavior, typography, color tokens, icons, and motion. Done when: decisions fit the project system, give the journey a focal hierarchy, and avoid speculative dependencies.
3. Define interaction and accessibility acceptance. Done when: keyboard, focus, names, contrast, touch targets, non-hover paths, reduced motion, and dynamic feedback have evidence owners.
4. Define implementation and verification boundaries. Done when: each design decision has a component owner, viewport coverage, proof type, and visual review step.

## Output

Frontend design contract with direction, review surface, journey/state matrix,
component boundaries, visual decisions, responsive/interaction rules,
accessibility conditions, and evidence plan.

## Guardrails

Do not select a framework or component library on behalf of the project. Do not
use visual polish to hide missing states, interaction feedback, or accessible
semantics. Do not add a design dependency without an acceptance need.

## Verification

Verify that design decisions use project tokens, clear the applicable quality bar,
preserve keyboard and responsive outcomes, cover applicable states, and distinguish
visual evidence from browser or accessibility evidence.
