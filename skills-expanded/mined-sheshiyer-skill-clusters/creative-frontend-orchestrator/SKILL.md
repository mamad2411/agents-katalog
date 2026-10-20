---
name: creative-frontend-orchestrator
description: "Route a creative-frontend task to the correct spoke — in-browser animation (GSAP ScrollTrigger, Anime.js, web-motion-library) over an Astro substrate, or render-time programmatic video (Remotion). USE WHEN a user wants motion, animation, scroll effects, or video on the web but hasn't named the specific tool, or needs to decide between a live interactive effect and a rendered video file."
cluster: creative-frontend
version: 1.0.0
---

# Creative Frontend Orchestrator

The single entry skill for animated / motion / video frontend work. It answers the one
question that determines everything downstream — **live interactive effect, or rendered
video file?** — then delegates to the right spoke. Shared rules (decision matrix,
reduced-motion, performance budget, Astro hydration boundaries) live in
`creative-frontend-core`; consult it before implementing.

## Cluster map (routing targets)

- `creative-frontend-core` — shared reference: in-browser-vs-video decision matrix, `prefers-reduced-motion` baseline, GPU/performance budget, Astro hydration boundaries, version matrix, guardrails.
- `astro-framework` — the substrate: Astro components, islands/hydration, content collections, view transitions, SSR adapters, deployment.
- `astro-gsap-scrolltrigger` — scroll-driven motion in Astro: pin, scrub, parallax, reveal-on-scroll, with view-transition-safe init/cleanup and reduced-motion.
- `animejs` — timeline-based JS animation, SVG draw/morph, stagger grids, keyframes, tweening arbitrary JS objects.
- `web-motion-library` — pre-built hero/landing animations, 3D/WebGL elements, and React/Tailwind/Framer-Motion components to drop in.
- `remotion` — programmatic video in React (entry point for most video tasks).
- `remotion-best-practices` — Remotion conventions, gotchas, and rules to follow.
- `remotion-video-toolkit` — advanced Remotion: Lambda/Cloud Run/Node rendering, captions, 3D, charts, large component toolkit.

## Folded spokes

Additional spokes folded into this cluster. They sit alongside the motion/video spokes
above and are routable the same way — load on demand by reading their `SKILL.md`.

- `artifacts-builder` — scaffold + bundle elaborate multi-component HTML artifacts (React 18 + TypeScript + Vite + Tailwind + shadcn/ui), inlined to a single self-contained `bundle.html`. Use when the deliverable is a standalone interactive UI/app artifact (state, routing, shadcn components) rather than a page animation or rendered video.
- `web-perf` — audit and optimize page-load performance via Chrome DevTools MCP: Core Web Vitals (LCP/INP/CLS), render-blocking resources, network dependency chains, layout shifts, caching, and accessibility gaps. Use to profile, debug, or optimize site speed / Lighthouse scores — including verifying that a heavy animation or hero stays within the cluster's performance budget.

**Awwwards / award-worthy aesthetic** (`ihlamury/design-skills`) — premium FWA/Awwwards-grade frontend:
- `awwwards-animations` — professional React animation (GSAP `useGSAP`, Motion/Framer, Anime.js, Lenis): premium 60fps scroll, custom cursors, page transitions, text/reveal/magnetic/parallax, kinetic typography, generative/algorithmic art. The go-to for "make it award-worthy."
- `gsap-awwwards-website` — a worked GSAP scroll-landing reference (React 19 + Tailwind 4); use as a concrete example when building a polished GSAP product/landing page.
- `awwwards-landing-page` — designer-portfolio / agency landing with Locomotive Scroll + GSAP + Framer Motion; use for portfolio/agency smooth-scroll sites.
- `awwwards-ui-skills` — the Awwwards UI design system (light mode, Inter, 4px grid); use for the Awwwards visual aesthetic / design-system rules (cross-refs the `design` cluster).

## Routing Rules by Intent

**First, classify the deliverable** (full criteria in `creative-frontend-core` → decision matrix):

- Responds to user input (scroll / hover / click / drag) in real time, lives on a page → **in-browser**.
- Final artifact is a file (`.mp4` / `.webm` / `.gif`) to upload or embed, needs deterministic frame timing, audio sync, or N data-driven variants → **render-time → Remotion**.

**In-browser →**
- Scroll-linked (pin, scrub, parallax, reveal, horizontal scroll) → `astro-gsap-scrolltrigger`.
- Complex timeline, SVG morph/draw, staggered grids, tween JS values → `animejs`.
- Simple enter/state transition or micro-interaction → prefer CSS / Astro **View Transitions** (`astro-framework`) before reaching for a JS lib.
- "Give me a ready-made hero / 3D / WebGL / Framer-Motion component" → `web-motion-library`.
- "Make it **Awwwards/FWA-grade** — premium 60fps scroll, custom cursor, magnetic, page transitions, kinetic type, generative art" → `awwwards-animations` (pair with `astro-gsap-scrolltrigger` / `web-motion-library` as needed).
- Worked **GSAP product-landing** example (React 19 + Tailwind 4) → `gsap-awwwards-website`.
- **Designer portfolio / agency landing** with Locomotive smooth scroll → `awwwards-landing-page`.
- **Awwwards UI aesthetic / design system** (light, Inter, 4px grid) → `awwwards-ui-skills`.
- Build / hydrate / deploy the Astro site itself → `astro-framework`.

**Render-time (video) →**
- Most tasks → `remotion`; check `remotion-best-practices` for conventions.
- Cloud/Lambda rendering, captions, 3D, charts, data-driven batch → `remotion-video-toolkit`.

**Standalone artifact / perf audit →** (folded spokes)
- "Build a self-contained interactive UI/app artifact" (React + shadcn/ui, state/routing, bundle to one HTML file) → `artifacts-builder`.
- "Audit / profile / optimize page-load performance, Core Web Vitals, Lighthouse, or site speed" — or check a hero/animation against the perf budget → `web-perf`.

**Composition** (common): "Astro landing page with a scroll hero **and** an embedded promo
video" → `astro-framework` (substrate) + `astro-gsap-scrolltrigger` (hero) + `remotion`
(render the promo, then embed as `<video>`). Sequence substrate → in-browser → video.

## Standard Operating Flow

1. Classify the deliverable into one route (in-browser vs render-time), per `creative-frontend-core`.
2. Confirm the objective, target surface (page vs file), and any reduced-motion / a11y / brand constraints.
3. Pull the shared rules from `creative-frontend-core` (perf budget, hydration directive, reduced-motion gate).
4. Delegate to the spoke(s); for compositions, order substrate → interaction → video.
5. Return a concise summary: chosen route, spoke(s) used, hydration/render strategy, and the next action.

## Guardrails

See `creative-frontend-core` for the shared guardrails — animate compositor-only props
(`transform`/`opacity`), always gate non-essential motion behind `prefers-reduced-motion`,
re-init and clean up animations across Astro view transitions, and confirm scope before
heavy renders (Lambda/Cloud Run cost + time).

## Loading spokes on demand

To keep CLI startup context lean, this cluster's spokes are **not** separately registered as skills — only this orchestrator and its `*-core` are enumerated. When you route to a spoke named above, **load it on demand** by reading its file:

`~/.agents/skill-clusters/skills/<spoke-name>/SKILL.md`  (or `skills/<spoke-name>/SKILL.md` inside the skill-clusters repo).
