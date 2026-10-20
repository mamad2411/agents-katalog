---
name: amplify-presentation
description: Generate polished, dark-themed HTML slide deck presentations using the Amplify design system. Creates single-file HTML presentations with smooth transitions, responsive layouts, and a professional Databricks-inspired dark teal + orange color palette. Use this skill when the user wants to create a slide deck, presentation, or pitch deck as an HTML file.
user-invocable: true
---

# Amplify Presentation Skill

Generate self-contained single-file HTML slide deck presentations with a polished dark theme, smooth slide transitions, responsive layouts, and professional styling.

## When to Use

- User asks for a "slide deck", "presentation", "pitch deck", or "slides"
- User wants an HTML presentation file
- User wants a dark-themed professional presentation
- User provides content and wants it formatted as slides

## Design System

### Color Palette

```javascript
const DB = {
  // Primary
  orange: '#FF3621',
  orangeLight: '#FF6B4A',
  orangeDim: 'rgba(255,54,33,0.12)',
  // Backgrounds
  teal: '#1B3139',
  tealDark: '#0F1F25',
  tealDeep: '#080F14',
  tealLight: '#2A4D5A',
  tealMid: '#1E3A44',
  // White overlays
  w: '#FFFFFF',
  w90: 'rgba(255,255,255,0.9)',
  w80: 'rgba(255,255,255,0.8)',
  w60: 'rgba(255,255,255,0.6)',
  w45: 'rgba(255,255,255,0.45)',
  w30: 'rgba(255,255,255,0.3)',
  w20: 'rgba(255,255,255,0.2)',
  w10: 'rgba(255,255,255,0.1)',
  w05: 'rgba(255,255,255,0.04)',
};
```

### Accent Colors (for categorization and variety)

| Name   | Hex       | Use Case                          |
|--------|-----------|-----------------------------------|
| Rose   | `#FB7185` | Alerts, quality, evaluation       |
| Cyan   | `#22D3EE` | Data, memory, infrastructure      |
| Gold   | `#F59E0B` | Governance, compliance, documents |
| Purple | `#A78BFA` | Builder, composition, agents      |
| Green  | `#64FFDA` | Code, framework, developer tools  |
| Amber  | `#F59E0B` | Horizon, future, stretch goals    |

### Typography

- **Font**: `'DM Sans', system-ui, sans-serif` (loaded from Google Fonts)
- **Headings (h1)**: `clamp(1.9rem, 4.3vw, 3rem)`, weight 800, letter-spacing -0.03em
- **Subheadings (h2)**: `clamp(1.1rem, 2vw, 1.35rem)`, weight 400, color w45
- **Body text**: 0.94-1.03rem, color w45-w60
- **Labels/badges**: 0.73-0.78rem, weight 800, letter-spacing 0.07-0.1em, uppercase
- **Monospace**: `monospace` for code/API snippets

### Slide Backgrounds

Alternate between two gradient patterns for visual rhythm:

```css
/* Pattern A: Radial from center */
radial-gradient(ellipse at 50% 35%, #162A34 0%, #080F14 70%)

/* Pattern B: Diagonal linear */
linear-gradient(160deg, #060D12, #0D1E27 40%, #132C38)
```

Vary the ellipse position (30% 30%, 50% 40%, 60% 30%) for subtle variation.

## Architecture: Single-File HTML

The entire presentation is a single `.html` file with no external dependencies (except Google Fonts). The structure is:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>PRESENTATION TITLE</title>
  <link rel="icon" href="data:image/svg+xml,...">
</head>
<body>
<div id="app"></div>
<script>
(() => {
  // 1. Color constants (DB object)
  // 2. Slides array (each slide = { id, bg, accent, body })
  // 3. CSS injected via document.createElement('style')
  // 4. Slide rendering + navigation logic
})();
</script>
</body>
</html>
```

## Slide Data Structure

Each slide is an object:

```javascript
{
  id: 'unique-slide-id',           // kebab-case identifier
  bg: `radial-gradient(...)`,       // CSS background
  accent: DB.orange,                // accent color for progress bar
  body: `<h1>...</h1><h2>...</h2><div class="...">...</div>`,  // HTML content
}
```

## Component Library

### 1. Cards (gap-card, cat-card, gov-f-card)

Glass-morphism cards with semi-transparent backgrounds:

```css
.card {
  padding: 14px-20px;
  border-radius: 12px-14px;
  background: rgba(255,255,255,0.04);    /* w05 */
  border: 1px solid rgba(255,255,255,0.1); /* w10 */
  text-align: left;
  display: flex;
  flex-direction: column;
  gap: 5px-7px;
  transition: all .3s;
}
.card:hover {
  transform: translateY(-3px);
  border-color: rgba(255,255,255,0.2);   /* w20 */
  background: rgba(255,255,255,0.06);
}
```

### 2. Icon Containers

Colored icon boxes with matching accent:

```css
.icon-box {
  width: 34px-44px;
  height: 34px-44px;
  border-radius: 9px-12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  /* Color variants: */
  background: rgba(ACCENT, 0.06-0.08);
  border: 1px solid rgba(ACCENT, 0.13-0.18);
}
```

### 3. Pills / Chips

Small tag-like elements:

```css
.pill {
  padding: 3px-5px 8px-16px;
  border-radius: 5px-20px;
  font-size: 0.88rem-1.03rem;
  font-weight: 600-700;
  /* Colored variant: */
  background: rgba(ACCENT, 0.07-0.12);
  border: 1px solid rgba(ACCENT, 0.18-0.3);
  color: ACCENT_LIGHT;
}
```

### 4. Phase Badges

Small uppercase labels for categorization:

```css
.phase-badge {
  font-size: 0.73rem;
  font-weight: 800;
  letter-spacing: 0.07em;
  text-transform: uppercase;
  padding: 2px 7px;
  border-radius: 4px;
  /* Position absolute top-right on cards */
  position: absolute;
  top: 9px;
  right: 9px;
}
```

### 5. Panels (found-panel)

Larger content panels with header bar:

```css
.panel {
  border-radius: 13px;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.1);
  overflow: hidden;
}
.panel-header {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 14px;
  font-size: 1.08rem;
  font-weight: 700;
  color: #fff;
  border-bottom: 1px solid rgba(255,255,255,0.1);
  /* Tinted background matching accent */
  background: rgba(ACCENT, 0.05-0.06);
}
.panel-body {
  padding: 12px 14px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}
```

### 6. Step Indicators

Numbered workflow steps:

```css
.step {
  display: flex;
  align-items: center;
  gap: 7px;
  padding: 4px 9px;
  border-radius: 6px;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.1);
}
.step-number {
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: rgba(255,255,255,0.08);
  font-size: 0.84rem;
  font-weight: 800;
  display: flex;
  align-items: center;
  justify-content: center;
}
/* Final/complete step: tinted background */
.step-final {
  background: rgba(ACCENT, 0.04-0.07);
  border-color: rgba(ACCENT, 0.14-0.2);
}
```

### 7. Code Snippets

Dark code blocks:

```css
.code-block {
  background: rgba(0,0,0,0.28);
  border-radius: 7px-8px;
  padding: 8px-9px 10px;
  border: 1px solid rgba(255,255,255,0.1);
  font-family: monospace;
}
.code-comment { font-size: 0.84rem; color: rgba(255,255,255,0.2); }
.code-command { font-size: 0.89rem; color: #64FFDA; }
```

### 8. API Displays

```css
.api-block {
  background: rgba(0,0,0,0.2);
  border-radius: 8px;
  padding: 8px 10px;
  border: 1px solid rgba(255,255,255,0.1);
}
.api-block code {
  font-size: 0.85rem;
  color: rgba(255,255,255,0.45);
  font-family: monospace;
  line-height: 1.55;
  display: block;
}
```

### 9. Architecture Diagrams (Layered Boxes)

Vertically stacked layers with down-arrows between them:

```html
<div class="arch-layer arch-layer-top">
  <div class="arch-layer-label">LAYER LABEL</div>
  <div class="arch-layer-chips">
    <div class="arch-chip">Item 1</div>
    <div class="arch-chip">Item 2</div>
  </div>
</div>
<!-- Down arrow SVG -->
<div class="arch-layer arch-layer-bridge">
  <div class="arch-bridge-text">BRIDGE DESCRIPTION</div>
</div>
```

### 10. Tree Structures (Governance/Hierarchy)

```css
.tree {
  font-family: monospace;
  font-size: 0.94rem;
  line-height: 1.9;
  background: rgba(0,0,0,0.25);
  border-radius: 13px;
  padding: 14px 16px;
  border: 1px solid rgba(255,255,255,0.1);
}
/* Use Unicode box-drawing: ... ... */
```

### 11. Timeline / Phasing

Horizontal columns with phase headers and service lists:

```html
<div class="timeline">
  <div class="phase-column">
    <div class="phase-header phase-1">
      <div class="phase-title">Phase Name</div>
    </div>
    <div class="phase-services">
      <div class="service-item">
        <div class="service-icon"><!-- SVG --></div>
        <div><strong>Service Name</strong><p>Description</p></div>
      </div>
    </div>
  </div>
  <!-- Arrow divider between columns -->
  <div class="phase-column">...</div>
</div>
```

### 12. Inline SVG Icons

Always use inline SVGs (no external icon libraries). Common pattern:

```html
<svg width="16-26" height="16-26" viewBox="0 0 24 24" fill="none"
     stroke="ACCENT_COLOR" stroke-width="1.6" stroke-linecap="round">
  <!-- path data -->
</svg>
```

Common icons to include:
- **Checkmark circle**: quality/evaluation
- **Database cylinder**: data/memory
- **Chat bubble**: assistant/chatbot
- **Document**: parsing/extraction
- **Lightning bolt**: batch/speed
- **Grid squares**: builder/composer
- **Code brackets**: framework/developer
- **Shield**: governance/security
- **Eye**: observability
- **Globe**: global/network

## Grid Layouts

| Layout          | CSS                                    | Use Case                |
|-----------------|----------------------------------------|-------------------------|
| 3-column cards  | `grid-template-columns: repeat(3,1fr)` | Service catalog, gaps   |
| 2-column panels | `grid-template-columns: 1fr 1fr`       | Deep-dive comparisons   |
| 2-col unequal   | `grid-template-columns: 1.1fr 1fr`     | Main + sidebar panels   |
| 2-col with tree | `grid-template-columns: 1fr 1.2fr`     | Tree + feature cards    |
| Timeline        | `display: flex` with equal flex columns | Phasing/roadmap         |

## Animation System

Fade-up animation with staggered delays per element:

```css
@keyframes fu {
  to { opacity: 1; transform: translateY(0); }
}
.A {
  opacity: 0;
  transform: translateY(16px);
  animation: fu .45s ease forwards;
  animation-delay: var(--d, .1s);
}
```

Apply to elements: `<div class="A" style="--d:0.08s">`. Increment delay by 0.06-0.12s per element.

## Slide Navigation System

The presentation engine handles:
- **Keyboard**: ArrowDown/Right = next, ArrowUp/Left = previous
- **Mouse wheel**: Scroll down = next (700ms debounce)
- **Touch**: Swipe up = next (50px threshold)
- **Click**: Click anywhere = next slide
- **Dot navigation**: Fixed right sidebar with clickable dots
- **Progress bar**: Top 3px bar showing position

### Navigation JavaScript

```javascript
let cur = 0, moving = false;

function go(idx) {
  if (moving || idx === cur || idx < 0 || idx >= slides.length) return;
  moving = true;
  const dir = idx > cur ? 'eu' : 'ed'; // exit-up or exit-down
  const prev = els[cur], next = els[idx];
  prev.classList.remove('on');
  prev.classList.add(dir);
  // Restart animations on entering slide
  next.querySelectorAll('.A').forEach(el => {
    el.style.animation = 'none';
    el.offsetHeight; // reflow
    el.style.animation = '';
  });
  next.classList.remove('eu', 'ed');
  next.classList.add('on');
  cur = idx;
  ui();
  setTimeout(() => { prev.classList.remove('eu', 'ed'); moving = false; }, 550);
}
```

### Slide Transition CSS

```css
.sl {
  position: absolute; inset: 0;
  display: flex; flex-direction: column;
  justify-content: center; align-items: center;
  padding: 28px 40px;
  opacity: 0; transform: translateY(36px) scale(.97);
  transition: opacity .5s cubic-bezier(.4,0,.2,1),
              transform .5s cubic-bezier(.4,0,.2,1);
  pointer-events: none; z-index: 0;
}
.sl.on  { opacity: 1; transform: none; pointer-events: auto; z-index: 2; }
.sl.eu  { opacity: 0; transform: translateY(-50px) scale(.96); z-index: 1; }
.sl.ed  { opacity: 0; transform: translateY(50px) scale(.96); z-index: 1; }
```

## Responsive Breakpoints

```css
@media (max-width: 900px) {
  .sl { padding: 20px 14px; }
  /* Stack grids to single column */
  .gap-grid, .found-grid, .scale-grid { grid-template-columns: 1fr; }
  .cat-grid { grid-template-columns: repeat(2, 1fr); }
  /* Stack horizontal layouts */
  .pr-arch { flex-direction: column; }
  .ph-timeline { flex-direction: column; }
  .gov-layout { grid-template-columns: 1fr; }
  .dots { display: none; }
}
@media (max-width: 600px) {
  .cat-grid { grid-template-columns: 1fr; }
}
```

## Slide Type Templates

### Type 1: Cover Slide

Center-aligned with logo, wordmark, title, tagline, and pills.

```html
<svg class="amp-logo" ...><!-- Logo SVG --></svg>
<div class="amp-wordmark A" style="--d:0.05s">BRAND NAME</div>
<h1 class="A" style="--d:0.12s">Main Title<br>Second Line</h1>
<p class="amp-tagline A" style="--d:0.2s">Tagline &mdash; Date</p>
<div class="amp-pills A" style="--d:0.3s">
  <span class="amp-pill amp-pill-orange">Pill 1</span>
  <span class="amp-pill amp-pill-teal">Pill 2</span>
  <span class="amp-pill amp-pill-gold">Pill 3</span>
</div>
<p class="amp-sub A" style="--d:0.4s">Subtitle description</p>
```

### Type 2: Problem / Gap Cards (3-column)

```html
<h1>Problem Statement</h1>
<h2>Supporting subheadline</h2>
<div class="gap-grid">
  <div class="gap-card A" style="--d:0.08s">
    <div class="gap-ico gap-ico-rose"><!-- icon SVG --></div>
    <div class="gap-num">01</div>
    <strong>Card Title</strong>
    <p>Description paragraph</p>
    <div class="gap-quote">&ldquo;Pull quote&rdquo;</div>
  </div>
  <!-- Repeat for 02, 03 -->
</div>
<div class="gap-footer A" style="--d:0.4s">
  <!-- Arrow icon --> <span>Footer call-to-action</span>
</div>
```

### Type 3: Two-Panel Deep Dive

```html
<h1>Section <span style="color:${DB.orange}">Title</span></h1>
<h2>Subheadline</h2>
<div class="found-grid">
  <div class="found-panel A" style="--d:0.08s">
    <div class="found-header found-h-rose">
      <!-- icon --> <strong>Panel Title</strong>
    </div>
    <div class="found-body">
      <p class="found-desc">Description</p>
      <!-- Nested components: connectors, steps, API blocks, etc. -->
    </div>
  </div>
  <div class="found-panel A" style="--d:0.2s">
    <!-- Second panel -->
  </div>
</div>
```

### Type 4: Service Catalog Grid (3x3)

```html
<h1>Catalog Title</h1>
<h2>Subheadline</h2>
<div class="cat-grid">
  <div class="cat-card A" style="--d:0.06s">
    <span class="cat-phase cat-ph1">Phase Label</span>
    <div class="cat-ico cat-ico-rose"><!-- icon --></div>
    <strong>Service Name</strong>
    <p>Short description</p>
  </div>
  <!-- Repeat for each service -->
</div>
```

### Type 5: Architecture Diagram

```html
<h1>Architecture</h1>
<h2>Subheadline</h2>
<div class="arch-diagram A">
  <div class="arch-layer arch-layer-top">
    <div class="arch-layer-label">TOP LAYER</div>
    <div class="arch-layer-chips"><!-- chips --></div>
  </div>
  <div class="arch-down"><!-- down arrow SVG --></div>
  <div class="arch-layer arch-layer-bridge">
    <div class="arch-bridge-text">MIDDLE LAYER</div>
  </div>
  <div class="arch-down"><!-- down arrow SVG --></div>
  <div class="arch-layer arch-layer-db">
    <div class="arch-layer-label">BOTTOM LAYER</div>
    <div class="arch-db-inner"><!-- grid items --></div>
  </div>
</div>
```

### Type 6: Governance / Tree + Features

```html
<h1>Governance</h1>
<h2>Subheadline</h2>
<div class="gov-layout A">
  <div class="gov-tree">
    <!-- Monospace tree using Unicode box-drawing characters -->
  </div>
  <div class="gov-features">
    <div class="gov-f-card A">
      <div class="gov-f-ico"><!-- icon --></div>
      <div>
        <strong>Feature Title</strong>
        <p>Description</p>
      </div>
    </div>
    <!-- More feature cards -->
  </div>
</div>
```

### Type 7: Timeline / Phasing

```html
<h1>Timeline</h1>
<h2>Subheadline</h2>
<div class="ph-timeline">
  <div class="ph-col A" style="--d:0.08s">
    <div class="ph-hdr ph-hdr-1">
      <div class="ph-hdr-title">Phase 1</div>
    </div>
    <div class="ph-services">
      <!-- Service items with icons -->
    </div>
  </div>
  <div class="ph-divider A"><!-- arrow SVG --></div>
  <div class="ph-col A"><!-- Phase 2 --></div>
  <div class="ph-divider A"><!-- arrow SVG --></div>
  <div class="ph-col A"><!-- Phase 3 --></div>
</div>
```

## Workflow

### Step 1: Gather Content

Ask the user for:
- Presentation title and subtitle
- Target audience / customer name
- Number of slides and their topics
- Key messages per slide
- Any specific data points, metrics, or quotes

### Step 2: Plan Slide Structure

Map content to slide types:
1. **Slide 1**: Always a Cover slide
2. **Slide 2**: Problem statement (3-column gap cards)
3. **Slides 3-N**: Mix of deep-dive panels, catalogs, architecture, governance
4. **Final slide**: Timeline/phasing or call-to-action

### Step 3: Generate the HTML File

Write a single self-contained HTML file following the architecture above. Include:
- The full DB color palette
- All CSS (inline in a `<style>` element created via JS)
- All slide data as a JavaScript array
- The navigation engine (keyboard, wheel, touch, click, dots)
- Google Fonts import for DM Sans

### Step 4: Customize Branding

Replace the AMPLIFY branding:
- Update the SVG logo in the cover slide
- Change the wordmark text
- Update pill labels
- Adjust accent colors if needed (but keep the overall palette)

### Step 5: Deliver

Save the file and tell the user to open it in a browser. The presentation works offline (except for Google Fonts, which can be replaced with system fonts if needed).

## Key Design Principles

1. **Dark theme only** — deep teal/black backgrounds, white text with opacity layers
2. **Orange as primary accent** — #FF3621 for emphasis, progress, CTAs
3. **Glass-morphism cards** — semi-transparent backgrounds with subtle borders
4. **Staggered animations** — every element fades up with increasing delay
5. **Readability first** — use legible font sizes (0.9-1.1rem body, 0.73-0.78rem labels) for comfortable reading
6. **Inline SVGs** — no external icon dependencies
7. **Single file** — everything in one HTML file, no build step
8. **Responsive** — works on desktop, tablet, and mobile
9. **Accent variety** — use rose, cyan, gold, purple, green to differentiate categories
10. **Professional typography** — DM Sans with tight letter-spacing on headings

## IMPORTANT: Coloring Heading Accent Words

Use inline spans to color key words in headings:

```html
<h1>Section <span style="color:${DB.orange}">Highlight</span></h1>
```

## IMPORTANT: Progress Bar and Navigation

Always include:
- A 3px progress bar fixed at the top
- Dot navigation fixed on the right side
- Both colored with the current slide's accent color

## Reference Template

A complete working example is available at:
`<skill_path>/resources/reference-template.html`

When generating a new presentation, read this file for the exact CSS class names, JavaScript engine, and HTML structure. Use it as the authoritative source for any implementation details not fully specified above.
