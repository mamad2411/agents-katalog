---
name: CSS
description: Avoid common CSS pitfalls — stacking context, layout quirks, and underused modern features.
metadata: {"clawdbot":{"emoji":"🎨","os":["linux","darwin","win32"]}}
---

## Stacking Context
- `z-index` only works with positioned elements — or flex/grid children
- `isolation: isolate` creates stacking context — contains z-index chaos without position
- `opacity < 1`, `transform`, `filter` create stacking context — unexpected z-index behavior
- New stacking context resets z-index hierarchy — child z-index:9999 won't escape parent

## Layout Gotchas
- Margin collapse only vertical, only block — flex/grid children don't collapse
- `gap` works in flex now — no more margin hacks for spacing
- `flex-basis` vs `width`: basis is before grow/shrink — width is after, basis preferred in flex
- `min-width: 0` on flex child for text truncation — default min-width is min-content
- `overflow: hidden` on flex container can break — use `overflow: clip` if you don't need scroll

## Sizing Functions
- `clamp(min, preferred, max)` for fluid typography — `clamp(1rem, 2.5vw, 2rem)`
- `min()` and `max()` — `width: min(100%, 600px)` replaces media query
- `fit-content` sizes to content up to max — `width: fit-content` or `fit-content(300px)`

## Modern Selectors
- `:is()` for grouping — `:is(h1, h2, h3) + p` less repetition
- `:where()` same as `:is()` but zero specificity — easier to override
- `:has()` parent selector — `.card:has(img)` styles card containing image
- `:focus-visible` for keyboard focus only — no outline on mouse click

## Responsive Without Media Queries
- `aspect-ratio` native property — `aspect-ratio: 16/9` no padding hack
- Container queries: `@container (min-width: 400px)` — component-based responsive
- `container-type: inline-size` on parent required — for container queries to work

## Scroll Behavior
- `scroll-behavior: smooth` on html — native smooth scroll for anchors
- `overscroll-behavior: contain` — prevents scroll chaining to parent/body
- `scroll-snap-type` and `scroll-snap-align` — native carousel without JS
- `scrollbar-gutter: stable` — reserves scrollbar space, prevents layout shift

## Performance
- `contain: layout` isolates layout recalc — `contain: strict` for maximum isolation
- `content-visibility: auto` skips rendering off-screen — huge paint savings on long pages
- `will-change` hints compositor — but don't overuse, creates layers

## Accessibility
- `prefers-reduced-motion: reduce` — disable animations for vestibular disorders
- `prefers-color-scheme` — `@media (prefers-color-scheme: dark)`
- `forced-colors` for high contrast mode — `@media (forced-colors: active)`

## Shorthand Traps
- `inset: 0` equals `top/right/bottom/left: 0` — less repetition
- `place-items` is `align-items` + `justify-items` — `place-items: center` centers both
- `margin-inline`, `margin-block` for logical properties — respects writing direction
