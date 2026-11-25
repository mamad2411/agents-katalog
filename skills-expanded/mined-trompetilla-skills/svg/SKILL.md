---
name: SVG
description: Create and optimize SVG graphics with proper viewBox, accessibility, and CSS styling.
metadata: {"clawdbot":{"emoji":"📐","requires":{},"os":["linux","darwin","win32"]}}
---

## viewBox Essentials

```svg
<svg viewBox="min-x min-y width height">
```

- `viewBox` defines the internal coordinate system
- `width`/`height` on `<svg>` define the display size
- Without viewBox, SVG won't scale responsively

```svg
<!-- ✅ Scales to any size -->
<svg viewBox="0 0 24 24">
  <circle cx="12" cy="12" r="10"/>
</svg>

<!-- ❌ Fixed 24x24, won't scale -->
<svg width="24" height="24">
  <circle cx="12" cy="12" r="10"/>
</svg>
```

Always include viewBox. Remove fixed `width`/`height` for responsive SVGs.

## Coordinates Must Match viewBox

Elements outside the viewBox are invisible:

```svg
<!-- ❌ Circle at 500,500 but viewBox only covers 0-100 -->
<svg viewBox="0 0 100 100">
  <circle cx="500" cy="500" r="40"/>  <!-- invisible -->
</svg>

<!-- ✅ Circle within viewBox range -->
<svg viewBox="0 0 100 100">
  <circle cx="50" cy="50" r="40"/>
</svg>
```

## Accessibility

**Informative SVGs (convey meaning):**
```html
<svg role="img" aria-labelledby="chart-title">
  <title id="chart-title">Sales increased 25% in Q4</title>
  <desc id="chart-desc">Bar chart showing quarterly revenue...</desc>
  <!-- paths -->
</svg>
```

**Decorative SVGs (purely visual):**
```html
<svg aria-hidden="true" focusable="false">
  <!-- paths -->
</svg>
```

Key rules:
- `role="img"` ensures assistive tech treats it as an image
- `<title>` must be the first child of `<svg>`
- `aria-labelledby` is more reliable than `aria-label` for SVG
- `focusable="false"` prevents tab stops in IE/Edge
- IDs must be unique across all inline SVGs on the page

## CSS Styling

**currentColor inheritance:**
```svg
<svg fill="currentColor">
  <path d="..."/>
</svg>
```

```css
.icon { color: blue; }
.icon:hover { color: red; }  /* SVG changes too */
```

**CSS custom properties inside SVG:**
```svg
<svg>
  <style>
    .primary { fill: var(--icon-primary, currentColor); }
    .secondary { fill: var(--icon-secondary, #ccc); }
  </style>
  <path class="primary" d="..."/>
  <path class="secondary" d="..."/>
</svg>
```

**Limitations:**
- `<img src="icon.svg">` cannot be styled with CSS
- `background-image: url(icon.svg)` cannot be styled
- Only inline SVG allows full CSS control

## SVGO Optimization

Critical config to preserve functionality:

```javascript
// svgo.config.mjs
export default {
  plugins: [{
    name: 'preset-default',
    params: {
      overrides: {
        removeViewBox: false,      // NEVER remove
        removeTitle: false,        // Keep for accessibility
        removeDesc: false,         // Keep for accessibility
        cleanupIds: false,         // Keep if CSS/JS references IDs
      }
    }
  }]
};
```

Safe to remove: metadata, comments, empty groups, editor cruft.

Typical reduction: 50-80% for Illustrator/Figma exports.

## Embedding Methods

| Method | CSS Styling | Caching | Best for |
|--------|-------------|---------|----------|
| Inline `<svg>` | ✅ Full | ❌ No | Dynamic styling, animation |
| `<img src>` | ❌ No | ✅ Yes | Static images |
| Symbol sprite `<use>` | ✅ Partial | ✅ Yes | Icon systems |
| CSS background | ❌ No | ✅ Yes | Decorative patterns |

## Performance

Benchmark (1000 icons):
- `<img>` data URI: 67ms (fastest)
- Inline SVG optimized: 75ms
- Symbol sprite: 99ms
- External sprite: 126ms (very slow in Chrome)

For many repeated icons, use symbol sprites. For few icons, inline is fine.

## Namespace

External `.svg` files require xmlns:

```svg
<!-- ✅ Works as external file -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">

<!-- ❌ May fail when loaded externally -->
<svg viewBox="0 0 24 24">
```

Inline SVG in HTML5 doesn't require xmlns, but including it doesn't hurt.

## Common Mistakes

- Missing viewBox—SVG displays at fixed size or not at all
- Coordinates outside viewBox range—elements invisible
- Hardcoded `fill="#000"`—can't theme with CSS
- Using `<img>` when styling is needed—no CSS access
- SVGO removing viewBox or title—check output before deploying
- Duplicate IDs across multiple inline SVGs—CSS/JS breaks
- `preserveAspectRatio="none"` without understanding—causes distortion
- viewBox with units `viewBox="0 0 100px 100px"`—viewBox uses unitless values
- Empty groups and paths from editors—bloat without purpose
