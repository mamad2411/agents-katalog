---
name: lenis-smooth-scroll
description: Add or fix Lenis smooth scrolling (darkroomengineering/lenis) in vanilla HTML, React/Next.js, or alongside GSAP ScrollTrigger / Motion. Use when the user asks for smooth scroll, buttery/inertia scrolling, "lenis", or when scroll-driven animations stutter because native scroll and the animation loop are out of sync.
---

# Lenis Smooth Scroll

Written for this agent-kit and checked against the official Lenis README (lenis v1.3.x, Sep 2026). Package name is `lenis` — the old `@studio-freight/lenis` package is legacy, never install it.

## Decide first

- Smooth scroll is a taste choice, not a default. Use it on marketing/portfolio/storytelling pages. Skip it for dashboards, docs, forms-heavy apps, and anything with lots of nested scroll areas.
- Only ONE scroll owner per page. Do not combine Lenis with Locomotive Scroll, GSAP ScrollSmoother, or another smooth-scroll lib.
- Lenis keeps native scroll (`window.scrollY` is real), so `position: sticky`, IntersectionObserver and ScrollTrigger keep working.

## Install

```bash
npm i lenis
```

Always load the recommended CSS (needed for `autoToggle`, stopping, and iframes):

```js
import 'lenis/dist/lenis.css'
```

## Vanilla / plain HTML

```html
<link rel="stylesheet" href="https://unpkg.com/lenis@1.3.26/dist/lenis.css">
<script src="https://unpkg.com/lenis@1.3.26/dist/lenis.min.js"></script>
<script>
  const lenis = new Lenis({ autoRaf: true, anchors: true })
</script>
```

## React / Next.js (App Router)

Put this in a client component mounted once near the root (e.g. `app/providers.tsx`, marked `'use client'`):

```tsx
'use client'
import { ReactLenis } from 'lenis/react'
import 'lenis/dist/lenis.css'

export function SmoothScroll({ children }: { children: React.ReactNode }) {
  return (
    <>
      <ReactLenis root options={{ anchors: true }} />
      {children}
    </>
  )
}
```

Read the instance anywhere with `useLenis((lenis) => { /* runs on every scroll */ })`.

## With GSAP ScrollTrigger (one clock, no jitter)

Vanilla:

```js
const lenis = new Lenis()               // autoRaf defaults to false
lenis.on('scroll', ScrollTrigger.update)
gsap.ticker.add((time) => lenis.raf(time * 1000)) // GSAP time is seconds, Lenis wants ms
gsap.ticker.lagSmoothing(0)
```

React:

```tsx
import gsap from 'gsap'
import { ReactLenis, type LenisRef } from 'lenis/react'
import { useEffect, useRef } from 'react'

const lenisRef = useRef<LenisRef>(null)
useEffect(() => {
  const update = (time: number) => lenisRef.current?.lenis?.raf(time * 1000)
  gsap.ticker.add(update)
  return () => gsap.ticker.remove(update)
}, [])
return <ReactLenis root options={{ autoRaf: false }} ref={lenisRef} />
```

With Motion: drive `lenis.raf` from Motion's `frame.update(cb, true)` and clean up with `cancelFrame(cb)` (import from `"motion/react"`), again with `autoRaf: false`.

## Options that matter

| Option | Use |
|---|---|
| `lerp` (default 0.1) | Smoothness. 0.08–0.12 feels premium. Lower = floatier. Overrides `duration`/`easing`. |
| `autoRaf` | `true` for standalone. `false` when GSAP/Motion drives the loop. |
| `anchors: true` | Smooth `#hash` links. Pass `{ offset: -80 }` for a fixed header. |
| `allowNestedScroll` | Easy nested-scroll handling, but has a perf cost — prefer `data-lenis-prevent`. |
| `respectReducedMotion` (default true) | Keep it on. Never force smoothing for reduced-motion users. |
| `syncTouch` | Leave off unless you need scroll-synced effects on touch; can be unstable on older iOS. |

## Must-do checklist

- [ ] Modals, drawers, dropdown lists, code blocks and any `overflow: auto` element get `data-lenis-prevent`.
- [ ] Opening a modal calls `lenis.stop()`, closing calls `lenis.start()`.
- [ ] Programmatic scroll uses `lenis.scrollTo(target, { offset })`, not `window.scrollTo`.
- [ ] On route change (SPA), scroll resets to top (`lenis.scrollTo(0, { immediate: true })`).
- [ ] Vanilla instances call `lenis.destroy()` on teardown; React cleans up the ticker in the effect return.
- [ ] Test: mouse wheel, trackpad, touch, keyboard (Space/PageDown/arrows), anchor links, browser find (Ctrl+F), reduced-motion setting.
- [ ] No `scroll-behavior: smooth` in CSS at the same time (double smoothing).
