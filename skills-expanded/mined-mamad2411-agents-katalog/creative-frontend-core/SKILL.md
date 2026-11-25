---
name: creative-frontend-core
description: "Shared reference for the creative-frontend cluster: the in-browser-vs-video decision matrix, in-browser tool selection, prefers-reduced-motion baseline, GPU/performance budget, Astro hydration boundaries for animation, and version matrix. USE WHEN deciding how to implement web motion/animation/video, or for the cross-cutting rules every spoke (GSAP, Anime.js, web-motion-library, Remotion) shares."
cluster: creative-frontend
version: 1.0.0
---

# Creative Frontend Core

Shared rules for the `creative-frontend` cluster. The orchestrator and every spoke reference
this — it holds the cross-cutting decisions so nothing is duplicated or contradicted.

## 1. Decision matrix — in-browser vs render-time (video)

| Question | If YES |
|---|---|
| Does it respond to user input (scroll, hover, click, drag) in real time? | **in-browser** |
| Must the artifact be a file (`.mp4`/`.webm`/`.gif`) to upload/embed? | **Remotion** |
| Needs deterministic frame timing, audio sync, or pixel-perfect output? | **Remotion** |
| One-off hero/section effect on a live page? | **in-browser** |
| Needs N data-driven variants (per-user, per-product, per-locale)? | **Remotion** (programmatic) |
| Must work with JS disabled / degrade gracefully? | **in-browser** (CSS-first) or a pre-rendered video |

When both apply (interactive page that also ships a video), do both: build the page
in-browser, render the video with Remotion, embed it.

## 2. In-browser tool selection

| Need | Use | Spoke |
|---|---|---|
| Scroll-linked: pin, scrub, parallax, reveal, horizontal-scroll | GSAP ScrollTrigger | `astro-gsap-scrolltrigger` |
| Timeline/sequence, SVG draw & morph, stagger grids, tween JS objects | Anime.js | `animejs` |
| Simple enter/exit, state change, page-to-page morph | CSS transitions / Astro **View Transitions** | `astro-framework` |
| Drop-in hero / landing / 3D / WebGL / Framer-Motion component | Pre-built library | `web-motion-library` |

Reach for CSS / View Transitions **first**; escalate to GSAP/Anime.js only when the effect
needs scroll-linking, sequencing, or fine timeline control.

## 3. Reduced motion (non-negotiable a11y baseline)

Gate every non-essential animation behind reduced-motion and provide a static end-state:

- CSS: wrap motion in `@media (prefers-reduced-motion: no-preference) { … }`.
- GSAP: use `gsap.matchMedia()` with a `"(prefers-reduced-motion: reduce)"` branch that sets the final state instantly.
- Anime.js: check `window.matchMedia('(prefers-reduced-motion: reduce)').matches` and skip or jump to the end.
- Remotion: accept a `reducedMotion` prop / offer a still poster frame for embeds.

Essential motion (e.g., a loading spinner conveying state) may remain, but minimize it.

## 4. Performance budget

- **Animate compositor-only properties: `transform` and `opacity`.** Never animate layout
  properties (`width`, `height`, `top`, `left`, `margin`, `padding`) — they trigger layout/paint and thrash.
- Use `will-change` **sparingly** and remove it after the animation; permanent `will-change` wastes memory.
- Target 60fps (≈16ms/frame); keep per-frame JS under ~4ms. Profile with DevTools Performance + the FPS meter.
- Defer animation scripts off the critical path (see hydration below). Lazy-load heavy libs (GSAP plugins, three.js) only on routes that use them.

## 5. Astro hydration boundaries for animation

Where animation code runs matters as much as what it does:

- **Plain `<script>` in `.astro`** — bundled, runs once on initial load. Good for global GSAP
  init. **But** under View Transitions it does **not** re-run on client-side nav.
- **Framework island directive** — pick by position/urgency:
  - `client:load` — above-the-fold hero that must animate immediately.
  - `client:visible` — below-the-fold; animate when scrolled into view (best default for reveals).
  - `client:idle` — non-urgent ambient motion.
  - `client:only` — client-only libraries (some WebGL/three.js) that can't SSR.
- **View Transitions gotchas** (when `<ClientRouter />` is enabled):
  - Re-init scroll/timeline logic on `astro:page-load` (fires on first load **and** after each nav); call `ScrollTrigger.refresh()` after layout settles.
  - **Clean up** on `astro:before-swap` — kill ScrollTriggers/timelines to prevent duplicates and leaks.
  - Use `transition:persist` for elements whose animation state must survive navigation.

## 6. Version / install matrix

| Spoke | Install | Notes |
|---|---|---|
| GSAP | `gsap` (+ `gsap/ScrollTrigger`, registered via `gsap.registerPlugin`) | Free tier covers ScrollTrigger; SplitText et al. now free in recent versions. |
| Anime.js | `animejs` | v3 (`anime()`) vs v4 (new `createTimeline`/import API) differ — confirm version; the `animejs` spoke covers both. |
| Remotion | `remotion` + `@remotion/cli` (+ `@remotion/lambda` / `@remotion/cloudrun` for scaled renders) | Renders need a bundler step; Lambda/Cloud Run incur real cost+time — confirm scope first. |
| Astro | `astro` + integrations (`@astrojs/react` etc.); `<ClientRouter />` for view transitions | Match integration versions to the Astro major. |

## 7. Shared guardrails

- Compositor-only props (`transform`/`opacity`); no layout-animating.
- Always provide a reduced-motion path and a sensible static fallback.
- Re-init **and** clean up animations across Astro view transitions — no duplicate ScrollTriggers, no leaks.
- Don't ship `will-change` permanently.
- Confirm scope and expected cost/time before heavy Remotion renders (Lambda/Cloud Run).
- Prefer CSS/View Transitions before adding a JS animation dependency.
