---
name: mood-scrolling
description: Design and build cinematic, scroll-directed web experiences in which motion, imagery, 3D scenes, or layered layouts respond to reading progress. Use for immersive landing pages, product stories, visual essays, scrollytelling, scroll-scrubbed video or canvas sequences, and requests to turn a brand narrative into an interactive journey. Covers concept development, storyboarding, renderer selection, implementation, responsive performance, accessibility, and visual QA across plain HTML, React, Next.js, Vue, Svelte, and similar web stacks.
---

# Mood Scrolling

Create a directed visual journey, not an effect reel. Make each scroll interval advance one idea, preserve user control, and keep the page understandable when animation is unavailable.

## Operating principles

- Begin with the existing project and brand system. Preserve its framework, conventions, content, and working behavior unless the request says otherwise.
- Treat scroll as an input signal, never as a hijacked transport. Do not trap, reverse, or forcibly smooth the user's scroll.
- Build a coherent spatial or thematic journey. Give every transition a narrative reason.
- Keep real HTML for headings, copy, links, and controls. Canvas and video are atmosphere, not the only source of meaning.
- Design desktop and mobile compositions independently where needed; do not merely scale down desktop.
- Prefer the least complex renderer that delivers the intended illusion.
- Measure progress against a stable container and update visuals with `requestAnimationFrame`.
- Respect `prefers-reduced-motion`, keyboard navigation, focus visibility, readable contrast, and semantic order.
- Do not invent brand assets or product claims. Mark assumptions and placeholders clearly.

## 1. Inspect before inventing

Read the repository instructions, framework, routes, styles, assets, dependencies, and existing test commands. Preview the current page when possible. Identify constraints before installing packages or replacing structure.

If the brief is incomplete, infer a reversible first direction from available brand material. Ask only when a missing choice would materially change cost, content, or architecture.

## 2. Write the experience brief

Define these six items in a short working note:

1. **Audience and action** — who arrives and what they should understand or do.
2. **Mood sentence** — one sensory sentence, such as “quiet precision emerging from fog.”
3. **Visual grammar** — palette, type, material, lighting, camera behavior, and motion character.
4. **Journey nodes** — 3–7 ordered moments, each with one message and one visual state.
5. **Continuity device** — the element that persists or transforms across nodes: a line, object, horizon, color field, camera path, or typographic motif.
6. **Exit state** — the final stable composition and call to action.

For detailed planning, read [references/journey-design.md](references/journey-design.md).

## 3. Select a renderer deliberately

Choose the lowest-cost option that satisfies the brief:

| Mode | Best for | Main tradeoff |
| --- | --- | --- |
| DOM + CSS | Typography, layers, masks, editorial scenes | Limited depth and complex camera motion |
| Canvas / WebGL | Procedural worlds, particles, real-time 3D | Engineering and GPU cost |
| Image sequence | Art-directed camera moves with exact frame control | Many requests and large payloads |
| Scrubbed video | Cinematic generated or filmed motion | Seeking quirks and encoding work |
| Hybrid | HTML content over one atmospheric renderer | More synchronization and QA |

Use CSS/DOM first for simple parallax or reveals. Use video or sequences when the pixels must be predetermined. Use WebGL only when real-time viewpoint, lighting, or interaction materially improves the story.

Read [references/rendering-patterns.md](references/rendering-patterns.md) before implementing video, frame sequences, canvas, or WebGL.

## 4. Create a journey manifest

Express the experience as data before wiring animation. Copy [assets/journey-manifest.json](assets/journey-manifest.json) or adapt its schema. Each node must define:

- a stable `id`;
- a progress interval from `start` to `end`;
- a human-readable `message`;
- the intended `visual` state;
- optional asset references;
- an accessible static fallback.

Keep intervals ordered and non-overlapping. Small intentional gaps may hold a composition; document them. Validate a JSON manifest with:

```sh
node scripts/check-journey.mjs path/to/journey-manifest.json
```

## 5. Build in passes

### Pass A: static story

Implement the complete semantic page with no animation. Ensure content order, responsive layout, navigation, and CTA already work.

### Pass B: progress signal

Copy or adapt [assets/scroll-director.js](assets/scroll-director.js). Derive normalized progress from a named story container. Batch visual writes in one animation frame and expose progress through CSS custom properties or a small render callback.

### Pass C: visual states

Implement node-to-node interpolation. Prefer transforms and opacity. Avoid animating layout properties in hot paths. Keep text legible during transitions and use restrained motion easing; scroll-linked state should track the user closely rather than lag theatrically.

### Pass D: assets

Generate or source assets only after the visual grammar and aspect ratios are fixed. Keep provider-specific commands outside the core architecture. Record prompt, model/tool, dimensions, seed if available, and usage rights alongside generated assets.

### Pass E: fallback and polish

Create reduced-motion and failure states. Poster images, static compositions, or discrete crossfades are valid fallbacks. The CTA and essential copy must remain available even if media fails.

## 6. Enforce budgets

Set budgets before final asset production. Use [references/quality-gates.md](references/quality-gates.md) for the test matrix. At minimum:

- reserve media dimensions to prevent layout shift;
- lazy-load noncritical segments and preload only the opening state;
- pause rendering when the experience is outside the viewport or tab is hidden;
- cap device pixel ratio for expensive canvas scenes;
- avoid simultaneous decodes of many large videos;
- provide responsive assets and poster frames;
- verify touch scrolling remains native and smooth;
- test with reduced motion and throttled network/CPU.

Treat budgets as project-specific, not universal magic numbers. When no product budget exists, state a provisional one and measure against it.

## 7. Verify the experience

Run the repository's checks, then inspect at narrow mobile, wide desktop, and at least one intermediate width. Test the beginning, every boundary, fast scroll, reverse scroll, reload at mid-page, resize, background-tab return, missing media, keyboard navigation, and reduced motion.

Capture evidence when tools permit. Fix console errors, clipped text, blank frames, progress jumps, media seams, and inaccessible contrast before handoff.

Report what was built, the chosen renderer and why, where content/assets remain placeholders, performance or browser caveats, and the checks performed.

## Portability

Keep the instructions and implementation provider-neutral. Use tools available in the host agent; do not require a named model, image service, browser harness, package manager, or deployment platform. When a capability is missing, complete the static architecture and leave a precise asset or verification manifest for the next tool-enabled pass.
