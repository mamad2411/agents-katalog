---
name: transition-patterns-reference
description: CSS transition patterns quick reference - timing functions, durations, common patterns, and performance best practices
searchable: true
tags: [css, transitions, animations, performance, accessibility, timing-functions]
---

# CSS Transition Patterns Reference

Quick reference for CSS transitions with production-ready patterns, timing functions, and performance optimization.

## Quick Reference Card

### Standard Durations
```css
/* UI Interactions (buttons, hovers) */
transition: all 200ms ease-out;

/* State Changes (toggles, modals) */
transition: all 300ms ease-in-out;

/* Entering Animations */
transition: all 300ms ease-out;

/* Exiting Animations */
transition: all 300ms ease-in;

/* Performance-Optimized */
transition: transform 300ms ease, opacity 300ms ease;
```

### Timing Functions Quick Guide

| Function | Use Case | Feel |
|----------|----------|------|
| `linear` | Progress bars, loaders | Mechanical, constant speed |
| `ease` | General purpose (default) | Natural, balanced |
| `ease-in` | Exiting elements | Accelerating out |
| `ease-out` | Entering elements | Decelerating in |
| `ease-in-out` | State changes | Smooth both ends |
| `cubic-bezier()` | Custom curves | Precise control |

## Performance-First Patterns

### GPU-Accelerated Properties (Use These)

```css
/* RECOMMENDED - Smooth 60fps */
.smooth {
  transition: transform 300ms ease, opacity 300ms ease;
}

.smooth:hover {
  transform: translate3d(0, -4px, 0); /* 3D transform forces GPU */
  opacity: 0.9;
}
```

### Avoid Layout-Triggering Properties

```css
/* AVOID - Causes repaints */
.slow {
  transition: width 300ms ease, height 300ms ease;
}

/* INSTEAD - Use transform */
.fast {
  transition: transform 300ms ease;
  transform: scale(1);
}

.fast:hover {
  transform: scale(1.05);
}
```

## Common UI Patterns

### 1. Button Hover

```css
.button {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 12px 24px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: transform 200ms ease-out, box-shadow 200ms ease-out;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
}

.button:active {
  transform: translateY(0);
  transition-duration: 100ms;
}
```

### 2. Input Focus

```css
.input {
  border: 2px solid #e5e7eb;
  border-radius: 4px;
  padding: 8px 12px;
  transition: all 200ms ease;
}

.input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
  background-color: #f9fafb;
}
```

### 3. Card Elevation

```css
.card {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: transform 250ms ease-out, box-shadow 250ms ease-out;
}

.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
}
```

### 4. Menu Slide-In

```css
.sidebar {
  position: fixed;
  left: 0;
  width: 300px;
  height: 100vh;
  background: white;
  transform: translateX(-100%);
  transition: transform 300ms cubic-bezier(0.4, 0, 0.2, 1);
}

.sidebar.open {
  transform: translateX(0);
}
```

### 5. Modal Fade + Scale

```css
.modal {
  position: fixed;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transform: scale(0.95);
  pointer-events: none;
  transition: opacity 300ms ease, transform 300ms ease;
}

.modal.open {
  opacity: 1;
  transform: scale(1);
  pointer-events: all;
}

.modal-overlay {
  background: rgba(0, 0, 0, 0.5);
  transition: opacity 200ms ease;
}
```

### 6. Dropdown Menu

```css
.dropdown-menu {
  max-height: 0;
  overflow: hidden;
  opacity: 0;
  transform: translateY(-10px);
  transition: max-height 300ms ease, opacity 200ms ease, transform 200ms ease;
}

.dropdown.open .dropdown-menu {
  max-height: 400px;
  opacity: 1;
  transform: translateY(0);
}
```

### 7. Tab Switching

```css
.tab-content {
  opacity: 0;
  transform: translateX(20px);
  position: absolute;
  transition: opacity 250ms ease, transform 250ms ease;
  pointer-events: none;
}

.tab-content.active {
  opacity: 1;
  transform: translateX(0);
  position: relative;
  pointer-events: all;
}
```

### 8. Staggered List Items

```css
.list-item {
  opacity: 0;
  transform: translateY(10px);
  transition: opacity 300ms ease-out, transform 300ms ease-out;
}

.list-item:nth-child(1) { transition-delay: 0ms; }
.list-item:nth-child(2) { transition-delay: 50ms; }
.list-item:nth-child(3) { transition-delay: 100ms; }
.list-item:nth-child(4) { transition-delay: 150ms; }
.list-item:nth-child(5) { transition-delay: 200ms; }

.list-item.visible {
  opacity: 1;
  transform: translateY(0);
}
```

## Timing Function Recipes

### Material Design Curves

```css
/* Standard Easing */
.material-standard {
  transition: all 300ms cubic-bezier(0.4, 0, 0.2, 1);
}

/* Deceleration (entering) */
.material-decelerate {
  transition: all 300ms cubic-bezier(0, 0, 0.2, 1);
}

/* Acceleration (exiting) */
.material-accelerate {
  transition: all 300ms cubic-bezier(0.4, 0, 1, 1);
}

/* Sharp (quick and immediate) */
.material-sharp {
  transition: all 200ms cubic-bezier(0.4, 0, 0.6, 1);
}
```

### iOS-Style Curves

```css
.ios-bounce {
  transition: all 400ms cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

.ios-smooth {
  transition: all 350ms cubic-bezier(0.25, 0.46, 0.45, 0.94);
}
```

### Custom Curves

```css
/* Anticipation */
.anticipation {
  transition: all 500ms cubic-bezier(0.68, -0.25, 0.265, 1.25);
}

/* Overshoot */
.overshoot {
  transition: all 400ms cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

/* Elastic */
.elastic {
  transition: all 600ms cubic-bezier(0.68, -0.6, 0.32, 1.6);
}
```

## Accessibility

### Respect Motion Preferences

```css
/* Disable transitions for users who prefer reduced motion */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

### Maintain Focus Visibility

```css
.interactive:focus-visible {
  outline: 2px solid #3b82f6;
  outline-offset: 2px;
  transition: outline-offset 150ms ease;
}
```

## Performance Optimization

### Will-Change Property

```css
/* Use sparingly - only when needed */
.heavy-animation {
  will-change: transform, opacity;
  transition: transform 300ms ease, opacity 300ms ease;
}

.heavy-animation:hover {
  transform: scale(1.1);
  opacity: 0.9;
}

/* Remove when not animating */
.heavy-animation:not(:hover) {
  will-change: auto;
}
```

### Hardware Acceleration

```css
/* Force GPU acceleration */
.gpu-accelerated {
  transform: translate3d(0, 0, 0);
  transition: transform 300ms ease;
}

/* Alternative */
.also-accelerated {
  transform: translateZ(0);
  transition: transform 300ms ease;
}
```

## Transition Events

### JavaScript Control

```javascript
// Listen for transition end
element.addEventListener('transitionend', (e) => {
  if (e.propertyName === 'opacity') {
    console.log('Opacity transition completed');
  }
});

// Trigger transition
element.classList.add('transition-active');

// Cancel transition
element.classList.remove('transition-active');
```

## Best Practices Checklist

✅ **DO:**
- Use GPU-accelerated properties (transform, opacity)
- Keep durations between 200-400ms for most interactions
- Use `ease-out` for entering elements
- Use `ease-in` for exiting elements
- Respect `prefers-reduced-motion`
- Test on low-end devices

❌ **DON'T:**
- Transition `width`, `height`, `top`, `left`
- Use transitions longer than 1 second
- Use `linear` timing for UI interactions
- Transition all properties (`transition: all`)
- Forget focus states
- Ignore accessibility

## Duration Guidelines

| Interaction Type | Duration | Timing |
|-----------------|----------|---------|
| Micro-interactions (button hover) | 150-200ms | ease-out |
| Dropdowns, tooltips | 200-300ms | ease-out |
| Modals, dialogs | 300-400ms | ease-in-out |
| Page transitions | 400-600ms | ease-in-out |
| Emphasis animations | 300-500ms | custom curve |

## Common Mistakes to Avoid

1. **Too Long** - Transitions over 600ms feel sluggish
2. **Transitioning Layout** - Use transform instead of width/height
3. **No Reduced Motion** - Always provide alternative
4. **Linear Timing** - Use ease curves for natural feel
5. **All Properties** - Transition specific properties only
6. **Excessive Delays** - Keep delays under 200ms

## Quick Patterns Cheat Sheet

```css
/* Button */
transition: transform 200ms ease-out, box-shadow 200ms ease-out;

/* Input */
transition: border-color 200ms ease, box-shadow 200ms ease;

/* Card */
transition: transform 250ms ease-out, box-shadow 250ms ease-out;

/* Modal */
transition: opacity 300ms ease, transform 300ms ease;

/* Sidebar */
transition: transform 300ms cubic-bezier(0.4, 0, 0.2, 1);

/* Dropdown */
transition: max-height 300ms ease, opacity 200ms ease;

/* Fade */
transition: opacity 300ms ease;

/* Slide */
transition: transform 350ms ease-out;
```

---

Use this reference for quick lookups when implementing smooth, performant transitions in your projects.
