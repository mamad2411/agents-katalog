---
name: phase-design
description: Phase A of the solution-design workflow: turn a broad idea or business/technical direction into candidate solutions using brainstorming, research, first-principles filtering, architecture evaluation, and PRD drafting.
origin: ECC automation-pack
---

# Phase Design

Use this skill when the user asks for `/phase-design`, solution design, product/technical concept design, brainstorming into a plan, or the first stage of a non-code solution workflow.

## Purpose

Turn an unclear direction into a small set of credible solution options.

## Workflow

1. Clarify the target user, outcome, constraints, and success criteria.
2. Brainstorm 3-5 candidate solutions.
3. Research market, prior art, competitors, or existing implementations when useful.
4. Filter with first-principles questions:
   - What is the core value?
   - What can be removed?
   - Which constraints are real?
   - Which dependencies should be bought, reused, or built?
5. Ask an architecture reviewer for feasibility when technical architecture matters.
6. Draft a PRD or design brief.
7. Save the design artifact in the project’s normal docs or planning location when appropriate.

## Output

Include:

- candidate solutions
- recommended solution
- assumptions
- architecture sketch
- PRD/design brief
- risks and validation plan

End with `PHASE_DESIGN_DONE` when the design artifact is ready.
