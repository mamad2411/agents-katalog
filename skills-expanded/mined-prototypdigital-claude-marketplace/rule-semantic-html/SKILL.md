---
name: semantic-html
description: Prefer native HTML elements over div+role soup; semantic elements are accessible by default
---

# Semantic HTML

Native HTML elements (`<button>`, `<nav>`, `<main>`, `<article>`, headings, lists) carry built-in accessibility semantics — role, name, keyboard behavior — that `<div>` and `<span>` do not. Reaching for a `<div>` + `role` + `tabIndex` + event handlers replicates what a single native element already provides, and gets it wrong more often than not.

## Rules

- **Use `<button>` for actions, `<a href>` for navigation.** A `<div onClick>` element is not keyboard-reachable by default, has no implicit role, and requires manual ARIA to announce its purpose to screen readers.
- **Use landmark elements to structure pages.** Every page should have exactly one `<main>`; navigation blocks go in `<nav>`; page-level complementary content goes in `<aside>`. Screen reader users navigate by landmark.
- **Use heading levels (`<h1>`–`<h6>`) to outline content.** Do not skip levels for visual effect; use CSS to control appearance. Each page should have one `<h1>`.
- **Use `<ul>`/`<ol>` for lists.** Groupings of links, options, or items that form a conceptual list should be marked up as such — screen readers announce the item count.
- **Use `<table>` for tabular data**, with `<th scope>` for headers. Never use a table for layout.
- **Do not add `role` to an element that already has that role.** `<nav role="navigation">` and `<button role="button">` are redundant.

## Examples

```html
<!-- BAD — all semantics must be bolted on manually and are easy to miss -->
<div class="btn" onclick="submit()" tabindex="0">Submit</div>
<div class="nav" role="navigation">...</div>
<div class="h2" style="font-size:1.5rem">Section Title</div>

<!-- GOOD — semantics are free with the right element -->
<button type="submit">Submit</button>
<nav aria-label="Main">...</nav>
<h2>Section Title</h2>
```

```tsx
// BAD — interactive list item built from scratch
<div role="listbox">
  {items.map(item => (
    <div
      key={item.id}
      role="option"
      tabIndex={0}
      onClick={() => select(item)}
      onKeyDown={e => e.key === 'Enter' && select(item)}
    >
      {item.label}
    </div>
  ))}
</div>

// GOOD — native select for simple cases; custom listbox only when native falls short
<select aria-label="Choose item">
  {items.map(item => (
    <option key={item.id} value={item.id}>{item.label}</option>
  ))}
</select>
```

## Gotchas

- Visual styling is not a reason to choose the wrong element. Style `<button>` to look like a link, or `<a>` to look like a button — do not swap the elements.
- `<section>` and `<article>` are only landmarks when they have an accessible name (`aria-label` or `aria-labelledby`). A nameless `<section>` is treated as a generic container.
- `<b>` and `<i>` have no semantic meaning in HTML5; use `<strong>` and `<em>` when emphasis matters to screen readers. Use `<b>`/`<i>` only for style-only text.
