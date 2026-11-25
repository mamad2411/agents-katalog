---
name: motion-language
description: Motion language engine for GSAP scroll timelines, Lenis inertia scrolling, Framer Motion spring physics, SplitType character reveals, and hardware acceleration.
---

# 🎬 04 - Motion Language & Physics Engine

## Purpose & Responsibility
Orchestrate purposeful 60 FPS motion with physical weight (magnetic pull, ink ripples, spring dampening).

## Directives
1. **Compositor Acceleration**: Animate ONLY `transform` and `opacity`. Never touch `width`, `height`, `margin`, or `padding` in animation loops.
2. **Spring Dampening Physics**: Use realistic spring configurations (`stiffness: 300, damping: 30, mass: 1`).
3. **Lenis Scroll Sync**: Synchronize Lenis smooth scroll ticker directly with GSAP ScrollTrigger.
