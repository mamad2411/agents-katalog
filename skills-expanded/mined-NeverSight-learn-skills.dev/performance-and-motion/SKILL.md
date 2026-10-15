---
name: performance-and-motion
description: Use when adding or changing animations, smooth scrolling, carousel behavior, lazy loading, service worker behavior, hydration strategy, or other performance-sensitive front-end behavior in this Astro site. Trigger for Lenis, Embla, reveal effects, runtime media loading, and interaction code that can affect responsiveness.
---

# Performance and Motion

Fast first. Fancy second.

## Priorities

1. Preserve static delivery whenever possible.
2. Keep hydration narrow and intentional.
3. Protect LCP, input responsiveness, and scroll smoothness.
4. Respect reduced motion before styling the effect.

## Rules

- Animate emphasis, transitions, or orientation. Not everything.
- Use transform and opacity for movement when possible.
- Avoid stacked scroll listeners when CSS or existing observers can do the job.
- Re-test page transitions and re-initialization after motion changes.
- Do not fight existing transforms with extra animation layers.
- Protect nested scroll regions with the appropriate Lenis escape hatch.
- Keep carousel content light and avoid heavy first-frame assets.
- Use Embla where horizontal comparison helps. Do not turn essential navigation or core reading flows into swipe traps.
- Prefer mobile-only carousel activation for dense card collections when desktop already has enough width.
- Dropdowns, drawers, and modal menus need deliberate overflow behavior. If the viewport is shorter than the design, the component still has to work.
- Treat hero media as LCP-critical and everything else as suspect.
- Lazy-load what is not needed immediately.
- Keep fonts and third-party scripts from blocking the page.

## Verification

- Check reduced-motion behavior after adding or changing animations.
- Check keyboard and touch interaction for carousels, accordions, and menus.
- Check that runtime initialization survives Astro page transitions and repeated menu opens.
