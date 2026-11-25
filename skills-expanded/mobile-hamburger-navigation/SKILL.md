---
name: mobile-hamburger-navigation
description: Fail-safe guidance for mobile hamburger navigation in static HTML/CSS/Vanilla JS sites.
---

# Mobile hamburger navigation

- Keep mobile navigation fail-safe: closed state must be inert and open state must be explicit.
- Closed menu/backdrop must be hidden and use `pointer-events: none`.
- Open menu/backdrop may use `pointer-events: auto` only while visible.
- Keep `aria-expanded` synchronized with the real menu state.
- Close via hamburger, backdrop, Escape, and menu links.
- Do not change desktop navigation behavior or desktop layout.