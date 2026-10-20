---
name: branding-generator
description: "Brand identity docs, color palettes, typography, voice guidelines, logo prompts, asset checklist. Use when creating brand identity from scratch."
---

# Branding Generator

## Overview

Generate a complete brand identity document for user-facing projects. Covers color palette, typography, brand voice, logo concepts, and asset checklist. Only generate when the project has a user interface.

**Core principle:** BRANDING IS NOT DECORATION. IT'S THE FIRST IMPRESSION USERS HAVE OF THE PRODUCT.

## The Iron Law

```
NEVER GENERATE A BRAND IDENTITY WITHOUT KNOWING THE TARGET AUDIENCE AND PRODUCT PERSONALITY
```

## When to Use

- After spec is approved and project is user-facing
- User asks for branding help
- Before frontend implementation (colors + fonts needed)
- Only if project has UI (skip for APIs, CLIs, libraries)

## Brand Identity Document

### 1. Brand Foundation

```
### Brand Personality
[3-5 adjectives describing the brand]
- e.g.: Professional, Warm, Innovative, Trustworthy, Minimalist

### Target Audience
[Who this brand speaks to — not just demographic, but psychographic]

### Brand Voice
- Tone: [Professional / Casual / Playful / Authoritative / Empathetic]
- Formality: [Formal / Neutral / Casual]
- Vocabulary: [Technical / Simple / Industry-specific]
- Examples:
  - Good: "[On-brand message]"
  - Bad: "[Off-brand message]"
```

### 2. Color Palette

```css
:root {
  /* Primary — main brand color, used for CTAs, links, key UI elements */
  --color-primary: #2563EB;
  --color-primary-hover: #1D4ED8;
  --color-primary-light: #DBEAFE;

  /* Neutral — backgrounds, text, borders */
  --color-bg: #FFFFFF;
  --color-bg-secondary: #F9FAFB;
  --color-text: #111827;
  --color-text-secondary: #6B7280;
  --color-border: #E5E7EB;

  /* Semantic — status-based colors */
  --color-success: #10B981;
  --color-warning: #F59E0B;
  --color-error: #EF4444;
  --color-info: #3B82F6;

  /* Dark mode (if applicable) */
  --color-bg-dark: #0F172A;
  --color-text-dark: #F8FAFC;
}
```

### 3. Typography

```css
/* Font stack */
--font-heading: 'Inter', system-ui, -apple-system, sans-serif;
--font-body: 'Inter', system-ui, -apple-system, sans-serif;
--font-mono: 'JetBrains Mono', 'Fira Code', monospace;

/* Scale */
--text-xs: 0.75rem;
--text-sm: 0.875rem;
--text-base: 1rem;
--text-lg: 1.125rem;
--text-xl: 1.25rem;
--text-2xl: 1.5rem;
--text-3xl: 1.875rem;
--text-4xl: 2.25rem;
```

### 4. Logo Generation Prompt

If the project needs a logo, generate an AI image prompt:

```markdown
## Logo Prompt for AI Generation

Style: [Minimalist / Geometric / Mascot / Letter-mark / Abstract]
Mood: [Professional / Playful / Trustworthy / Innovative]
Subject: [Core concept represented visually]
Colors: [Primary colors from palette]
Format: SVG (for web) + PNG (for social)
```

### 5. Asset Checklist

```
☐ Logo (SVG + PNG, dark + light variants, favicon)
☐ Favicon (16×16, 32×32, 180×6, svg)
☐ Social card (1200×630 for Open Graph)
☐ App icon (for PWA/mobile — multiple sizes)
☐ Color palette (CSS variables file)
☐ Typography (font files or CDN links)
☐ Brand guidelines (one-page PDF or markdown)
```

## Red Flags

Skipping branding for a user-facing project. Using generic colors without thinking about brand personality. Generating a logo prompt without asking the user about their vision.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "We'll nail down the brand after launch" | Colors and fonts are baked into components from day one. Rebranding after launch means touching every stylesheet. |
| "Any professional-looking palette will do" | Generic palettes produce generic products. Brand personality must drive color choice, not the other way around. |
| "The developer can just pick fonts" | Typography communicates authority, warmth, or playfulness before a single word is read. It is a brand decision, not a style preference. |
| "We don't need brand guidelines for an MVP" | The MVP is often the only version investors and early users ever see. First impressions compound. |
| "We can use placeholder colors and swap them later" | Placeholder colors become permanent. Teams ship around them and replatform decisions get deferred indefinitely. |

## Your Human Partner's Signals You're Doing It Wrong

**Watch for these redirections:**
- "This doesn't feel like us" — you generated a generic brand instead of one grounded in the product's personality and audience
- "Can you make it less corporate / more playful / more premium?" — your tone and color choices didn't match the brand adjectives the user described
- "We already have a color, just extend from that" — you ignored existing brand seeds and started from scratch when you should have built on what exists
- "The contrast is too low" — you skipped the accessibility check (WCAG 4.5:1 minimum contrast ratio)
- "What do I actually do with this?" — your output was a description of a brand rather than actionable CSS variables, font links, and asset specifications

**When you see these:** STOP. Return to Brand Foundation (Section 1). Confirm personality adjectives, target audience, and any existing brand elements before regenerating the palette, typography, or voice.

## Related Skills

- **frontend-senior-engineer** — implements the brand tokens
- **spec-first-development** — spec determines if branding is needed

## Verification

- [ ] Project is user-facing (skip if API/CLI/library)
- [ ] Color palette has light mode + dark mode
- [ ] Typography scale covers all text sizes
- [ ] Accessibility: color contrast ≥ 4.5:1
- [ ] Assets in right formats (SVG, PNG, favicon)
