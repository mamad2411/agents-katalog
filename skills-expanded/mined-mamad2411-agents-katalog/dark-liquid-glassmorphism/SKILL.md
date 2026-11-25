---
name: dark-liquid-glassmorphism
description: Modern dark glassmorphism UI component library with liquid metal aesthetics. Features frosted glass panels on deep black backgrounds, subtle white edge highlights, fluid rounded corners, and chrome-like reflective accents. Combines iOS-style blur effects with premium liquid metal finishes. Use for futuristic dashboards, AI interfaces, premium dark-mode apps, and sophisticated modern UIs in Newgraph/Newfoundation projects.
---

# Dark Liquid Glassmorphism UI Library

A modern dark UI aesthetic combining frosted glass transparency with liquid metal highlights — sleek, futuristic, and premium.

## Design Philosophy

This style merges two aesthetics:
1. **Glassmorphism** — Frosted glass panels with backdrop blur, translucent backgrounds
2. **Liquid Metal** — Chrome-like edge highlights, reflective surfaces, fluid forms

The result is a sophisticated dark UI that feels both transparent and tactile.

## Components Included

1. **Glass Buttons** — Frosted pill buttons with subtle borders and glow
2. **Dropdown Menus** — Translucent menus with blur and edge highlights
3. **Glass Windows/Panels** — Floating cards with liquid chrome borders
4. **Checkboxes** — Minimal glass checkboxes with glow states
5. **Radio Buttons** — Circular glass controls with inner glow
6. **Showcase/Slideshow** — 3D stacked glass panels with depth

---

## Design Characteristics

### Background
- **Primary**: Pure black `#000000` or near-black `#0a0a0a`
- **Gradient option**: Subtle radial from `#0a0a0a` to `#000000`
- **Ambient shapes**: Soft blurred orbs or waves in dark grays

### Glass Panels
- **Background**: `rgba(255, 255, 255, 0.03)` to `rgba(255, 255, 255, 0.08)`
- **Backdrop blur**: `blur(20px)` to `blur(40px)`
- **Border**: 1px solid `rgba(255, 255, 255, 0.1)` with highlight on top/left
- **Border-radius**: 16px - 24px (generous rounding)

### Liquid Metal Edge Highlights
The signature look — bright white/silver edges that catch light:
```css
border: 1px solid rgba(255, 255, 255, 0.1);
box-shadow:
  inset 0 1px 0 rgba(255, 255, 255, 0.15),
  inset 1px 0 0 rgba(255, 255, 255, 0.05),
  0 0 20px rgba(0, 0, 0, 0.5);
```

### Typography
- **Font**: Newfoundation Whyte (brand font), -apple-system fallback
- **Primary text**: `rgba(255, 255, 255, 0.9)`
- **Secondary text**: `rgba(255, 255, 255, 0.5)`
- **Font weight**: 400 (Regular) for body, 500 (Medium) for headings

---

## CSS Variables

```css
:root {
  /* Backgrounds */
  --glass-bg-dark: #000000;
  --glass-bg-panel: rgba(255, 255, 255, 0.05);
  --glass-bg-panel-hover: rgba(255, 255, 255, 0.08);
  --glass-bg-elevated: rgba(255, 255, 255, 0.1);

  /* Borders */
  --glass-border: rgba(255, 255, 255, 0.1);
  --glass-border-highlight: rgba(255, 255, 255, 0.2);
  --glass-border-subtle: rgba(255, 255, 255, 0.05);

  /* Text */
  --glass-text-primary: rgba(255, 255, 255, 0.9);
  --glass-text-secondary: rgba(255, 255, 255, 0.5);
  --glass-text-tertiary: rgba(255, 255, 255, 0.3);

  /* Accent (lime/yellow-green glow) */
  --glass-accent: #E0FD8C;
  --glass-accent-glow: rgba(224, 253, 140, 0.3);

  /* Effects */
  --glass-blur: blur(20px);
  --glass-blur-heavy: blur(40px);
  --glass-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
  --glass-shadow-glow: 0 0 30px rgba(255, 255, 255, 0.05);

  /* Radius */
  --glass-radius-sm: 8px;
  --glass-radius-md: 12px;
  --glass-radius-lg: 16px;
  --glass-radius-xl: 24px;
  --glass-radius-pill: 100px;
}
```

---

## Component Reference

### 1. Glass Button

```html
<button class="glass-button">
  <span>Button Label</span>
</button>
<button class="glass-button primary">
  <span>Primary Action</span>
</button>
```

**Key styling:**
- Frosted background with subtle blur
- 1px border with top highlight
- Soft glow on hover
- Pill shape (border-radius: 100px)

### 2. Glass Dropdown

```html
<div class="glass-dropdown">
  <button class="glass-dropdown-trigger">
    <span>Select option</span>
    <svg class="chevron">...</svg>
  </button>
  <div class="glass-dropdown-menu">
    <div class="glass-menu-item selected">Option 1</div>
    <div class="glass-menu-item">Option 2</div>
    <div class="glass-divider"></div>
    <div class="glass-menu-item">Option 3</div>
  </div>
</div>
```

### 3. Glass Panel/Window

```html
<div class="glass-panel">
  <div class="glass-panel-header">
    <div class="glass-panel-dots">
      <span class="dot"></span>
      <span class="dot"></span>
      <span class="dot"></span>
    </div>
    <span class="glass-panel-title">Panel Title</span>
  </div>
  <div class="glass-panel-content">
    <!-- Content -->
  </div>
</div>
```

### 4. Glass Checkbox

```html
<label class="glass-checkbox">
  <input type="checkbox" />
  <span class="glass-checkbox-box"></span>
  <span class="glass-checkbox-label">Label</span>
</label>
```

### 5. Glass Radio

```html
<label class="glass-radio">
  <input type="radio" name="group" />
  <span class="glass-radio-circle"></span>
  <span class="glass-radio-label">Option</span>
</label>
```

### 6. Glass Slideshow (Stacked Panels)

3D perspective stack of glass panels, similar to Time Machine but with liquid glass aesthetic.

---

## Interaction States

| Component | State | Visual Change |
|-----------|-------|---------------|
| Button | Hover | Brighter background, subtle glow |
| Button | Active | Slight scale down, deeper shadow |
| Menu Item | Hover | White highlight bg `rgba(255,255,255,0.1)` |
| Checkbox | Checked | Lime accent fill with glow |
| Radio | Selected | Lime center dot with glow |
| Panel | Hover | Increased border brightness |

---

## The Liquid Metal Effect

Key technique for achieving the liquid chrome look:

```css
.liquid-edge {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid transparent;
  border-radius: 16px;
  position: relative;

  /* Gradient border for liquid effect */
  background:
    linear-gradient(rgba(255,255,255,0.05), rgba(255,255,255,0.02)) padding-box,
    linear-gradient(
      135deg,
      rgba(255,255,255,0.3) 0%,
      rgba(255,255,255,0.1) 50%,
      rgba(255,255,255,0.05) 100%
    ) border-box;

  /* Inner glow on top edge */
  box-shadow:
    inset 0 1px 1px rgba(255, 255, 255, 0.1),
    0 10px 40px rgba(0, 0, 0, 0.5);
}
```

---

## Ambient Background Elements

Add depth with blurred shapes behind panels:

```css
.ambient-orb {
  position: absolute;
  width: 300px;
  height: 300px;
  background: radial-gradient(
    circle,
    rgba(255, 255, 255, 0.03) 0%,
    transparent 70%
  );
  filter: blur(60px);
  pointer-events: none;
}
```

---

## Implementation Notes

1. **Backdrop filter support**: Use `@supports (backdrop-filter: blur())` for fallbacks.

2. **Performance**: Heavy blur can impact performance. Use `will-change: transform` on animated elements.

3. **Contrast**: Ensure text meets accessibility standards — `rgba(255,255,255,0.9)` on dark backgrounds provides good contrast.

4. **Border gradients**: Use the background-clip technique for gradient borders.

5. **Glow effects**: Use `box-shadow` with spread and blur for glows, not `filter: drop-shadow`.

6. **The 3-dot pattern**: Minimalist alternative to traffic lights — three small white dots vertically.

---

## Color Accents

While primarily monochrome, accent colors can be added:

| Accent | Color | Usage |
|--------|-------|-------|
| Lime (Primary) | `#E0FD8C` | Primary actions, selected states |
| Purple | `#a855f7` | Secondary highlights |
| Green | `#22c55e` | Success states |
| Red | `#ef4444` | Error/destructive |

Accents should glow subtly:
```css
box-shadow: 0 0 20px rgba(224, 253, 140, 0.3);
```

---

## Typography

| Element | Size | Weight | Color |
|---------|------|--------|-------|
| Panel Title | 14px | 500 | `rgba(255,255,255,0.9)` |
| Body Text | 14px | 400 | `rgba(255,255,255,0.7)` |
| Label | 13px | 400 | `rgba(255,255,255,0.5)` |
| Button | 14px | 500 | `rgba(255,255,255,0.9)` |
| Caption | 12px | 400 | `rgba(255,255,255,0.4)` |

---

## Usage Context

This library fits modern, premium UI requirements:
- AI/ML dashboards and interfaces
- Futuristic app designs
- Premium SaaS products
- Dark-mode first applications
- Music/media players
- Developer tools

See `assets/demo.html` for complete working implementation with all components.
