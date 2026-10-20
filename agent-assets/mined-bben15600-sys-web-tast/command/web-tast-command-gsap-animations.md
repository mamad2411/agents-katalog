# GSAP Animation Skill

## Setup

```bash
npm install gsap
# Premium plugins (Club GreenSock required for SplitText, Flip, DrawSVG):
# import from gsap/all or register individually
```

```js
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { Flip } from 'gsap/Flip';
gsap.registerPlugin(ScrollTrigger, Flip);
```

## Core Concepts

### Tween (single animation)
```js
gsap.to('.box', { x: 200, opacity: 1, duration: 0.5, ease: 'power2.out' });
gsap.from('.box', { y: 40, opacity: 0, duration: 0.6 });
gsap.fromTo('.box', { opacity: 0 }, { opacity: 1, duration: 0.4 });
```

### Timeline (sequenced)
```js
const tl = gsap.timeline({ defaults: { ease: 'power2.out', duration: 0.5 } });
tl.from('.hero-title', { y: 60, opacity: 0 })
  .from('.hero-sub', { y: 40, opacity: 0 }, '-=0.3')   // overlap 300ms
  .from('.hero-cta', { scale: 0.9, opacity: 0 }, '-=0.2');
```

### Stagger
```js
gsap.from('.card', { y: 30, opacity: 0, stagger: 0.08, duration: 0.5 });
// Advanced stagger
gsap.from('.grid-item', {
  scale: 0.85, opacity: 0,
  stagger: { amount: 0.6, from: 'center', grid: [3, 4] },
});
```

## ScrollTrigger

```js
// Basic scroll animation
gsap.from('.section', {
  scrollTrigger: { trigger: '.section', start: 'top 80%', toggleActions: 'play none none reverse' },
  y: 50, opacity: 0, duration: 0.7,
});

// Scrub (tied to scroll position)
gsap.to('.parallax', {
  scrollTrigger: { trigger: '.parallax', scrub: 1.5 },
  yPercent: -30,
});

// Pinned section
ScrollTrigger.create({
  trigger: '.sticky-section',
  start: 'top top',
  end: '+=500',
  pin: true,
  scrub: true,
});

// Batch for performance (many elements)
ScrollTrigger.batch('.card', {
  onEnter: els => gsap.from(els, { y: 40, opacity: 0, stagger: 0.08 }),
});
```

## Flip (layout transitions)

```js
// Capture state → change DOM → animate difference
const state = Flip.getState('.item');
container.appendChild(item); // DOM change
Flip.from(state, { duration: 0.5, ease: 'power2.inOut' });
```

## Text Animations (SplitType or SplitText)

```js
import SplitType from 'split-type'; // free alternative to SplitText
const split = new SplitType('.heading', { types: 'chars,words' });
gsap.from(split.chars, { y: '100%', opacity: 0, stagger: 0.02, duration: 0.5 });
```

## Easing Reference

| Ease | Use |
|---|---|
| `power1.out` | Subtle, natural |
| `power2.out` | Standard UI enter |
| `power3.out` | Snappy |
| `expo.out` | Dramatic deceleration |
| `back.out(1.7)` | Overshoot/bounce feel |
| `elastic.out(1, 0.3)` | Playful spring |
| `none` | Linear, scrub animations |

## Performance Rules

- Only animate `transform` (x, y, rotation, scale) and `opacity`.
- Set `will-change: transform` on elements before animation starts; remove after.
- Use `gsap.ticker` for custom render loops instead of `requestAnimationFrame`.
- Kill ScrollTriggers on component unmount to prevent memory leaks.

```js
// React cleanup
useEffect(() => {
  const ctx = gsap.context(() => { /* animations */ }, ref);
  return () => ctx.revert();
}, []);
```

## Accessibility

```js
// Check for reduced motion preference
const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const duration = prefersReduced ? 0 : 0.5;
```

## Common Patterns

### Page transition
```js
const pageEnter = () => gsap.from('main', { opacity: 0, y: 20, duration: 0.4, clearProps: 'all' });
const pageLeave = () => gsap.to('main', { opacity: 0, y: -20, duration: 0.3 });
```

### Counter / number roll
```js
gsap.to(obj, { value: 1250, duration: 1.5, ease: 'power1.out',
  onUpdate: () => (el.textContent = Math.round(obj.value).toLocaleString()) });
```

### SVG path draw
```js
gsap.from('.path', { drawSVG: '0%', duration: 1.5, ease: 'power2.inOut' });
```
