---
name: responsive-css-mobile-viewport
description: Mobile-only CSS guardrails for drawers, backdrops, viewport units, and z-index.
---

# Responsive CSS mobile viewport

- Put visual mobile navigation changes inside the mobile media query only.
- Use fixed positioning for mobile drawer/backdrop.
- Use clear z-index layering: header below drawer controls, backdrop below drawer.
- Prefer `100dvh` for mobile viewport height when needed.
- If menu content can exceed viewport height, make the drawer scroll internally.
- Closed drawer/backdrop must not receive pointer events.