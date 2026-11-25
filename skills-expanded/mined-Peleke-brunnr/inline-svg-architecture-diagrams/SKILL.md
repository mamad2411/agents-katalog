---
name: inline-svg-architecture-diagrams
description: Generate production-quality inline SVG architecture diagrams with theme-aware CSS variables, animated flow lines, glow effects, feedback loops, and responsive layout. No external dependencies, no build steps, no image files. Use when creating system architecture visuals that integrate with a design system.
license: Complete terms in LICENSE.txt
metadata:
  openclaw:
    emoji: "\U0001F3D7\uFE0F"
---

# Inline SVG Architecture Diagrams

> Create production-quality inline SVG architecture diagrams that integrate with any design system. No external dependencies, no build steps, no image files.

## TL;DR Execution Flow

```
Phase 0: Gather inputs (layers, connections, feedback loops, external I/O, theme vars)
Phase 1: Compute layout (positions, spacing, viewBox)
Phase 2: Generate SVG foundation (defs: filters, gradients, grid pattern)
Phase 3: Render layers (rectangles, labels, mini-icons, highlight treatment)
Phase 4: Render connections (flow lines with animated dashes, arrowheads)
Phase 5: Render feedback loops (curved return paths with reverse animation)
Phase 6: Render external I/O (dashed boundary lines with labels)
Phase 7: Wrap in container with hover styles and caption
```

## When to Use

- Architecture diagrams that live in the page design (not external images)
- System diagrams that must respect light/dark mode automatically
- Any diagram where animated flow lines convey data direction
- Situations where Mermaid/D2/Excalidraw look too generic or don't integrate with the design system

## When NOT to Use

- Simple box-and-arrow diagrams (Mermaid is fine)
- Diagrams that need to be editable by non-developers (use Figma/Excalidraw)
- Charts/graphs with data (use a charting library)

## Inputs

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `layers` | Layer[] | Yes | Ordered list of layer/node definitions |
| `connections` | Connection[] | Yes | Flow lines between layers |
| `feedback_loops` | FeedbackLoop[] | No | Return paths (e.g., bottom layer back to top) |
| `external_io` | ExternalIO[] | No | Inputs/outputs at system boundaries |
| `theme_vars` | ThemeVars | No | CSS custom property names (has sensible defaults) |
| `viewbox` | {w, h} | No | ViewBox dimensions (auto-calculated from layer count if omitted) |
| `highlight_layer` | string | No | Layer ID to highlight with glow + pulse |

### Layer Definition

```yaml
- id: knowledge
  label: "01 · KNOWLEDGE"
  title: "core-engine"
  output_label: "→ rules"        # optional right-side annotation
  icon: knowledge-graph           # see Icon Reference below
  link: "https://..."             # optional clickable link
```

### Connection Definition

```yaml
- from: knowledge
  to: learning
  label_left: "projects"          # left-side label
  label_right: "rules"            # right-side label
  direction: down                 # down | up | lateral
```

### Feedback Loop Definition

```yaml
- from: interoception
  to: learning
  label: "feedback"
  side: left                      # which side the curve routes through
```

### External I/O Definition

```yaml
- target: nervous-system
  side: left                      # left = input, right = output
  labels: ["external", "signals"]
```

---

## Phase 1: Layout Computation

### Vertical Stack Layout

```
Layer spacing:
  layer_height = 60
  gap = 40 (between layers, includes connection line space)
  margin_top = 20
  margin_bottom = 20

  layer_y(i) = margin_top + i * (layer_height + gap)

  viewbox_height = margin_top + n * layer_height + (n-1) * gap + margin_bottom

Layer positioning:
  layer_width = 260
  layer_x = (viewbox_width - layer_width) / 2

  Default viewbox_width = 600
```

### Space Reservations

```
If feedback_loops exist on left:   reserve 110px left margin
If external_io on left:            reserve 110px left margin (overlaps with above)
If external_io on right:           reserve 110px right margin
If neither:                        center layers in viewbox
```

---

## Phase 2: SVG Foundation

### 2.1 Filter Definitions

**Standard Glow** — For highlighted layer border:

```xml
<filter id="glow">
  <feGaussianBlur stdDeviation="2" result="blur"/>
  <feMerge>
    <feMergeNode in="blur"/>
    <feMergeNode in="SourceGraphic"/>
  </feMerge>
</filter>
```

**Pulse Glow** — For animated emphasis ring:

```xml
<filter id="pulse-glow">
  <feGaussianBlur stdDeviation="3" result="blur"/>
  <feMerge>
    <feMergeNode in="blur"/>
    <feMergeNode in="SourceGraphic"/>
  </feMerge>
</filter>
```

### 2.2 Gradient Definitions

```xml
<!-- Downward flow: accent at top, transparent at bottom -->
<linearGradient id="flow-down" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0%" stop-color="var(--color-accent)" stop-opacity="0.6"/>
  <stop offset="100%" stop-color="var(--color-accent)" stop-opacity="0.1"/>
</linearGradient>

<!-- Upward flow: accent at bottom, transparent at top -->
<linearGradient id="flow-up" x1="0" y1="1" x2="0" y2="0">
  <stop offset="0%" stop-color="var(--color-accent)" stop-opacity="0.6"/>
  <stop offset="100%" stop-color="var(--color-accent)" stop-opacity="0.1"/>
</linearGradient>

<!-- Rightward flow: transparent at left, accent at right -->
<linearGradient id="flow-right" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0%" stop-color="var(--color-accent)" stop-opacity="0.1"/>
  <stop offset="100%" stop-color="var(--color-accent)" stop-opacity="0.6"/>
</linearGradient>
```

### 2.3 Background Grid Pattern

```xml
<pattern id="grid" width="30" height="30" patternUnits="userSpaceOnUse">
  <path d="M 30 0 L 0 0 0 30" fill="none"
        stroke="var(--color-border-subtle)" stroke-width="0.5" opacity="0.3"/>
</pattern>

<!-- Apply as first element after defs -->
<rect width="100%" height="100%" fill="url(#grid)" opacity="0.5"/>
```

---

## Phase 3: Render Layers

### 3.1 Standard Layer

```xml
<g data-layer="{id}">
  <!-- Background rect -->
  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8"
        fill="var(--color-bg)" stroke="var(--color-border)" stroke-width="1"/>

  <!-- Mini-icon (left side, see Icon Reference) -->
  {icon_svg}

  <!-- Layer number + label (top-left, small) -->
  <text x="{x+30}" y="{y+18}" font-family="var(--font-mono)" font-size="9"
        fill="var(--color-text-faint)" text-transform="uppercase" letter-spacing="0.05em">
    {label}
  </text>

  <!-- Title (center-left, larger) -->
  <text x="{x+30}" y="{y+42}" font-family="var(--font-sans)" font-size="14"
        fill="var(--color-text)">
    {title}
  </text>

  <!-- Output annotation (right side, small) -->
  <text x="{x+w-10}" y="{y+42}" font-family="var(--font-mono)" font-size="8"
        fill="var(--color-text-faint)" text-anchor="end" opacity="0.5">
    {output_label}
  </text>
</g>
```

### 3.2 Highlighted Layer (active/core)

Add these extras to the standard layer:

```xml
<!-- Accent border instead of standard -->
<rect ... stroke="var(--color-accent)" stroke-width="2" filter="url(#glow)"/>

<!-- Pulse ring (animated opacity) -->
<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8"
      fill="none" stroke="var(--color-accent)" stroke-width="0.5" opacity="0.3">
  <animate attributeName="opacity" values="0.3;0.1;0.3" dur="3s" repeatCount="indefinite"/>
</rect>

<!-- "← core" marker (right side) -->
<text x="{x+w+8}" y="{y+h/2+4}" font-family="var(--font-mono)" font-size="8"
      fill="var(--color-accent)" opacity="0.5">← core</text>
```

### 3.3 Clickable Layer (with link)

Wrap in an anchor with hover class:

```xml
<a href="{link}" class="layer-link">
  <g data-layer="{id}">
    <!-- rect gets class="layer-rect" for hover targeting -->
    <rect class="layer-rect" .../>
    ...
  </g>
</a>
```

---

## Phase 4: Render Connections

### 4.1 Downward Flow Line

Between consecutive layers:

```xml
<g>
  <!-- The line -->
  <line x1="{center_x}" y1="{from_y + from_h}" x2="{center_x}" y2="{to_y}"
        stroke="url(#flow-down)" stroke-width="1.5" stroke-dasharray="4 3">
    <animate attributeName="stroke-dashoffset" from="0" to="-14" dur="2s" repeatCount="indefinite"/>
  </line>

  <!-- Arrowhead at target -->
  <polygon points="{cx},{to_y-4} {cx-4},{to_y+2} {cx+4},{to_y+2}"
           fill="var(--color-accent)" opacity="0.4"/>

  <!-- Left label -->
  <text x="{center_x - 8}" y="{midpoint_y}" font-size="8"
        fill="var(--color-text-faint)" text-anchor="end" opacity="0.4">
    {label_left}
  </text>

  <!-- Right label -->
  <text x="{center_x + 8}" y="{midpoint_y}" font-size="8"
        fill="var(--color-text-faint)" opacity="0.4">
    {label_right}
  </text>
</g>
```

### 4.2 Animation Direction

| Direction | `stroke-dashoffset` from→to | Visual effect |
|-----------|---------------------------|---------------|
| Down | `0` → `-14` | Dashes march downward |
| Up | `0` → `14` | Dashes march upward |
| Right | `0` → `-14` | Dashes march rightward |
| Left | `0` → `14` | Dashes march leftward |

The key: **negative offset = forward march, positive offset = reverse march**.

Dash pattern `4 3` with offset `14` (= 2 × (4+3)) gives smooth looping.

---

## Phase 5: Render Feedback Loops

### 5.1 Left-Side Return Path

Routes outside the layer stack, up the left side:

```xml
<g>
  <!-- Path: exit from layer left, go left, go up, enter target layer left -->
  <path d="M {from_x} {from_cy} L {left_margin} {from_cy} L {left_margin} {to_cy} L {to_x} {to_cy}"
        fill="none" stroke="var(--color-accent)" stroke-width="1.5"
        stroke-dasharray="4 3" opacity="0.5">
    <animate attributeName="stroke-dashoffset" from="0" to="14" dur="3s" repeatCount="indefinite"/>
  </path>

  <!-- Arrowhead at target -->
  <polygon points="{to_x},{to_cy-4} {to_x-6},{to_cy} {to_x},{to_cy+4}"
           fill="var(--color-accent)" opacity="0.5"/>

  <!-- Vertical label (rotated -90°) -->
  <text x="{left_margin - 8}" y="{midpoint_y}" font-size="8"
        fill="var(--color-accent)" opacity="0.4" text-anchor="middle"
        transform="rotate(-90, {left_margin - 8}, {midpoint_y})">
    {label} ↑ feedback
  </text>
</g>
```

### 5.2 Animation: Reverse Direction

Feedback loops use **positive** stroke-dashoffset (`0` → `14`) to visually convey upstream/return flow. This contrasts with the downward flows (`0` → `-14`), making the feedback direction immediately obvious.

Slower duration (`3s` vs `2s`) further distinguishes feedback from forward flow.

---

## Phase 6: Render External I/O

### 6.1 Input Arrow (Left Side)

```xml
<g>
  <line x1="{left_edge}" y1="{target_cy}" x2="{target_x}" y2="{target_cy}"
        stroke="var(--color-accent)" stroke-width="1" stroke-dasharray="3 2" opacity="0.4"/>

  <polygon points="{target_x},{target_cy-3} {target_x-5},{target_cy} {target_x},{target_cy+3}"
           fill="var(--color-accent)" opacity="0.4"/>

  <!-- Stacked labels -->
  <text x="{left_edge - 5}" y="{target_cy - 6}" font-size="8"
        fill="var(--color-text-faint)" text-anchor="end" opacity="0.4">{labels[0]}</text>
  <text x="{left_edge - 5}" y="{target_cy + 6}" font-size="8"
        fill="var(--color-text-faint)" text-anchor="end" opacity="0.4">{labels[1]}</text>
</g>
```

### 6.2 Output Arrow (Right Side)

```xml
<g>
  <line x1="{target_x + target_w}" y1="{target_cy}" x2="{right_edge}" y2="{target_cy}"
        stroke="var(--color-accent)" stroke-width="1" stroke-dasharray="3 2" opacity="0.4"/>

  <polygon points="{right_edge},{target_cy-3} {right_edge+5},{target_cy} {right_edge},{target_cy+3}"
           fill="var(--color-accent)" opacity="0.4"/>

  <!-- Stacked labels -->
  <text x="{right_edge + 10}" y="{target_cy - 8}" font-size="8"
        fill="var(--color-text-faint)" opacity="0.4">{labels[0]}</text>
  <text x="{right_edge + 10}" y="{target_cy + 2}" font-size="8"
        fill="var(--color-text-faint)" opacity="0.4">{labels[1]}</text>
  <!-- ... more stacked labels as needed -->
</g>
```

---

## Phase 7: Container & Hover Styles

### 7.1 Container HTML

```html
<div class="system-diagram relative overflow-hidden rounded-lg border"
     style="background: var(--color-bg-elevated); border-color: var(--color-border);">
  <div class="p-4 sm:p-8">
    <svg viewBox="0 0 {vb_w} {vb_h}" class="w-full h-auto"
         aria-label="{description}">
      <defs>...</defs>
      <!-- grid, layers, connections, loops, I/O -->
    </svg>
  </div>
  <p class="text-center text-sm pb-4" style="color: var(--color-text-muted);">
    {caption}
  </p>
</div>
```

### 7.2 Hover CSS

```css
.layer-link:hover .layer-rect {
  stroke: var(--color-accent);
  stroke-width: 2;
  transition: stroke 0.2s ease, stroke-width 0.2s ease;
}

.layer-link:hover text[font-size="14"],
.layer-link:hover text[font-size="13"] {
  fill: var(--color-accent);
}

.layer-link-text:hover {
  opacity: 1 !important;
  text-decoration: underline;
}
```

---

## Icon Reference

Mini-icons are placed inside each layer rect at `(x+12, cy)`. All use `var(--color-accent)` with reduced opacity.

### knowledge-graph
Three interconnected dots forming a triangle:
```xml
<circle cx="{ix}" cy="{iy-4}" r="2" fill="var(--color-accent)" opacity="0.8"/>
<circle cx="{ix+8}" cy="{iy-4}" r="2" fill="var(--color-accent)" opacity="0.8"/>
<circle cx="{ix+4}" cy="{iy+4}" r="2" fill="var(--color-accent)" opacity="0.8"/>
<line x1="{ix}" y1="{iy-4}" x2="{ix+8}" y2="{iy-4}" stroke="var(--color-accent)" stroke-width="0.7" opacity="0.5"/>
<line x1="{ix}" y1="{iy-4}" x2="{ix+4}" y2="{iy+4}" stroke="var(--color-accent)" stroke-width="0.7" opacity="0.5"/>
<line x1="{ix+8}" y1="{iy-4}" x2="{ix+4}" y2="{iy+4}" stroke="var(--color-accent)" stroke-width="0.7" opacity="0.5"/>
```

### beta-curve
Stylized beta distribution curve:
```xml
<path d="M {ix-5} {iy+2} Q {ix-1} {iy-13}, {ix+4} {iy-5} Q {ix+9} {iy+5}, {ix+13} {iy+2}"
      fill="none" stroke="var(--color-accent)" stroke-width="1.5" opacity="0.8"/>
```

### signal-wave
Zigzag signal waveform:
```xml
<path d="M {ix} {iy} L {ix+4} {iy-6} L {ix+8} {iy+6} L {ix+12} {iy-6} L {ix+16} {iy}"
      fill="none" stroke="var(--color-accent)" stroke-width="1.2" opacity="0.6"
      stroke-linecap="round"/>
```

### shield
Security shield outline:
```xml
<path d="M {ix-3} {iy-4} L {ix+4} {iy-8} L {ix+11} {iy-4} L {ix+11} {iy+6}
         Q {ix+4} {iy+12}, {ix-3} {iy+6} Z"
      fill="none" stroke="var(--color-accent)" stroke-width="1.2" opacity="0.6"/>
```

### heartbeat
Animated pulsing circle (for monitoring/interoception):
```xml
<circle cx="{ix+4}" cy="{iy}" r="9" fill="none"
        stroke="var(--color-accent)" stroke-width="1" opacity="0.5">
  <animate attributeName="r" values="9;10;9" dur="2s" repeatCount="indefinite"/>
  <animate attributeName="opacity" values="0.5;0.3;0.5" dur="2s" repeatCount="indefinite"/>
</circle>
<circle cx="{ix+4}" cy="{iy}" r="3" fill="var(--color-accent)" opacity="0.4">
  <animate attributeName="opacity" values="0.4;0.7;0.4" dur="2s" repeatCount="indefinite"/>
</circle>
```

### database
Simple cylinder:
```xml
<ellipse cx="{ix+4}" cy="{iy-5}" rx="7" ry="3" fill="none"
         stroke="var(--color-accent)" stroke-width="1" opacity="0.6"/>
<line x1="{ix-3}" y1="{iy-5}" x2="{ix-3}" y2="{iy+5}"
      stroke="var(--color-accent)" stroke-width="1" opacity="0.6"/>
<line x1="{ix+11}" y1="{iy-5}" x2="{ix+11}" y2="{iy+5}"
      stroke="var(--color-accent)" stroke-width="1" opacity="0.6"/>
<ellipse cx="{ix+4}" cy="{iy+5}" rx="7" ry="3" fill="none"
         stroke="var(--color-accent)" stroke-width="1" opacity="0.6"/>
```

### gear
Simple cog outline:
```xml
<circle cx="{ix+4}" cy="{iy}" r="5" fill="none"
        stroke="var(--color-accent)" stroke-width="1" opacity="0.6"/>
<circle cx="{ix+4}" cy="{iy}" r="2" fill="var(--color-accent)" opacity="0.4"/>
```

---

## Theme Variables (Defaults)

If the host page doesn't define these, provide fallback values:

```css
:root {
  --color-accent: #6366f1;
  --color-accent-dim: #4f46e5;
  --color-bg: #1a1a2e;
  --color-bg-elevated: #16213e;
  --color-border: #334155;
  --color-border-subtle: #1e293b;
  --color-text: #e2e8f0;
  --color-text-muted: #94a3b8;
  --color-text-faint: #64748b;
  --font-mono: 'JetBrains Mono', 'Fira Code', monospace;
  --font-sans: 'Inter', system-ui, sans-serif;
}
```

These are dark-mode defaults. The point of CSS variables is that light-mode themes override them automatically — the SVG adapts without changes.

---

## Quality Checklist

### SVG Validity
- [ ] Valid inline SVG (no `xmlns` needed for inline, but include if standalone)
- [ ] All `id` attributes are unique within the page
- [ ] `viewBox` is set, no fixed `width`/`height` (responsive)
- [ ] `aria-label` describes the diagram purpose

### Theme Integration
- [ ] ALL colors use `var(--color-*)` — zero hardcoded hex values
- [ ] ALL fonts use `var(--font-*)` — no hardcoded font stacks
- [ ] Works in both light and dark mode without changes

### Animation
- [ ] Flow lines animate with `stroke-dasharray` + `stroke-dashoffset`
- [ ] Feedback loops animate in reverse direction (positive offset)
- [ ] Highlighted layer has pulse ring (`opacity` animation)
- [ ] No JavaScript required — pure CSS/SMIL animations
- [ ] Animations are subtle (low opacity, slow duration)

### Accessibility
- [ ] SVG has `aria-label`
- [ ] Layer groups have `data-layer` attributes
- [ ] Animations respect `prefers-reduced-motion` (add media query)
- [ ] Text is readable at small sizes (minimum 8px, prefer 9px+)

### Responsiveness
- [ ] No fixed pixel widths on the SVG element
- [ ] `viewBox` maintains aspect ratio
- [ ] Container has responsive padding (`p-4 sm:p-8`)
- [ ] Readable on mobile (320px viewport)

---

## Style Variant: Portfolio Hand-Drawn

> External `.svg` files with a hand-drawn, sketchy aesthetic. Transparent background, Caveat cursive font, wobbly path-based shapes, `feTurbulence` displacement filter. No CSS variables, no grid backgrounds, no build steps.

### When to Use This Style

- Portfolio articles, blog posts, writing collections
- Diagrams that sit inside prose content (not dashboards or app UIs)
- Visual storytelling where warmth and approachability matter
- Any context where the rigid CSS-variable system feels too "enterprise"

### Color Palette (Hardcoded — No CSS Variables)

| Role | Value | Usage |
|------|-------|-------|
| Primary text | `#e0e0e0` | Labels, titles, main content |
| Muted text | `#888888` | Captions, annotations, sub-labels |
| Accent | `rgb(168,85,247)` | Borders, highlights, numbered callouts, animated elements |
| Accent fill | `rgba(168,85,247,0.08)` | Box backgrounds (subtle) |
| Accent fill (glow) | `rgba(168,85,247,0.12-0.14)` | Highlighted/glowing box backgrounds |
| Success | `#4ade80` | Accept, positive signals |
| Danger | `#f87171` | Reject, negative signals, warnings |
| Background | transparent | SVG has no background — inherits from page |

### Typography

All text uses:
```
font-family="'Caveat', 'Comic Sans MS', cursive"
```

No monospace. No sans-serif. Everything is hand-drawn cursive.

| Element | Size | Weight | Fill |
|---------|------|--------|------|
| Diagram title | 20-22px | bold | `#e0e0e0` |
| Section headers / labels | 15px | bold | `#e0e0e0` |
| Body text / descriptions | 12-13px | normal | `#888888` |
| Annotations / captions | 10-11px | normal | `#888888` |
| Accent annotations | 12px | normal | `rgb(168,85,247)` |

### Filter Definitions

**Roughen filter** — Applies to box paths for hand-drawn wobble:
```xml
<filter id="roughen" x="-2%" y="-2%" width="104%" height="104%">
  <feTurbulence type="turbulence" baseFrequency="0.03" numOctaves="2" result="noise" seed="3"/>
  <feDisplacementMap in="SourceGraphic" in2="noise" scale="1.2" xChannelSelector="R" yChannelSelector="G"/>
</filter>
```

Vary the `seed` value (1-10) per diagram for different wobble patterns. Keep `scale` between 1.0-1.2.

**Glow filter** — For emphasized/highlighted elements:
```xml
<filter id="glow">
  <feGaussianBlur stdDeviation="3" result="blur"/>
  <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
</filter>
```

### Arrow Markers

Open chevron style — not filled triangles. Stroke-only, rounded caps:
```xml
<marker id="arrow" viewBox="0 0 12 10" refX="10" refY="5"
        markerWidth="8" markerHeight="6" orient="auto-start-reverse"
        fill="none" stroke="#e0e0e0" stroke-width="1.5"
        stroke-linecap="round" stroke-linejoin="round">
  <path d="M 1,1 L 10,5 L 1,9"/>
</marker>
```

Color variants (same shape, different stroke):
- `id="arrow-purple"` → `stroke="rgb(168,85,247)"`
- `id="arrow-green"` → `stroke="#4ade80"`
- `id="arrow-red"` → `stroke="#f87171"`

### Wobbly Box Technique

Use `<path>` with slightly irregular coordinates instead of `<rect>`:

```xml
<!-- WRONG: rigid rectangle -->
<rect x="132" y="68" width="430" height="60" rx="8"/>

<!-- RIGHT: organic wobbly path -->
<path d="M 132,68 C 230,65 430,71 562,67
         C 565,85 563,105 565,128
         C 430,131 230,127 132,131
         C 129,113 131,87 129,68"
      stroke="rgb(168,85,247)" stroke-width="2" fill="rgba(168,85,247,0.08)"
      stroke-linecap="round" stroke-linejoin="round"/>
```

Key technique: Each control point varies **±3px** from the "perfect" rectangle coordinates. The `C` (cubic bezier) commands create subtle organic curves. Always use `stroke-linecap="round"` and `stroke-linejoin="round"`.

### Organic Touches

These details make the difference between "SVG diagram" and "hand-drawn sketch":

- **Slight rotation transforms**: `transform="rotate(-0.4, cx, cy)"` on groups — vary between ±0.3° and ±0.8°
- **Title underline**: Wobbly `<path>` under title text, not a `<line>` — slightly off-center, accent color at 0.5 opacity
- **Decorative margin sketches**: Tiny illustrations at 0.25-0.35 opacity (mini knowledge graphs, beta curves, coffee cups, etc.)
- **Numbered callouts**: Purple filled circles with white bold numbers
- **Animated dashed lines**: `stroke-dasharray="8 5"` with `<animate>` on `stroke-dashoffset`
- **Bottom caption**: Muted italic-feeling observation, `font-size="11"`, `fill="#888888"`, `opacity="0.6"`

### Numbered Callout Pattern

```xml
<circle cx="108" cy="82" r="14" fill="rgb(168,85,247)" stroke="none" opacity="0.9"/>
<text x="108" y="87" text-anchor="middle"
      font-family="'Caveat', 'Comic Sans MS', cursive"
      font-size="14" fill="white" font-weight="bold">1</text>
```

### Standard Layout

- `viewBox="0 0 672 {height}"` — 672px wide to match content column
- External `.svg` files in `public/diagrams/`, referenced via `<img src="/diagrams/name.svg">`
- Include `xmlns="http://www.w3.org/2000/svg"` on root `<svg>` element
- No `width`/`height` attributes — let the img container control sizing

### Quality Checklist (Hand-Drawn Style)

- [ ] All colors hardcoded (zero CSS variables)
- [ ] Font is Caveat/cursive throughout — no monospace, no sans-serif
- [ ] Boxes use `<path>` not `<rect>` — visibly wobbly
- [ ] `roughen` filter applied to box paths where appropriate
- [ ] Background is transparent (no grid pattern, no fill on root)
- [ ] At least one decorative margin sketch (graph, curve, icon)
- [ ] Slight rotation transforms on groups (±0.3° to ±0.8°)
- [ ] Title has wobbly underline path
- [ ] Animations are subtle and loop smoothly
- [ ] Caption text at bottom in muted `#888888` at reduced opacity

### Full Example: Feedback Loop Diagram

From `portfolio/public/diagrams/feedback-loop.svg` — a 6-step vertical flow with feedback arc, decorative margin sketches, and accent annotations:

```xml
<svg viewBox="0 0 672 920" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <filter id="roughen" x="-2%" y="-2%" width="104%" height="104%">
      <feTurbulence type="turbulence" baseFrequency="0.03" numOctaves="2" result="noise" seed="3"/>
      <feDisplacementMap in="SourceGraphic" in2="noise" scale="1.2" xChannelSelector="R" yChannelSelector="G"/>
    </filter>
    <filter id="glow">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <marker id="arrow" viewBox="0 0 12 10" refX="10" refY="5"
            markerWidth="8" markerHeight="6" orient="auto-start-reverse"
            fill="none" stroke="#e0e0e0" stroke-width="1.5"
            stroke-linecap="round" stroke-linejoin="round">
      <path d="M 1,1 L 10,5 L 1,9"/>
    </marker>
    <marker id="arrow-purple" viewBox="0 0 12 10" refX="10" refY="5"
            markerWidth="8" markerHeight="6" orient="auto-start-reverse"
            fill="none" stroke="rgb(168,85,247)" stroke-width="1.5"
            stroke-linecap="round" stroke-linejoin="round">
      <path d="M 1,1 L 10,5 L 1,9"/>
    </marker>
  </defs>

  <!-- TITLE with wobbly underline -->
  <text x="336" y="38" text-anchor="middle"
        font-family="'Segoe Print', 'Comic Sans MS', 'Caveat', cursive"
        font-size="22" fill="#e0e0e0" font-weight="bold"
        transform="rotate(-0.6, 336, 38)">
    Feedback Loop
  </text>
  <path d="M 182,46 C 230,48 340,44 490,47"
        stroke="rgb(168,85,247)" stroke-width="1.5" fill="none"
        stroke-linecap="round" opacity="0.6"/>

  <!-- STEP: Numbered callout + wobbly box + labels -->
  <g transform="rotate(-0.4, 336, 100)">
    <circle cx="108" cy="82" r="14" fill="rgb(168,85,247)" stroke="none" opacity="0.9"/>
    <text x="108" y="87" text-anchor="middle"
          font-family="'Segoe Print', 'Comic Sans MS', cursive"
          font-size="14" fill="white" font-weight="bold">1</text>

    <path d="M 132,68 C 230,65 430,71 562,67
             C 565,85 563,105 565,128
             C 430,131 230,127 132,131
             C 129,113 131,87 129,68"
          stroke="rgb(168,85,247)" stroke-width="2" fill="rgba(168,85,247,0.08)"
          stroke-linecap="round" stroke-linejoin="round"/>

    <text x="348" y="92" text-anchor="middle"
          font-family="'Segoe Print', 'Comic Sans MS', cursive"
          font-size="15" fill="#e0e0e0" font-weight="bold">Query Arrives</text>
    <text x="348" y="114" text-anchor="middle"
          font-family="'Segoe Print', 'Comic Sans MS', cursive"
          font-size="12" fill="#888888">vector similarity finds seed concepts</text>
  </g>

  <!-- ARROW between steps -->
  <path d="M 336,134 C 338,150 334,162 336,176"
        stroke="#e0e0e0" stroke-width="2" fill="none"
        stroke-linecap="round" marker-end="url(#arrow)"/>

  <!-- ... more steps ... -->

  <!-- FEEDBACK ARC: loops back from bottom to top -->
  <path d="M 128,790 C 78,788 42,760 38,700
           C 34,580 36,400 36,260
           C 36,160 42,100 62,82
           C 72,73 90,70 108,68"
        stroke="rgb(168,85,247)" stroke-width="2.2" fill="none"
        stroke-linecap="round" stroke-dasharray="8 5"
        opacity="0.7" filter="url(#glow)"
        marker-end="url(#arrow-purple)"/>

  <!-- DECORATIVE: Mini knowledge graph in margin -->
  <g transform="translate(580, 210)" opacity="0.35">
    <circle cx="0" cy="0" r="5" fill="rgb(168,85,247)" stroke="#e0e0e0" stroke-width="1"/>
    <circle cx="30" cy="-20" r="4" fill="rgb(168,85,247)" stroke="#e0e0e0" stroke-width="1"/>
    <circle cx="35" cy="15" r="4" fill="rgb(168,85,247)" stroke="#e0e0e0" stroke-width="1"/>
    <path d="M 4,0 C 15,-8 22,-16 27,-18" stroke="#e0e0e0" stroke-width="0.8" fill="none"/>
    <path d="M 4,3 C 15,8 28,12 32,14" stroke="#e0e0e0" stroke-width="0.8" fill="none"/>
  </g>

  <!-- BOTTOM CAPTION -->
  <text x="336" y="910" text-anchor="middle"
        font-family="'Segoe Print', 'Comic Sans MS', cursive"
        font-size="11" fill="#888888" opacity="0.6">
    each cycle sharpens the graph — good paths get stronger, bad paths decay
  </text>
</svg>
```

Also see: `portfolio/public/diagrams/broken-loop-vs-pipeline.svg`, `parking-lot-timeline.svg`, `pipeline-architecture.svg`, `ppr-traversal.svg`, `convergence-plot.svg`

---

## Reference Implementation

### Design System Style (CSS Variables)

See `portfolio/src/pages/lab.astro` — Five-layer agent architecture diagram with:
- 5 vertically stacked layers with mini-icons
- Downward flow lines with animated dashes between all layers
- Feedback loop (Interoception → Learning) with reverse animation on the left
- External signals input (left → Nervous System)
- Measurement output (Learning → right)
- Glow filter + pulse ring on the core (Learning) layer
- Clickable layers linking to project doc sites
- Full hover interaction CSS

### Hand-Drawn Style (Hardcoded Colors)

See `portfolio/public/diagrams/` — External SVG files for blog articles:
- `feedback-loop.svg` — 6-step vertical flow with feedback arc and margin decorations
- `ppr-traversal.svg` — Animated graph traversal with CSS keyframes
- `convergence-plot.svg` — Hand-drawn chart with wobbly axes and data curves
- `broken-loop-vs-pipeline.svg` — Side-by-side comparison with animated loop
- `pipeline-architecture.svg` — Numbered pipeline stages with I/O annotations
- `parking-lot-timeline.svg` — Horizontal timeline with alternating above/below labels
