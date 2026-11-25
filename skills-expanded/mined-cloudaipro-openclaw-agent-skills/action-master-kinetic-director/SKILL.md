---
name: action-master-kinetic-director
description: Dynamic motion direction skill that converts action-heavy scene ideas into Traditional Chinese motion scripts and English video prompts for Runway, Kling, Luma, or Sora. Use when users request fight choreography, chase dynamics, flight motion, dance kinetics, or high-energy scene prompting.
---

# Action Master Kinetic Director

## Objective
Transform dynamic scene intent into choreography-aware scripts and tool-ready motion prompts.

## Trigger Rules
Use when motion design is the center of the request.

Positive cues:
- Fight choreography, chase scene, aerial pursuit.
- Dance kinetics, mechanical motion, impact rhythm.
- Prompt packs for motion-first video generation tools.

Do not use when:
- The request is static visual concepting only.
- The request is narrative treatment without kinetic focus.
- The request is ad strategy without choreography detail.

## Inputs
Required:
- Motion scenario description.
- Desired energy level and style direction.

Optional:
- Tool target (Runway, Kling, Luma, Sora).
- Shot duration constraints.
- Character and environment details.

## Output Schema
Return the universal envelope from `../shared/references/output-schemas.md`.

Artifacts order:
1. Dynamic script in Traditional Chinese.
2. English prompt pack for four video tools.
3. Motion safety and continuity checklist.

## Workflow
1. Classify kinetic style engine.
2. Build movement arc with tempo phases.
3. Convert arc into beat-based Chinese script.
4. Compile English prompt variants per target tool.
5. Ensure motion continuity and camera readability.
6. Return assumptions, risks, and next actions.

## Quality Bar
- Keep action geography readable.
- Keep tempo escalation intentional.
- Keep style language consistent.
- Keep prompts executable without extra guessing.

## Safety Rules
- Refuse gore-focused or harmful real-world violence instructions.
- Keep content stylized and non-instructional.
- Avoid tactical real-world harm guidance.

## Resources
- Domain framework: `references/domain.md`
- Envelope validator: `scripts/validate_output.py`
- Creative artifact validator: `scripts/validate_creative_artifacts.py`
