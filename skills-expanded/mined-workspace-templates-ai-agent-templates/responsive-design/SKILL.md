---
name: responsive-design
description: Makes a page work from 320px up using fluid type, container queries and breakpoints chosen by the content and tested at real widths.
---

# Responsive design

Start from the narrowest screen and add layout only where the content needs it.

## Steps

1. Ensure `<meta name="viewport" content="width=device-width, initial-scale=1">` exists and no zoom lock is set.
2. Reset the base: `box-sizing: border-box`, `img, video { max-width: 100%; height: auto }`, and no fixed widths on containers; use `max-width` with `width: min(100% - 2rem, 70rem)`.
3. Build the single-column layout first. It must work at 320px with no horizontal scroll.
4. Use fluid values: `font-size: clamp(1rem, 0.9rem + 0.5vw, 1.25rem)` and spacing from `clamp()` or `rem` tokens. Prefer `gap` over margins.
5. Add breakpoints only where the layout actually breaks, found by widening the viewport slowly. Write them in `em` or `rem`, mobile first with `min-width`.
6. For reusable components use `container-type: inline-size` and `@container (min-width: 30rem)` so a card adapts to its slot, not the screen.
7. Use `grid-template-columns: repeat(auto-fit, minmax(16rem, 1fr))` for card grids before reaching for breakpoints.
8. Test at 320, 375, 768, 1024 and 1440 pixels, and at 200 percent text zoom. Touch targets stay at least 44px.

## Rules

- No `vw`-only font sizes; they ignore user zoom.
- Never hide essential content on small screens.
- Do not use device names as breakpoints.

## Report

The breakpoints you used and why, widths tested, and anything still cramped.
