---
name: a11y-patterns
description: "When to activate: accessibility, ARIA, WCAG, screen reader, keyboard navigation, focus management, a11y audit"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: frontend
  language: web
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---
# Accessibility Patterns

## ARIA Roles & Attributes

```html
<!-- Landmark roles -->
<header role="banner">
<nav aria-label="Main navigation">
<main role="main">
<aside aria-label="Related articles">
<footer role="contentinfo">

<!-- Button vs div -->
<!-- WRONG: -->
<div class="btn" onclick="submit()">Submit</div>
<!-- RIGHT: -->
<button type="submit">Submit</button>

<!-- Icon button — always needs label -->
<button aria-label="Close dialog">
  <svg aria-hidden="true" focusable="false">...</svg>
</button>

<!-- Toggle button -->
<button aria-pressed="false" id="theme-toggle">Dark mode</button>
```

## Live Regions

```html
<!-- Announce dynamic content to screen readers -->
<div aria-live="polite" aria-atomic="true" class="sr-only" id="status"></div>

<!-- Urgent announcements (interrupts) -->
<div role="alert">Your session expires in 5 minutes.</div>
```

```js
function announce(message, urgency = 'polite') {
  const el = document.getElementById('status');
  el.setAttribute('aria-live', urgency);
  el.textContent = '';
  requestAnimationFrame(() => { el.textContent = message; });
}
```

## Keyboard Navigation

```js
// Roving tabindex for widget internals (e.g., toolbar, listbox)
class RovingTabindex {
  constructor(container) {
    this.items = [...container.querySelectorAll('[role="option"]')];
    this.current = 0;
    this.items[0].tabIndex = 0;
    this.items.slice(1).forEach(el => (el.tabIndex = -1));
    container.addEventListener('keydown', this.#onKey.bind(this));
  }

  #onKey(e) {
    const map = { ArrowDown: 1, ArrowUp: -1, Home: -Infinity, End: Infinity };
    if (!(e.key in map)) return;
    e.preventDefault();
    this.current = Math.max(0, Math.min(this.items.length - 1,
      e.key === 'Home' ? 0 : e.key === 'End' ? this.items.length - 1
      : this.current + map[e.key]
    ));
    this.items.forEach((el, i) => (el.tabIndex = i === this.current ? 0 : -1));
    this.items[this.current].focus();
  }
}
```

## Focus Management

```js
// Trap focus in modal
function trapFocus(modal) {
  const focusable = modal.querySelectorAll(
    'a[href], button:not([disabled]), input, select, textarea, [tabindex]:not([tabindex="-1"])'
  );
  const first = focusable[0];
  const last = focusable[focusable.length - 1];

  modal.addEventListener('keydown', e => {
    if (e.key !== 'Tab') return;
    if (e.shiftKey ? document.activeElement === first : document.activeElement === last) {
      e.preventDefault();
      (e.shiftKey ? last : first).focus();
    }
  });
  first.focus();
}

// Restore focus on modal close
let previousFocus;
function openModal(modal) {
  previousFocus = document.activeElement;
  trapFocus(modal);
}
function closeModal(modal) {
  modal.hidden = true;
  previousFocus?.focus();
}
```

## Skip Links

```html
<a href="#main-content" class="skip-link">Skip to main content</a>
<main id="main-content" tabindex="-1">...</main>
```

```css
.skip-link {
  position: absolute;
  transform: translateY(-100%);
  transition: transform 200ms;
}
.skip-link:focus { transform: translateY(0); }
```

## Forms

```html
<!-- Associate label explicitly -->
<label for="email">Email address</label>
<input id="email" type="email" autocomplete="email"
       aria-required="true" aria-describedby="email-hint email-error">
<p id="email-hint">We'll never share your email.</p>
<p id="email-error" role="alert" hidden>Please enter a valid email.</p>

<!-- Fieldset for grouped controls -->
<fieldset>
  <legend>Preferred contact method</legend>
  <label><input type="radio" name="contact" value="email"> Email</label>
  <label><input type="radio" name="contact" value="phone"> Phone</label>
</fieldset>
```

## Color Contrast

```css
/* WCAG AA: 4.5:1 for normal text, 3:1 for large text */
/* Use oklch for perceptually uniform color adjustments */
:root {
  --text-on-surface: oklch(15% 0 0);      /* ~12:1 on white */
  --text-muted: oklch(45% 0 0);           /* ~4.6:1 on white — passes AA */
  --color-primary: oklch(40% 0.22 260);   /* ensure contrast on both themes */
}
```

## Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

## axe-core Integration

```js
// In development only
if (process.env.NODE_ENV === 'development') {
  import('axe-core').then(({ default: axe }) => {
    axe.run().then(({ violations }) => {
      violations.forEach(v => console.error(`[a11y] ${v.impact}: ${v.description}`, v.nodes));
    });
  });
}
```
