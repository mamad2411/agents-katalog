---
name: animation-guide
description: Guide for choosing and implementing animations with GSAP, Lenis, Framer Motion, and Three.js. Use when adding animations, reviewing animation code, or deciding which library to use.
---

# Animation Implementation Guide

## Library Decision
Before writing any animation, decide which library to use:

### GSAP (Primary)
- ScrollTrigger for scroll-driven reveals, parallax, pinning
- SplitText for text animations (always use `autoSplit: true` for responsive)
- Timeline for sequenced animations (`.to()` chaining)
- MorphSVG for SVG path morphing
- CustomEase for branded easing curves
- Setup: always use `useGSAP` hook from `@gsap/react`

### Lenis
- Smooth scroll ONLY -- never use for individual animations
- ONE instance at layout level, never per-component
- Integrate with GSAP ScrollTrigger via `lenis.on('scroll', ScrollTrigger.update)`
- Control: `lenis.stop()` for modals, `lenis.start()` to resume

### Framer Motion
- `AnimatePresence` for mount/unmount animations
- `layoutId` for shared element transitions
- `motion.div` with `animate`, `initial`, `exit` for React state-driven animations
- Spring physics via `type: "spring"`
- Do NOT use for scroll animations -- use GSAP ScrollTrigger instead

### Three.js / React Three Fiber
- 3D scenes only -- particles, 3D models, WebGL effects
- Use `@react-three/fiber` + `@react-three/drei` for React integration
- Always lazy-load with `next/dynamic`: `const Scene = dynamic(() => import('./Scene'), { ssr: false })`

## Responsive Animation
- All animations must work at every breakpoint
- Use `gsap.matchMedia()` for breakpoint-specific animations
- Test with `prefers-reduced-motion` -- provide reduced/no-motion fallbacks
