---
name: sketches
description: Create hand-drawn-style visual sketches, wireframes, and diagrams using inline SVG. Produces rough, sketchy visuals with a whiteboard/napkin aesthetic (think Balsamiq or Excalidraw). Use when users ask to sketch, wireframe, mock up, diagram, or visually explain something -- including UI wireframes, architecture diagrams, flowcharts, process diagrams, concept sketches, and brainstorming visuals. Also use when users say "draw", "sketch", "wireframe", "mock up", "diagram", or "visualize".
metadata:
  openclaw:
    emoji: "\u270F\uFE0F"
---

# Sketches

Create hand-drawn-style SVG sketches that look like whiteboard drawings or napkin doodles. Never produce clean, polished vector graphics. Every output should feel informal and human.

## Sketch Types

### UI Wireframe

Use for page layouts, app screens, or component mockups. Include device frame (phone, tablet, or browser chrome), placeholder content (squiggly lines for text, X-boxes for images), and interactive elements (buttons, inputs, toggles).

### Architecture Diagram

Use for system overviews, service maps, or infrastructure layouts. Show components as labeled boxes, connections as arrows with labels, and group related items with dashed boundaries.

### Flowchart

Use for processes, decision trees, or user journeys. Use boxes for steps, diamonds for decisions, arrows for flow direction. Keep it top-to-bottom or left-to-right.

### Concept Sketch

Use for brainstorming, explaining ideas, or quick visual notes. Freeform layout. Mix icons, labels, arrows, and annotations. Prioritize clarity over structure.

## Core Technique: Sketchy SVG

The hand-drawn look comes from one principle: **replace geometric primitives with imperfect paths.**

### Sketchy Lines

Never use `<line>` for visible strokes. Use `<path>` with cubic beziers and slight vertical jitter (1-3px offset on control points).

```xml
<!-- Wrong: too clean -->
<line x1="50" y1="50" x2="250" y2="50" stroke="#333" stroke-width="2"/>

<!-- Right: wobbly and human -->
<path d="M 50,51 C 90,48 130,53 170,49 C 210,52 240,48 250,51"
      stroke="#333" stroke-width="2" fill="none" stroke-linecap="round"/>
```

### Sketchy Rectangles

Never use `<rect>` for content boxes. Build rectangles from 4-segment `<path>` elements with 1-3px jitter on each corner and midpoint.

```xml
<path d="M 52,51 C 120,48 230,53 298,50
         C 301,75 249,110 251,149
         C 200,152 100,148 52,151
         C 49,120 51,80 49,52"
      stroke="#333" stroke-width="2" fill="#fef9e7"
      stroke-linecap="round" stroke-linejoin="round"/>
```

**Jitter algorithm for rect(x, y, w, h):** Offset each corner by random(-2, 2) on both axes. Add 1-2 control points per edge, also jittered. Connect with cubic beziers (C command).

### Sketchy Circles

Replace `<circle>` with a closed bezier path that slightly overshoots its start point.

### When to Use Clean Primitives

Use actual `<rect>` and `<line>` only for:
- Background fills (`<rect width="100%" height="100%" fill="#fafafa"/>`)
- Grid/guide lines meant to be invisible structure
- Device frames (phone outlines, browser chrome) where crispness is expected
- The image-placeholder X pattern

## SVG Output Format

Always produce a complete, self-contained SVG. Every output must:

1. Start with `<svg viewBox="..." xmlns="http://www.w3.org/2000/svg">`
2. Set `viewBox` to appropriate dimensions (no fixed `width`/`height` -- let it be responsive)
3. Include a background rect as the first element
4. Be saveable as a standalone `.svg` file
5. Use no external dependencies (no linked stylesheets, fonts, or images)

### ViewBox Sizing Guide

| Sketch Type | Recommended ViewBox |
|-------------|-------------------|
| Mobile wireframe | `0 0 375 812` |
| Tablet wireframe | `0 0 768 1024` |
| Desktop wireframe | `0 0 1200 800` |
| Flowchart (3-5 steps, vertical) | `0 0 500 400` to `0 0 500 700` |
| Flowchart (horizontal) | `0 0 800 300` |
| Architecture diagram | `0 0 800 500` to `0 0 1000 600` |
| Concept sketch | `0 0 600 400` |
| Small diagram / icon | `0 0 300 200` |

Adjust as needed. The viewBox should fit the content with 20-40px margins on all sides.

## Style Guide

### Fonts

Use handwriting-style fonts. Declare a fallback stack:

```
font-family="'Segoe Print', 'Comic Sans MS', cursive"
```

- Titles: 18-24px, bold optional
- Labels: 14-16px
- Annotations: 11-13px
- Small notes: 9-11px

### Stroke Style

- Primary strokes: `stroke-width="2"`, `stroke-linecap="round"`, `stroke-linejoin="round"`
- Secondary strokes (connectors, guidelines): `stroke-width="1.5"`
- Faint strokes (placeholders, grid): `stroke-width="1"` with reduced opacity
- Always use `stroke-linecap="round"` for the hand-drawn feel

### Color Palette (Default: Whiteboard)

Use muted, natural colors. Avoid saturated or neon colors.

| Role | Color |
|------|-------|
| Background | `#fafafa` |
| Primary stroke | `#333333` |
| Secondary stroke | `#888888` |
| Placeholder lines | `#cccccc` |
| Fill: primary | `#fef9e7` (soft yellow) |
| Fill: secondary | `#d4e6f1` (soft blue) |
| Fill: accent | `#d5f5e3` (soft green) |
| Fill: warning | `#fadbd8` (soft pink) |
| Highlight | `#e74c3c` (red marker) |
| Links/actions | `#3498db` (blue marker) |

For other palettes (blueprint, notebook, pastel), see [references/svg-patterns.md](references/svg-patterns.md).

### Rotation for Casual Feel

Apply slight rotation transforms (0.5-2 degrees, alternating positive/negative) to element groups. This creates the "placed on a desk" feeling.

```xml
<g transform="rotate(-1.2, 150, 100)">
  <!-- box and label here -->
</g>
```

Vary the rotation per element. Do not rotate everything the same direction.

## Layout Principles

### Wireframes

- Use device frames (phone, browser) to set context
- Place elements in a single-column flow for mobile, multi-column for desktop
- Use squiggly horizontal lines for text placeholders
- Use X-boxes for image placeholders
- Space elements 20-30px apart vertically
- Use 16-24px margins from edges

### Flowcharts

- Flow top-to-bottom (preferred) or left-to-right
- Keep nodes 140-200px wide, 60-80px tall
- Space nodes 60-80px apart (enough room for arrows and labels)
- Center arrows between nodes
- Use diamonds (rotated squares) for decision points
- Label every arrow at decision points (yes/no, true/false)

### Architecture Diagrams

- Use a layered vertical stack or cluster layout
- Group related components with dashed boundary boxes and a group label
- Show data flow direction with arrows
- Label every connection
- Place external systems at the edges

### Concept Sketches

- No strict grid; organic placement is fine
- Use size to indicate importance (bigger = more important)
- Connect related ideas with arrows or lines
- Add annotations with callout lines
- Use numbered callouts for sequential explanations

## Building Blocks

### Arrows

Always draw arrow bodies as sketchy paths. Draw arrowheads as small open chevrons:

```xml
<path d="M 270,93 L 282,100 L 270,107" stroke="#555" stroke-width="2"
      fill="none" stroke-linecap="round" stroke-linejoin="round"/>
```

### Text Placeholders

Represent body text with 2-4 wavy horizontal lines of varying length:

```xml
<path d="M 50,80 C 100,78 200,82 300,80" stroke="#ccc" stroke-width="2"
      fill="none" stroke-linecap="round"/>
<path d="M 50,100 C 100,98 200,102 300,100" stroke="#ccc" stroke-width="2"
      fill="none" stroke-linecap="round"/>
<path d="M 50,120 C 100,118 150,122 200,119" stroke="#ccc" stroke-width="2"
      fill="none" stroke-linecap="round"/>
```

Make the last line shorter to simulate a paragraph ending.

### Image Placeholders

Use a rectangle with an X through it:

```xml
<rect x="50" y="50" width="200" height="120" fill="#e8e8e8" stroke="#999" stroke-width="1.5"/>
<line x1="50" y1="50" x2="250" y2="170" stroke="#bbb" stroke-width="1"/>
<line x1="250" y1="50" x2="50" y2="170" stroke="#bbb" stroke-width="1"/>
```

### Cross-Hatch Fill

For shaded or highlighted areas:

```xml
<defs>
  <pattern id="hatch" width="8" height="8" patternTransform="rotate(45)"
           patternUnits="userSpaceOnUse">
    <line x1="0" y1="0" x2="0" y2="8" stroke="#999" stroke-width="0.8" opacity="0.3"/>
  </pattern>
</defs>
```

## Pattern Reference

For detailed SVG snippet patterns (all primitive shapes, all arrow types, all icon symbols, complete wireframe examples, and all color palettes), read [references/svg-patterns.md](references/svg-patterns.md).

Load the patterns file when:
- Building a wireframe with multiple UI components (inputs, buttons, toggles, navbars)
- Needing specific icon shapes (user, cloud, database, gear, etc.)
- Using a non-default color palette (blueprint, notebook, pastel)
- Needing device frame templates (mobile, tablet, desktop)
- Building a complete multi-step flowchart

Do not load it for simple, single-element sketches where the patterns in this file suffice.

## Checklist

Before delivering a sketch, verify:

- [ ] Output is a complete, standalone SVG with `viewBox` and `xmlns`
- [ ] No `width`/`height` attributes on the root SVG (responsive)
- [ ] Background rect is present
- [ ] All visible boxes use sketchy paths, not clean `<rect>`
- [ ] All visible lines use sketchy paths, not clean `<line>`
- [ ] Handwriting font stack is used for all text
- [ ] Slight rotation applied to element groups (varied, not uniform)
- [ ] Colors are muted/pastel, not saturated
- [ ] File is self-contained with no external dependencies
- [ ] The sketch looks hand-drawn, not computer-generated
