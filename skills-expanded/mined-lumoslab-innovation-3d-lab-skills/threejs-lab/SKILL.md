---
name: threejs-lab
description: Router and baseline workflow for Three.js lab work. Use when the user asks for any web 3D lab, learning simulation, model viewer, Three.js scene, GLB/GLTF asset flow, physics demo, canvas bug, visual QA, or performance pass and a more specific plugin skill may apply.
---

# Three.js Lab

## Route First

Load the most specific skill before building:

- Prompt/image to a model with human option selection or Blender MCP: use `$threejs-studio` first. Its image approval gate takes precedence; the educational workflow below applies only if the requested asset is a learning lab.
- Advanced procedural graphics: use `$threejs-skill-router` and load only the relevant expert references.
- Product lab, curriculum scene, agent-connected simulation, or reusable 3D lesson: use `$learning-lab-3d-creator`.
- Science concept, variable mapping, causal logic, or visual necessity: use `$science-model-director`.
- 3D morphology, object necessity, reference interpretation, and composition logic: use `$threejs-design-director`.
- Art direction, reference likeness, visual taste, material polish, or toy-like/crude 3D: use `$threejs-art-director`.
- Visual quality, fancy demo acceptance, image-reference direction, chemistry/biology beauty/detail complaints, or before/after screenshot comparison: use `$visual-lab-qa-agent`.
- 3D model, procedural object, materials, GLB/GLTF, texture, articulation, or asset optimization: use `$threejs-model-creator`.
- Physics, force, collision, rigid body, particle, fluid-like, field, motion, numerical simulation, or calibration: use `$threejs-physics-simulation`.
- Blank canvas, slow scene, WebGL budget, responsive framing, screenshot QA, or release verification: use `$threejs-performance-qa`.
- Strict product/QA gate before claiming done: use `$learning-lab-qa-pm-reviewer`.

## Workflow

1. Define the lab surface first: learning goal, one primary 3D scene, 1-3 controls, visible measurement/output, reset, and pause/play when motion matters.
2. Run `$science-model-director` to map controls -> visible changes -> measured outputs.
3. Run `$threejs-design-director` to decide real 3D objects versus annotations and morphology anchors.
4. Run `$threejs-art-director` to check reference likeness, material polish, composition, and non-toy aesthetics.
5. For demo/lab creation, run `$visual-lab-qa-agent` start pass before implementation to set the visual target and start a prompt loop ledger.
6. Inspect the project: package scripts, installed 3D deps, existing canvas/components/assets, route/layout conventions, and current build/test commands.
7. Pick the smallest renderer path that fits:
   - Use existing React Three Fiber if already installed and used.
   - Use imperative Three.js for a single embedded canvas or a non-React page.
   - Do not add physics, postprocessing, state, or control libraries unless the lab requires them.
8. Build with stable scene lifecycle: camera, renderer/canvas sizing, lights, objects/models, controls, animation loop, resize handling, and cleanup.
9. Add real lab controls: variables, units, measured output, reset, and a short result readout.
10. Verify in browser, then run `$visual-lab-qa-agent` end pass. A Three.js lab is not done until the canvas is nonblank, framed correctly, responsive, interactive, visually accepted, and the prompt/reference/fix loop is recorded.

## Must-Haves

- Clamp pixel ratio with `Math.min(window.devicePixelRatio, 2)`.
- Handle resize by updating renderer size, camera aspect/projection, and composer size if postprocessing exists.
- Use `requestAnimationFrame`, `renderer.setAnimationLoop`, or R3F `useFrame`; update `Clock`-based deltas for animation mixers.
- Use the import style already present in the project. For fresh Three.js code, prefer `three/addons/...`; keep local consistency unless modernizing a whole surface.
- Use `MeshStandardMaterial`/`MeshPhysicalMaterial` with lights or environment maps for realistic labs; use `MeshBasicMaterial` only for unlit UI/debug visuals.
- Load GLB/GLTF assets from the app's public/static path; add loading and error states.
- Reuse/dispose geometries, materials, textures, controls, renderers, and event listeners on unmount.
- Use `InstancedMesh` or merged geometry for many repeated objects.
- For physics/science labs, expose calibration constants when approximations or real-world drift matter.

## References

Read only what the task needs:

- `references/threejs-patterns.md`: API patterns for scene setup, assets, interaction, animation, shaders, postprocessing, and R3F.
- `references/lab-qa.md`: browser/build QA checklist and blank-canvas triage.
- `references/sources.md`: source repos reviewed while creating this skill.

## Script

Run the lightweight static check after editing Three.js files:

```bash
node <skill-dir>/scripts/check-threejs-lab.mjs <changed-file.tsx> [more files]
```

The script catches missing render loops, resize handling, common asset-loading omissions, and similar failures. It is not a replacement for a browser screenshot.
