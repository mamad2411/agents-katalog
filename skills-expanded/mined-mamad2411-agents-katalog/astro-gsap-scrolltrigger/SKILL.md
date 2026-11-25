---
name: astro-gsap-scrolltrigger
description: Use when adding, fixing, or reviewing GSAP ScrollTrigger behavior in Astro pages, especially with view transitions, static routes, client scripts, reduced motion, cleanup, or browser-only lifecycle constraints.
cluster: creative-frontend
version: 1.0.0
---

# Astro GSAP ScrollTrigger

## Purpose

Use GSAP in Astro without breaking static rendering, route transitions, accessibility, or mobile performance.

## Required Pattern

- Keep all `window`, `document`, `matchMedia`, `gsap`, and `ScrollTrigger` initialization inside client-side `<script>` blocks or imported browser scripts.
- Never access browser APIs in Astro frontmatter; frontmatter runs on the server/build side.
- Register `ScrollTrigger` once in the browser script.
- Initialize on `astro:page-load`.
- Cleanup on `astro:before-swap`.
- Respect `prefers-reduced-motion: reduce`.
- Animate only `transform` and `opacity` unless there is a measured reason.
- Call `ScrollTrigger.refresh()` after layout-affecting images/content are ready.

## Minimal Lifecycle Shape

```astro
<script>
  import gsap from 'gsap';
  import { ScrollTrigger } from 'gsap/ScrollTrigger';

  gsap.registerPlugin(ScrollTrigger);

  let ctx;
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

  function cleanup() {
    ScrollTrigger.getAll().forEach((trigger) => trigger.kill());
    ctx?.revert?.();
    ctx = undefined;
  }

  function init() {
    cleanup();
    if (reduceMotion.matches) return;

    ctx = gsap.context(() => {
      gsap.to('[data-narrative]', {
        opacity: 1,
        y: 0,
        duration: 0.7,
        ease: 'power3.out',
        scrollTrigger: {
          trigger: '[data-narrative]',
          start: 'top 85%',
        },
      });
    });

    requestAnimationFrame(() => ScrollTrigger.refresh());
  }

  document.addEventListener('astro:page-load', init);
  document.addEventListener('astro:before-swap', cleanup);
  if (document.readyState !== 'loading') init();
</script>
```

## Review Checklist

- Does the page still render meaningful content without JavaScript?
- Does reduced motion show content immediately?
- Does route navigation avoid duplicate triggers?
- Are pinned sections bounded and mobile-safe?
- Are images/layout changes followed by a refresh?
- Are there no global scroll listeners doing animation work manually?

## Tool Routing

- Use `astro-framework` for Astro lifecycle and routing.
- Use `webapp-testing` or `browser` to verify console errors and layout behavior.
- Use `web-motion-library` only for generic animation inspiration.
- Use `animejs` only inside HyperFrames compositions; do not substitute it for live Astro ScrollTrigger work unless explicitly requested.
