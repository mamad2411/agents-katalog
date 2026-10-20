---
name: web-motion-library
description: Select and implement interactive web animations, 3D elements, and pre-built React/Tailwind/Framer Motion components for landing pages and hero sections. Use when adding hover effects, morphing shapes, hero sections with background video, or choosing from Magic UI's 50+ animated component library.
cluster: creative-frontend
version: 1.0.0
---

# Web Motion Library

Reference library for interactive web animations and pre-built component systems. Covers hover motion patterns, morphing background shapes, full-screen hero sections, and the Magic UI component library (50+ animated React/Tailwind/Framer Motion components).

## When to Use

- Adding interactive hover animations to image grids or text rows
- Implementing morphing SVG background shapes
- Building full-screen hero sections with background video
- Selecting pre-built animated components from Magic UI
- Choosing between animation approaches for landing pages

## Animation Patterns

| Pattern | Source | Tech Stack | Best For |
|---------|--------|-----------|----------|
| Hover Motion Grid | sink.design / Codrops | CSS + JS | Image grids that respond to mouse movement, intro animations |
| Morphing Shapes | Codrops | SVG + CSS | Organic background transitions, exhibition-style layouts |
| Hero Section | Viktor Oddy | React + Tailwind CSS | Full-screen hero with background video, Rubik font, SVG CTA |
| Magic UI Components | magicui.design | React + Tailwind + Framer Motion | 50+ pre-built animated components (marquees, borders, cards) |

## Component Selection Guide

### When you need...

| Need | Use | Why |
|------|-----|-----|
| Mouse-reactive image grid | Hover Motion pattern | Rows move in sync with cursor, supports intro animation reveal |
| Organic background animation | Morphing Shapes pattern | SVG shape transitions, exhibition/gallery aesthetic |
| Full-screen landing hero | Viktor Oddy Hero | Background video, Rubik typography, custom SVG button |
| Animated marquee/ticker | Magic UI: Marquee | Infinite scroll with pause-on-hover |
| Glowing card borders | Magic UI: Shine Border | Animated gradient border effect |
| Notification feed | Magic UI: Notification List | Stacked animated notification cards |
| Social proof logos | Magic UI: Company Logos | Auto-scrolling logo strip |
| Concentric circles | Magic UI: Circles | Expanding ring animation |
| Ripple effects | Magic UI: Ripple | Click/hover ripple animations |

## Key Technical Notes

- Magic UI is a **shadcn/ui companion** — install components individually, not as a monolithic package
- All Magic UI components are **open-source** (React + TypeScript + Tailwind + Framer Motion)
- Hero section uses **Rubik font** (Google Fonts) with tight line-height (0.98) and negative letter-spacing (-2px to -4px)
- SVG CTA buttons use custom path fills instead of standard CSS backgrounds for unique shapes

See `references/patterns.md` for implementation details and component specifications.
