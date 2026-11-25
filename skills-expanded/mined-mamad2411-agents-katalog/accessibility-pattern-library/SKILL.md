---
name: "Accessibility Pattern Library"
version: "1.0.0"
description: "Provides accessible UI component patterns with ARIA attributes, keyboard navigation, and screen reader support."
author: "workspace"
activated: false
---

# Accessibility Pattern Library

Provides accessible UI component patterns following WCAG 2.1 AA guidelines.

## Decision Framework

### When to Apply
Use when:
- Building interactive UI components (modals, dropdowns, tabs, forms)
- Implementing keyboard navigation
- Adding screen reader support
- Auditing existing components for accessibility

### When NOT to Apply
Don't use when:
- Server-side rendering without client interaction
- Non-interactive content display
- Using a component library that already handles accessibility

## Anti-Patterns

### 1. Non-Semantic Interactive Elements
```html
<!-- BAD -->
<div onclick="openModal()">Open</div>
<span class="button" tabindex="0">Click me</span>

<!-- GOOD -->
<button aria-haspopup="dialog" aria-expanded="false">Open</button>
```

### 2. Missing Focus Management
```javascript
// BAD: Modal opens but focus stays on trigger
openModal();

// GOOD: Move focus to modal, trap focus inside
openModal();
modal.querySelector('[autofocus]')?.focus() || modal.focus();
```

### 3. Invisible Focus Indicators
```css
/* BAD */
*:focus { outline: none; }

/* GOOD */
*:focus-visible { outline: 2px solid var(--focus-color); outline-offset: 2px; }
```


## Trigger Phrases

- "Add accessibility"
- "ARIA support"
- "Keyboard navigation"
- "Screen reader"
- "WCAG compliance"

## Patterns

### Modal Dialog
```html
<div role="dialog" aria-modal="true" aria-labelledby="dialog-title">
  <h2 id="dialog-title">Dialog Title</h2>
  <button aria-label="Close dialog" onclick="close()">&times;</button>
  <!-- Content -->
</div>
```

### Tab Panel
```div [role="tablist"]
  <button role="tab" aria-selected="true" aria-controls="panel-1" id="tab-1">Tab 1</button>
  <button role="tab" aria-selected="false" aria-controls="panel-2" id="tab-2">Tab 2</button>
</div>
<div role="tabpanel" id="panel-1" aria-labelledby="tab-1">Content 1</div>
<div role="tabpanel" id="panel-2" aria-labelledby="tab-2" hidden>Content 2</div>
```

### Live Region for Dynamic Updates
```html
<div aria-live="polite" aria-atomic="true">
  <!-- Dynamic status messages announced by screen readers -->
</div>
```

## Integration
- Works with: form-pattern-engine, mobile-gesture-handler, design-audit
- Validates with: performance-budget-enforcer
