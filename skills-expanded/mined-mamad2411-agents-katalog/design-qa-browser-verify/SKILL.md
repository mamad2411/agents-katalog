---
name: design-qa-browser-verify
description: Validate generated pages against DESIGN.md specs via browser tools — catch layout drift, brand violations, console errors, and visual regression. Auto-repair mode feeds findings back for a refinement pass.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [design, qa, verification, browser, visual, brand-consistency, auto-repair]
    triggers: [design-qa, design-verify, browser-verify, visual-regression, brand-check, layout-check, responsive-check, design-spec-validation]
    related_skills: [web-app-qa, design-md, excalidraw, gsap-animations, service-site-design]
---

# Design QA Browser Verify

> Use Hermes browser tools to validate a generated page against DESIGN.md specs — layout, responsiveness, brand consistency, and console errors — then auto-repair in a refinement loop.

## When to Use

- After generating a new page or component (via `sketch`, `claude-design`, `pretext`, etc.)
- Before shipping a design to production — design QA is a pre-deployment gate
- When a design spec references specific colors, spacing, breakpoints, or brand elements
- When a scroll-world, service site, or landing page looks "off" but you can't pinpoint why
- After any auto-repair / code-fix action on a design page

## Workflow

```
DESIGN.md Spec → Browser Capture → Elements Checked   → Findings → Pass?
                                              ↓                       ↓ no
                                     Refinement Pass (auto-repair) ←────
                                              ↓
                                        Re-verify ←────────────────────
                                              ↓ yes
                                        ✅ Done
```

### Step 1: Extract Design Spec

Read the DESIGN.md (or visual spec) to build a checklist of measurable assertions:

```markdown
## Design Spec Assertions (from DESIGN.md)
- Primary color: `#1a365d` (appears in header bg, footer bg, primary buttons)
- Secondary color: `#3182ce` (appears in links, secondary buttons, accents)
- Font stack: `Inter, system-ui, sans-serif`
- Max content width: 1200px
- Breakpoints: 768px (tablet), 480px (mobile)
- Header height: ~80px
- Footer: 4-column layout, dark bg
- CTA button: rounded (`border-radius: 8px`), primary color bg, white text
```

For `design-md` skills, extract the token spec directly from its structured format.

### Step 2: Browser Capture & Element Audit

Navigate to the generated page and capture it with browser tools:

```bash
# Navigate to page
browser_navigate(url="http://localhost:PORT/path")

# Capture with SOM for element identification
browser_vision("Take a full-page screenshot of the design")
```

Check against assertions from Step 1:

```javascript
// Run in browser_console:
const assertions = {
  primaryColor: '#1a365d',
  secondaryColor: '#3182ce',
  fontStack: 'Inter, system-ui, sans-serif',
  maxWidth: '1200px',
  headerHeight: '80px'
};

const results = {};

// Check primary color usage
const headerBg = getComputedStyle(document.querySelector('header')).backgroundColor;
const headerBgHex = rgbToHex(headerBg);
results.headerBg = headerBgHex === assertions.primaryColor;

// Check font stack
const bodyFont = getComputedStyle(document.body).fontFamily;
results.bodyFont = bodyFont.includes('Inter');

// Check max-width on main container
const mainMaxWidth = getComputedStyle(document.querySelector('main')).maxWidth;
results.mainMaxWidth = mainMaxWidth === assertions.maxWidth || mainMaxWidth === assertions.maxWidth + 'px';

// Check header height
const headerH = getComputedStyle(document.querySelector('header')).height;
results.headerHeight = headerH === assertions.headerHeight || headerH === assertions.headerHeight + 'px';

// Collect all results
console.table(results);
JSON.stringify(results, null, 2);
```

#### Design Assertion Check Types

| Check | Method | Pass/Fail |
|-------|--------|-----------|
| **Color matches spec** | `getComputedStyle(el).backgroundColor` → hex | Exact hex match |
| **Font family** | `getComputedStyle(body).fontFamily` | Contains spec'd font name |
| **Max width** | `getComputedStyle(main).maxWidth` | Value matches spec |
| **Spacing / padding** | `getComputedStyle(el).padding` | Within tolerance (±4px) |
| **Border radius** | `getComputedStyle(el).borderRadius` | Matches spec |
| **Box shadow** | `getComputedStyle(el).boxShadow` | Non-none if spec'd |
| **Image present** | `document.querySelector('img').complete` | True with non-zero natural dimensions |
| **Heading hierarchy** | `document.querySelectorAll('h1, h2, h3').length` | At least one h1, logical hierarchy |
| **Link hover state** | JS hover simulation + check computed style | Hover color matches spec |
| **SVG/icon present** | `document.querySelectorAll('svg').length` | > 0 if design spec'd icons |

### Step 3: Responsiveness Check

Resize the viewport to each spec'd breakpoint and re-audit:

```javascript
// Run at each breakpoint
const breakpoints = [1200, 768, 480];

for (const width of breakpoints) {
  // Set viewport (via CDP or browser resize)
  // In Playwright: await page.setViewportSize({ width, height: 900 });
  
  const noHorizontalScroll = document.documentElement.scrollWidth <= window.innerWidth;
  const navVisible = window.getComputedStyle(document.querySelector('nav')).display !== 'none';
  const noOverflowHidden = window.getComputedStyle(document.body).overflow !== 'hidden';
  
  console.log(`Breakpoint ${width}px: scroll=${!noHorizontalScroll} nav=${navVisible} overflow-ok=${noOverflowHidden}`);
}
```

Check specifically for:
- **No horizontal scrollbar** at any breakpoint
- **Navigation** renders correctly at each breakpoint (hamburger vs full menu)
- **Images** don't overflow their containers
- **Text** doesn't overflow or get clipped
- **CTA and forms** remain usable (buttons not overlapping)

### Step 4: Console & Network Error Check

Always check console errors — a blank-looking render may hide JS failures:

```javascript
// Check for console errors
const consoleErrors = [];
performance.getEntriesByType('resource').filter(e => e.responseStatus >= 400).forEach(e => {
  consoleErrors.push(`${e.name} (${e.responseStatus})`);
});
console.log('Network errors:', consoleErrors.length ? consoleErrors : 'none');
```

| Signal | Action |
|--------|--------|
| Console errors | Fix JS bugs before re-verifying design |
| 404 CSS/JS chunks | Wait for compilation or restart dev server |
| Blank page with 200 HTTP | Likely JS crash — check `pageerror` handler |
| CORS errors | Check for system env var overrides |

### Step 5: Brand Consistency Check

For multi-page designs, verify consistent brand application across all pages:

```javascript
const pages = ['/', '/about', '/services', '/contact'];
let inconsistentElements = [];

for (const page of pages) {
  // Navigate to page
  const h1 = document.querySelector('h1')?.textContent || '(no h1)';
  const headerColor = getComputedStyle(document.querySelector('header')).backgroundColor;
  const ctaColor = getComputedStyle(document.querySelector('a[class*="cta"], button[class*="cta"]')).backgroundColor;
  
  inconsistentElements.push({
    page,
    h1,
    headerBg: headerColor,
    ctaBg: ctaColor
  });
}

console.table(inconsistentElements);
```

Cross-page brand checks:
- **Header bg** consistent across all pages
- **CTA button** same color, shape, and hover state
- **Footer** identical across pages
- **Typography** consistent (same font sizes for h1, h2, p)
- **Spacing rhythm** consistent (same padding/margin for similar elements)

### Step 6: Visual Regression (Optional)

Compare against a known-good screenshot baseline:

```bash
# Take baseline capture
browser_vision("Capture full page at 1440px width")
# Save reference image
browser_vision("Capture full page at 1440px width after fix")
```

For automated comparison, use the `vision_analyze` tool on before/after captures:
```
Are the header colors (#1a365d) consistent between these two pages?
```

### Step 7: Auto-Repair Loop (When Findings Exist)

Feed design violations back into a refinement pass:

```
🔴 Design QA Findings:
1. Header bg is #1a3d5d, expected #1a365d
2. Footer is missing 4-column layout (renders as single column)
3. CTA border-radius is 4px, expected 8px
4. Font-stack falls back to system-ui (Inter not applied)

→ Route to refinement: "Fix 4 design QA violations against DESIGN.md"
→ After fix: Re-run steps 2-6
→ Max 3 repair iterations before escalation
```

Pass the findings as structured context:

```
Fix these DESIGN.md violations on the generated page:
1. Header: change background-color from #1a3d5d to #1a365d
2. Footer: implement 4-column grid layout (currently single column)
3. CTA: set border-radius to 8px (currently 4px)
4. Font: ensure Inter font is loaded and applied (currently system-ui fallback)
```

## Integration with Companion Skills

| Skill | Integration Point |
|-------|------------------|
| **`web-app-qa`** | Use its browser QA templates for console error checking and multi-role verification, then layer design assertions on top |
| **`design-md`** | Extract token spec (colors, fonts, spacing) from DESIGN.md to build automated assertions |
| **`excalidraw`** | Compare wireframe layout (from Excalidraw JSON) against rendered page element positions |
| **`gsap-animations`** | After verifying static design, check scroll-triggered animation timing and final states |
| **`service-site-design`** | Validate that generated service sites maintain brand-consistency rules (per-site variety, hard design laws) |
| **`sketch`** | Run design QA after each sketch variant to validate before presenting to user |

## Verification

Run this checklist after authoring a design-qa-browser-verify pass:

- [ ] Extracted at least 5 measurable assertions from DESIGN.md
- [ ] Browser open and navigated to target page
- [ ] Colors match spec within tolerance (±1 hex digit for manual approximation)
- [ ] No console errors on the page
- [ ] No 4xx/5xx network errors for CSS/JS/font assets
- [ ] Responsive at all spec'd breakpoints (no horizontal scroll)
- [ ] Brand consistent across all pages (header, footer, CTA match)
- [ ] Either all assertions pass or auto-repair loop triggered
- [ ] Max 3 repair iterations before escalating

## Pitfalls

- **Computed color values normalize to rgb()** — `getComputedStyle(el).backgroundColor` returns `rgb(26, 54, 93)` not `#1a365d`. You need a hex conversion function or an approximate match (±1 per channel).
- **Font-family includes fallbacks** — `getComputedStyle(body).fontFamily` returns the full stack like `Inter, system-ui, sans-serif`. Check with `.includes('Inter')` not strict equality.
- **CSS transitions/animations in progress** — Capturing during a transition gives intermediate values. Wait 300ms after page load before measuring.
- **Font loading race** — Fonts (especially Inter, system fonts) may not be loaded when computed style is read. The `font-family` in computed style includes Inter in the stack, but it may render in a fallback. Check `document.fonts.ready` before taking measurements.
- **Dev server chunk compilation** — After clean start, JS/CSS chunks may 404 until compiled. Wait for chunk availability before design QA (see web-app-qa Pitfalls).
- **Auto-repair loop needs clear stop condition** — Without a max iteration count, the refinement loop can oscillate (fix A breaks B, fix B breaks A). Hard limit at 3 iterations, then escalate to human.
- **Screenshots are resolution-dependent** — A capture at 1440px may look perfect but break at 768px. Always check all spec'd breakpoints.
- **Design QA is not functional QA** — `web-app-qa` checks for JS crashes and API errors. Design QA checks for visual fidelity. Both are needed and complementary.
