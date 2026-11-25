---
name: brand-guidelines
description: Applies Anthropic's official brand colors and typography to any sort of artifact that may benefit from having Anthropic's look-and-feel. Use it when brand colors or style guidelines, visual formatting, or company design standards apply.
license: Complete terms in LICENSE.txt
---

# Anthropic Brand Guidelines

## Color Palette

| Role | Color | Hex |
|------|-------|-----|
| Primary text | Dark | `#141413` |
| Light background | Light | `#faf9f5` |
| Accent orange | Orange | `#d97757` |
| Accent blue | Blue | `#6a9bcc` |
| Accent green | Green | `#788c5d` |

## Typography

**Headings**: Poppins (Arial fallback)
- Apply to text 24pt and larger
- Weights: 300 (light), 400 (regular), 600 (semibold)

**Body**: Lora (Georgia fallback)
- Apply to body content and smaller text
- Use italic variant for quotes and emphasis

## Loading Fonts

```html
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&family=Lora:ital,wght@0,400;1,400&display=swap" rel="stylesheet">
```

## CSS Variables

```css
:root {
  --color-dark: #141413;
  --color-light: #faf9f5;
  --color-accent-orange: #d97757;
  --color-accent-blue: #6a9bcc;
  --color-accent-green: #788c5d;
  --font-heading: 'Poppins', Arial, sans-serif;
  --font-body: 'Lora', Georgia, serif;
}
```

## Application Rules

- **Headings (≥24pt)**: Poppins
- **Body text**: Lora
- **Primary text color**: `#141413` (dark)
- **Background**: `#faf9f5` (light, warm white)
- **Accent colors**: Cycle through orange, blue, green for visual elements
- **Contrast**: Always ensure readability — dark text on light background

## Design Principles

- Clean, minimal aesthetic
- Warmth through off-white backgrounds (not pure white)
- Subtle sophistication — avoid garish colors
- Consistent brand application across all surfaces
