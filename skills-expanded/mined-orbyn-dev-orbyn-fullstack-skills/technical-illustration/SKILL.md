---
name: technical-illustration
description: "Create or repair deterministic code-only motion films, music and lyric videos, character animation, 3D worlds and model-driven technical illustrations, with accessible interaction and inspected SVG, React, print or conditional WebGL/beta3D outputs."
---

# Model-driven technical illustrations

Use for an explanatory interactive figure, code-driven timed prototype, motion
film or music-led artwork/lyric video whose model controls what is drawn, moved,
read and exported. This owner constructs motion from an explicit sampled model.
Choose a physical metaphor only when it clarifies the idea; disclose where the
analogy stops.

## Build only from code

Every picture and movement comes from code written in the project: no generators, hosted
models, 3D or animation libraries, stock or downloaded assets, rigs, motion capture or
creative tools. Music videos use no album artwork unless the user asks for it, and an image that is
used must have its character animated, not just a moving camera. Treat a
missing asset as code to write. Read the [code-only rule](references/code-only.md) before
starting a video, and only the user can lift it for a named item.

## Check the route

Send these to their owners: ordinary app layout to UI design; social posters to social-preview; faux product UI, feature cards and cursor demos to product-illustration; architecture and stack diagrams to [stack-diagram](../stack-diagram/SKILL.md) (other simple flow diagrams to existing explanation methods); data-driven scientific plots to the project's plotting library; ordinary editing of existing video footage to the project media tools (this owner is not a general video editor).

Apply these contracts when the request matches ([route contracts](references/route-contracts.md)):

- Requested illustrated statecharts: architect's [art contract](../architect/references/illustrated-statecharts.md); architect retains state, guard, projection and verification ownership. Keep exact numbered paths and the plain/text fallback.
- Arbitrary code-authored layered compositions, sampled tracks, rational clocks, vector/audio/media adapters or conditional 3D/simulation/effects: the [code-driven motion contract](../orbyn-ui-design/examples/spatial-review/motion/README.md). Its Lottie input, Three.js profile and packaged adapters fall under the [code-only rule](references/code-only.md), so use them only when the user approves them.

## Set the boundary

Resolve the target, its instructions, artifact/output owner and allowed effects.
Shared methods stay in the outer library. Authorized drawing modules may be
packaged into the actual artifact; never install shared instructions into targets.
No browser bypass, publisher, auth edit, history capture or model call is implied.

## Build one coherent artifact

1. State the explanation, audience, inputs, meaningful states and smallest useful
   output. Define a pure model and labelled limits ([craft and model](references/craft-and-model.md)). Do not invent measured product behavior.
2. Make geometry, phase, caption, numeric readout and accessible description consume
   the same sampled state. Establish projection, actual drawn shape records,
   clipping, depth and attachments ([geometry and lines](references/geometry-and-lines.md)).
3. Define takeover, reversal, readiness, timing and cleanup ([motion and input](references/motion-and-input.md)). Keep usable controls and
   meaningful updates with reduced motion and without advanced rendering. For
   timed UI, explainers/data, 3D choreography or kinetic films, use
   [motion sequences](references/motion-sequences.md) (deterministic scenes, interruption, text/media and delivery qualification).
4. Select only the required delivery path: standalone SVG/HTML core;
   [React/accessibility](references/react-and-accessibility.md);
   [print](references/print.md); [WebGL](references/webgl.md); or documented
   [beta 3D](references/3d.md). Advanced paths are conditional, not defaults.
5. Run independent bad and legitimate controls; drive actual interaction and inspect
   the images ([capture and drive](references/capture-and-drive.md)).
   Fix the model/source before recapturing. A saved image or green banner is not
   proof of geometry, accessibility, complete input coverage or a real GPU path.
6. For MP4 delivery, use the original [motion-film exporter](../orbyn-ui-design/examples/spatial-review/motion-films.md) via the [film pipeline](references/film-pipeline.md): validated scene/beat spec, `check-code-only.py` before rendering, `flash-check.py` on the finished file (exit 1: fix the source, render again), the legibility check when it carries words or a logo, and `audio-bake.py` for audio-reactive or lyric frames.
7. Package the selected modules, artifact model/style/assets and reproducible checks
   ([dependencies and update](references/dependencies-and-update.md)). Preserve
   notices and original/adapted hashes. Deliver artifact, evidence and actual limits.

## Read when needed

- Full-length song, or any film over 120 seconds or 3,600 frames: [long-form streaming](../orbyn-ui-design/examples/spatial-review/motion-films.md#stream-a-full-length-film).
- WebGL framebuffers or `readPixels`: [full-screen pass orientation](references/fullscreen-pass-orientation.md).
- Flash result scope and action: [motion sequences](references/motion-sequences.md#check-flashing-on-the-rendered-file).
- Any video built from an image: [animate an image](references/animate-an-image.md) (fixed crop, slow drawn blinks); the character in it must move, and camera motion alone never counts.
- Music video, lyric video, anime-style or ambient background, full animation, motion graphics or visualizer: [video scenarios](references/video-scenarios.md) first.
- Measuring a reference's motion and proving a build matches it: [motion-match](../motion-match/SKILL.md).
- A style's motion and timing, such as hit-pulse, word-stack or kinetic-cut: [video styles](references/video-styles.md).
- Character, body movement, walk, face, hair or acting: [character animation](references/character-animation.md).
- Terrain, worlds, raymarching, cameras or a figure in 3D: [3D worlds](references/3d-worlds.md).
- Individually timed lyric typography with artwork performance: [lyric performance](references/lyric-performance.md) (representative preview, local puppeting limits, blink integrity).
- Logo, brand mark, intro, outro or end card: [logo and branding](references/logo-and-branding.md).
- Relighting, parallax or echoes on an animated image, only if the user approves OpenCV: [still to layers](references/still-to-layers.md).

## Bundled support and evidence limits

- Bundled support under `references/upstream/anatomy/` is a pinned, maintained MIT adaptation, not an upstream installation or active skill; read actual APIs before authoring a new model ([bundled support](references/dependencies-and-update.md#bundled-support-and-audit-limits)).
- Browser, React peers, PDF tools and GPU are conditional prerequisites, and OpenCV is one
  only when the user approves it; unavailable surfaces remain blocked. Core SVG does not qualify React, print, WebGL or beta 3D.
- Keep supported runtime/platform evidence separate from written methods and model behavior (the full configured audits are finite sampled checks).
- Existing TDD, UI, performance and publication policies own their general contracts.
