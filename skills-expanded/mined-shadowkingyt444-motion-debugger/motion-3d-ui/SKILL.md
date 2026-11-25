---
name: motion-3d-ui
description: Build original cinematic, video-like or interactive 3D web UI with deliberate renderer selection, procedural geometry, lighting, camera and input design, responsive fallbacks and real motion verification. Use for spatial product scenes, articulated characters and immersive interface visuals, not static presentation graphics.
---

# Make a spatial interface, not a rotating placeholder

Start with the user's visual goal and the existing stack. A scene should explain or embody the product, and its controls should remain ordinary usable UI. Read `motion-design` when the surrounding page also needs art direction.

## Choose the renderer honestly

- CSS transforms: perspective cards, layered panels and light 2.5D object motion; minimal cost, normal DOM semantics
- SVG: articulated flat characters, diagrams and stylized depth where a fixed viewpoint is enough; original paths and layered shapes work well
- Canvas 2D: many lightweight particles or drawn effects when no real spatial camera is needed
- Three.js/WebGL: actual mesh depth, occlusion, spatial lights, camera movement or orbitable objects. If the brief explicitly asks for real 3D, implement real geometry instead of claiming an SVG gradient is a 3D renderer

Use an installed renderer first. Add a dependency only when its capability earns its cost. In React, isolate the scene in a mounted leaf; do not recreate the renderer on every state change. Use the installed library's API, not a guessed version. Keep model/font/texture imports local or same-origin for credential-free captures.

## Art-direct the stage

Choose a camera, a silhouette and a small material palette before adding detail. Block out original forms with primitives, extrusion or procedural curves, then judge them in the actual camera. A convincing character needs proportion, a readable pose and joint hierarchy; a product needs recognizable volume and contact with its support. Avoid a pile of unrelated spinning primitives.

Compose foreground, subject and backdrop with useful negative space for the interface. Use a controlled key light, softer fill and optional rim when the silhouette needs separation. Roughness, metalness and light size should explain the material; blasting ambient light makes depth disappear. Ground the subject with a restrained contact shadow or a low-cost shadow proxy. Postprocessing is optional, not a substitute for composition.

Choose an orthographic camera for graphic/product clarity, perspective for spatial scale. Define the important view and safe camera range. Orbit controls are appropriate for object inspection; automatic camera travel needs a pause/replay path and cannot hide the main action. Check occlusion and near-plane clipping in every intended pose.

## Design a motion sequence

Give the motion a beginning, a useful transformation and a settled pose. Layer primary movement with smaller anticipation/follow-through so the scene reads as articulated rather than one rigid wrapper. Separate intentional motion from input response; two controllers must not fight over the same transform.

Use one time source and a stable scene graph. Store continuous simulation values in refs, mutable scene objects or the renderer's motion facilities rather than rerendering the entire UI every frame. Consider position and velocity when an interaction retargets unfinished motion. Inspect the result rather than assuming a spring setting guarantees continuity.

Pointer input should map to a bounded scene-local intent. Keyboard/buttons must expose the same action, including pause, replay and reset where relevant. Avoid a separate “test animation” that exercises different state logic. Motion Debugger's recipe supports click, hover, key, pointer move, bounded vertical wheel scroll and bounded wait; it does not currently synthesize drag-button gestures. Use an equivalent production control or a separate authorized browser test for those interactions, and name the distinction.

## Keep it usable and affordable

Size the canvas from its container; update camera projection on resize. Choose one pixel-ratio strategy so size is not multiplied twice. Cap pixel density and geometry detail for the actual device budget; profile before adding multisampled shadows, bloom or large textures. Reuse materials/geometries or instance repeated objects. Track frame cadence and renderer resource counts rather than declaring “60 fps” from animation duration.

Pause unnecessary rendering when hidden/offscreen. Bound catch-up after a long suspended frame. Reduced-motion mode should retain a useful composed pose and functional controls, with nonessential camera travel and loops removed. Provide a readable DOM label/description and accessible controls outside the canvas, plus a meaningful non-WebGL fallback. Do not make the canvas a keyboard trap.

On unmount, stop the animation loop and remove listeners/observers. Dispose resources this component owns: geometries, materials, textures, render targets, controls and renderer. Shared assets need one owner; removing a mesh alone does not free GPU allocations. Confirm repeated mounting/resetting does not steadily grow renderer resources. [Three.js disposal](https://threejs.org/manual/pages/how-to-dispose-of-objects.html) and [responsive sizing](https://threejs.org/manual/pages/responsive.html) are the primary references.

## Verify what actually moved

Record replay and rapid retargeting, inspect intermediate recorded frames, and compare a repair through `motion-build-inspect-repair`. A fixed canvas element can pass DOM position contracts while an internal mesh jumps. DOM geometry metrics describe the selected DOM element, not mesh motion, occlusion or lighting.

For 3D, inspect actual video-derived images and scene state. Optional projected landmark probes or `motion:mark` events can help locate a window, but label them app annotations and cross-check them against the recording. Never present a stationary canvas rectangle as proof that the 3D animation is smooth. Review the narrow viewport and reduced-motion behavior as separate variants with their own expectations.
