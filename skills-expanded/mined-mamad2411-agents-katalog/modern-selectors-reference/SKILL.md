---
description: Modern CSS Selectors Quick Reference - :has(), :is(), :where(), :not(), and advanced selector patterns
---

# Modern CSS Selectors Quick Reference

Comprehensive reference for modern CSS selectors including :has(), :is(), :where(), :not(), :nth-child(), :focus-visible, attribute selectors, and combinators.

## Table of Contents

1. [:has() - Parent Selector](#has---parent-selector)
2. [:is() - Selector List](#is---selector-list)
3. [:where() - Zero Specificity](#where---zero-specificity)
4. [:not() - Negation](#not---negation)
5. [:nth-child() - Positional](#nth-child---positional)
6. [:focus-visible - Keyboard Focus](#focus-visible---keyboard-focus)
7. [Attribute Selectors](#attribute-selectors)
8. [Combinators](#combinators)
9. [Specificity Patterns](#specificity-patterns)
10. [Common Use Cases](#common-use-cases)

---

## :has() - Parent Selector

Select parent elements based on their descendants.

### Syntax
```css
parent:has(selector) { }
```

### Common Patterns

#### Style card based on content
```css
/* Card with image */
.card:has(img) {
  display: grid;
  grid-template-columns: 200px 1fr;
}

/* Card without image */
.card:not(:has(img)) {
  display: block;
  max-width: 600px;
}
```

#### Form validation styling
```css
.form-group:has(input:invalid) {
  border-left: 3px solid #ef4444;
  background-color: #fef2f2;
}

.form-group:has(input:valid) {
  border-left: 3px solid #10b981;
  background-color: #f0fdf4;
}

.form-group:has(input:focus) {
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}
```

#### Interactive highlights
```css
.list-item:has(button:hover) {
  background-color: #f3f4f6;
  transform: translateX(4px);
}

.card:has(a:hover) {
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  transform: translateY(-4px);
}
```

#### Empty state detection
```css
.gallery:not(:has(img)) {
  min-height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f9fafb;
  border: 2px dashed #d1d5db;
}

.gallery:not(:has(img))::after {
  content: "No images to display";
  color: #6b7280;
}
```

#### CSS-only tabs/accordions
```css
.accordion-item:has(input[type="checkbox"]:checked) .accordion-content {
  max-height: 500px;
  opacity: 1;
  padding: 1rem;
}

.tabs:has(#tab1:checked) #panel1,
.tabs:has(#tab2:checked) #panel2 {
  display: block;
}
```

#### Quantity-based styling
```css
.grid:has(> .item:nth-child(n+7)) {
  /* 7+ items - use 4 columns */
  grid-template-columns: repeat(4, 1fr);
}

.grid:has(> .item:nth-child(n+4):nth-child(-n+6)) {
  /* 4-6 items - use 3 columns */
  grid-template-columns: repeat(3, 1fr);
}
```

---

## :is() - Selector List

Group selectors with maintained specificity.

### Syntax
```css
:is(selector1, selector2, selector3) { }
```

### Common Patterns

#### Multiple element types
```css
:is(h1, h2, h3, h4, h5, h6) {
  font-family: 'Inter', sans-serif;
  font-weight: 700;
  line-height: 1.2;
}

:is(h1, h2, h3) {
  color: #1f2937;
}
```

#### State combinations
```css
button:is(:hover, :focus-visible, :active) {
  outline: 2px solid #3b82f6;
  outline-offset: 2px;
}

input:is(:hover, :focus) {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}
```

#### Form element grouping
```css
:is(input, select, textarea):is(:focus, :focus-visible) {
  outline: 2px solid #3b82f6;
  border-color: #3b82f6;
}

:is(input, select, textarea):disabled {
  opacity: 0.6;
  cursor: not-allowed;
  background-color: #f3f4f6;
}
```

#### Complex nested selectors
```css
/* Before: */
article h2,
aside h2,
section h2 {
  font-size: 1.5rem;
}

/* After: */
:is(article, aside, section) h2 {
  font-size: 1.5rem;
}
```

#### Data attribute targeting
```css
:is([data-state="loading"], [data-state="pending"], [data-state="processing"]) {
  pointer-events: none;
  opacity: 0.6;
}

:is([data-theme="dark"], [data-mode="night"]) {
  --bg-color: #1f2937;
  --text-color: #f9fafb;
}
```

---

## :where() - Zero Specificity

Same as :is() but with zero specificity (easy to override).

### Syntax
```css
:where(selector1, selector2) { }
```

### Common Patterns

#### Base styles (easy to override)
```css
:where(button, .btn) {
  /* Specificity: 0,0,0 - easily overridden */
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 0.375rem;
}

/* Simple class overrides */
.btn-large {
  /* Specificity: 0,1,0 - wins */
  padding: 1rem 2rem;
}
```

#### Reset styles
```css
:where(ul, ol)[role="list"] {
  list-style: none;
  padding: 0;
  margin: 0;
}

:where(h1, h2, h3, h4, h5, h6) {
  margin: 0;
  font-weight: inherit;
  font-size: inherit;
}
```

#### Link defaults
```css
:where(a) {
  color: inherit;
  text-decoration: none;
}

/* Easy to override */
.nav-link {
  color: #3b82f6;
}
```

#### Form defaults
```css
:where(input, select, textarea) {
  font-family: inherit;
  font-size: 100%;
  line-height: 1.5;
  margin: 0;
}
```

#### Theme defaults
```css
:where([data-theme="dark"]) :where(h1, h2, h3, p) {
  color: #f9fafb;
}

:where([data-theme="dark"]) :where(input, textarea) {
  background-color: #374151;
  color: #f9fafb;
}
```

---

## :not() - Negation

Exclude elements from selection.

### Syntax
```css
:not(selector) { }
:not(selector1, selector2) { } /* Multiple */
```

### Common Patterns

#### Exclude specific elements
```css
button:not(.btn-danger) {
  background-color: #3b82f6;
}

button:not(.btn-danger):not(.btn-ghost):not(:disabled) {
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}
```

#### All but first/last
```css
.list-item:not(:first-child) {
  margin-top: 1rem;
}

.list-item:not(:last-child) {
  border-bottom: 1px solid #e5e7eb;
  padding-bottom: 1rem;
}
```

#### Form validation
```css
input:not(:invalid):not(.error):focus {
  border-color: #10b981;
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
}

input:not(:placeholder-shown):invalid {
  border-color: #ef4444;
}
```

#### Accessibility checks
```css
img:not([alt]) {
  /* Highlight images missing alt text */
  outline: 3px solid #ef4444;
}

a:not([href]) {
  color: inherit;
  cursor: default;
}
```

#### Type exclusions
```css
input:not([type="checkbox"]):not([type="radio"]):not([type="hidden"]) {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #d1d5db;
}
```

#### Combining with :has()
```css
.card:not(:has(img)) {
  padding: 2rem;
}

.form:not(:has(input:invalid)) .submit-btn {
  opacity: 1;
  cursor: pointer;
}
```

---

## :nth-child() - Positional

Select elements based on their position.

### Syntax
```css
:nth-child(n)        /* Number */
:nth-child(odd)      /* Keyword */
:nth-child(even)     /* Keyword */
:nth-child(2n+1)     /* Formula */
:nth-child(n+3)      /* Starting from */
:nth-child(-n+5)     /* First n */
```

### Common Patterns

#### Zebra striping
```css
tr:nth-child(odd) {
  background-color: #f9fafb;
}

tr:nth-child(even) {
  background-color: #ffffff;
}
```

#### Every nth element
```css
.grid-item:nth-child(3n) {
  /* Every 3rd item */
  grid-column: span 2;
}

.grid-item:nth-child(5n) {
  /* Every 5th item */
  background-color: #fef3c7;
}
```

#### First/last n elements
```css
.list-item:nth-child(-n+3) {
  /* First 3 items */
  font-weight: 600;
  background-color: #eff6ff;
}

.list-item:nth-last-child(-n+3) {
  /* Last 3 items */
  opacity: 0.6;
}
```

#### Range selection
```css
.item:nth-child(n+4):nth-child(-n+8) {
  /* Items 4-8 */
  border-left: 3px solid #3b82f6;
}
```

#### Color patterns
```css
.tag:nth-child(5n+1) { background-color: #ef4444; }
.tag:nth-child(5n+2) { background-color: #3b82f6; }
.tag:nth-child(5n+3) { background-color: #10b981; }
.tag:nth-child(5n+4) { background-color: #f59e0b; }
.tag:nth-child(5n) { background-color: #8b5cf6; }
```

#### Animation delays
```css
.fade-in:nth-child(1) { animation-delay: 0s; }
.fade-in:nth-child(2) { animation-delay: 0.1s; }
.fade-in:nth-child(3) { animation-delay: 0.2s; }

/* Or formula */
.fade-in:nth-child(n) {
  animation-delay: calc(0.1s * (var(--index)));
}
```

#### Quantity queries
```css
/* Exactly 4 items */
li:first-child:nth-last-child(4),
li:first-child:nth-last-child(4) ~ li {
  width: 25%;
}

/* 5+ items */
li:first-child:nth-last-child(n+5),
li:first-child:nth-last-child(n+5) ~ li {
  width: 20%;
}
```

---

## :focus-visible - Keyboard Focus

Show focus only for keyboard navigation.

### Syntax
```css
:focus-visible { }    /* Keyboard navigation only */
:focus-within { }     /* Parent when child focused */
```

### Common Patterns

#### Keyboard-only focus
```css
button:focus-visible {
  outline: 2px solid #3b82f6;
  outline-offset: 2px;
}

button:focus:not(:focus-visible) {
  /* Mouse click - no outline */
  outline: none;
}
```

#### Enhanced navigation
```css
a:focus-visible {
  outline: 2px dashed #3b82f6;
  outline-offset: 4px;
  background-color: #eff6ff;
  border-radius: 0.25rem;
}
```

#### Form container focus
```css
.form-group:focus-within {
  background-color: #eff6ff;
  border-left: 3px solid #3b82f6;
}

.form-group:focus-within label {
  color: #1e40af;
  font-weight: 600;
}
```

#### Search box expansion
```css
.search-container:focus-within {
  width: 400px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.search-container:focus-within .search-suggestions {
  display: block;
  opacity: 1;
}
```

#### Card interaction
```css
.card:focus-within {
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
  border-color: #3b82f6;
}
```

#### Skip link visibility
```css
.skip-link {
  position: absolute;
  top: -100px;
}

.skip-link:focus-visible {
  top: 0;
  z-index: 9999;
  padding: 1rem 2rem;
  background-color: #1f2937;
  color: white;
}
```

---

## Attribute Selectors

Powerful attribute-based element selection.

### Syntax
```css
[attr]                  /* Has attribute */
[attr="value"]          /* Exact match */
[attr~="value"]         /* Word in list */
[attr|="value"]         /* Exact or prefix */
[attr^="value"]         /* Starts with */
[attr$="value"]         /* Ends with */
[attr*="value"]         /* Contains */
[attr operator value i] /* Case-insensitive */
```

### Common Patterns

#### Required fields
```css
input[required] {
  border-left: 3px solid #ef4444;
}

input[required]:valid {
  border-left-color: #10b981;
}
```

#### Input types
```css
input[type="email"] {
  background-image: url('icons/email.svg');
  background-position: right 0.5rem center;
  background-repeat: no-repeat;
}

input[type="password"] {
  font-family: 'monospace';
  letter-spacing: 0.1em;
}
```

#### External links
```css
a[href^="http://"],
a[href^="https://"] {
  padding-right: 1.25rem;
  background-image: url('icons/external-link.svg');
  background-position: right center;
}

a[href^="mailto:"] {
  color: #3b82f6;
  text-decoration: underline;
}
```

#### File types
```css
a[href$=".pdf"]::after {
  content: " (PDF)";
  font-size: 0.75rem;
  color: #ef4444;
}

a[href$=".doc"]::after,
a[href$=".docx"]::after {
  content: " (Word)";
  color: #2563eb;
}
```

#### Data attributes
```css
[data-state="loading"] {
  pointer-events: none;
  opacity: 0.6;
}

[data-state="error"] {
  background-color: #fef2f2;
  border-color: #ef4444;
}

[data-state="success"] {
  background-color: #f0fdf4;
  border-color: #10b981;
}
```

#### ARIA attributes
```css
[aria-expanded="true"] .icon-chevron {
  transform: rotate(180deg);
}

[aria-disabled="true"] {
  opacity: 0.5;
  cursor: not-allowed;
}

[aria-current="page"] {
  font-weight: 700;
  border-left: 3px solid #3b82f6;
}
```

#### Case-insensitive matching
```css
a[href$=".PDF" i]::after,
a[href$=".pdf" i]::after {
  content: " (PDF)";
}
```

---

## Combinators

Select elements based on relationships.

### Syntax
```css
parent descendant    /* Descendant (any depth) */
parent > child       /* Direct child only */
element + adjacent   /* Immediately following */
element ~ sibling    /* All following siblings */
```

### Common Patterns

#### Descendant
```css
article p {
  line-height: 1.6;
  margin-bottom: 1rem;
}

.card a {
  color: #3b82f6;
  text-decoration: none;
}
```

#### Direct child
```css
nav > ul {
  display: flex;
  gap: 1rem;
  list-style: none;
}

.container > * {
  margin-bottom: 1rem;
}
```

#### Adjacent sibling
```css
h2 + p {
  /* Paragraph immediately after h2 */
  font-size: 1.125rem;
  font-weight: 500;
}

label + input {
  margin-top: 0.25rem;
}
```

#### General sibling
```css
h2 ~ p {
  /* All paragraphs after h2 */
  text-align: left;
}

input:checked ~ label {
  font-weight: 600;
  color: #1f2937;
}
```

#### Combined patterns
```css
.form-field + .form-field {
  margin-top: 1.5rem;
}

.breadcrumb > li + li::before {
  content: "/";
  margin: 0 0.5rem;
  color: #9ca3af;
}
```

#### Checkbox/radio UI
```css
input[type="checkbox"]:checked + label {
  color: #10b981;
  font-weight: 600;
}

input[type="radio"]:checked ~ .radio-content {
  display: block;
  padding: 1rem;
  background-color: #f0fdf4;
}
```

---

## Specificity Patterns

Understanding and managing CSS specificity.

### Specificity Values
- Inline styles: `1,0,0,0`
- IDs: `0,1,0,0`
- Classes/attributes/pseudo-classes: `0,0,1,0`
- Elements/pseudo-elements: `0,0,0,1`
- `:where()` always: `0,0,0,0`
- `:is()/:not()/:has()`: specificity of most specific argument

### Common Patterns

#### Use :where() for base styles
```css
/* Specificity: 0,0,0,0 */
:where(.btn) {
  padding: 0.5rem 1rem;
}

/* Specificity: 0,0,1,0 - easily wins */
.btn-primary {
  background-color: #3b82f6;
}
```

#### Use :is() for grouping
```css
/* Specificity: 0,0,1,0 (from .active) */
:is(.active, p) {
  font-weight: 600;
}
```

#### Layer specificity strategically
```css
/* Layer 1: Resets - 0 specificity */
:where(*, *::before, *::after) {
  box-sizing: border-box;
}

/* Layer 2: Elements - 0,0,0,1 */
button {
  font-family: inherit;
}

/* Layer 3: Utilities - 0,0,1,0 */
.text-center { text-align: center; }

/* Layer 4: Components - 0,0,1,0 to 0,0,2,0 */
.btn { padding: 0.5rem 1rem; }
.btn.btn-large { padding: 1rem 2rem; }

/* Layer 5: States - 0,0,2,0 */
.btn:hover { transform: translateY(-2px); }
```

---

## Common Use Cases

### No-JS Accordions
```css
details {
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  padding: 1rem;
}

details summary {
  cursor: pointer;
  font-weight: 600;
  list-style: none;
}

details summary::before {
  content: "▶";
  margin-right: 0.5rem;
  transition: transform 0.3s;
}

details[open] summary::before {
  transform: rotate(90deg);
}

details:has(summary:hover) {
  border-color: #3b82f6;
  background-color: #eff6ff;
}
```

### Form Validation UI
```css
.form-field:has(input:not(:placeholder-shown):invalid) {
  border-left: 3px solid #ef4444;
  background-color: #fef2f2;
}

.form-field:has(input:not(:placeholder-shown):valid) {
  border-left: 3px solid #10b981;
  background-color: #f0fdf4;
}

.error-message {
  display: none;
  color: #ef4444;
}

.form-field:has(input:invalid:not(:placeholder-shown)) .error-message {
  display: block;
}
```

### Interactive Cards
```css
.card {
  border: 1px solid #e5e7eb;
  transition: all 0.3s;
}

.card:has(a:hover),
.card:has(button:hover) {
  border-color: #3b82f6;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  transform: translateY(-4px);
}
```

### Quantity Queries
```css
/* Exactly 4 items */
li:first-child:nth-last-child(4),
li:first-child:nth-last-child(4) ~ li {
  width: 25%;
}

/* 5-8 items */
li:first-child:nth-last-child(n+5):nth-last-child(-n+8),
li:first-child:nth-last-child(n+5):nth-last-child(-n+8) ~ li {
  width: calc(100% / 4);
}

/* 9+ items - switch to grid */
ul:has(> li:nth-child(9)) {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
}
```

## Browser Support

### :has()
- Chrome 105+
- Safari 15.4+
- Firefox 121+

**Fallback:**
```css
@supports selector(:has(*)) {
  .card:has(img) {
    display: grid;
  }
}
```

### :is(), :where()
- Chrome 88+
- Safari 14+
- Firefox 78+

### :focus-visible
- Chrome 86+
- Safari 15.4+
- Firefox 85+

## Performance Tips

1. **Scope :has() queries**
   ```css
   /* SLOW */
   body:has(.modal-open) { }

   /* BETTER */
   .modal-wrapper:has(.modal.is-open) { }
   ```

2. **Use specific selectors**
   ```css
   /* SLOW */
   div div div p { }

   /* FAST */
   .article-content p { }
   ```

3. **Avoid universal selectors in :has()**
   ```css
   /* SLOW */
   :has(*) { }

   /* BETTER */
   .container:has(.specific-class) { }
   ```

This reference covers the most common modern CSS selector patterns. Use these to reduce JavaScript dependencies, create more maintainable stylesheets, and build accessible interfaces.
