---
name: design-md-chrome
description: Automated design system extractor that inspects websites, extracts computed styles, typography, color palettes, spacing tokens, and generates a structured DESIGN.md file.
---

# design-md-chrome: Design System Extractor

Extracts design systems from any web page or live URL into a standardized `DESIGN.md` specification for AI coding agents.

## Extraction Pipeline
1. **DOM & CSS Inspection**:
   - Queries `:root` and computed styles for CSS variables (`--color-*`, `--radius-*`, `--font-*`).
   - Identifies background colors, foreground typography, primary brand accents, and contrast ratios.
2. **Typography Hierarchy**:
   - Extracts font families (Google Fonts, custom web fonts, system fallbacks).
   - Maps font sizes, line heights, and weights for `H1`, `H2`, `H3`, `Body`, and `Caption`.
3. **Spacing & Elevation**:
   - Computes standard container widths, grid gaps, padding tokens, and shadow elevations.
4. **Export**:
   - Synthesizes an interactive `DESIGN.md` file ready to drop into any project root.
