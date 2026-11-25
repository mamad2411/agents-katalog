---
name: mobile-sticky-drawer-theme-glitch
description: Diagnose and fix mobile-only hamburger drawer bugs caused by sticky headers, fixed nav/backdrop layers, scroll locking, and broad theme-switch transitions in static HTML/CSS/Vanilla JS sites. Use when a mobile menu works at the top of the page but breaks after scrolling, or when changing light/dark theme causes flicker, jumps, or drawer glitches while desktop must remain unchanged.
---

# Mobile Sticky Drawer Theme Glitch

Use this skill for static or lightly enhanced frontend sites where mobile navigation and theme switching interact badly with scroll position. Keep desktop behavior visually unchanged.

## Workflow

1. Build a mobile repro before editing.
   - Use a viewport like `390x844`.
   - Test menu open at `scrollY = 0`.
   - Close, scroll to the middle of the page, then open again.
   - Capture `getBoundingClientRect()` for the header, drawer, backdrop, and a theme button.
   - Check `html/body` classes and inline styles before open, during open, after theme switch, and after close.

2. Look for this failure signature.
   - The drawer has `position: fixed`, but its `top` becomes negative after opening from a scrolled page.
   - The backdrop does not cover the full viewport.
   - The drawer/backdrop live inside a `position: sticky` header.
   - Opening the menu adds `overflow: hidden` to `html` or `body`.
   - A broad selector such as `body.is-theme-switching *` overrides transitions for every element.

3. Fix the layer model first.
   - Keep desktop nav markup and layout intact.
   - On mobile open, move the mobile drawer and backdrop to a body-level layer, or render a dedicated body-level mobile drawer.
   - Restore the nodes when the menu closes or when the viewport returns to desktop.
   - Closed drawer and backdrop must remain inert: hidden plus `pointer-events: none`.

4. Fix scroll locking deliberately.
   - Store the current `scrollY` when opening.
   - Lock mobile body with fixed positioning and `top: -scrollYpx`.
   - On close, remove inline lock styles and restore the saved scroll position.
   - Ensure every close path cleans `nav-open`, `is-open`, body styles, and html styles.

5. Fix theme switching narrowly.
   - Do not transition every element and pseudo-element on mobile.
   - Preserve drawer `transform` and backdrop `opacity` transitions.
   - Limit theme transitions to color/background/border/shadow on named surfaces and controls.
   - Theme buttons inside the drawer must not leave the menu locked or scrolled to the top.

## Validation

Run a browser probe after the fix. The scrolled-open case should satisfy:

```js
const navRect = document.querySelector(".site-nav").getBoundingClientRect();
const backdropRect = document.querySelector(".nav-backdrop").getBoundingClientRect();

navRect.top === 0;
navRect.bottom >= window.innerHeight;
backdropRect.height >= window.innerHeight;
document.body.classList.contains("nav-open") === true;
```

Also verify:

- Closing by hamburger, close button, backdrop, Escape, and menu links restores scroll.
- Theme switching while the mobile drawer is open keeps the drawer visible and interactive.
- At `min-width: 760px`, desktop nav remains in the header and mobile drawer state is cleaned up.
