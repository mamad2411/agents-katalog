---
name: core-web-vitals-optimization
description: Improves LCP, INP and CLS with measured fixes to images, fonts, scripts and layout, and reports before and after numbers for each change.
---

# Core Web Vitals optimization

Measure, fix one thing, measure again. Targets at the 75th percentile: LCP under 2.5 s, INP under 200 ms, CLS under 0.1.

## Steps

1. Baseline. Run `npx lighthouse <url> --only-categories=performance --preset=desktop --output=json` (and mobile) three times and take the median. Note the LCP element, the longest tasks, and the layout shifts with their sources. Use field data if the user has it; lab numbers alone can mislead.
2. LCP. Identify the element. If it is an image: serve a correctly sized AVIF or WebP, add `fetchpriority="high"`, never `loading="lazy"`, and preload it only when it is not in the initial HTML. If it is text: fix the font (below) and render-blocking CSS. Cut server time to first byte before touching anything else if it exceeds 600 ms.
3. Fonts. Self-host, subset, `font-display: swap` or `optional`, preload only the one or two files used above the fold, and match fallback metrics with `size-adjust` to avoid shifts.
4. CLS. Give every image, video and embed `width` and `height` or `aspect-ratio`. Reserve space for ads and banners. Animate `transform` and `opacity`, not layout properties. Never insert content above existing content after load.
5. INP. Find the slow interaction in the performance profile. Break up tasks over 50 ms (`scheduler.yield()` or `setTimeout`), debounce expensive handlers, and defer third-party scripts with `async` or `defer`, or load them after interaction.
6. Re-measure after each change. Revert any change that did not improve its metric.

## Report

A table of metric, before, after and the change that caused it. List third-party scripts by cost and recommend which to remove.
