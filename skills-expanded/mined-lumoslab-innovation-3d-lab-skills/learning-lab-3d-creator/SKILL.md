---
name: learning-lab-3d-creator
description: Build complete production-grade 3D educational labs and simulations. Use when creating or refactoring science/physics labs, KHTN8 lessons, experiment scenes, Three.js/Babylon scenes, agent-connected simulation flows, control panels, reports, quizzes, tutorial phases, or reusable lab architecture.
---

# Learning Lab 3D Creator

Ship a learning lab with scene, controls, state, agent events, and verification. Do not stop at a pretty canvas.

## First Pass

1. Inspect the target repo before coding: package scripts, existing simulation folders, shared scene helpers, chatbot/report/question components, and available deps.
2. Choose the local pattern:
   - For `services/frontend`, prefer imperative Three.js scene controllers for simulation folders unless the surrounding feature already uses R3F.
   - Use existing `three`, `@react-three/fiber`, `@react-three/drei`, `cannon-es`, and Babylon deps before adding anything.
   - Use primitives/parametric geometry for curriculum labs unless GLB adds real understanding.
3. Write the lab contract before implementation: lesson goal, variables with units, scene objects, interactions, feedback, reset behavior, and QA command.
4. Run `$science-model-director`, `$threejs-design-director`, then `$visual-lab-qa-agent` start pass before coding demo visuals. The visual QA start pass must create a prompt loop ledger for serious demos.

## Lab Structure

For learning-lab simulations, keep this split:

- `constants.ts`: IDs, units, physical constants, specimen/object data, formatters, answer checks.
- `setup<Name>Scene.ts`: Three.js scene lifecycle, model construction/loading, pointer interaction, animation, disposal.
- `<Name>ControlPanel.tsx`: sliders, toggles, step controls, formula/result display.
- `<Name>Lab.tsx`: React state, agent events, chatbot, phase popups, quiz/report integration.
- `scene-utils.ts`: disposal, shared geometry helpers, math helpers used by this lab only.
- `index.ts`: exports.

If an existing lab already uses a different split, follow it unless it is causing the bug.

## Creator Checklist

Build every lab with:

- A single primary phenomenon visible within 2 seconds.
- Units shown beside every numeric control.
- At least one manipulated variable and one measured/result variable.
- Reset, pause/play for time-based motion, and deterministic initial state.
- Loading and error states for external assets.
- Visual labels that do not block the object.
- Prompt/reference/fix loop evidence for serious visual demos: reference prompt or spec, role-gate verdicts, desktop/mobile screenshots, benchmark path, and final visual verdict.
- Cleanup for animation frames, event listeners, controls, renderers, materials, geometries, textures, and DOM overlays.
- Agent payloads that include `simulation_type`, `experiment_type`, `state_snapshot`, `metadata.contract_version`, and `client_ts` when the lab talks to the agent API.

## Design Bar

Make the scene feel like a premium learning instrument, not a toy pile:

- Use restrained background, floor/table, contact shadows, and 2-3 purposeful lights.
- Materials should communicate function: metal, glass, plastic, liquid, field lines, measurement overlays.
- Establish a focal hierarchy: one hero phenomenon, supporting apparatus, then labels/readouts.
- Use postprocessing only when it improves the phenomenon: bloom for energy/light, ambient occlusion/shadows for contact, tone mapping for polish.
- Include at least one high-quality visual cue for invisible forces: field lines, vector arrows, particles, heat map, ray path, or wavefront.
- Use camera limits that keep the learner near the experiment.
- Avoid oversized decorative panels; controls should be compact and scannable.
- Keep mobile usable: canvas visible, panels collapsible, no text overlapping the 3D viewport.

## References

- Read `references/engine-decision.md` before converting an existing 3D surface or choosing Three.js/R3F/Babylon.
- Read `references/project-stack.md` before project-specific work.
- Read `references/lab-contract.md` before adding a new lab.
- For model-heavy work, also use `$threejs-model-creator`.
- For physics-heavy work, also use `$threejs-physics-simulation`.
- For science/visual planning, also use `$science-model-director` and `$threejs-design-director`.
- Before finishing, use `$threejs-performance-qa`, `$visual-lab-qa-agent` end pass, then `$learning-lab-qa-pm-reviewer`.
