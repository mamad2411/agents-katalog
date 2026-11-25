---
name: mobile-tailwind-responsive-policy
description: Use when creating mobile-first responsive CSS, Tailwind-like utility layouts, viewport-safe sections, accessible utilities, hover/touch variants, and reduced-motion policies.
metadata:
  short-description: Mobile-first responsive CSS policy from Tailwind
---

# Mobile Tailwind Responsive Policy

Use this skill for mobile-first styling patterns inspired by `tailwindlabs/tailwindcss`.

Primary source:
- https://github.com/tailwindlabs/tailwindcss

Focus areas:
- Mobile-first breakpoints.
- Responsive spacing, type, grids, and images.
- Avoiding accidental horizontal overflow.
- Handling hover-only interactions on touch devices.
- Respecting `prefers-reduced-motion`.
- Using `sr-only` style utilities for accessible labels.

Checklist:
- Start from the smallest viewport and progressively enhance.
- Verify no element causes horizontal scroll at 320px.
- Use fluid sizing carefully; avoid viewport-width font scaling.
- Use `min-height: 100dvh` for full-height mobile sections.
- Add width/height or aspect-ratio to images to reduce layout shift.
- Lazy-load only below-the-fold media.
- Do not rely on hover as the only way to reveal content.

Common fixes:
- Replace fixed desktop widths with `max-width`, flexible grids, and wrapping.
- Replace `height: 100vh` with `min-height: 100dvh` where mobile browser chrome breaks layout.
- Use explicit tap targets of at least 44px, preferably 48px.
