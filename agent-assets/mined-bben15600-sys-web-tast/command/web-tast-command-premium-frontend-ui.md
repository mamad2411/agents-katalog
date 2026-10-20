# Premium Frontend UI Craftsmanship

## Mandate

A blank screen on load is unacceptable. Every premium experience sets expectations from frame one. Generic code produces generic results — this skill enforces intentional aesthetic direction.

## Four Visual Philosophies

| Style | When to use | Key traits |
|---|---|---|
| **Editorial Brutalism** | Bold brand, creative agency, portfolio | Raw grid, oversized type, high contrast, intentional tension |
| **Organic Fluidity** | Wellness, lifestyle, luxury | Curves, warm palette, slow animations, soft textures |
| **Cyber/Technical** | SaaS, dev tools, fintech | Monospace, grid lines, data visualization, cool palette |
| **Cinematic Pacing** | Storytelling, product launches | Scroll-driven narrative, pinned sections, dramatic transitions |

## Architectural Layers (Required)

### 1. Entry Sequence
Every page must have a preloader or entry animation:
```js
// GSAP entry sequence
gsap.timeline()
  .from('.preloader', { duration: 0.6, opacity: 0 })
  .to('.preloader', { duration: 0.4, yPercent: -100, delay: 0.8 })
  .from('.hero', { duration: 0.8, opacity: 0, y: 30 }, '-=0.2')
```

### 2. Hero Architecture
Full-viewport sections with structured typography:
```css
.hero-title {
  font-size: clamp(2.5rem, 8vw, 9rem);
  line-height: 0.95;
  letter-spacing: -0.03em;
}
```
Support cascading entrance effects and depth layering (parallax at 10–30% rate).

### 3. Contextual Navigation
Header responds to scroll direction:
- Scroll down → hide header (–100% translateY, 300ms ease-in)
- Scroll up → reveal header (0% translateY, 300ms ease-out)
- Add blur/glass effect when over content

## Motion as Connective Tissue

### Scroll-Driven Narrative
```js
// GSAP ScrollTrigger pin
ScrollTrigger.create({
  trigger: '.story-section',
  pin: true,
  scrub: 1,
  start: 'top top',
  end: '+=300%',
});
```

### Magnetic Buttons
```js
el.addEventListener('mousemove', (e) => {
  const rect = el.getBoundingClientRect();
  const x = (e.clientX - rect.left - rect.width / 2) * 0.3;
  const y = (e.clientY - rect.top - rect.height / 2) * 0.3;
  gsap.to(el, { x, y, duration: 0.4, ease: 'power2.out' });
});
```

### Custom Cursor
```js
// Mathematical interpolation — no snap
let curX = 0, curY = 0;
const lerp = (a, b, t) => a + (b - a) * t;
const tick = () => {
  curX = lerp(curX, mouseX, 0.1);
  curY = lerp(curY, mouseY, 0.1);
  cursor.style.transform = `translate(${curX}px, ${curY}px)`;
  requestAnimationFrame(tick);
};
```

## Technical Standards

### Performance
- Only animate `transform` and `opacity` — never `width`, `height`, `top`, `left`.
- Use `will-change: transform` sparingly (only during active animation).
- Hardware-accelerated via `translateZ(0)` or `translate3d`.

### Typography
```css
/* Variable font for premium feel */
font-variation-settings: 'wght' 400;
transition: font-variation-settings 300ms ease;
/* Dramatic scale with clamp */
font-size: clamp(1rem, 4vw + 0.5rem, 5rem);
```

### Accessibility
- All animations respect `prefers-reduced-motion`:
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: 0.01ms !important; }
}
```

## Recommended Stack

| Need | React | Vanilla |
|---|---|---|
| Animation | Framer Motion | GSAP |
| Smooth scroll | Lenis | Lenis |
| 3D | React Three Fiber | Three.js |
| Text split | — | SplitType |

## Timing Reference

| Interaction | Duration | Easing |
|---|---|---|
| Micro (hover, press) | 100–150ms | ease-out |
| UI transition | 200–300ms | ease-out (enter) / ease-in (exit) |
| Page transition | 400–600ms | custom cubic-bezier |
| Scroll narrative | scrub:1–2 | natural |
| Entry preloader | 600–1200ms | staged timeline |

## Anti-Patterns

- No animation without purpose — every motion answers "why?"
- No simultaneous animation of 5+ elements
- No `margin`/`padding` animation — use `transform` only
- No blocking animations — UI stays interactive during motion
- No ignored `prefers-reduced-motion`
