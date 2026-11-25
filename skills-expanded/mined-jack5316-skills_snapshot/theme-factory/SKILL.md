---
name: theme-factory
description: Toolkit for styling artifacts with a theme. These artifacts can be slides, docs, reportings, HTML landing pages, etc. There are 10 pre-set themes with colors/fonts that you can apply to any artifact that has been created, or can generate a new theme on-the-fly.
license: Complete terms in LICENSE.txt
---

# Theme Factory

Apply professional themes to presentations, documents, and web pages using curated color palettes and font pairings.

## Available Themes

10 themes are available, each with a curated color palette and font pairings:

1. **Ocean Depths** — Professional and calming maritime theme
2. **Sunset Boulevard** — Warm and vibrant sunset colors
3. **Forest Canopy** — Natural and grounded earth tones
4. **Modern Minimalist** — Clean and contemporary grayscale
5. **Golden Hour** — Rich and warm autumnal palette
6. **Arctic Frost** — Cool and crisp winter-inspired theme
7. **Desert Rose** — Soft and sophisticated dusty tones
8. **Tech Innovation** — Bold and modern tech aesthetic
9. **Botanical Garden** — Fresh and organic garden colors
10. **Midnight Galaxy** — Dramatic and cosmic deep tones

Each theme specification includes a cohesive color palette with hex codes and complementary font pairings for headers and body text.

See `themes/` directory for complete color and font specifications per theme.

## Custom Theme Creation

When existing themes don't fit, generate a custom theme by specifying:
- **Mood/context**: Corporate, creative, technical, warm, cool, etc.
- **Key color**: Starting point for the palette
- **Industry**: Finance, healthcare, tech, arts, etc.

Apply complementary color theory:
1. Start with the key color
2. Find analogous colors for secondary
3. Use complementary color for accent
4. Derive light version for background

## Applying Themes

### CSS
```css
:root {
  --color-primary: [primary hex];
  --color-secondary: [secondary hex];
  --color-accent: [accent hex];
  --color-bg: [background hex];
  --font-heading: '[Heading Font]', serif;
  --font-body: '[Body Font]', sans-serif;
}

h1, h2, h3 { font-family: var(--font-heading); color: var(--color-primary); }
body { font-family: var(--font-body); background: var(--color-bg); }
.accent { color: var(--color-accent); }
```

### Google Fonts Import
```html
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Source+Sans+Pro:wght@400;600&display=swap" rel="stylesheet">
```

## Process

1. User describes their artifact and context
2. Present 3 relevant theme options with previews
3. User selects (or requests custom)
4. Apply theme colors and fonts consistently throughout
5. Verify visual consistency before finishing
