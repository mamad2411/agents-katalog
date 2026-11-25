---
name: mobile-bootstrap-offcanvas-navbar
description: Use when building or fixing mobile-first navbar collapse, offcanvas drawers, ARIA-expanded sync, overflow handling, and Bootstrap-like responsive navigation.
metadata:
  short-description: Mobile navbar collapse and offcanvas patterns from Bootstrap
---

# Mobile Bootstrap Offcanvas Navbar

Use this skill for mobile-first navbars, collapse panels, and offcanvas drawers inspired by `twbs/bootstrap`.

Primary source:
- https://github.com/twbs/bootstrap

Focus areas:
- Navbar collapse state.
- Offcanvas drawer layout and transitions.
- `aria-expanded` and collapsed class synchronization.
- Mobile menu overflow when the menu is taller than the viewport.
- Modal/offcanvas scroll behavior on iOS.

Checklist:
- Toggle with a real `button`.
- Keep `aria-expanded`, hidden state, and visual class state aligned.
- Make long collapsed menus scrollable with `max-height` and `overflow-y: auto`.
- Use fixed positioning for offcanvas panels and a separate backdrop layer.
- Lock background scroll when offcanvas is modal.
- Test with many menu items, landscape mobile, and small 320px screens.

Common fixes:
- If an expanded navbar cannot scroll on mobile, constrain its height and enable vertical overflow.
- If the body scrolls behind offcanvas, add modal-style scroll lock.
- If state desynchronizes after resizing, reset mobile collapse state at desktop breakpoints.
