---
name: gsap-motion
description: Complex GSAP timeline orchestrations, ScrollTrigger pin triggers, path clipping animations, SVG morphing, and ticker loop synchronization.
---

# 🪄 10 - GSAP Advanced Motion Engine

## Purpose & Responsibility
Execute complex multi-stage GSAP timeline sequences, scroll-bound pin triggers, vector path clipping, and ticker synchronization.

## Key Snippet
```javascript
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

const tl = gsap.timeline({
  scrollTrigger: {
    trigger: '.hero-container',
    start: 'top top',
    end: '+=200%',
    pin: true,
    scrub: 1,
  }
});

tl.to('.hero-title', { opacity: 0, y: -50 })
  .to('.hero-card', { scale: 1.05, borderRadius: '24px' }, '<');
```
