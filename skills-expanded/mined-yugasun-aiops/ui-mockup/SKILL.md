---
name: ui-mockup
description: >
  Generate HTML/CSS mockups for UI design. Produces browser-previewable
  mockup files with placeholder data. Use when the user says ui-mockup,
  mockup, design UI, wireframe, or needs visual reference for a feature.
---

# UI Mockup

Generate static HTML mockups as visual reference for Builder implementation.

## Output structure

```
.scratch/<feature>/mockups/
├── index.html              # Entry page linking to all mockups
├── <page-name>.html        # One HTML per page/state
└── design-notes.md         # Design decisions and interactions
```

## Mockup rules

### HTML

- Self-contained: open directly in browser, no build step
- Inline CSS via `<style>` or CDN frameworks (Tailwind CDN preferred)
- Semantic HTML structure
- Placeholder data marked with `[placeholder]`

### CSS

- 8px grid spacing system
- CSS variables for colors and spacing
- Responsive: Desktop (>1024px), Tablet (768-1024px), Mobile (<768px)
- Use media queries for responsive breakpoints

### States

Show key states as separate files or CSS classes:
- Default
- Hover / Active
- Error / Validation
- Loading / Empty
- Success

### No JavaScript logic

- No event handlers
- No dynamic data fetching
- Interactions described in `design-notes.md`
- CSS `:hover`, `:active`, `:focus` allowed for visual states

## Template

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[Page Name] — Mockup</title>
  <style>
    :root {
      --color-primary: #1a73e8;
      --color-error: #d93025;
      --color-success: #188038;
      --spacing-unit: 8px;
      --font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: var(--font-family); padding: calc(var(--spacing-unit) * 3); }
    /* page-specific styles */
  </style>
</head>
<body>
  <!-- mockup content -->
</body>
</html>
```

## index.html

Entry page with links to all mockup files:

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <title>Mockups — [Feature Name]</title>
  <style>
    body { font-family: sans-serif; padding: 32px; max-width: 600px; }
    h1 { margin-bottom: 16px; }
    ul { list-style: none; }
    li { margin: 8px 0; }
    a { color: #1a73e8; text-decoration: none; }
    a:hover { text-decoration: underline; }
  </style>
</head>
<body>
  <h1>[Feature Name] Mockups</h1>
  <ul>
    <li><a href="page-name.html">Page Name</a> — description</li>
  </ul>
</body>
</html>
```

## Design notes format

Write `design-notes.md` with:

1. **Pages** — table of all mockup files and their purpose
2. **Design Decisions** — colors, fonts, spacing rationale
3. **Interactions** — describe hover, click, transitions in words
4. **Responsive** — breakpoint behavior for each page
5. **Components** — table of UI components used and their variants

## Flow

1. Read `.scratch/<feature>/NOTES.md` and `tech-spec.md` for context
2. Identify pages and states needed
3. Generate `index.html` first
4. Generate each page HTML
5. Write `design-notes.md`
6. Report: list of generated files + open browser command

## Integration with design systems

If the target project has a design system:
- Use its color tokens as CSS variables
- Match its component patterns
- Reference its component names in design-notes.md
