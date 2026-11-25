---
name: motion
description: Create and verify polished website motion from a normal website or app prompt. Use when the user tags Motion Debugger or asks for expressive animations, spatial scenes, scroll choreography or refined microinteractions. Includes runnable spring, scroll chapter, articulated colony, task handoff, elapsed task sequence, kinetic identity field and modal drawer recipes, then actual browser evidence.
---

# Build motion into the requested product

**Building or upgrading a whole page, landing page or site?** Follow the `premium-motion` skill first. It covers art direction, motion tokens, choreography, the motion kit and the required `motion-debugger critique` loop, where you look at the contact sheets and fix what you see. The recipes and evidence tools below are for specific interactions inside that page.

The user's ordinary design prompt remains the brief. Tagging this skill supplies concrete motion construction and verification; do not require the user to write a second animation specification. Read the project first, preserve its stack and primary journeys, and select a clear visual direction with `motion-design`. Use `motion-3d-ui` for spatial composition. A plugin tag alone does not prove the MCP server is connected.

For an existing design, use the constrained [transition authoring workflow](references/transition-authoring.md): freeze protected bytes, bind the user's actors, and compare at most three motion candidates with native event/frame evidence. The namespaced `$motion-debugger` entry is available when another animation kit supplies `/motion`.

Identify one main story the motion should communicate: agents assembling around a task, work changing hands, an explanation unfolding with scroll, or an interface responding to a decision. Create a few deliberate moments with clear start, transition, completion and interruption states. Avoid applying the same entrance animation to every section.

If browser access is available and the brief benefits from visual references, inspect official reference pages for composition and live behavior. Retain the URL and what was actually observed. Static images establish framing and materials; they do not establish timing or smoothness. Prefer references relevant to the user's requested identity. Do not invent a product launch or copy protected artwork into the app. Use original geometry and project assets.

## Choose concrete construction

Read [usage](references/usage.md) and only the recipes needed. When MCP tools are connected, `motion_recipe({})` lists the shipped catalog; `motion_recipe({id:"colony-scene"})` returns actual allowlisted code and usage. With no MCP tool, read the same files directly from this skill. Copy the modules into the project so builds do not depend on an absolute plugin installation path. Adapt their visual mappings to the page; do not copy a generic full-page layout.

| Moment | Recipe | Concrete use |
| --- | --- | --- |
| Existing design transitions | [bindings](recipes/transition-bindings.mjs) and [patterns](recipes/transition-patterns.mjs) | Persistent handoff, staged decomposition and drag release over the user's original DOM/SVG/Three objects. |
| Reversals and interruption | [spring](recipes/spring.mjs) | Preserve position and velocity across target changes. |
| Scroll narrative | [scroll-chapters](recipes/scroll-chapters.mjs) | Measured progress drives a sticky scene and three meaningful chapters. |
| Kinetic identity/editor | [kinetic-field](recipes/kinetic-field.mjs) | Distinct Pulse/Weave/Orbit formations with stable IDs and continuous multi-channel retargeting; author the product geometry and rendering. |
| Spatial colony hero | [colony-scene](recipes/colony-scene.mjs) | Real lit meshes with articulated legs; scouts form branching task queues. |
| Agents exchanging work | [task-handoff](recipes/task-handoff.mjs) | One persistent token moves between interactive worker cards and completes on arrival. |
| Scripted task lifecycle | [elapsed-sequence](recipes/elapsed-sequence.mjs) | Pause, resume, cancel and replay using elapsed time; hidden tabs suspend and reduced motion keeps meaningful phase poses. |
| Primary navigation/details | [drawer](recipes/drawer.mjs) | Native modal semantics, visible final state and reversible travel. |

The scene factory accepts the consumer's Three.js module and renderer. It does not install dependencies, create a WebGL context or require a CDN. Keep the actual product usable if spatial rendering is unavailable, including a readable task summary and functional controls. Supply pause/replay when motion repeats. Reduced motion must retain the final meaning and primary journeys.

## Inspect the delivered behavior

Use [evidence workflow](references/evidence.md) and `motion-build-inspect-repair`. First execute ordinary unforced primary input to positive result, with a bounded deadline and visible-error check. Then use the actual `motion_capture`, `motion_inspect`, `motion_frames`, and, after a repair, `motion_compare` tools on a trusted credential-free local page. Inspect the returned native frames. Preserve the explicit contracts between runs, including completion state. Fix functional breakage before polishing curves.

For canvas/3D, inspect timed frames for actual internal scene motion and record whole journeys. DOM rectangles do not measure animated legs, materials, occlusion or camera composition. Source annotations and scene counters are debugging context, not an independent smoothness verdict. Verify desktop and narrow composition, keyboard operation, reversal, replay, final state, pause and reduced motion. Report functional completion, visual review and temporal evidence separately. Missing or inadequate footage stays unverified.

Deliver the requested interface, its preview/source, the meaningful motion moments, exact captures and remaining limits. Do not call a handwritten recipe demonstration a blind agent benchmark or claim that a passing motion contract establishes visual quality.
