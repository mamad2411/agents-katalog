---
name: design-inspector
description: Extract design tokens, component inventory, and interaction patterns from any live website using Playwright MCP. Outputs structured design system docs without cloning. Triggers on "inspect design", "extract design tokens", "analyze design", "design audit", "what design system does this site use". Provide the target URL as an argument.
argument-hint: "<url>"
user-invocable: true
---

# Design Inspector

Inspect **$ARGUMENTS** and extract a complete design system analysis.

This is a **read-only reconnaissance** skill — it analyzes a live website's visual design, extracts tokens, documents components, and outputs structured specs. It does NOT clone or rebuild anything.

Use this when you want to:
- Understand a site's design system before building something similar
- Extract exact colors, typography, spacing for use in your own project
- Document component patterns and interaction behaviors
- Create a design reference for a frontend team

## Requirements

- **Playwright MCP** must be available (`browser_navigate`, `browser_evaluate`, `browser_take_screenshot`, `browser_snapshot`, `browser_resize`, `browser_hover`, `browser_click`)

## Execution

### Step 1: Navigate and Screenshot

```
browser_navigate → $ARGUMENTS
browser_resize → 1440x900 → browser_take_screenshot (desktop)
browser_resize → 768x1024 → browser_take_screenshot (tablet)
browser_resize → 390x844 → browser_take_screenshot (mobile)
```

### Step 2: Extract Design Tokens

Run via `browser_evaluate`:

```javascript
(function() {
  const body = document.body;
  const allEls = [...document.querySelectorAll('*')].slice(0, 500);

  // Colors
  const colors = new Set();
  allEls.forEach(el => {
    const cs = getComputedStyle(el);
    [cs.color, cs.backgroundColor, cs.borderColor, cs.outlineColor].forEach(c => {
      if (c && c !== 'rgba(0, 0, 0, 0)' && c !== 'transparent') colors.add(c);
    });
  });

  // Typography
  const fonts = new Map();
  allEls.forEach(el => {
    const cs = getComputedStyle(el);
    const key = `${cs.fontFamily}|${cs.fontSize}|${cs.fontWeight}|${cs.lineHeight}`;
    if (!fonts.has(key)) {
      fonts.set(key, {
        family: cs.fontFamily,
        size: cs.fontSize,
        weight: cs.fontWeight,
        lineHeight: cs.lineHeight,
        letterSpacing: cs.letterSpacing,
        tag: el.tagName,
        sample: el.textContent?.trim().slice(0, 50)
      });
    }
  });

  // Spacing scale
  const spacings = new Set();
  allEls.slice(0, 200).forEach(el => {
    const cs = getComputedStyle(el);
    ['paddingTop','paddingRight','paddingBottom','paddingLeft',
     'marginTop','marginRight','marginBottom','marginLeft','gap'].forEach(p => {
      const v = cs[p];
      if (v && v !== '0px' && v !== 'auto' && v !== 'normal') spacings.add(v);
    });
  });

  // Border radii
  const radii = new Set();
  allEls.slice(0, 200).forEach(el => {
    const r = getComputedStyle(el).borderRadius;
    if (r && r !== '0px') radii.add(r);
  });

  // Shadows
  const shadows = new Set();
  allEls.slice(0, 200).forEach(el => {
    const s = getComputedStyle(el).boxShadow;
    if (s && s !== 'none') shadows.add(s);
  });

  // Breakpoints (from media queries in stylesheets)
  const breakpoints = new Set();
  try {
    [...document.styleSheets].forEach(sheet => {
      try {
        [...sheet.cssRules].forEach(rule => {
          if (rule.media) {
            const m = rule.media.mediaText;
            const match = m.match(/(\d+)px/g);
            if (match) match.forEach(bp => breakpoints.add(bp));
          }
        });
      } catch(e) {}
    });
  } catch(e) {}

  // Font sources
  const fontLinks = [...document.querySelectorAll('link[href*="font"], link[href*="Font"]')]
    .map(l => l.href);

  // Icons
  const iconLib = document.querySelector('[class*="lucide"]') ? 'Lucide' :
    document.querySelector('[class*="fa-"]') ? 'FontAwesome' :
    document.querySelector('[class*="material"]') ? 'Material' :
    document.querySelector('svg') ? 'Custom SVG' : 'Unknown';

  return JSON.stringify({
    colors: [...colors].sort(),
    typography: [...fonts.values()],
    spacing: [...spacings].sort((a,b) => parseFloat(a) - parseFloat(b)),
    borderRadii: [...radii].sort(),
    shadows: [...shadows],
    breakpoints: [...breakpoints].sort((a,b) => parseInt(a) - parseInt(b)),
    fontSources: fontLinks,
    iconLibrary: iconLib,
    svgCount: document.querySelectorAll('svg').length,
    totalElements: allEls.length
  }, null, 2);
})();
```

### Step 3: Component Inventory

Use `browser_snapshot` to get the DOM tree, then categorize:

- **Navigation**: headers, sidebars, bottom bars, breadcrumbs
- **Content**: cards, list items, grids, carousels
- **Actions**: buttons (variants), links, CTAs
- **Forms**: inputs, selects, checkboxes, toggles, search bars
- **Feedback**: modals, toasts, tooltips, popovers, alerts
- **Media**: images, videos, avatars, icons, illustrations
- **Layout**: containers, sections, dividers, spacers

For each distinct component, extract its computed styles via `browser_evaluate`.

### Step 4: Interaction Audit

**Scroll behaviors** — `browser_evaluate` with `window.scrollBy(0, 300)` repeatedly:
- Sticky/fixed elements
- Scroll-triggered animations
- Parallax effects
- Scroll-snap sections

**Hover states** — `browser_hover` on key interactive elements:
- Buttons, cards, nav items, links
- Record property changes

**Click behaviors** — `browser_click` on interactive elements:
- Tabs, dropdowns, accordions, modals
- Record transitions and state changes

### Step 5: Tech Stack Detection

Run via `browser_evaluate`:

```javascript
(function() {
  return JSON.stringify({
    framework: window.__NEXT_DATA__ ? 'Next.js' :
      window.__NUXT__ ? 'Nuxt' :
      document.querySelector('[ng-version]') ? 'Angular' :
      window.__REACT_DEVTOOLS_GLOBAL_HOOK__ ? 'React' :
      window.__VUE__ ? 'Vue' : 'Unknown',
    css: document.querySelector('[class*="tw-"]') || document.querySelector('[class*="flex"]') ? 'Tailwind (likely)' :
      document.querySelector('[class*="css-"]') ? 'CSS-in-JS' :
      document.querySelector('[class*="module"]') ? 'CSS Modules' : 'Vanilla/Custom',
    animations: window.gsap ? 'GSAP' :
      document.querySelector('[class*="framer"]') ? 'Framer Motion' :
      document.querySelector('.lenis') ? 'Lenis smooth scroll' : 'CSS transitions',
    lazyLoading: document.querySelector('img[loading="lazy"]') ? true : false,
    darkMode: window.matchMedia('(prefers-color-scheme: dark)').matches,
    viewport: { width: window.innerWidth, height: window.innerHeight }
  }, null, 2);
})();
```

## Output Format

Create a single structured report:

```markdown
# Design System Report: [Site Name]

**URL**: $ARGUMENTS
**Inspected**: [date]
**Tech Stack**: [framework] + [CSS approach] + [animation lib]

## Color Palette
| Token | Value | Usage |
|-------|-------|-------|
| primary | #xxx | Buttons, links |
| ... | ... | ... |

## Typography Scale
| Level | Family | Size | Weight | Line Height | Usage |
|-------|--------|------|--------|-------------|-------|
| h1 | ... | ... | ... | ... | Page titles |
| ... | ... | ... | ... | ... | ... |

## Spacing Scale
[Extracted spacing values organized into a scale]

## Border Radii
[Extracted radius values]

## Shadows / Elevation
[Extracted shadow values with usage context]

## Breakpoints
[Media query breakpoints]

## Component Inventory
[Table of components with variant counts and interaction types]

## Interaction Patterns
[Scroll behaviors, hover states, click interactions, animations]

## Assets
- Font sources: [links]
- Icon library: [name]
- SVG count: [n]
- Image strategy: [lazy loading, CDN, etc.]

## Recommendations
[Suggestions for implementing this design system in your own project]
```

Save to `docs/design-references/DESIGN_REPORT.md` (if in a project) or output directly.
