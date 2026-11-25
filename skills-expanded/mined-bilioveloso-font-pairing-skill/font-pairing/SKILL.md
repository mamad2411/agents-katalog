---
name: font-pairing-skill
description: >-
  Typeface selection, pairing rules, loading strategy, and variable font guidance
  for UI and branding design. Use when choosing fonts, pairing a display with a
  body typeface, selecting a monospace font for code, setting type scale, or
  matching typography to a brand tier or palette. Works alongside color-combo-skill,
  design-effects-skill, and icon-system-skill. Activate on: "what font",
  "choose a typeface", "font pairing", "heading font", "body font", "monospace font",
  "type scale", "web font", "variable font", "/font-pairing-skill".
trigger_keywords:
  - font
  - typeface
  - font pairing
  - heading font
  - body font
  - monospace
  - type scale
  - web font
  - variable font
  - serif
  - sans-serif
  - display font
  - Google Fonts
  - /font-pairing-skill
author: bilioveloso
version: "1.1"
---

# Font Pairing Skill

## Purpose
This skill teaches an agent to make deliberate, brand-appropriate typeface decisions — from choosing a display font to pairing it with a body face, setting a type scale, and loading fonts efficiently. For any project requiring typography decisions, the agent should:

1. Identify the brand tier and mood.
2. Check the Archetype Recipes section first — if it matches, use that stack directly.
3. Use the Pairing Rules and Category Guide to customize if needed.
4. Cross-reference [color-combo-skill](https://github.com/bilioveloso/color-combo-skill) to confirm the palette matches the typographic mood.
5. Cross-reference [design-effects-skill](https://github.com/bilioveloso/design-effects-skill) to confirm the chosen typeface supports planned effects (variable weight animation, stroke text, gradient fill).
6. Cross-reference [icon-system-skill](https://github.com/bilioveloso/icon-system-skill) to ensure icon weight and style complement the type system.

## Core Rules
- **Never use more than 2 typefaces per project.** One display/heading face, one body face. A monospace for code counts as a third only in developer tools.
- **Type must work before effects are added.** A weak font with a gradient fill is just a weak font with a gradient fill.
- **Match optical weight.** A heavy display font needs a body font with enough personality to not disappear next to it.
- **Serif ≠ formal, Sans ≠ casual.** Match category to mood, not assumption.
- **Variable fonts are the default choice** when animation or responsive weight is needed.
- **Always define `font-display: swap`** to prevent invisible text during font loading.
- **Subset fonts** when loading from a CDN. Full font files are often 200KB+. Subset to Latin saves 60–80%.

---

## Typeface Categories

### Display / Heading Serifs
High personality, strong at large sizes, carries the brand's voice.

| Typeface | Mood | Brand tier | Variable? | Source |
|---|---|---|---|---|
| **Fraunces** | Literary, warm, editorial, craft | Premium, Luxury, Editorial | Yes | Google Fonts |
| **Playfair Display** | Classic, high-fashion, heritage | Luxury, Gothic, Rustic | No | Google Fonts |
| **Cormorant Garamond** | Refined, whisper-thin, old-world luxury | Luxury, High-end Fashion | No | Google Fonts |
| **DM Serif Display** | Modern editorial, confident | Premium SaaS, Creative | No | Google Fonts |
| **Libre Baskerville** | Trustworthy, readable, anchored | Corporate, Healthcare, Editorial | No | Google Fonts |
| **Lora** | Warm literary, human, calm authority | Wellness, Editorial, Luxury Facade | No | Google Fonts |

### Display / Heading Sans-Serifs
Modern, structural, brand-forward at scale.

| Typeface | Mood | Brand tier | Variable? | Source |
|---|---|---|---|---|
| **Clash Display** | Bold editorial, contemporary, fashion-forward | Creative, Premium, Acid | No | Fontshare (free) |
| **Syne** | Geometric, futuristic, art-adjacent | Creative Portfolio, Agency | No | Google Fonts |
| **Space Grotesk** | Tech-editorial, structured, slightly quirky | SaaS, Developer, Futuristic | No | Google Fonts |
| **Cabinet Grotesk** | Friendly-premium, modern, rounded authority | Consumer SaaS, Lifestyle, Premium | No | Fontshare (free) |
| **Bebas Neue** | Maximum impact, condensed, sports/editorial | Gaming, Sports, Esports | No | Google Fonts |
| **Outfit** | Clean, versatile, modern neutrality | Corporate, SaaS, Multipurpose | No | Google Fonts |
| **Plus Jakarta Sans** | Balanced, premium, slightly warm | Premium SaaS, Startup, App | No | Google Fonts |

### Body / Reading Faces
Optimized for comfort at 14–18px, long-form readability, and UI legibility.

| Typeface | Mood | Best paired with | Variable? | Source |
|---|---|---|---|---|
| **Inter** | Neutral, UI-native, precise | Almost anything sans-heavy | Yes | Google Fonts / rsms.me |
| **Geist** | Developer, clean, Vercel-adjacent | Space Grotesk, Syne, monospace | No | Vercel (free) |
| **DM Sans** | Friendly, modern, approachable | DM Serif Display, Fraunces | No | Google Fonts |
| **Nunito** | Warm, rounded, consumer-app | Clay UI, lifestyle apps, Claymorphism | No | Google Fonts |
| **Manrope** | Modern, balanced, slightly geometric | Space Grotesk, Cabinet Grotesk | No | Google Fonts |
| **Source Serif 4** | Editorial, readable, warm authority | Used alone or with Inter | Yes | Google Fonts |
| **Literata** | Long-form reading, eBook-quality | Editorial, journal, content-heavy UI | Yes | Google Fonts |

### Monospace / Code Faces
For developer tools, code blocks, terminals, and CLI-adjacent UI.

| Typeface | Mood | Source |
|---|---|---|
| **Geist Mono** | Clean, Vercel-adjacent, modern | Vercel (free) |
| **JetBrains Mono** | Developer-native, ligature-rich | JetBrains (free) |
| **Fira Code** | Open source, ligature-focused | Google Fonts |
| **IBM Plex Mono** | Corporate-developer, structured | Google Fonts |
| **Commit Mono** | Neutral, no-nonsense, invisible | commit-mono.com (free) |

---

## Pairing Rules

### The fundamental rule
Contrast one dimension, match another. If the display font is geometric (Clash Display), the body should be neutral (Inter). If the display is expressive (Fraunces), the body should be calm (DM Sans). Never pair two expressive faces.

### Weight contrast
- Display: 700–900 weight for headings
- Body: 400 for paragraphs, 500–600 for labels and UI text
- Never use the same weight for both heading and body at adjacent sizes

### Serif + Sans combinations (always safe)
```
Fraunces (heading) + Inter (body)           → editorial-premium, warm
Playfair Display (heading) + DM Sans (body) → classic luxury, approachable
Lora (heading) + Manrope (body)             → calm authority, wellness
DM Serif Display (heading) + Inter (body)   → modern editorial, SaaS
```

### Sans + Sans combinations (needs size contrast)
```
Clash Display (heading) + Inter (body)           → editorial-bold, contemporary
Syne (heading) + Manrope (body)                  → futuristic, creative
Space Grotesk (heading) + Geist (body)           → developer, tech
Cabinet Grotesk (heading) + Nunito (body)        → friendly-premium, consumer
Bebas Neue (heading) + Inter (body)              → sports, gaming, high-energy
Plus Jakarta Sans (heading) + Inter (body)       → startup, modern SaaS
```

### Anti-patterns — never do these
- Playfair Display + Cormorant Garamond (two expressive serifs — competing)
- Bebas Neue + Bebas Neue (same face at different sizes — not a system)
- Clash Display + Syne (two personality-heavy display faces — fighting)
- System font stack as a deliberate choice without acknowledging it's a choice

---

## Archetype Recipes

Complete font stacks per project type. Use these directly. They mirror the Page-Type Recipes in [design-effects-skill](https://github.com/bilioveloso/design-effects-skill) and the palettes in [color-combo-skill](https://github.com/bilioveloso/color-combo-skill).

### Recipe 1 — Premium AI / SaaS
- **Display:** Plus Jakarta Sans (700–800)
- **Body:** Inter (400, 500)
- **Mono:** Geist Mono (code blocks, CLI)
- **Effect compatibility:** Works with GradientText, BlurText, variable weight animation
- **Palette match:** Otherworldly, Dreamy Periwinkle, Silver Pulse
- **Icon match:** Phosphor (regular weight) or Lucide — see [icon-system-skill](https://github.com/bilioveloso/icon-system-skill)

### Recipe 2 — Gaming / Esports
- **Display:** Bebas Neue (400) or Space Grotesk (700–900)
- **Body:** Inter or Geist (400)
- **Effect compatibility:** Works with GlitchText, SplitText, outlined stroke text
- **Palette match:** Gaming / Esports (Midnight Frag, Ember Clan, Toxic Ranked)
- **Icon match:** Phosphor (bold weight) or custom SVG — see [icon-system-skill](https://github.com/bilioveloso/icon-system-skill)
- **Note:** Bebas Neue needs letter-spacing: 0.08em minimum

### Recipe 3 — Wellness / Healthcare
- **Display:** Lora (600–700) or Fraunces (600)
- **Body:** DM Sans (400) or Manrope (400)
- **Effect compatibility:** Works with FadeContent, BlurText (slow), subtle variable weight
- **Palette match:** Nature / Organic (Eucalyptus Glow), Healthcare (Clinical Clarity, Vital Green), Soft Gradients
- **Icon match:** Phosphor (light or regular, rounded) — see [icon-system-skill](https://github.com/bilioveloso/icon-system-skill)

### Recipe 4 — Developer Tool / Open Source
- **Display:** Space Grotesk (700) or Outfit (700–800)
- **Body:** Geist (400) or Inter (400)
- **Mono:** JetBrains Mono or Geist Mono
- **Effect compatibility:** Works with ShinyText (badge), SVG stroke animation, CountUp
- **Palette match:** Acid Contemporary (Ink Volt), Minimalist (Bone & Carbon, Chalk & Ink)
- **Icon match:** Lucide or Heroicons (stroke, 1.5px) — see [icon-system-skill](https://github.com/bilioveloso/icon-system-skill)

### Recipe 5 — Creative Portfolio / Agency
- **Display:** Clash Display (600–700) or Syne (700–800)
- **Body:** Manrope (400) or Inter (400)
- **Effect compatibility:** Works with variable font hover, outlined stroke text, SplitText, GlitchText
- **Palette match:** Any — commit to one. Luxury, Gothic / Dark Romance, Acid Contemporary all work.
- **Icon match:** Minimal or custom — see [icon-system-skill](https://github.com/bilioveloso/icon-system-skill)

### Recipe 6 — Consumer Lifestyle App
- **Display:** Cabinet Grotesk (700–800) or Plus Jakarta Sans (700)
- **Body:** Nunito (400–500) or DM Sans (400)
- **Effect compatibility:** Works with BlurText, RotatingText, CountUp
- **Palette match:** Warm Tropical / Resort, Soft Gradients (Peach Champagne, Dreamy Periwinkle)
- **Icon match:** Phosphor (regular, rounded preferred) — see [icon-system-skill](https://github.com/bilioveloso/icon-system-skill)

### Recipe 7 — Dark Editorial / Magazine
- **Display:** Playfair Display (700–900) or Fraunces (700–900)
- **Body:** Lora (400) or Source Serif 4 (400)
- **Effect compatibility:** Works with oversized display texture, outlined stroke text, FadeContent, variable weight hover
- **Palette match:** Gothic / Dark Romance (Velvet Crypt, Bone & Wine), Luxury
- **Icon match:** Minimal — see [icon-system-skill](https://github.com/bilioveloso/icon-system-skill)

### Recipe 8 — Enterprise Dashboard / B2B SaaS
- **Display:** Inter (600–700) or Outfit (600–700)
- **Body:** Inter (400) or Manrope (400)
- **Mono:** IBM Plex Mono or Commit Mono (data tables and code values)
- **Effect compatibility:** Works with Skeleton loaders, CountUp, FadeContent, AnimatedList
- **Palette match:** Corporate / Enterprise (Steel Authority, Slate Trust), Minimalist
- **Icon match:** Lucide or Heroicons (consistent stroke, 16–20px) — see [icon-system-skill](https://github.com/bilioveloso/icon-system-skill)

---

## Type Scale

```css
/* Major Third scale (×1.25) — compact UI */
:root {
  --text-xs:   0.64rem;   /* 10.2px */
  --text-sm:   0.8rem;    /* 12.8px */
  --text-base: 1rem;      /* 16px */
  --text-lg:   1.25rem;   /* 20px */
  --text-xl:   1.563rem;  /* 25px */
  --text-2xl:  1.953rem;  /* 31px */
  --text-3xl:  2.441rem;  /* 39px */
  --text-4xl:  3.052rem;  /* 49px */
  --text-hero: clamp(3rem, 7vw, 6rem);
}

/* Perfect Fourth scale (×1.333) — editorial / expressive */
:root {
  --text-xs:   0.563rem;
  --text-sm:   0.75rem;
  --text-base: 1rem;
  --text-lg:   1.333rem;
  --text-xl:   1.777rem;
  --text-2xl:  2.369rem;
  --text-3xl:  3.157rem;
  --text-4xl:  4.209rem;
  --text-hero: clamp(3.5rem, 9vw, 7rem);
}
```

---

## Variable Fonts

```css
@font-face {
  font-family: 'Inter Variable';
  src: url('/fonts/InterVariable.woff2') format('woff2-variations');
  font-weight: 100 900;
  font-display: swap;
}

.headline {
  font-family: 'Inter Variable', sans-serif;
  font-variation-settings: 'wght' 300;
  transition: font-variation-settings 0.35s cubic-bezier(0.22, 1, 0.36, 1);
}
.headline:hover {
  font-variation-settings: 'wght' 800;
}
```

**Free variable fonts:**
- Inter Variable — [rsms.me/inter](https://rsms.me/inter)
- Source Serif 4, Literata, Fraunces — Google Fonts
- Recursive — [recursive.design](https://www.recursive.design) (includes MONO axis)

---

## Web Font Loading

```html
<!-- Preconnect in <head> -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

<!-- Preload critical font -->
<link rel="preload" href="/fonts/InterVariable.woff2" as="font" type="font/woff2" crossorigin>
```

```css
/* Font stack fallbacks */
--font-sans:  'Inter Variable', 'Inter', system-ui, -apple-system, sans-serif;
--font-serif: 'Fraunces', 'Georgia', serif;
--font-mono:  'Geist Mono', 'JetBrains Mono', 'Fira Code', monospace;
```

---

## Effects Compatibility

Cross-reference with [design-effects-skill](https://github.com/bilioveloso/design-effects-skill).

| Effect | Best typefaces | Avoid |
|---|---|---|
| Variable weight animation | Inter Variable, Source Serif 4, Fraunces | Non-variable fonts |
| Outlined / stroke text | Clash Display, Bebas Neue, Syne, Fraunces | Thin or script faces |
| Gradient text fill | Any bold sans or serif at large size | Light weights under 40px |
| Oversized display texture | Bebas Neue, Clash Display, Playfair Display | Body-weight faces |
| GlitchText | Space Grotesk, Bebas Neue, Syne | Thin serifs |
| BlurText | Inter, DM Sans, Plus Jakarta Sans | Decorative scripts |
| Kinetic / scroll-driven | Variable fonts only | Static fonts |

---

## Color & Palette Match

Cross-reference with [color-combo-skill](https://github.com/bilioveloso/color-combo-skill).

| Palette | Display font | Body font |
|---|---|---|
| Golden Obsession (Luxury) | Playfair Display or Cormorant | DM Sans |
| Midnight Frag (Gaming) | Bebas Neue or Space Grotesk | Inter or Geist |
| Dreamy Periwinkle (Soft Gradients) | Plus Jakarta Sans or Cabinet Grotesk | Nunito or DM Sans |
| Clinical Clarity (Healthcare) | Libre Baskerville or Outfit | Inter or Manrope |
| Ink Volt (Acid Contemporary) | Clash Display or Bebas Neue | Inter |
| Velvet Crypt (Gothic) | Playfair Display or Fraunces | Lora or Source Serif 4 |
| Steel Authority (Corporate) | Inter or Outfit | Inter or Manrope |
| Eucalyptus Glow (Nature / Organic) | Fraunces or Lora | DM Sans |
| Mango Shore (Warm Tropical) | Cabinet Grotesk or Plus Jakarta Sans | Nunito |
| Bone & Carbon (Minimalist) | DM Serif Display or Cormorant | Inter |

---

## Skill Network

This skill is part of a four-skill design system. Each skill cross-references the others:

| Skill | What it covers | Repo |
|---|---|---|
| **color-combo-skill** | Named palettes, contrast tiers, CSS usage | [github.com/bilioveloso/color-combo-skill](https://github.com/bilioveloso/color-combo-skill) |
| **design-effects-skill** | Animations, morphisms, motion patterns, page recipes | [github.com/bilioveloso/design-effects-skill](https://github.com/bilioveloso/design-effects-skill) |
| **font-pairing-skill** | Typeface selection, pairing rules, type scale | *This skill* |
| **icon-system-skill** | Icon library selection, sizing, weight, animated icons | [github.com/bilioveloso/icon-system-skill](https://github.com/bilioveloso/icon-system-skill) |

> **Need pre-built UI components?** [React Bits](https://www.reactbits.dev/get-started/index) has ready-to-use animated and interactive components that pair well with these font stacks. Install only the specific component you need and credit the source when adapting their work.

---

## Google Fonts Import Reference

Copy-paste `@import` URLs for the most common pairings. Add to the top of your CSS file or use `<link>` tags in `<head>`. All include `display=swap` for performance.

### Luxury / Editorial

| Pairing | Import |
|---|---|
| Playfair Display + Inter | `@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@400;500;600;700&display=swap');` |
| Cormorant Garamond + Libre Baskerville | `@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600;700&family=Libre+Baskerville:wght@400;700&display=swap');` |
| Cormorant + Montserrat | `@import url('https://fonts.googleapis.com/css2?family=Cormorant:wght@400;500;600;700&family=Montserrat:wght@300;400;500;600;700&display=swap');` |
| Bodoni Moda + Jost | `@import url('https://fonts.googleapis.com/css2?family=Bodoni+Moda:wght@400;500;600;700&family=Jost:wght@300;400;500;600;700&display=swap');` |
| Lora + Raleway (Wellness) | `@import url('https://fonts.googleapis.com/css2?family=Lora:wght@400;500;600;700&family=Raleway:wght@300;400;500;600;700&display=swap');` |
| Great Vibes + Cormorant Infant (Wedding) | `@import url('https://fonts.googleapis.com/css2?family=Cormorant+Infant:wght@300;400;500;600;700&family=Great+Vibes&display=swap');` |

### Corporate / SaaS / Dashboard

| Pairing | Import |
|---|---|
| Inter (all weights) | `@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');` |
| Plus Jakarta Sans | `@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');` |
| Poppins + Open Sans | `@import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@300;400;500;600;700&family=Poppins:wght@400;500;600;700&display=swap');` |
| Lexend + Source Sans 3 (Accessibility) | `@import url('https://fonts.googleapis.com/css2?family=Lexend:wght@300;400;500;600;700&family=Source+Sans+3:wght@300;400;500;600;700&display=swap');` |
| IBM Plex Sans (Finance) | `@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600;700&display=swap');` |
| Figtree + Noto Sans (Healthcare) | `@import url('https://fonts.googleapis.com/css2?family=Figtree:wght@300;400;500;600;700&family=Noto+Sans:wght@300;400;500;700&display=swap');` |
| Fira Code + Fira Sans (Dashboard/Data) | `@import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600;700&family=Fira+Sans:wght@300;400;500;600;700&display=swap');` |

### Tech / Developer / Startup

| Pairing | Import |
|---|---|
| Space Grotesk + DM Sans | `@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');` |
| JetBrains Mono + IBM Plex Sans | `@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap');` |
| Outfit + Work Sans | `@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Work+Sans:wght@300;400;500;600;700&display=swap');` |
| Syne + Manrope (Fashion Forward) | `@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;600;700&family=Syne:wght@400;500;600;700&display=swap');` |
| Archivo + Space Grotesk (Portfolio) | `@import url('https://fonts.googleapis.com/css2?family=Archivo:wght@300;400;500;600;700&family=Space+Grotesk:wght@300;400;500;600;700&display=swap');` |

### Gaming / Esports / Bold

| Pairing | Import |
|---|---|
| Bebas Neue + Source Sans 3 | `@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Source+Sans+3:wght@300;400;500;600;700&display=swap');` |
| Russo One + Chakra Petch | `@import url('https://fonts.googleapis.com/css2?family=Chakra+Petch:wght@300;400;500;600;700&family=Russo+One&display=swap');` |
| Orbitron + Exo 2 (Crypto/Web3) | `@import url('https://fonts.googleapis.com/css2?family=Exo+2:wght@300;400;500;600;700&family=Orbitron:wght@400;500;600;700&display=swap');` |
| Barlow Condensed + Barlow (Sports) | `@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;500;600;700&family=Barlow:wght@300;400;500;600;700&display=swap');` |
| Space Mono (Brutalism) | `@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&display=swap');` |

### Editorial / News / Blog

| Pairing | Import |
|---|---|
| Newsreader + Roboto | `@import url('https://fonts.googleapis.com/css2?family=Newsreader:wght@400;500;600;700&family=Roboto:wght@300;400;500;700&display=swap');` |
| Libre Bodoni + Public Sans (Magazine) | `@import url('https://fonts.googleapis.com/css2?family=Libre+Bodoni:wght@400;500;600;700&family=Public+Sans:wght@300;400;500;600;700&display=swap');` |
| EB Garamond + Lato (Legal/Academic) | `@import url('https://fonts.googleapis.com/css2?family=EB+Garamond:wght@400;500;600;700&family=Lato:wght@300;400;700&display=swap');` |
| Crimson Pro + Atkinson Hyperlegible (Research) | `@import url('https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:wght@400;700&family=Crimson+Pro:wght@400;500;600;700&display=swap');` |

### Playful / Kids / Craft

| Pairing | Import |
|---|---|
| Fredoka + Nunito (Playful) | `@import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@400;500;600;700&family=Nunito:wght@300;400;500;600;700&display=swap');` |
| Baloo 2 + Comic Neue (Kids) | `@import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@400;500;600;700&family=Comic+Neue:wght@300;400;700&display=swap');` |
| Amatic SC + Cabin (Indie/Craft) | `@import url('https://fonts.googleapis.com/css2?family=Amatic+SC:wght@400;700&family=Cabin:wght@400;500;600;700&display=swap');` |
| Varela Round + Nunito Sans (Soft) | `@import url('https://fonts.googleapis.com/css2?family=Nunito+Sans:wght@300;400;500;600;700&family=Varela+Round&display=swap');` |

### Restaurant / Hospitality / Food

| Pairing | Import |
|---|---|
| Playfair Display SC + Karla (Restaurant) | `@import url('https://fonts.googleapis.com/css2?family=Karla:wght@300;400;500;600;700&family=Playfair+Display+SC:wght@400;700&display=swap');` |
| Abril Fatface + Merriweather (Retro) | `@import url('https://fonts.googleapis.com/css2?family=Abril+Fatface&family=Merriweather:wght@300;400;700&display=swap');` |

### Accessibility-Critical

| Pairing | Import |
|---|---|
| Atkinson Hyperlegible (single) | `@import url('https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:wght@400;700&display=swap');` |
| Lexend + Source Sans 3 | `@import url('https://fonts.googleapis.com/css2?family=Lexend:wght@300;400;500;600;700&family=Source+Sans+3:wght@300;400;500;600;700&display=swap');` |

> **Note:** Fontshare fonts (Clash Display, Cabinet Grotesk, Satoshi) are not on Google Fonts. Download from [fontshare.com](https://www.fontshare.com) and self-host, or use the Fontshare CDN.

```html
<!-- Fontshare CDN example -->
<link href="https://api.fontshare.com/v2/css?f[]=clash-display@400,500,600,700&display=swap" rel="stylesheet">
```
