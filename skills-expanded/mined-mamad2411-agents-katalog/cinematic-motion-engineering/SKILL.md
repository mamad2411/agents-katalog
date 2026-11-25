---
name: cinematic-motion-engineering
description: >
  Use this skill when designing or implementing highly animated, immersive,
  and cinematic web user interfaces. Activated when the user asks to build
  animations, integrate GSAP, use ScrollTrigger, build Three.js R3F models,
  implement video-scrubbing, image mask scaling, modulo-based infinite
  sliders, bento grid lighting, or premium interactive web layouts.
  Do NOT use for standard, non-animated web interfaces or pure backend APIs.
---

# Cinematic Motion Engineering

## WHEN TO USE THIS
- Load when building high-end, immersive landing pages, portfolios, or interactive WebGL 3D showcase viewers.
- Load when mapping complex mousemove events, scroll-locked page segments, and dynamic staggers.
- Load when binding video frame playback to user scroll positions or handling mathematical circular slides.

## NEVER DO
- Never bind raw, compressed, standard-interval MP4s to high-precision scroll scrubbing (produces heavy jittering).
- Never allow three-dimensional Canvas elements to trap scroll events (always lock zoom in embedded views).
- Never stack homogeneous visual elements continuously; strictly alternate density to preserve dopaminergic pacing.
- Never write ad-hoc conditional wrapping logic for infinite sliders (always use clean modulo formulas).

## DOMAIN SECTION 1: VISUAL LAYOUTS & depth METAPHORS
- **Continuous Alignment Vectors (Power Lines):** Draw invisible vertical alignment grids spanning the entire scroll depth. Snap seemingly disconnected elements to these persistent axes to force subconscious layout consistency.
- **Icelandic Flag Structuring:** Offset the core UI (like hamburger menus) away from the mathematical center or absolute margins, deriving structural layout lines from intersecting cross-axes.
- **Unconventional Image Grids:** Fix grid column widths but apply variable `fit` heights to imagery. This breaks uniform rows and forces dynamic proportions.
- **Mosaic Balance:** Employ chaotic, layered arrangements bounded by immense anchoring typography and a strictly conventional sticky header to achieve orderly overwhelm.
- **Depth & Spatial Metaphors:**
  - Apply continuous 3D transforms tracking `mousemove` events uniformly across global site layouts.
  - Implement draggable, intersecting UI cards modeled on Desktop OS/Mac aesthetic window metaphors.
  - Pin massive, overlapping background typography beneath scrolling 3D product assets. Repeat critical occluded text elsewhere at functional sizes.
- **Bento Grid Illumination:** Upgrade standard bento grid cells with cursor-tracked HSL spotlight lighting to dynamically shift illumination coordinates and reveal underlying layered aesthetics on hover.
- **Timeline Morphology:** Pin static timeline prefixes (e.g., pinning the "19" in 1990) while exclusively scrolling the shifting suffix digits dynamically.
- **Alternating Dopamine Pacing:** Modulate scroll velocity by strictly alternating module density: cycle from text-only functional data, to full-bleed visual media, to massive purely ornamental typography.
- **Continuous Flow:** Mutate the URL state dynamically via Intersection Observers to create infinite scroll loops between distinct articles or case studies without click-throughs.

## DOMAIN SECTION 2: MOTION & TIMELINE ARCHITECTURE (GSAP)
- **React Architecture:** Always wrap animation logic inside the `@gsap/react` `useGSAP` hook for automated garbage collection. Pass state dependencies (e.g., `currentIndex`) into the hook's dependency array to recalculate and replay targeted timelines.
- **Tween Construction:** Instantiate state transitions using `gsap.to()` for targeting end-states, `gsap.from()` for entrance animations, or `gsap.fromTo()` for absolute state enforcement.
- **Physics Curves:** Apply exact GSAP easing strings per context:
  - `power1.inOut`: Default buttery, decelerating UI transitions.
  - `elastic.out`: High-tension, spring-like snapping interfaces.
  - `bounce.out`: Hard, gravity-based physical stopping bounds.
  - `back.inOut`: Emphasized overshoot/return for attention mapping.
- **Staggers & Grids:** Configure advanced staggering to cascade elements. Set `stagger: 0.06` for character waves. Define stagger grids with start parameters (e.g., `stagger: { grid: [14, 28], from: "center", amount: 1.5 }`) to ripple animations bidirectionally.
- **ScrollTrigger Constraints:** Bind animations directly to the viewport. Register the plugin at the root (`gsap.registerPlugin(ScrollTrigger)`). Apply `scrub: true` for 1:1 scroll-locking, or smooth interpolation via numerical configurations like `scrub: 1` or `scrub: 1.5`. Define strict intersection limits (e.g., `start: "top center"`, `end: "bottom top"`).
- **SplitText Typographic Motion:** Instantiate `new SplitText(target, {type: "chars, words, lines"})`. Target `.chars` to stagger individual glyphs upward via Y-transforms, `.words` for staccato block reveals, and `.lines` for paragraph cascading. Add timeline `delay: 1` to secondary lines to ensure primary headers resolve first.

## DOMAIN SECTION 3: CINEMATIC MULTIMEDIA & PHYSICS
- **Scroll-Scrubbed Video Frame Playback:** Bind HTML5 `<video>` element tracking explicitly to a pinned ScrollTrigger timeline. Disable autoplay and native looping. In the `onLoadedMetadata` callback, map `video.currentTime` to the total `video.duration` multiplied by the ScrollTrigger progress tracker.
- **FFmpeg GOP=1 Keyframe Encoding:** Never attempt to scrub highly-compressed streaming MP4s. Force raw frame-by-frame encoding (I-frames only) to prevent scroll skipping by compiling the video using the exact command:
  ```bash
  ffmpeg -i input.mp4 -g 1 -codec:v libx264 -crf 18 output.mp4
  ```
- **Mask Scaling Operations:** Embed SVGs as CSS `mask-image` definitions on absolute overlay elements. Using GSAP, scale the `mask-size` exponentially (e.g., `100%` to `400%`) while pinned, transforming a small shape cutout into a fully revealed full-bleed viewport.
- **Endless Modulo Remainder Carousel:** Execute infinite wrapping index loops (sliding arrays safely backwards and forwards) without nested conditionals using the zero-safe modulo remainder formula:
  ```javascript
  const getIndexAt = (offset) => {
    const len = array.length;
    const target = currentIndex + offset;
    return ((target % len) + len) % len;
  };
  ```

## DOMAIN SECTION 4: THREE.JS & REACT THREE FIBER (R3F) INTEGRATIONS
- **Perspective Camera & Controls:** Wrap scenes in the `<Canvas>` tag. Manually define `PerspectiveCamera` parameters (e.g., `fov={50}`, `near={0.1}`, `far={100}`) to flatten or exaggerate depth. Mount `OrbitControls` or `PresentationControls`. Force `enableZoom={false}` to preserve standard page scrolling, and clamp constraints via `polar` and `azimuth` angle arrays to restrict mesh rotation.
- **Zustand State Sync:** Sync 3D parameters outside the Canvas context utilizing a Zustand store (`set({ color, scale })`). Read store values inside R3F hooks, triggering `scene.traverse()` inside a `useEffect` bounded to the state slice. Execute `child.material.color = new THREE.Color(stateColor)` to repaint specific geometries instantly.
- **Color & Lighting Topology:** Render studio-grade setups using Drei's `<Environment>` nodes mixed with `<Lightformer>` arrays. Apply `colorSpace={THREE.SRGBColorSpace}` explicitly to screen textures to prevent gamma-washed renderings.
- **Video Texture Preloading & Mapping:** When painting `.mp4` files onto R3F materials, instantiate hidden DOM elements `document.createElement('video')` with `preload="auto"` and `playsInline` in a `useEffect` prior to render. Mount via Drei's `useVideoTexture(storePath)` hook and inject directly into the target child mesh as a `meshBasicMaterial map={texture}` child.

## OUTPUT SHAPE
When this skill is active, the AI response must generate raw, production-ready code (React, TSX, CSS) or architectural JSON files. The output will exclusively feature functional implementations of the requested visual pattern. It will omit installation guides and basic setup, returning pure logic: highly-optimized GSAP timelines, precise Math.PI calculations for 3D meshes, bound scroll-trigger directives, and modular React component structures mapped to the specified layout metaphors.

## NON-NEGOTIABLE CHECKLIST
1. Verify `@gsap/react` is in scope and timelines are destroyed on unmount via `useGSAP`.
2. Confirm the `((I % L) + L) % L` index formula replaces all boolean boundary checks in sliders.
3. Verify `<Canvas>` controls explicitly disable scroll zooming to prevent UX trapping.
4. Confirm video sources meant for scrubbing are processed with GOP=1 Keyframes.
5. Check that layouts possess alternating pacing density and avoid homogeneous block stacking.
6. Ensure Zustand stores handle cross-canvas DOM-to-WebGL synchronization.
