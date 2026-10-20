---
name: accessibility-wcag
description: WCAG 2.1 AA accessibility standards — contrast, focus, keyboard, ARIA, touch targets
globs: ["**/*.tsx", "**/*.jsx", "**/*.html"]
alwaysApply: false
---

# WCAG 2.1 AA Accessibility Standards

Accessibility is not an afterthought — it's a requirement. WCAG 2.1 AA ensures your UI works for everyone: users with vision impairment, motor disabilities, cognitive differences, and temporary impairments (broken arm, bright sunlight, noisy environment).

---

## Contrast Requirements

**ALWAYS**:
- Normal text (< 18px): 4.5:1 contrast ratio minimum
- Large text (≥ 18px bold): 3:1 contrast ratio minimum
- UI components (icons, borders): 3:1 minimum
- Test contrast ratios with tools: WebAIM, Contrast Checker
- Check both light and dark modes

**NEVER**:
- Low contrast text (will fail WCAG AA)
- Assume color is enough (test with tools)
- Ignore dark mode contrast (often worse)
- Place light text on light backgrounds

### ✅ GOOD Contrast

```css
/* 4.5:1 ratio — WCAG AA ✅ */
body {
  background-color: #ffffff;
  color: #111827;  /* Dark gray on white: 12.5:1 ✅ */
}

/* Large text: 3:1 minimum */
h1 {
  color: #1f2937;  /* Even larger ratio: 8.3:1 ✅ */
  font-size: 32px;
  font-weight: bold;
}

/* Buttons */
.btn-primary {
  background-color: #0066cc;
  color: #ffffff;  /* Blue on white: 5.1:1 ✅ */
}

.btn-secondary {
  background-color: #ffffff;
  border: 2px solid #0066cc;
  color: #0066cc;  /* Blue on white: 5.1:1 ✅ */
}

/* Dark mode */
@media (prefers-color-scheme: dark) {
  body {
    background-color: #1f2937;
    color: #f9fafb;  /* Light text on dark: 12.6:1 ✅ */
  }
}

/* Icon buttons */
svg {
  color: #0066cc;
  width: 24px;
  height: 24px;  /* 3:1 minimum with background ✅ */
}
```

### ❌ BAD Contrast

```css
/* ❌ 2.3:1 — FAILS WCAG AA */
body {
  background-color: #ffffff;
  color: #cccccc;  /* Light gray on white: FAILS ❌ */
}

/* ❌ Dark mode with low contrast */
body {
  background-color: #1f2937;
  color: #6b7280;  /* Gray on dark: 3:1 (borderline, risky) */
}

/* ❌ Placeholder text too light */
input::placeholder {
  color: #d1d5db;  /* Too light, hard to read */
}
```

---

## Focus Indicators (Keyboard Navigation)

**ALWAYS**:
- Visible focus outline on ALL interactive elements
- Focus outline: 2px solid accent color, 2px offset
- Focus visible only on keyboard (not on mouse click)
- Never use `outline: none` without replacement
- Tab order logical and sequential

**NEVER**:
- Remove focus outlines (outline: none)
- Make focus indicators hard to see (light gray on white)
- Keyboard traps (can't tab out of element)
- Skip focus on important elements

### ✅ GOOD Focus States

```css
/* Visible focus outline */
button:focus-visible,
a:focus-visible,
input:focus-visible {
  outline: 2px solid #0066cc;
  outline-offset: 2px;
}

/* Remove focus ring on mouse click (optional) */
button:focus-visible:not(:focus-visible) {
  outline: none;
}

/* Input focus */
input:focus-visible {
  border-color: #0066cc;
  box-shadow: 0 0 0 3px rgba(0, 102, 204, 0.2);
  outline: 2px solid #0066cc;
  outline-offset: 2px;
}

/* Skip link for keyboard nav */
a.skip-link {
  position: absolute;
  top: -40px;
  left: 0;
  background: #0066cc;
  color: white;
  padding: 8px;
}

a.skip-link:focus {
  top: 0;
}

/* Logical tab order */
<form>
  <label>Name: <input name="name" /></label>
  <label>Email: <input name="email" /></label>
  <button type="submit">Submit</button>
</form>
```

### ❌ BAD Focus States

```css
/* ❌ Removed focus outline with no replacement */
button:focus {
  outline: none;  /* INACCESSIBLE ❌ */
}

/* ❌ Focus outline same color as background */
input:focus {
  outline: 1px solid #f9fafb;  /* Invisible! ❌ */
}

/* ❌ Keyboard trap */
<div contenteditable>
  Try to Tab out... can't!  <!-- Trap ❌ -->
</div>

/* ❌ Tab order not logical */
<form>
  <button>Next</button>
  <input name="name" />  <!-- Should come first! -->
</form>
```

---

## Semantic HTML & ARIA

**ALWAYS**:
- Use semantic HTML: `<button>`, `<nav>`, `<main>`, `<article>`, `<section>`
- Use ARIA labels: aria-label for icon-only buttons
- Use ARIA attributes: aria-expanded, aria-hidden, aria-describedby, aria-live
- One `<h1>` per page (page title)
- Heading hierarchy: h1 → h2 → h3 (no skipping)
- Form labels: always `<label>` for inputs (linked via `for` attribute)

**NEVER**:
- Use `<div>` for interactive elements (use `<button>`, `<a>`, `<input>`)
- Skip heading levels (h1 → h3 → h2)
- Icon-only buttons without aria-label
- Unlabeled form inputs
- Divs styled as links (use `<a>`)

### ✅ GOOD Semantic HTML & ARIA

```html
<!-- Semantic page structure -->
<body>
  <nav>
    <h1>MyApp</h1>
    <a href="/">Home</a>
    <a href="/about">About</a>
  </nav>

  <main>
    <article>
      <h1>Page Title</h1>  <!-- One h1 per page -->
      <section>
        <h2>Section</h2>
        <p>Content</p>
      </section>
    </article>
  </main>

  <footer>
    <p>&copy; 2026</p>
  </footer>
</body>

<!-- Proper form labels -->
<form>
  <label for="email">Email:</label>
  <input id="email" name="email" type="email" required />
  
  <label for="message">Message:</label>
  <textarea id="message" name="message"></textarea>
  
  <button type="submit">Send</button>
</form>

<!-- Icon-only buttons need aria-label -->
<button aria-label="Close menu">
  <svg><!-- close icon --></svg>
</button>

<!-- Collapsible content -->
<button aria-expanded="false" aria-controls="menu">
  Menu
</button>
<nav id="menu" hidden>
  <a href="/home">Home</a>
  <a href="/about">About</a>
</nav>

<!-- Live regions for dynamic content -->
<div aria-live="polite" aria-atomic="true">
  Loading...
</div>

<!-- Links are for navigation, buttons for actions -->
<a href="/contact">Contact</a>  <!-- Navigation -->
<button>Save</button>           <!-- Action -->
```

### ❌ BAD Semantic HTML & ARIA

```html
<!-- ❌ Using div for interactive elements -->
<div onclick="handleClick()" role="button">
  Click me  <!-- Keyboard users can't use this -->
</div>

<!-- ❌ Multiple h1s -->
<h1>Page Title</h1>
<h1>Section Title</h1>  <!-- WRONG ❌ -->

<!-- ❌ Skipped heading levels -->
<h1>Title</h1>
<h3>Subtitle</h3>  <!-- Should be h2 ❌ -->

<!-- ❌ Icon-only button without label -->
<button>
  <svg><!-- close icon --></svg>
</button>  <!-- What does this do? ❌ -->

<!-- ❌ Unlabeled input -->
<input type="email" placeholder="Email" />  <!-- No label ❌ -->

<!-- ❌ Styled div as link -->
<div onclick="navigate('/home')" style="color: blue; cursor: pointer;">
  Home  <!-- Not keyboard accessible ❌ -->
</div>
```

---

## Touch Targets & Motor Control

**ALWAYS**:
- Touch targets minimum 44×44px (48×48px recommended)
- Gap between targets: 8px minimum
- Click areas clearly defined
- No tiny buttons or links
- Enough space for finger interaction

**NEVER**:
- Small buttons (< 44px)
- Buttons too close together (no gap)
- Hovering to reveal buttons (mobile users can't)
- Double-tap to activate (single tap required)

### ✅ GOOD Touch Targets

```css
/* 44px minimum */
button, a {
  min-width: 44px;
  min-height: 44px;
  padding: var(--spacing-sm) var(--spacing-base);  /* 8px 16px */
}

/* Gaps between buttons */
button + button {
  margin-left: var(--spacing-sm);  /* 8px gap */
}

/* Click area includes padding */
.card {
  padding: var(--spacing-base);
  cursor: pointer;  /* Whole card is clickable */
}

.icon-button {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Links have clickable area */
a {
  padding: var(--spacing-xs) var(--spacing-sm);  /* 4px 8px */
  border-radius: 4px;  /* Highlight on focus */
}
```

### ❌ BAD Touch Targets

```css
/* ❌ Too small */
button {
  width: 30px;
  height: 30px;
  padding: 0;  /* No padding ❌ */
}

/* ❌ Too close together */
button + button {
  margin-left: 2px;  /* Not enough gap ❌ */
}

/* ❌ Tiny link text */
a {
  font-size: 10px;
  padding: 0;  /* No area ❌ */
}
```

---

## Color Not Conveyed Alone

**ALWAYS**:
- Use color + icon/text/pattern to convey meaning
- Error messages: red border + text + icon
- Success states: green + checkmark + text
- Status indicators: color + label
- Don't rely on color alone

**NEVER**:
- Color as only indicator (confuses colorblind users)
- Red/green alone for errors/success (color-blind inaccessible)
- Pie charts with color only (use labels, patterns)

### ✅ GOOD Color + Meaning

```html
<!-- Error: color + icon + text -->
<div class="error">
  <svg class="icon-error"><!--error icon--></svg>
  <span>Email is required</span>
</div>

<!-- Success: color + checkmark + text -->
<div class="success">
  <svg class="icon-check"><!--checkmark--></svg>
  <span>Saved successfully</span>
</div>

<!-- Required field: label + asterisk + color -->
<label>
  Email
  <span aria-label="required" style="color: red;">*</span>
  <input type="email" required />
</label>

<!-- Status with color + icon + text -->
<span class="status-online">
  <span class="status-dot">●</span>
  Online
</span>
```

### ❌ BAD Color Alone

```html
<!-- ❌ Just red, no text -->
<div style="color: red;">Error</div>  <!-- Colorblind users? -->

<!-- ❌ Red/green pie chart, color only -->
<div style="background: linear-gradient(90deg, red 50%, green 50%);">
  <!-- Which is which? Colorblind users lost ❌ -->
</div>

<!-- ❌ Status indicator color only -->
<span style="color: green;">●</span>  <!-- What does green mean? -->
```

---

## Accessibility Checklist

- [ ] All text 4.5:1 contrast (normal) or 3:1 (large, ≥18px bold)
- [ ] Focus indicators visible (2px outline, 2px offset)
- [ ] Tab order logical and complete
- [ ] No keyboard traps
- [ ] Semantic HTML (`<button>`, `<nav>`, `<main>`, `<article>`)
- [ ] One `<h1>` per page
- [ ] Heading hierarchy (h1 → h2 → h3, no skips)
- [ ] Form labels with `<label>` tags
- [ ] Icon-only buttons have aria-label
- [ ] Touch targets 44×44px minimum, 8px gaps
- [ ] Color + text/icon (never color alone)
- [ ] prefers-reduced-motion respected
- [ ] Images have alt text
- [ ] Tested with screen reader (NVDA, JAWS, VoiceOver)
- [ ] Tested with keyboard only (no mouse)
- [ ] Tested in light and dark modes

---

## Testing Tools

- **WebAIM Contrast Checker** — Test contrast ratios
- **Lighthouse** — Built into Chrome, audits accessibility
- **NVDA** — Free screen reader (Windows)
- **JAWS** — Popular screen reader (payware)
- **VoiceOver** — Built into Mac/iOS
- **axe DevTools** — Browser extension for accessibility audits
- **WAVE** — Browser extension for accessibility feedback

---

## Summary

Good accessibility:
1. **Contrast** — Text readable for everyone (4.5:1 normal, 3:1 large)
2. **Focus** — Keyboard users can navigate (visible focus, logical order)
3. **Semantic** — HTML meaningful (buttons, headings, landmarks)
4. **Motor** — Touch targets large enough (44×44px, 8px gaps)
5. **Vision** — Color + text/icon (never color alone)
6. **Tested** — Validated with real tools and real users

This isn't extra work — it's good design that benefits everyone.
