---
name: accessibility
description: WCAG 2.1 AA compliance — ARIA labels, keyboard navigation, color contrast, semantic HTML, screen reader support
globs: ["**/*.html", "**/*.ts"]
alwaysApply: false
---

# Accessibility (WCAG 2.1 AA)

All UI must be accessible to users with disabilities. Follow WCAG 2.1 Level AA standards: keyboard navigation, color contrast, ARIA labels, semantic HTML, screen reader support.

## Core Principles

**WCAG 2.1 has 4 pillars**: Perceivable (users can see/hear), Operable (users can use keyboard), Understandable (users understand it), Robust (works with assistive tech).

**Target**: WCAG 2.1 Level AA (minimum for government, education, large enterprises).

---

## 1. Semantic HTML (Perceivable + Understandable)

**ALWAYS**:
- Use semantic tags: `<header>`, `<nav>`, `<main>`, `<article>`, `<section>`, `<footer>`
- Use `<button>` for clickable actions, not `<div onclick="">`
- Use `<a href="">` for navigation, not `<span onclick="">`
- Use `<input type="text">`, `<input type="email">`, `<input type="number">` (correct type matters)
- Use `<label for="inputId">` for form labels (not floating labels without labels)
- Use `<fieldset>` and `<legend>` for grouped form controls
- Use `<table>` with `<thead>`, `<tbody>`, `<th>` for data tables (not layout)
- Use heading hierarchy: `<h1>` page title, `<h2>` sections, `<h3>` subsections (no skipping)

**NEVER**:
- Use `<div>` or `<span>` for buttons/links
- Skip labels on form inputs
- Use `<br>` for spacing
- Use nested `<button>` or `<a>` tags
- Use tables for layout
- Skip heading structure (go h1 → h3, skipping h2)

### ✅ GOOD Semantic HTML
```html
<!-- Correct semantic structure -->
<header role="banner">
  <nav>
    <a href="/">Home</a>
    <a href="/about">About</a>
  </nav>
</header>

<main>
  <article>
    <h1>Article Title</h1>
    <p>Article content...</p>
  </article>

  <section>
    <h2>Related Articles</h2>
    <ul>
      <li><a href="/article1">Article 1</a></li>
      <li><a href="/article2">Article 2</a></li>
    </ul>
  </section>

  <!-- Form with labels -->
  <form>
    <fieldset>
      <legend>Contact Information</legend>
      <label for="email">Email</label>
      <input type="email" id="email" name="email" required>

      <label for="message">Message</label>
      <textarea id="message" name="message"></textarea>

      <button type="submit">Send</button>
    </fieldset>
  </form>

  <!-- Data table with proper markup -->
  <table>
    <thead>
      <tr>
        <th>Name</th>
        <th>Email</th>
        <th>Status</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Alice</td>
        <td>alice@example.com</td>
        <td>Active</td>
      </tr>
    </tbody>
  </table>
</main>

<footer>
  <p>&copy; 2026 Company Name</p>
</footer>
```

### ❌ BAD Semantic HTML
```html
<!-- Using divs for everything -->
<div onclick="navigate('/')">Home</div>

<!-- Missing labels on input -->
<input type="email" placeholder="Email">

<!-- Skipped heading levels (h1 → h3) -->
<h1>Page Title</h1>
<h3>Subsection</h3>

<!-- Table used for layout -->
<table>
  <tr><td>Logo</td><td>Navigation</td></tr>
</table>

<!-- Button inside link -->
<a href="#"><button>Click Me</button></a>
```

---

## 2. Color Contrast (Perceivable)

**ALWAYS**:
- **Normal text** (< 18px): **4.5:1 contrast ratio** (text to background)
- **Large text** (≥ 18px / 14px bold): **3:1 contrast ratio**
- **UI components** (buttons, inputs, borders): **3:1 contrast ratio**
- Test contrast with tools: WebAIM Contrast Checker, Chrome DevTools, axe DevTools
- Don't rely on color alone to convey information (use text, icons, patterns)

**NEVER**:
- Light gray text on white (#CCCCCC on white is too low)
- Color-only instructions ("click the red button")
- Using color to indicate required fields (use asterisk + red)
- Contrast < 3:1 for any UI element

### ✅ GOOD Contrast Examples
- Black `#000000` on white `#FFFFFF` = 21:1 ✅
- Dark blue `#003366` on white `#FFFFFF` = 11:1 ✅
- Dark gray `#404040` on white `#FFFFFF` = 12:1 ✅

### ❌ BAD Contrast Examples
- Light gray `#CCCCCC` on white `#FFFFFF` = 1.2:1 ❌ (too low)
- Medium gray `#999999` on white `#FFFFFF` = 4:1 ⚠️ (ok for large text only)

### How to Test (CSS)
```css
/* Check contrast in DevTools */
/* Chrome: Right-click element → Inspect → Color picker shows contrast ratio */
/* Firefox: Developer Tools → Inspector → Style Inspector → Click color swatch */

/* Good accessible palette */
:root {
  --text-primary: #212121;    /* Black, 21:1 on white */
  --text-secondary: #666666;  /* Dark gray, 7:1 on white */
  --bg-white: #FFFFFF;
  --bg-light: #F5F5F5;
  --error: #D32F2F;            /* 6:1 on white */
  --success: #1976D2;          /* 7:1 on white */
}
```

---

## 3. Keyboard Navigation (Operable)

**ALWAYS**:
- All interactive elements reachable via keyboard (Tab key)
- Focus visible (outline or highlight when tabbed to)
- Focus order logical (left-to-right, top-to-bottom)
- Modals trap focus (Tab cycles within modal)
- Skip links: `<a href="#main">Skip to main content</a>` (appears on focus)
- `Escape` closes modals, dropdowns, menus
- `Enter` or `Space` activates buttons
- Arrow keys navigate menus, tabs, sliders

**NEVER**:
- Remove focus outline (`outline: none` without replacement)
- Tab order jumps around randomly
- Keyboard shortcuts without alternative
- Modal without focus trap
- Interactive elements not reachable via Tab

### ✅ GOOD Keyboard Navigation (Angular)
```typescript
// Component: Menu with keyboard support
import { Component, HostListener } from '@angular/core';

@Component({
  selector: 'app-dropdown-menu',
  template: `
    <button 
      (click)="toggleMenu()" 
      [attr.aria-expanded]="isOpen"
      [attr.aria-haspopup]="true"
    >
      Menu
    </button>

    <ul *ngIf="isOpen" role="menu">
      <li *ngFor="let item of items; let i = index" role="none">
        <a 
          [href]="item.href"
          role="menuitem"
          (keydown)="onKeydown($event, i)"
          #menuItem
        >
          {{ item.label }}
        </a>
      </li>
    </ul>
  `
})
export class DropdownMenu {
  isOpen = false;
  @ViewChildren('menuItem') menuItems!: QueryList<ElementRef>;

  toggleMenu() {
    this.isOpen = !this.isOpen;
    if (this.isOpen) {
      setTimeout(() => this.menuItems?.first?.nativeElement?.focus());
    }
  }

  @HostListener('keydown', ['$event'])
  onKeydown(event: KeyboardEvent, index: number) {
    const key = event.key;
    const items = this.menuItems.toArray();

    if (key === 'ArrowDown') {
      event.preventDefault();
      const next = (index + 1) % items.length;
      items[next].nativeElement.focus();
    } else if (key === 'ArrowUp') {
      event.preventDefault();
      const prev = (index - 1 + items.length) % items.length;
      items[prev].nativeElement.focus();
    } else if (key === 'Escape') {
      event.preventDefault();
      this.isOpen = false;
    }
  }
}
```

### ✅ GOOD Focus Management (HTML + CSS)
```html
<!-- Skip link (hidden, visible on focus) -->
<a href="#main" class="skip-link">Skip to main content</a>

<style>
  .skip-link {
    position: absolute;
    top: -40px;
    left: 0;
    background: #000;
    color: white;
    padding: 8px;
    z-index: 100;
  }

  .skip-link:focus {
    top: 0;
  }

  /* Visible focus indicator on all interactive elements */
  button:focus,
  a:focus,
  input:focus {
    outline: 3px solid #4A90E2;
    outline-offset: 2px;
  }
</style>
```

---

## 4. ARIA Labels (Perceivable + Robust)

**ALWAYS**:
- `<button>` content describes action ("Delete", not "X")
- `<a>` content describes destination ("Contact Us", not "Click Here")
- Icon-only buttons: `aria-label="Close"` or `<span class="sr-only">Close</span>`
- Form inputs: `<label for="inputId">` or `aria-label="Search"`
- Landmarks: `<nav>`, `<main>`, `<aside>`, `<section>` with `aria-label` if multiple
- Images: `<img alt="Description of image">` (meaningful, not "image" or "photo")
- Links in lists: `<li><a href="...">Link text</a></li>` (not just `<a>`)
- Dialogs: `role="dialog"`, `aria-labelledby="title"`, `aria-modal="true"`
- Status/alerts: `role="status"` or `role="alert"` with `aria-live="polite"` or `"assertive"`

**NEVER**:
- `alt=""` on meaningful images (use alt text)
- `aria-label` on focusable elements that already have text
- `aria-hidden="true"` on interactive elements
- Icon-only buttons without labels
- Links with no text ("Click here", "Read more" without context)

### ✅ GOOD ARIA Labels (HTML)
```html
<!-- Icon button with label -->
<button aria-label="Close dialog">
  <svg><use href="#icon-close"></use></svg>
</button>

<!-- Icon button using sr-only text -->
<button>
  <svg><use href="#icon-search"></use></svg>
  <span class="sr-only">Search</span>
</button>

<!-- Form input with label -->
<label for="search">Search products</label>
<input type="search" id="search" placeholder="e.g., laptop">

<!-- Multiple nav elements -->
<nav aria-label="Main navigation">
  <a href="/">Home</a>
  <a href="/products">Products</a>
</nav>

<nav aria-label="Footer navigation">
  <a href="/about">About</a>
  <a href="/contact">Contact</a>
</nav>

<!-- Image with description -->
<img src="hero.jpg" alt="Coffee cup on wooden desk, morning sunlight">

<!-- Modal dialog -->
<div role="dialog" aria-labelledby="dialog-title" aria-modal="true">
  <h2 id="dialog-title">Confirm Action</h2>
  <p>Are you sure?</p>
  <button>Cancel</button>
  <button>Confirm</button>
</div>

<!-- Status message -->
<div role="status" aria-live="polite">
  ✓ Changes saved successfully
</div>

<!-- Alert (high priority) -->
<div role="alert" aria-live="assertive">
  ⚠ Network error. Please try again.
</div>
```

### ❌ BAD ARIA Labels
```html
<!-- Icon button without label -->
<button>
  <svg><use href="#icon-close"></use></svg>
</button>

<!-- Link with vague text -->
<a href="/article">Click here</a>

<!-- Image without alt text -->
<img src="logo.png">

<!-- Accessible name is unclear -->
<button aria-label="X">X</button>

<!-- ARIA on non-interactive element -->
<div onclick="...">Not a button</div>
```

---

## 5. Screen Reader Testing

**Test with**:
- NVDA (Windows, free)
- JAWS (Windows, paid but industry standard)
- VoiceOver (Mac, built-in)
- TalkBack (Android)
- VoiceOver (iOS)

**What to test**:
- Headings announced correctly
- Form labels associated with inputs
- Buttons have accessible names
- Images have descriptions
- Navigation structure clear
- Focus order logical
- Dynamic content announced (live regions)
- Error messages announced

### ✅ GOOD Screen Reader Experience
- "Heading level 1: Article Title"
- "Email, email input, required"
- "Delete button"
- "Main navigation, list, 5 items"
- "Status message: Changes saved successfully"

### ❌ BAD Screen Reader Experience
- "Heading: Untitled"
- "Input"
- "Button" (no accessible name)
- "Link: Click here"
- No status announcement when data loads

---

## Accessibility Checklist

- [ ] All headings use semantic `<h1>-<h6>` in logical order
- [ ] All images have descriptive `alt` text
- [ ] All form inputs have associated `<label>` or `aria-label`
- [ ] Color contrast ≥ 4.5:1 for normal text
- [ ] All interactive elements keyboard accessible
- [ ] Focus indicator visible on all elements
- [ ] Icon-only buttons have `aria-label` or `sr-only` text
- [ ] Multiple navigation areas have `aria-label`
- [ ] Modals trap focus with `aria-modal="true"`
- [ ] Status messages use `aria-live="polite"` or `"assertive"`
- [ ] No content conveyed by color alone
- [ ] Link text is descriptive (not "Click here")
- [ ] Tables have `<thead>`, `<th>`, `scope` attributes
- [ ] Skip links present and functional
- [ ] Tested with screen reader (NVDA, JAWS, VoiceOver)
