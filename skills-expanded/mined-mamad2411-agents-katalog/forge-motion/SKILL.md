---
name: forge-motion
description: >
  Advanced motion and animation design skill.
  Covers scroll-storytelling, physics-grade interactions, Three.js/WebGL,
  GSAP choreography, and cinematic page transitions.
  Use alongside forge-core when MOTION_DEPTH >= 8 is needed.
version: 1.0.0
---

# FORGE MOTION — Cinematic Animation & Physics Skill

> Motion is not decoration. It is communication.
> Every animation must answer: what does this movement *mean* to the user?

---

## DIAL CONFIGURATION

```
CHOREOGRAPHY:    8   (1=Simple fade / 10=Hollywood-grade sequencing)
PHYSICS_GRADE:   8   (1=Linear ease / 10=Mass, friction, spring simulation)
PERFORMANCE_CAP: 9   (1=Any GPU cost / 10=60fps on mid-range Android)
```

---

## SECTION 1 — THE MOTION PHILOSOPHY

### Meaning Before Movement
Before adding any animation, answer:
1. What state change is this communicating?
2. Does removing this animation hurt comprehension?
3. Is this respecting `prefers-reduced-motion`?

If #2 is "no" and #3 is "no" → remove the animation.

### Hierarchy of Motion
1. **Functional** — Loading states, page transitions, validation feedback. Always present.
2. **Feedback** — Button press, hover response, drag confirmation. Always present.
3. **Contextual** — List stagger, scroll reveals, shared element. Present when CHOREOGRAPHY ≥ 4.
4. **Ambient** — Background meshes, floating particles, cursor trails. Present when CHOREOGRAPHY ≥ 7.

### `prefers-reduced-motion`
Every animation MUST respect the user's system preference:
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```
In Framer Motion: check `useReducedMotion()` and substitute with instant opacity changes.

---

## SECTION 2 — SPRING PHYSICS REFERENCE

The spring is the universal language of premium motion. Use these configurations:

```js
// Definitions
const springs = {
  // Heavy, authoritative — modals, drawers
  heavy:   { type: 'spring', stiffness: 80,  damping: 18, mass: 1.2 },
  // Standard UI — buttons, cards, list items
  default: { type: 'spring', stiffness: 140, damping: 20, mass: 0.8 },
  // Snappy, direct — tooltips, badges, micro-interactions
  snappy:  { type: 'spring', stiffness: 300, damping: 28, mass: 0.5 },
  // Gentle, atmospheric — hero reveals, page entries
  drift:   { type: 'spring', stiffness: 60,  damping: 15, mass: 1.0 },
  // Aggressive overshoot — celebration, success confirmations
  bounce:  { type: 'spring', stiffness: 400, damping: 12, mass: 0.6 },
};
```

**Rule:** Never use `ease`, `ease-in-out`, or `linear` for interactive elements. Springs only.
CSS transitions on non-interactive ambient elements may use `cubic-bezier(0.16, 1, 0.3, 1)`.

---

## SECTION 3 — FRAMER MOTION PATTERNS

### Page Transitions
```jsx
const pageVariants = {
  initial: { opacity: 0, y: 12, filter: 'blur(4px)' },
  animate: { opacity: 1, y: 0,  filter: 'blur(0px)', transition: springs.drift },
  exit:    { opacity: 0, y: -8, filter: 'blur(4px)', transition: { duration: 0.2 } },
};
// Wrap in <AnimatePresence mode="wait"> at router level
```

### Staggered List Reveal
```jsx
const container = {
  hidden: {},
  show: { transition: { staggerChildren: 0.07, delayChildren: 0.1 } },
};
const item = {
  hidden: { opacity: 0, y: 16 },
  show:   { opacity: 1, y: 0, transition: springs.default },
};
// Parent + children MUST be in same Client Component tree
```

### Magnetic Button Effect
```jsx
// useMotionValue OUTSIDE render — never useState
const x = useMotionValue(0);
const y = useMotionValue(0);
const springX = useSpring(x, { stiffness: 200, damping: 20 });
const springY = useSpring(y, { stiffness: 200, damping: 20 });

function handleMouse(e) {
  const rect = ref.current.getBoundingClientRect();
  const centerX = rect.left + rect.width  / 2;
  const centerY = rect.top  + rect.height / 2;
  x.set((e.clientX - centerX) * 0.35); // 35% pull intensity
  y.set((e.clientY - centerY) * 0.35);
}
function handleLeave() { x.set(0); y.set(0); }
```

### Shared Element Transition
```jsx
// Source list item
<motion.div layoutId={`card-${id}`}>
  <motion.h3 layoutId={`title-${id}`}>{title}</motion.h3>
</motion.div>

// Target detail view (same layoutId)
<motion.div layoutId={`card-${id}`}>
  <motion.h1 layoutId={`title-${id}`}>{title}</motion.h1>
</motion.div>
// Wrap both in <LayoutGroup> at parent level
```

### Scroll-Triggered Reveal (Framer)
```jsx
const { scrollYProgress } = useScroll({ target: ref, offset: ['start end','end start'] });
const opacity = useTransform(scrollYProgress, [0, 0.3], [0, 1]);
const y       = useTransform(scrollYProgress, [0, 0.3], [32, 0]);
```

---

## SECTION 4 — GSAP PATTERNS (CHOREOGRAPHY >= 9)

**CRITICAL:** Never mix GSAP with Framer Motion in the same component.
GSAP is for: scrolltelling, full-page sequences, canvas backgrounds.

### Setup Pattern
```jsx
useEffect(() => {
  const ctx = gsap.context(() => {
    // All GSAP code inside ctx
    gsap.from('.hero-title', {
      y: 60, opacity: 0, duration: 1,
      ease: 'expo.out', stagger: 0.08,
    });

    ScrollTrigger.create({
      trigger: sectionRef.current,
      start: 'top 80%',
      onEnter: () => gsap.to(sectionRef.current, { opacity: 1, y: 0, duration: 0.8 }),
    });
  }, containerRef);

  return () => ctx.revert(); // ALWAYS clean up
}, []);
```

### Horizontal Scroll Section
```jsx
gsap.to(trackRef.current, {
  x: () => -(trackRef.current.scrollWidth - window.innerWidth),
  ease: 'none',
  scrollTrigger: {
    trigger: containerRef.current,
    pin: true,
    scrub: 1,
    end: () => `+=${trackRef.current.scrollWidth - window.innerWidth}`,
  },
});
```

---

## SECTION 5 — THREE.JS / WEBGL (CHOREOGRAPHY = 10)

Use only for: hero canvas backgrounds, 3D product showcases, data globe visualizations.

### Setup Template
```jsx
useEffect(() => {
  const renderer = new THREE.WebGLRenderer({ canvas: canvasRef.current, alpha: true, antialias: true });
  const scene  = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(60, width / height, 0.1, 100);
  camera.position.z = 5;

  // ... scene setup ...

  let rafId;
  const animate = () => { rafId = requestAnimationFrame(animate); renderer.render(scene, camera); };
  animate();

  return () => {
    cancelAnimationFrame(rafId);
    renderer.dispose(); // Critical — prevents GPU memory leak
    scene.clear();
  };
}, []);
```

### Performance Rules
- Max 300k vertices per scene for mobile.
- Use `BufferGeometry`, never legacy `Geometry`.
- Limit draw calls: merge static geometries with `BufferGeometryUtils.mergeBufferGeometries`.
- Mobile fallback: if GPU tier < 1, replace WebGL canvas with static image.

---

## SECTION 6 — CSS ANIMATION PRIMITIVES

Premium CSS animations for when JS animation is overkill:

```css
/* Shimmer skeleton */
@keyframes shimmer {
  from { background-position: -200% 0; }
  to   { background-position:  200% 0; }
}
.skeleton {
  background: linear-gradient(90deg, hsl(220 13% 91%) 25%, hsl(220 13% 96%) 50%, hsl(220 13% 91%) 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s ease-in-out infinite;
}

/* Status ping beacon */
@keyframes ping {
  0%   { transform: scale(1);   opacity: 1; }
  75%  { transform: scale(2.2); opacity: 0; }
  100% { transform: scale(2.2); opacity: 0; }
}

/* Directional hover fill (clip-path) */
.btn { position: relative; overflow: hidden; }
.btn::before {
  content: ''; position: absolute; inset: 0;
  background: var(--accent-dim);
  clip-path: inset(0 100% 0 0);
  transition: clip-path 300ms cubic-bezier(0.16, 1, 0.3, 1);
}
.btn:hover::before { clip-path: inset(0 0% 0 0); }

/* Float ambient animation */
@keyframes float {
  0%, 100% { transform: translateY(0); }
  50%       { transform: translateY(-8px); }
}
```

---

## SECTION 7 — PERFORMANCE CHECKLIST

- [ ] Only `transform` and `opacity` animated (no layout-triggering properties)
- [ ] `will-change: transform` removed after animation completes
- [ ] Grain/noise on `fixed` pseudo-element only, not scrolling containers
- [ ] All GSAP instances destroyed in `useEffect` cleanup
- [ ] All Three.js renderers disposed in cleanup
- [ ] Perpetual animations in isolated `React.memo` components
- [ ] `prefers-reduced-motion` respected with CSS media query + Framer `useReducedMotion()`
- [ ] GSAP and Framer Motion NOT mixed in same component tree
- [ ] `staggerChildren` parent + children in same Client Component
