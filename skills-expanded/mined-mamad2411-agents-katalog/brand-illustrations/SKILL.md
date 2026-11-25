---
name: brand-illustrations
description: Use when creating or updating SVG illustrations for documentation pages - ensures brand colors, consistent chart styling, and proper layout conventions
---

# Brand illustrations

Create SVG illustrations for Altua/Grunt documentation that follow brand guidelines and established conventions.

## Brand color palette

| Role | Hex | Usage |
| --- | --- | --- |
| Primary / bar fills | `#264653` | Chart bars, primary data elements |
| Teal | `#2a9d8f` | Bounds outlines, dimension arrows, positive annotations |
| Orange-red | `#e76f51` | Callout arrows, warning annotations, alignment guides |
| Label gray | `#64748b` | Axis labels, secondary text |
| Background | `#f8fafc` | SVG background fill |
| Chart background | `#ffffff` | Plot area fill |
| Chart border | `#e2e8f0` | Plot area stroke |
| Grid lines | `#f1f5f9` | Horizontal/vertical grid lines inside chart area |
| Dark text | `#334155` | Titles, headings |

Full palette (light to dark): `#000000`, `#ffffff`, `#264653`, cream, `#2a9d8f`, yellow-green, medium teal, light teal, light gray, near-white, `#e76f51`, orange, light orange, yellow.

## SVG conventions

- **Format:** SVG with `font-family="Segoe UI, system-ui, sans-serif"`
- **Viewbox:** ~520px wide for chart diagrams, scale height to content
- **Background:** Full-size rect with `fill="#f8fafc"` and `rx="8"`
- **Bar segments:** No corner radius (`rx` omitted), use `#264653`
- **Axis labels:** `text-anchor="end"` for Y-axis, `text-anchor="middle"` for X-axis, `font-size="10"` or `"11"`, fill `#64748b`
- **Dashed bounds:** `stroke-width="2"` with `stroke-dasharray="8 4"`
- **Arrowheads:** Use inline `<polygon>` elements, not SVG `<marker>`. Keeps sizing consistent across arrows.
- **Z-order:** Draw chart area (white rect) before dashed bounds so dashes render on top at full thickness
- **Text knockouts:** When a guide line crosses a title or label, place a `<rect>` filled with background color behind the text to keep it legible

## Arrowhead pattern

Horizontal (pointing left):
```xml
<line x1="105" y1="100" x2="72" y2="100" stroke="#e76f51" stroke-width="1.5"/>
<polygon points="64,100 72,97 72,103" fill="#e76f51"/>
```

Vertical (pointing down):
```xml
<line x1="205" y1="284" x2="205" y2="304" stroke="#e76f51" stroke-width="1.5"/>
<polygon points="205,312 202,304 208,304" fill="#e76f51"/>
```

Dimension arrows (horizontal, two-headed):
```xml
<line x1="110" y1="38" x2="450" y2="38" stroke="#2a9d8f" stroke-width="1"/>
<polygon points="110,38 118,34 118,42" fill="#2a9d8f"/>
<polygon points="450,38 442,34 442,42" fill="#2a9d8f"/>
```

## File location

Store illustrations in `/images/powerpoint-add-in/` (or the relevant product subfolder under `/images/`).

## Mintlify usage

Wrap images in a `<Frame>` with a descriptive caption:

```mdx
<Frame caption="Description of what the illustration shows">
  <img src="/images/powerpoint-add-in/example.svg" alt="Descriptive alt text" />
</Frame>
```
