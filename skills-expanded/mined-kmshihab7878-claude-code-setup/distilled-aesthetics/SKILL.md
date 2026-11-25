---
name: distilled-aesthetics
description: Anti-AI-slop frontend aesthetics enforcement from Anthropic's cookbook. Typography, color, motion, backgrounds, and spatial composition guidelines that produce distinctive, non-generic UI. Use when building any web UI, landing page, dashboard, or component.
---

# Distilled Aesthetics — Anti-AI-Slop Frontend Guidelines

Extracted from Anthropic's official [Frontend Aesthetics Cookbook](https://github.com/anthropics/claude-cookbooks/blob/main/coding/prompting_for_frontend_aesthetics.ipynb) and enhanced with typography, theme, and composition presets.

## Core Directive

You tend to converge toward generic, "on distribution" outputs. In frontend design, this creates what users call the "AI slop" aesthetic. Avoid this: make creative, distinctive frontends that surprise and delight.

## The Four Pillars

### 1. Typography

Choose fonts that are beautiful, unique, and interesting. Avoid generic fonts; opt for distinctive choices that elevate the frontend's aesthetics.

**Never use:** Inter, Roboto, Arial, Open Sans, Lato, default system fonts

**Font categories by context:**
| Context | Fonts |
|---------|-------|
| Code aesthetic | JetBrains Mono, Fira Code, Space Grotesk |
| Editorial | Playfair Display, Crimson Pro, Fraunces |
| Startup | Clash Display, Satoshi, Cabinet Grotesk |
| Technical | IBM Plex family, Source Sans 3 |
| Distinctive | Bricolage Grotesque, Obviously, Newsreader |

**Pairing principle:** High contrast = interesting. Display + monospace, serif + geometric sans, variable font across weights.

**Weight extremes:** Use 100/200 vs 800/900, never 400 vs 600. Size jumps of 3x+, never 1.5x.

Pick one distinctive font, use it decisively. Load from Google Fonts. State your choice before coding.

### 2. Color & Theme

Commit to a cohesive aesthetic. Use CSS variables for consistency. Dominant colors with sharp accents outperform timid, evenly-distributed palettes. Draw from IDE themes and cultural aesthetics for inspiration.

**Anti-patterns to avoid:**
- Purple gradients on white backgrounds (the #1 AI slop signal)
- Evenly-distributed, balanced palettes (pick a dominant color)
- Default blue (#007bff) as primary

**Techniques:**
- Pick a dominant color, then one sharp accent
- Use CSS custom properties for theme-wide consistency
- Draw inspiration from IDE themes (Dracula, Catppuccin, Gruvbox, Nord, Solarized)
- Vary between light and dark themes across generations

### 3. Motion

Use animations for effects and micro-interactions. Prioritize CSS-only solutions for HTML. Use Motion library for React when available.

**Focus on high-impact moments:**
- One well-orchestrated page load with staggered reveals (`animation-delay`) creates more delight than scattered micro-interactions
- Scroll-triggered animations that surprise
- Hover states that transform rather than just color-shift
- Page transitions that guide attention

**Priority order:** Page load orchestration > scroll reveals > hover states > micro-interactions

### 4. Backgrounds & Visual Details

Create atmosphere and depth rather than defaulting to solid colors.

**Techniques:**
- Gradient meshes and layered CSS gradients
- Noise textures and grain overlays
- Geometric patterns with SVG or CSS
- Layered transparencies for depth
- Dramatic shadows (not subtle drop-shadows)
- Decorative borders with context-specific character
- Custom cursors for differentiation

### 5. Spatial Composition (Beyond Anthropic Cookbook)

**Techniques:**
- Asymmetric layouts, diagonal flow
- Grid-breaking elements that create focal points
- Overlap between sections for continuity
- Generous negative space OR controlled density (pick one)
- Avoid excessive centered layouts (AI slop signal)
- Avoid uniform rounded corners on everything

## Anti-Pattern Checklist

Before showing any frontend output, verify NONE of these are present:

| Anti-Pattern | Fix |
|---|---|
| Inter/Roboto/Arial font | Use a distinctive font from the categories above |
| Purple gradient on white | Pick a non-purple dominant color, or use dark theme |
| Everything centered | Use asymmetry, left-aligned text, grid-breaking elements |
| Uniform border-radius on all elements | Vary radii: sharp corners on some, rounded on others |
| Evenly-distributed color palette | One dominant color + one sharp accent |
| 400/600 font weights only | Use extremes: 100-200 for light, 800-900 for bold |
| Subtle 1.5x size hierarchy | Jump 3x+ between heading levels |
| Generic card grid layout | Break the grid, overlap, use asymmetry |
| No animation | Add page-load stagger at minimum |
| Solid white/gray background | Add gradient, texture, pattern, or atmospheric effect |

## Theme Presets

When the user doesn't specify a theme, pick one of these (rotate, never repeat):

### Solarpunk
Warm, optimistic (greens, golds, earth tones). Organic shapes mixed with technical elements. Nature-inspired textures. Bright, hopeful atmosphere. Retro-futuristic typography.

### Cyberpunk
Dark backgrounds, neon accents (cyan, magenta, electric blue). Glitch effects, scan lines. Monospace/terminal fonts. High contrast, low-light atmosphere.

### Editorial
Magazine-quality typography. Serif display fonts at extreme sizes. Generous whitespace. Muted, sophisticated palette. Grid-based with intentional breaks.

### Brutalist
Raw, honest interfaces. System fonts or monospace at large sizes. Exposed structure. High contrast black/white with one accent. Borders over shadows.

### Glassmorphism
Frosted glass effects with `backdrop-filter`. Layered depth with transparency. Soft, luminous color palette. Subtle border highlights.

### Retro Terminal
CRT-green-on-black or amber-on-dark. Scanline effects. Monospace fonts only. Blinking cursors. ASCII art accents.

## Cross-References

- **`/interface-design`** — For dashboards, admin panels, SaaS apps (persistent design system)
- **`/frontend-design`** — For landing pages, marketing sites, creative projects
- **`/baseline-ui`** — For animation limits, typography scale, layout anti-patterns
- **`/ui-ux-pro-max`** — For 50+ styles, 97 color palettes, 57 font pairings
- **`/fixing-motion-performance`** — For animation performance auditing
- **`/fixing-accessibility`** — For WCAG compliance on styled components
