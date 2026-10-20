---
name: animation-motion
description: Animation and motion standards — GPU acceleration, easing, durations, accessibility, performance
globs: ["**/*.tsx", "**/*.jsx", "**/*.ts", "**/*.css"]
alwaysApply: false
---

# Animation & Motion Standards

Animation makes interfaces feel alive. Bad animation confuses users, causes motion sickness, and kills performance. Good animation guides attention, provides feedback, and respects accessibility needs.

---

## GPU-Accelerated Animations

**ALWAYS**:
- Animate ONLY transform and opacity (GPU accelerated)
- Use will-change for animation hints
- 60fps minimum (1000ms/60 frames ≈ 16.67ms per frame)
- Test performance with DevTools

**NEVER**:
- Animate width, height, margin, padding (causes layout recalculation)
- Animate position, left/right/top/bottom (slow, non-GPU)
- Animate background-color without opacity fallback
- Create janky animations (visible frame drops)

### ✅ GOOD GPU-Accelerated Animations

```css
/* ✅ Transform: smooth, GPU-accelerated */
.button:hover {
  transform: scale(1.05);  /* Hardware accelerated */
}

.menu.open {
  transform: translateX(0);  /* Slide in smoothly */
}

animation: slideIn 300ms ease-out forwards;

@keyframes slideIn {
  from {
    transform: translateX(-100px);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

/* ✅ Opacity: smooth fade */
.fade-out {
  animation: fadeOut 300ms ease-in forwards;
}

@keyframes fadeOut {
  from { opacity: 1; }
  to { opacity: 0; }
}

/* ✅ Will-change hint */
.animated-element {
  will-change: transform, opacity;
  animation: spin 2s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
```

### ❌ BAD Non-Accelerated Animations

```css
/* ❌ Width animation: triggers layout recalculation */
.expand {
  animation: expandWidth 300ms ease forwards;
}

@keyframes expandWidth {
  from { width: 0; }
  to { width: 200px; }  /* Layout thrashing! ❌ */
}

/* ❌ Position animation: non-GPU */
.slide {
  animation: slideLeft 300ms ease forwards;
}

@keyframes slideLeft {
  from { left: 0; }
  to { left: 100px; }  /* Non-GPU, jerky ❌ */
}

/* ❌ Background color: can be slow */
button {
  animation: colorChange 300ms ease;
}

@keyframes colorChange {
  from { background-color: blue; }
  to { background-color: red; }  /* Non-GPU, slow ❌ */
}
```

---

## Animation Durations

**ALWAYS**:
- Use consistent duration values
- Standard durations: 50ms (instant), 100ms (fast), 200ms (normal), 300ms (slow), 500ms (slower)
- Match duration to animation type (simple = fast, complex = slow)
- Respect prefers-reduced-motion (disable or reduce duration)

**NEVER**:
- Arbitrary durations (125ms, 350ms, etc.)
- Animations longer than 500ms (feels sluggish)
- Same duration for all animations (looks robotic)
- Ignore accessibility preferences

### ✅ GOOD Duration Timing

```css
:root {
  --duration-instant: 50ms;
  --duration-fast: 100ms;
  --duration-normal: 200ms;
  --duration-slow: 300ms;
  --duration-slower: 500ms;
}

/* Instant: instant feedback (opacity toggle) */
.show {
  animation: appear 50ms ease-out;
}

/* Fast: quick interactions (button hover) */
button:hover {
  animation: bounce 100ms ease-out;
}

/* Normal: standard animations (modal open) */
.modal {
  animation: slideUp 200ms ease-out;
}

/* Slow: complex animations (page transitions) */
page-transition {
  animation: fadeIn 300ms ease-out;
}

/* Slower: microinteractions (loading spinner) */
.spinner {
  animation: spin 500ms linear infinite;
}

/* Respect reduced motion */
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## Easing Functions

**ALWAYS**:
- ease-out: default (object slowing down)
- ease-in: exit animations (disappearing)
- ease-in-out: complex motions
- bounce: playful, interactive elements
- linear: continuous rotations, progress

**NEVER**:
- ease-in for entrance (feels sluggish)
- ease-out for exit (feels jerky)
- Arbitrary cubic-bezier values (hard to maintain)
- Linear for all animations (robotic, unnatural)

### ✅ GOOD Easing

```css
:root {
  /* Easing functions */
  --ease-out: cubic-bezier(0, 0, 0.2, 1);      /* Object slowing down */
  --ease-in: cubic-bezier(0.4, 0, 1, 1);       /* Object speeding up */
  --ease-in-out: cubic-bezier(0.4, 0, 0.2, 1); /* Both directions */
  --ease-bounce: cubic-bezier(0.34, 1.56, 0.64, 1);  /* Playful */
}

/* Entrance: ease-out (content appearing) */
.modal {
  animation: slideUp 300ms var(--ease-out) forwards;
}

/* Exit: ease-in (content disappearing) */
.close {
  animation: slideDown 200ms var(--ease-in) forwards;
}

/* Bounce: playful interactions */
button:active {
  animation: bounce 100ms var(--ease-bounce);
}

/* Linear: continuous rotations */
.spinner {
  animation: spin 2s linear infinite;
}

/* Smooth: transitions */
button {
  transition: all 200ms var(--ease-out);
}
```

---

## Accessibility (prefers-reduced-motion)

**ALWAYS**:
- Detect prefers-reduced-motion media query
- Disable or reduce animations for affected users
- Test with: DevTools > Rendering > Emulate CSS media feature prefers-reduced-motion
- Respect: 15% of users prefer reduced motion (not just vestibular issues)

**NEVER**:
- Ignore accessibility preferences
- Auto-play animations on page load
- Animation-heavy interactions without opt-out
- Parallax scrolling without disable option

### ✅ GOOD Reduced Motion Support

```css
/* Default: animations enabled */
button {
  transition: all 200ms ease-out;
}

.modal {
  animation: slideUp 300ms ease-out;
}

/* Respect reduced motion preference */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}

/* Optional: provide motion toggle */
body.reduce-motion * {
  animation: none !important;
  transition: none !important;
}
```

```html
<!-- User preference button -->
<button id="motion-toggle" aria-label="Toggle animations">
  🎬 Toggle Motion
</button>

<script>
  const toggle = document.getElementById('motion-toggle');
  const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  
  if (prefersReduced) {
    document.body.classList.add('reduce-motion');
  }
  
  toggle.addEventListener('click', () => {
    document.body.classList.toggle('reduce-motion');
  });
</script>
```

---

## Loading States & Skeleton Screens

**ALWAYS**:
- Show loading state immediately (< 100ms)
- Use spinner or skeleton screen
- Prevent layout shift (reserve space)
- Disable interactions while loading
- Add timeout (max 10 seconds)

**NEVER**:
- Hide UI without feedback
- Allow clicks during loading
- Unexpected loading states
- Skeleton screens without timeout

### ✅ GOOD Loading States

```html
<!-- Loading spinner -->
<div class="spinner" role="status" aria-live="polite">
  <span class="sr-only">Loading...</span>
  <svg><!-- spinner icon --></svg>
</div>

<!-- Skeleton screen -->
<div class="skeleton">
  <div class="skeleton-line"></div>
  <div class="skeleton-line"></div>
  <div class="skeleton-line"></div>
</div>

<!-- Button loading state -->
<button disabled class="loading">
  <span class="sr-only">Saving...</span>
  <svg class="spinner"><!-- spinner --></svg>
  Saving...
</button>
```

```css
.spinner {
  width: 24px;
  height: 24px;
  border: 3px solid rgba(0, 0, 0, 0.1);
  border-top-color: #0066cc;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.skeleton {
  background: linear-gradient(
    90deg,
    #f0f0f0 25%,
    #e0e0e0 50%,
    #f0f0f0 75%
  );
  background-size: 200% 100%;
  animation: loading 1.5s infinite;
}

@keyframes loading {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
```

---

## Micro-interactions

**ALWAYS**:
- Provide feedback for every user action
- Hover states on interactive elements
- Focus states (keyboard users)
- Active/pressed states for buttons
- Success/error feedback

**NEVER**:
- Silent actions (no feedback)
- Hover without focus (keyboard users excluded)
- Unclear state changes

### ✅ GOOD Micro-interactions

```css
/* Button states */
button {
  /* Default */
  background-color: #0066cc;
  color: white;
  transition: all 200ms ease-out;
}

button:hover {
  /* Hover: background darker */
  background-color: #0052a3;
}

button:active {
  /* Pressed: slight scale down */
  transform: scale(0.98);
}

button:focus-visible {
  /* Focus: outline */
  outline: 2px solid #0066cc;
  outline-offset: 2px;
}

button:disabled {
  /* Disabled: opacity reduced */
  opacity: 0.5;
  cursor: not-allowed;
}

/* Link states */
a:hover {
  color: #0052a3;
  text-decoration: underline;
}

a:focus-visible {
  outline: 2px solid #0066cc;
  border-radius: 2px;
}

/* Form input focus */
input:focus-visible {
  border-color: #0066cc;
  box-shadow: 0 0 0 3px rgba(0, 102, 204, 0.1);
}
```

---

## Performance Checklist

- [ ] Only transform and opacity animated
- [ ] Animations 60fps (no frame drops)
- [ ] Durations: 50ms, 100ms, 200ms, 300ms, 500ms (consistent)
- [ ] Easing: ease-out (default), ease-in (exit), bounce (playful)
- [ ] prefers-reduced-motion respected
- [ ] No layout thrashing
- [ ] will-change used for complex animations
- [ ] GPU acceleration enabled (check DevTools)
- [ ] Tested on low-end devices
- [ ] Loading states shown immediately
- [ ] All interactive elements have states (hover, active, focus, disabled)

---

## Animation Checklist

- [ ] Animations serve a purpose (not gratuitous)
- [ ] Entrance animations (ease-out, 200-300ms)
- [ ] Exit animations (ease-in, 100-200ms)
- [ ] Loading spinners (linear, continuous)
- [ ] Button states (hover, active, focus, disabled)
- [ ] Form feedback (success, error animations)
- [ ] Page transitions (fade, slide)
- [ ] Micro-interactions (subtle, quick)
- [ ] Accessibility: prefers-reduced-motion supported
- [ ] Performance: tested on slow devices

---

## Summary

Good animation:
1. **GPU-accelerated** — transform and opacity only
2. **Purposeful** — guides attention, provides feedback
3. **Performant** — 60fps, no jank
4. **Consistent** — standard durations and easing
5. **Accessible** — respects prefers-reduced-motion
6. **Subtle** — enhances without overwhelming

Animation is the craft of making interfaces feel alive and responsive.
