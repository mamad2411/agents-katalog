---
name: baufest-brand
description: >-
  Apply Baufest brand identity — colors, typography, and voice — to any
  deliverable. Use this skill when styling documents, decks, emails, or any
  content that should look and sound like Baufest. Triggers for: brand colors,
  brand guidelines, Baufest styling, corporate identity, deck formatting,
  look-and-feel, brand voice, visual identity, branded output, magenta and
  green palette. Also use when generating CSS, design tokens, or theme
  configuration for Baufest-branded applications. Do NOT use for logo file
  requests (those require asset management) or for non-Baufest client branding.
license: Apache-2.0
metadata:
  author: baufest
  version: "1.0"
---

# Baufest Brand Guidelines

## Overview

This skill provides the complete Baufest visual and verbal identity system. Apply these standards to every deliverable — documents, presentations, applications, emails, and generated content — so that output is immediately recognizable as Baufest.

## Color Palette

### Primary Colors

| Role | Name | Hex | RGB | Usage |
|------|------|-----|-----|-------|
| Primary | Black | `#000000` | 0, 0, 0 | Backgrounds, primary text, headers |
| Accent 1 | Magenta | `#FF02AD` | 255, 2, 173 | CTAs, highlights, key data points, links |
| Accent 2 | Neon Green | `#AFFF00` | 175, 255, 0 | Secondary highlights, success states, badges |
| Neutral | White | `#FFFFFF` | 255, 255, 255 | Backgrounds, body text on dark |

### Extended Neutrals

| Name | Hex | Usage |
|------|-----|-------|
| Dark Gray | `#1A1A1A` | Subtle background variation |
| Mid Gray | `#4A4A4A` | Secondary text, borders |
| Light Gray | `#E5E5E5` | Dividers, background accents |
| Off-White | `#F5F5F5` | Light mode backgrounds |

### Color Application Rules

1. **Dark-first**: Default to dark backgrounds (`#000000` or `#1A1A1A`) with light text. Baufest's identity is bold and high-contrast.
2. **Magenta for emphasis**: Use `#FF02AD` for the single most important element on any page — a CTA, a key metric, or a highlight. Never use magenta for body text.
3. **Neon green sparingly**: `#AFFF00` is a secondary accent. Use for tags, badges, success indicators, or to create energy in data visualizations. Avoid large blocks of neon green.
4. **Contrast ratios**: Ensure WCAG AA compliance. White text on black passes. Magenta on black passes. Neon green on black passes. Magenta on white fails — use black text with magenta accents instead.
5. **No gradients** between brand colors unless explicitly approved. Flat color blocks are the default.

## Typography

### Font Stack

| Role | Font | Weight | Fallback |
|------|------|--------|----------|
| Headings | Barlow Semicondensed | 600 (SemiBold), 700 (Bold) | Arial Narrow, sans-serif |
| Body | Montserrat | 400 (Regular), 500 (Medium) | Arial, Helvetica, sans-serif |
| Code / Data | JetBrains Mono | 400 | Consolas, monospace |

### Typography Rules

1. **Headings**: Barlow Semicondensed, uppercase for H1 only. Sentence case for H2–H4. Tracking: +0.02em for headings.
2. **Body text**: Montserrat Regular (400) at 16px base. Line height 1.5. Paragraph spacing 1em.
3. **Emphasis**: Use Montserrat Medium (500) for inline emphasis rather than italic. Reserve bold (700) for critical callouts.
4. **Size scale**: 14 / 16 / 18 / 24 / 32 / 48px. Do not use sizes outside this scale without justification.

### CSS Variables (for application theming)

```css
:root {
  /* Colors */
  --bf-black: #000000;
  --bf-magenta: #FF02AD;
  --bf-green: #AFFF00;
  --bf-white: #FFFFFF;
  --bf-dark-gray: #1A1A1A;
  --bf-mid-gray: #4A4A4A;
  --bf-light-gray: #E5E5E5;
  --bf-off-white: #F5F5F5;

  /* Typography */
  --bf-font-heading: 'Barlow Semicondensed', 'Arial Narrow', sans-serif;
  --bf-font-body: 'Montserrat', Arial, Helvetica, sans-serif;
  --bf-font-mono: 'JetBrains Mono', Consolas, monospace;

  /* Spacing */
  --bf-space-xs: 4px;
  --bf-space-sm: 8px;
  --bf-space-md: 16px;
  --bf-space-lg: 32px;
  --bf-space-xl: 64px;
}
```

## Voice & Tone

### Core Attributes

1. **Precise**: State facts directly. Avoid hedging ("we believe", "we think"). Lead with the conclusion, then support it.
2. **Confident**: Use active voice. "We will deliver" not "It is expected that delivery will occur." Avoid qualifiers unless uncertainty is genuine.
3. **Forward-looking**: Frame everything in terms of what comes next, not what happened. "The next milestone is..." not "We completed...". Progress is assumed; direction is what matters.
4. **Technical but accessible**: Baufest teams are technical. Use precise terminology. But when writing for executives or mixed audiences, define terms on first use.

### Tone Calibration by Context

| Context | Tone Dial |
|---------|-----------|
| Client proposals | Confident + precise. No overselling. |
| Status reports | Forward-looking. Lead with next actions. |
| Architecture docs | Technical + precise. Show tradeoffs clearly. |
| Internal comms | Direct + concise. Respect the reader's time. |
| Marketing / case studies | Confident + outcome-focused. Quantify impact. |

### Writing Rules

1. **No passive voice** in headlines, subject lines, or opening sentences.
2. **Quantify** wherever possible. "Reduced latency by 40%" not "significantly improved performance."
3. **One idea per paragraph**. Short paragraphs. Generous whitespace.
4. **Bullet points** for lists of 3+ items. No walls of text.
5. **No jargon without definition** when audience includes non-engineers.

## Applying the Brand

When asked to style or format a deliverable:

1. **Documents (Markdown/HTML)**: Apply the color palette, font stack, and voice guidelines. Use dark headers with magenta accents. Structure with clear hierarchy.
2. **Presentations**: Black backgrounds, white text, magenta for emphasis. One idea per slide. Barlow Semicondensed for titles.
3. **Code/Applications**: Use the CSS variables above. Dark theme default. Magenta for interactive elements.
4. **Emails/Messages**: Concise. Forward-looking subject lines. Magenta only for key CTAs.
5. **Data Visualizations**: Black background, magenta for primary series, neon green for secondary, white for labels. No more than 4 colors per chart.
