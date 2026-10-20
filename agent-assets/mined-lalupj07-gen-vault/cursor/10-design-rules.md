---
description: Visual design rules to avoid AI-generated look
globs: "**/*.{html,css,scss,tsx,jsx,vue,svelte,astro}"
alwaysApply: false
---

# Design Rules

## NEVER

- NEVER use purple, indigo or violet gradients (no `from-purple-*`, `via-violet-*`, `to-indigo-*`, `#8b5cf6`, `#6366f1` style gradients). Use one primary color, one accent, and neutrals defined as CSS variables or Tailwind theme tokens.
- NEVER use pill-shaped buttons. Never use `rounded-full` or `border-radius: 9999px` on buttons or CTAs. Use a radius scale of 0, 4px, 6px or 8px, applied consistently.
- NEVER use emoji as icons or bullets. Use an icon library (lucide-react, Heroicons, Phosphor) or inline SVG.
- NEVER use AI-generated or generic stock-looking photos. Use real photos, product screenshots, brand illustrations, or a typographic layout. If an image is missing, use a neutral placeholder labeled `TODO`.
- NEVER add crazy scroll animations: no scroll-jacking, heavy parallax, or elements flying in on every section. Banned libraries by default: locomotive-scroll, lenis smooth-scroll hijack, GSAP ScrollTrigger pinning, unless I explicitly ask.
- NEVER add custom cursors or cursor-follow effects (no `cursor: none`, no mousemove-driven blobs or trails).
- NEVER use more than two typefaces on new surfaces. Exception: a project's established, documented type system.

## Allowed

- Motion: hover, focus, and simple fade or translate transitions of 150 to 250ms. Always respect `prefers-reduced-motion`.
- Maintain a consistent spacing scale and a clear type hierarchy.
