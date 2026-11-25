---
name: scroll-storytelling
description: Plan and build scroll-driven narrative pages — pinned chapters, scrubbed sequences, progressive reveals, horizontal sections, image-sequence or 3D camera moves tied to scroll. Use for product launches, case studies, portfolios, "Apple-style" scroll pages, or when the user says scrollytelling, scroll story, pinned section, or scroll-driven animation.
---

# Scroll Storytelling

Written for this agent-kit. Pair with: `gsap-scrolltrigger` (implementation details), `lenis-smooth-scroll` (feel), `motion-framer` (React micro-motion), `threejs-webgl` / `react-three-fiber` (3D chapters), `gsap-performance`.

## 1. Story before code

Write a beat sheet first and show it to the user if the page is large:

| # | Chapter | Message (one sentence) | Visual | Scroll behaviour | Length |
|---|---|---|---|---|---|
| 1 | Hook | What it is | Hero visual | Static + subtle parallax | 100vh |
| 2 | Problem | Why it matters | ... | Pin + scrub text reveal | +150vh |
| 3 | ... | | | | |

Rules:
- One idea per chapter. If a chapter needs two messages, split it.
- Every pinned/scrubbed chapter must earn its scroll length. Default budget: at most 2–3 pinned chapters per page, each ≤ 200vh of extra scroll.
- The CTA must be reachable without scrolling through every animation (nav link or visible button in hero).

## 2. Pick the right tool

| Need | Use |
|---|---|
| Fade/slide in once when visible | CSS + IntersectionObserver, or Motion `whileInView` — no ScrollTrigger needed |
| Progress tied to scroll (scrub), pinning, snapping | GSAP ScrollTrigger |
| Simple progress in React | Motion `useScroll` + `useTransform` |
| Modern CSS-only progress bars / reveals | CSS scroll-driven animations (`animation-timeline: view()`/`scroll()`) with a static fallback — check support first |
| 3D camera moves on scroll | ScrollTrigger scrub → update camera in the render loop (or drei `ScrollControls` in R3F) |
| Frame-by-frame product spin | Image sequence drawn to `<canvas>` (preload, WebP/AVIF, ≤ ~120 frames, lower count on mobile) |

## 3. Implementation rules

- Register plugins once: `gsap.registerPlugin(ScrollTrigger)`. In React use `useGSAP()` from `@gsap/react` with a `scope` ref so everything is reverted on unmount.
- Build a timeline per chapter; attach ONE ScrollTrigger to the timeline, not one per tween.
- `scrub: true` or a small number (`0.5`–`1`) for smoothing. Use `pin: true` on the chapter wrapper, never on an element whose parent is transformed.
- Create ScrollTriggers top-to-bottom in page order (or set `refreshPriority`), and call `ScrollTrigger.refresh()` after fonts/images that change layout load.
- Animate only `transform` and `opacity` (and `clip-path` sparingly). Never animate `top/left/width/height` on scroll.
- Horizontal section: pin the wrapper, translate the track by `-(track.scrollWidth - window.innerWidth)`, and use `containerAnimation` for triggers inside it.
- Use `gsap.matchMedia()` to give mobile a shorter, simpler version (often no pinning) and to honour `(prefers-reduced-motion: reduce)` with instant, non-scrubbed states.
- Remove `markers: true` before finishing.

## 4. Must-pass checks

- [ ] Content is readable and in logical order with JS disabled or animations off (no text stuck at `opacity: 0`).
- [ ] Reduced motion: no scrubbing/parallax, content shown immediately.
- [ ] Mobile: address-bar resize doesn't cause jumps (`ScrollTrigger.config({ ignoreMobileResize: true })` if needed); pins feel OK on touch.
- [ ] 60fps on a mid-range laptop; no layout shift while pinning (reserve height).
- [ ] Deep-linking to an anchor mid-story lands in the right state.
- [ ] Headings stay semantic (`h1` → `h2` per chapter) — the story must make sense to a screen reader.
