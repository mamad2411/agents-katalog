---
name: motion-system
description: Routes web animation to the right engine on an Astro 7 plus Cloudflare site — native CSS scroll-driven animations for reveals, parallax, progress, and CSS-achievable animated gradient or background effects; GSAP with ScrollTrigger for scrubbed cinematic timelines, pinning, and sequencing; Motion only inside React islands that already exist. Also owns view transitions (the animateView and ClientRouter ladder, native cross-document as enhancement) and CSS hover micro-interactions. Use when building scroll, entrance, background, or cinematic motion, animating page navigation, choosing between native CSS and a JS library, loading GSAP or Motion under a strict hash-based CSP, or wiring prefers-reduced-motion. Trigger on add a scroll reveal, animate on scroll, animated gradient background, pinned cinematic section, view transitions between pages, hover effects, lazy-load GSAP, or respect reduced motion. Not for Lottie; for WebGL shader heroes use webgl-atmosfera, for a Rive moment use signature-anim.
---

# motion-system

> Pick the lightest animation engine that does the job on Astro 7 plus Cloudflare. Default to native CSS scroll-driven animations; escalate to GSAP only for scrub, pin, snap, or nested-timeline orchestration; reach for Motion only inside a React island that already exists. Honor prefers-reduced-motion on every engine and keep all motion JS off the critical path.

## TL;DR
- Three engines on a native-first ladder, chosen by job-fit, never by default: CSS scroll-driven (zero JS) for reveals and parallax; GSAP plus ScrollTrigger for cinematic scrub and pinning; Motion only inside an existing React island.
- CSS scroll-driven is production-viable but NOT Baseline (Chrome and Edge 115 plus, Safari 26 plus, Firefox behind a flag in stable — default-on in Nightly 156, watch stable around Oct 2026; ~85 percent global support). Always ship it behind an `@supports` guard with an accessible default state so unsupported browsers stay readable.
- CSP is safe for all three engines under Astro 7 hash-based CSP, with one rule: load engine scripts as bundled Astro scripts or hydrated islands, never `is:inline`. Runtime `element.style` writes by GSAP and Motion are exempt from style-src, so no unsafe-inline is needed.
- prefers-reduced-motion handling is gate-relevant, not optional, because sibling skill perf-ci-gates floors accessibility at 0.95. Wire it into every engine.
- Keep animation JS off the critical path. Budget about 45 KB gzipped for a GSAP plus ScrollTrigger page; Motion Mini is about 2.3 KB.

## When to use this document
Use when adding scroll, entrance, or cinematic motion to an Astro 7 site; animating page navigation or in-page state morphs (view transitions — see references/view-transitions.md); adding hover micro-interactions; deciding whether an effect needs JS at all; loading GSAP or Motion under a hash-based CSP; or wiring reduced-motion. Do not use for WebGL hero atmosphere (webgl-atmosfera), a bespoke Rive moment (signature-anim), or Lottie and video motion.

## The three engines

| Engine | Job | Cost |
|---|---|---|
| CSS scroll-driven | reveals, parallax, progress bars, sticky effects, staggered reveals, horizontal galleries | zero JS, zero CSP interaction |
| GSAP plus ScrollTrigger | scrubbed cross-element timelines, pin with content lock, snap to panels, nested orchestration, motion paths | about 45 KB gzipped, lazy-loaded |
| Motion (in island only) | imperative or declarative motion inside a React island that already exists | Mini useAnimate about 2.3 KB; full motion/react about 34 KB |

Selection is by technical merit. The site stack already names these three engines, so the skill encodes the how, not the choice. The escalation ladder, the exact capability boundary, and the when-each table live in references/motor-decision-matrix.md.

## Capability boundary CSS versus GSAP

Native CSS scroll-driven animations express reveals, scroll and view progress, parallax, sticky and progress bars, staggered reveals via animation-delay, and horizontal galleries. They run on the compositor thread, off the main thread.

Escalate to GSAP only when the effect needs one of these, which native CSS cannot express: scrubbed multi-element timing with one timeline driving many tweens; true pinning with content lock (ScrollTrigger pin plus scrub); snapping to panels; nested timeline orchestration with callbacks; or motion-path animation. Both can do reveals and parallax, so the rule is native CSS unless you need scrub, pin, snap, nested orchestration, or motion paths.

## Loading and CSP

Load every JS engine as a bundled Astro script (a script tag Astro processes) or a hydrated island. Astro hash-based CSP automatically hashes those, so they pass a strict script-src. An `is:inline` script is not processed or hashed and will be blocked under the strict policy. GSAP and Motion animate by writing per-property inline styles through CSSOM (element.style.transform), which is exempt from style-src, so no unsafe-inline or unsafe-hashes is needed; avoid bulk `el.style.cssText` and `setAttribute("style")` writes, which are governed. CSS scroll-driven is pure declarative CSS with zero CSP interaction. Full per-engine recipe in references/csp-and-reduced-motion.md.

## prefers-reduced-motion

Every engine must honor reduced-motion because perf-ci-gates floors accessibility at 0.95 (WCAG 2.3.3). CSS gates scroll-driven animations inside `@media (prefers-reduced-motion: no-preference)`; GSAP uses `gsap.matchMedia()` with a reduce condition; Motion uses the useReducedMotion hook or a MotionConfig wrapper. Recipes in references/csp-and-reduced-motion.md.

## Recipe

1. Reveals and parallax: author as CSS scroll-driven, wrapped in both `@supports (animation-timeline: view())` and `@media (prefers-reduced-motion: no-preference)`, with a visible final-state default so unsupported and reduce-motion users keep readable content. No JS. See references/css-scroll-driven.md.
2. Cinematic scrub or pin: GSAP plus ScrollTrigger. On a static page load it via a bundled Astro script; inside an existing island use the useGSAP hook. Register ScrollTrigger client-side, lazy-load on intersection or with client:visible, and gate with gsap.matchMedia. See references/gsap-astro.md.
3. In-island imperative sequence: Motion Mini useAnimate (2.3 KB, WAAPI, auto-cleanup). Reserve full motion/react for declarative component motion already justified by the island. See references/motion-islands.md.
4. CSP: bundled scripts or islands only, never is:inline. Do not add unsafe-inline for runtime style writes.
5. Budget: lazy-load all motion JS; reserve about 45 KB gzipped for a GSAP page in the perf-ci-gates budget.json and keep it off the critical path.

## View transitions (fourth surface — W4 extension)

Same-document morphs are Baseline (2025-10-14) and run through `animateView` from the already-pinned `motion` package or the raw API, with a hand-wired reduced-motion gate. Animated NAVIGATION goes through Astro's `<ClientRouter />` — not deprecated, and the only rung with automatic reduced-motion and a route announcer. Native cross-document `@view-transition` is progressive enhancement ONLY (not Baseline, no Firefox, no built-in a11y): if it ships, it ships inside a `prefers-reduced-motion: no-preference` media query. Full ladder, the a11y gap, and composition rules in references/view-transitions.md.

## Hover micro-interactions (W4 extension)

Plain CSS, never an engine: `transition` on the hovered property (transform/opacity/color — compositor-friendly ones), wrapped in `@media (hover: hover)` so touch devices are not left with sticky states, and inside the same reduced-motion gate as everything else when the effect moves (color-only hovers need no gate). Durations come from the token layer (astro-css-tokens' duration/easing tokens), not magic numbers. If a hover needs JS, it is not a micro-interaction — re-route it up the ladder.

## Gotchas
- Do not use the discrete `animation-trigger` property (scroll-triggered, not scroll-driven). It is Chrome and Edge only in mid-2026. Use the continuous `view()` timeline for reveals, or IntersectionObserver or GSAP for cross-browser discrete triggers.
- Firefox needs a non-zero animation-duration (convention 1ms) for scroll-driven animations to apply.
- GSAP and ScrollTrigger are client-only; never run them in .astro frontmatter or a React render body (server context throws document is not defined). Use useGSAP, a bundled script, or a dynamic import.
- GSAP is 100 percent free including ScrollTrigger and SplitText for commercial use since April 2025; the older claim that SplitText needs a Club membership is false.

## Limitations & Out-of-Scope
- Does NOT cover WebGL, Rive, Lottie, or video motion. (View transitions and hover micro-interactions joined this skill in W4 — the pre-W4 exclusion is superseded.)
- Does NOT design the specific animations of a given site; it encodes the engine-selection method and the integration, not the choreography.
- CSS scroll-driven Baseline status and the GSAP bundle weight move; re-verify the pins and the Firefox flag at author time. The exact ScrollTrigger gzip figure is a single-source estimate; confirm against a real compressed build.

## References
- [motor-decision-matrix.md](./references/motor-decision-matrix.md): the escalation ladder, the CSS-versus-GSAP boundary, and the when-each decision table.
- [css-scroll-driven.md](./references/css-scroll-driven.md): scroll() and view() timelines, the @supports fallback, the Firefox quirk, and the capability and limit list.
- [gsap-astro.md](./references/gsap-astro.md): loading via bundled script versus useGSAP island, SSR-safety, tree-shaking, lazy import, weight, and pin plus scrub.
- [motion-islands.md](./references/motion-islands.md): Motion Mini versus full, useAnimate, island hydration, and when to prefer it over GSAP.
- [csp-and-reduced-motion.md](./references/csp-and-reduced-motion.md): the ship-safe CSP recipe per engine and the prefers-reduced-motion recipe per engine.
