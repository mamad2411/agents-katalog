---
name: ux-feasibility
description: "Determine whether a proposed UX can be implemented well on target platforms within stack, performance, accessibility and schedule constraints. Use when UX feasibility, mockup review, complex interaction."
license: MIT
compatibility: "Agent Skills compatible hosts; optimized for coding agents with repository and test/tool access."
metadata:
  category: "frontend"
  version: "0.1.0"
  maintainer: "SkillShop maintainers"
  maturity: "draft"
---

# Ux Feasibility

Determine whether a proposed UX can be implemented well on target platforms within stack, performance, accessibility and schedule constraints.

## Activate when

- UX feasibility
- mockup review
- complex interaction

## Focus

- Primary mission: Determine whether a proposed UX can be implemented well on target platforms within stack, performance, accessibility and schedule constraints.
- Use project/runtime evidence; this skill is a workflow, not a role-play persona.
- If another skill owns a deeper specialist concern, hand off instead of duplicating its entire workflow.

## Workflow

1. Describe the intended user interaction without assuming the mockup is implementable as drawn.
2. List target platforms/devices and required capabilities such as GPS, camera, NFC, background execution, maps, gestures, realtime updates or offline mode.
3. Map the interaction to backend, data, synchronization and permission requirements.
4. Identify performance risks such as huge lists, complex maps, WebGL/canvas, animation, video or aggressive polling.
5. Check touch, keyboard, accessibility, safe-area and responsive implications.
6. Prototype the highest-risk unknown rather than estimating the entire feature from vibes.
7. Return one of: feasible, feasible with changes, risky, or infeasible under current constraints, with a simpler alternative where appropriate.

## Deliverables

- User-task findings
- Reusable design/interaction fixes
- Device/accessibility/performance gaps
- A result that directly satisfies: Determine whether a proposed UX can be implemented well on target platforms within stack, performance, accessibility and schedule constraints.

## Common failure modes

- Designing only for a single desktop screenshot
- Adding tooltips to compensate for bad information architecture
- Gratuitous cards, pills, gradients, huge radii, or icon noise
- Hiding uncertainty instead of stating what was not inspected, reproduced, measured, or verified.

## Composition

Use `skill-router` when this task needs multiple specialties. Prefer composition over copying another skill's workflow into this one.

## Exit criteria

- The requested decision, change, test, or review is supported by concrete evidence.
- Important residual risks, limitations, and unknowns are explicit.
- The output is specific enough for another engineer or agent to act on without reconstructing hidden reasoning.
