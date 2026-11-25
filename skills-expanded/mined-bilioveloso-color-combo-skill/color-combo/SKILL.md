---
name: color-combo-skill
description: >-
  Curated named color palettes grouped by mood, style, and intent.
  Use when choosing colors for UI, branding, content, or visual design.
  Includes hex codes, color roles, gradient pairs with CSS, and WCAG contrast notes.
  Trigger on: "choose colors", "color palette", "color scheme", "what colors should I use",
  "palette for", "/color-combo-skill", intent=color_choice, intent=design.
license: MIT
metadata:
  author: bilioveloso
  version: "2.0.0"
  date: June 2026
trigger_keywords:
  - color palette
  - color scheme
  - choose colors
  - what colors
  - palette for
  - color combo
  - /color-combo-skill
---

# Color Combo Skill

Curated named color palettes grouped by mood, style, and intent. When choosing colors
for any visual output — UI, branding, content, or design — follow this workflow:

1. Consult the Decision Guide to identify the right category.
2. Pick the named combo that fits the mood.
3. Apply colors using the defined roles consistently.
4. Check WCAG contrast notes before using Accent on text.

## Skill Network

This skill is part of a modular design system. After choosing a palette here, chain to:

| Need | Skill to load next |
|---|---|
| Visual effects, glass morphism, gradients, motion | `design-effects-skill` |
| Typeface and font pairing that matches the palette mood | `font-pairing-skill` |
| Icon library, sizing, and weight to match the palette style | `icon-system-skill` |

For a complete design brief (colors + effects + fonts + icons in one pass), load the **design-mapper** entry point first — it routes to all four skills in the right order.

## Color Roles

- **Primary** — dominant background or base color.
- **Secondary** — supporting surface or text background.
- **Accent** — highlight, CTA, or attention-grabbing element.
- **Supporting** — subtle fill, border, divider, or shadow tones.

## Implementation Pattern

Emit palette choices as CSS custom properties so any UI system can consume them:

```css
:root {
  --color-primary:    <hex>;
  --color-secondary:  <hex>;
  --color-accent:     <hex>;
  --color-supporting: <hex>;
}
```

## Decision Guide

| Goal | Category to use |
|---|---|
| Premium, exclusive, editorial | Luxury |
| Aspirational, polished, budget-friendly | Luxury Facade |
| Calm, clean, editorial, soft brand | Luxury Facade › Soft Prestige |
| Futuristic, neon, surreal, cyber | Otherworldly |
| Disruptive, urban, bold, street-level | Acid Contemporary |
| Replacing a raw default color with a tasteful alternative | Refined Defaults |
| Soft background, calming gradient, wellness, airy UI | Soft Gradients |
| Organic, eco, botanical, outdoor, farm-to-table | Nature / Organic |
| Clean, structured, whitespace-first, mono | Minimalist |
| Artisan, coffee, wood, handmade, craft food | Rustic / Craft |
| Dark editorial, candles, alternative, perfume niche | Gothic / Dark Romance |
| Resort, cocktails, tropical, summer hospitality | Warm Tropical / Resort |
| Nostalgia, 70s/90s revival, vintage branding | Retro / Vintage |
| B2B SaaS, enterprise software, finance, legal | Corporate / Enterprise |
| Medical, clinical, healthcare, pharma, wellness tech | Healthcare / Medical |
| Gaming, esports, streaming, competitive, dark neon | Gaming / Esports |
| Spring campaign, seasonal refresh, renewal | Seasonal / Spring |
| Summer campaign, outdoor, peak season | Seasonal / Summer |
| Autumn campaign, harvest, back-to-school | Seasonal / Autumn |
| Winter campaign, holiday, festive | Seasonal / Winter |

---

## Luxury

High-end, genuinely premium, opulent palettes. Use when the output must feel expensive, exclusive, and authoritative.

### Golden Obsession
- Style: Bold, opulent, high-impact luxury.
- Primary: #0B0B0F
- Secondary: #1C1A17
- Accent: #D4AF37
- Supporting: #B87333, #2D3138, #E9E1D0
- Best for: Premium branding, fashion, luxury product visuals, dramatic editorial layouts.
- WCAG: Accent (#D4AF37) on Primary (#0B0B0F) → **9.8:1 ✅** (AAA). Safe for all text sizes.

### Arctic Prestige
- Style: Pure, crisp, controlled, refined luxury.
- Primary: #F5F8FA
- Secondary: #D6DEE6
- Accent: #9DB4C6
- Supporting: #5C7386, #1E2A39, #0B0F14
- Best for: Minimal premium UI, cold-tech branding, high-trust interfaces, clean editorial design.
- WCAG: Accent (#9DB4C6) on Primary (#F5F8FA) → **2.8:1 ⚠️** Decorative use only. Use Supporting #1E2A39 for body text → **12.1:1 ✅**.

### Volcanic Intensity
- Style: Fierce, energetic, aggressive luxury.
- Primary: #0B0B0B
- Secondary: #1A1A1D
- Accent: #FF4D00
- Supporting: #8B1E00, #4A4746, #F2F1EE
- Best for: Sports branding, performance themes, launch campaigns, bold visual identities.
- WCAG: Accent (#FF4D00) on Primary (#0B0B0B) → **5.1:1 ✅** (AA). Safe for large text and UI components.

### Futuristic Elegance
- Style: Sleek, cinematic, modern, premium-tech luxury.
- Primary: #F6F2E8
- Secondary: #C5C0C9
- Accent: #4B2E83
- Supporting: #0D1B2A, #FF7A00, #8FA7FF
- Best for: Luxury tech, innovation branding, futuristic interfaces, product storytelling.
- WCAG: Accent (#4B2E83) on Primary (#F6F2E8) → **8.4:1 ✅** (AAA).

### Emerald Dynasty
- Style: Regal, timeless, heritage-rich, ornate luxury.
- Primary: #0A5E4E
- Secondary: #093B33
- Accent: #D8C08A
- Supporting: #F2EDE1, #103F46, #071B1E
- Best for: Heritage brands, premium hospitality, jewel-tone identities, luxury packaging.
- WCAG: Accent (#D8C08A) on Primary (#0A5E4E) → **5.7:1 ✅** (AA).

### Gradients

#### Obsidian Gold
- Saturated Stop: #1C1A17 → Light Stop: #D4AF37
- Style: Opulent, dramatic, deep-luxury.
```css
background: linear-gradient(135deg, #1C1A17 0%, #D4AF37 100%);
```

#### Champagne Mist
- Saturated Stop: #C5C0C9 → Light Stop: #F6F2E8
- Style: Soft, sophisticated, cool luxury.
```css
background: linear-gradient(135deg, #C5C0C9 0%, #F6F2E8 100%);
```

#### Emerald Dusk
- Saturated Stop: #0A5E4E → Light Stop: #D8C08A
- Style: Rich, jewel-tone, heritage warmth.
```css
background: linear-gradient(135deg, #0A5E4E 0%, #D8C08A 100%);
```

---

## Luxury Facade

Aspirational, polished, premium-looking palettes for products or brands that need to appear more expensive or elevated than their price point suggests.

### Caramel Air
- Style: Soft, warm, approachable, upscale.
- Primary: #C07F45
- Secondary: #FCEDD6
- Accent: #97C6E0
- Supporting: #7A5030, #E8D0A8, #F8F2E8
- Best for: Lifestyle branding, packaging, soft premium visuals, calm aspirational layouts.
- WCAG: Use Supporting #7A5030 for body text on Secondary → **5.2:1 ✅**.

### Moss Iris
- Style: Elegant, muted, artistic, boutique-like.
- Primary: #8F9D68
- Secondary: #FFF8EB
- Accent: #7A57CD
- Supporting: #5A6A40, #D8D0A8, #F8F4EC
- Best for: Boutique packaging, creative branding, elevated calm visuals, editorial accents.
- WCAG: Accent (#7A57CD) on Secondary (#FFF8EB) → **5.3:1 ✅** (AA).

### Citrus Royal
- Style: Bright, polished, clean, product-forward.
- Primary: #EF8E01
- Secondary: #0038BD
- Accent: #EEEEEE
- Supporting: #B86A00, #0028A0, #F8F8F8
- Best for: Consumer products, punchy premium-style branding, modern retail visuals.

### Skyline Poise
- Style: Cool, structured, calm, contemporary.
- Primary: #27262E
- Secondary: #E19C63
- Accent: #8BA5BE
- Supporting: #3E3D48, #C07840, #F0EAE0
- Best for: Corporate branding, premium service design, modern calm interfaces.
- WCAG: Accent (#8BA5BE) on Primary (#27262E) → **5.6:1 ✅** (AA).

### Blue Horizon
- Style: Fresh, quiet, spacious, lightly premium.
- Primary: #F4FEFF
- Secondary: #A9C0E0
- Accent: #0E2F76
- Supporting: #70A0C8, #D8E8F8, #FAFEFE
- Best for: Calm UI, airy branding, wellness, minimal product design.
- WCAG: Accent (#0E2F76) on Primary (#F4FEFF) → **12.8:1 ✅** (AAA).

### Coastal Contrast
- Style: Fresh, bright, accessible, polished.
- Primary: #95D9C0
- Secondary: #FFFFFF
- Accent: #D41F26
- Supporting: #60B898, #E8F8F0, #F8F8F8
- Best for: Lifestyle products, cheerful packaging, clean promotional graphics.
- WCAG: Accent (#D41F26) on Secondary (#FFFFFF) → **5.9:1 ✅** (AA).

### Soft Prestige

Calm, editorial, premium-looking palettes for clean brand systems.

#### Arctic Teal × Cloud Pearl
- Style: Clean, corporate, trustworthy.
- Primary: #0E7490 / Secondary: #F2F5F7 / Supporting: #0A5068, #D0D8E0
- WCAG: Primary on Secondary → **4.6:1 ✅** (AA).

#### Terracotta Bloom × Sand Dune
- Style: Warm, earthy, editorial.
- Primary: #C96A4A / Secondary: #EEDCC8 / Supporting: #A04830, #E0C8A8

#### Forest Moss × Vanilla Silk
- Style: Organic, natural, timeless.
- Primary: #4E6B45 / Secondary: #F4E8D0 / Supporting: #365030, #E8D8B8
- WCAG: Primary on Secondary → **5.1:1 ✅** (AA).

#### Indigo Night × Wisteria Glow
- Style: Modern, soft, premium.
- Primary: #2D4275 / Secondary: #D6C6F7 / Supporting: #1A2A58, #C0A8F0
- WCAG: Primary on Secondary → **6.2:1 ✅** (AA).

### Gradients

#### Caramel Drift
- Saturated Stop: #C07F45 → Light Stop: #FCEDD6
```css
background: linear-gradient(135deg, #C07F45 0%, #FCEDD6 100%);
```

#### Teal Pearl
- Saturated Stop: #0E7490 → Light Stop: #F2F5F7
```css
background: linear-gradient(135deg, #0E7490 0%, #F2F5F7 100%);
```

#### Wisteria Cloud
- Saturated Stop: #2D4275 → Light Stop: #D6C6F7
```css
background: linear-gradient(135deg, #2D4275 0%, #D6C6F7 100%);
```

---

## Otherworldly

Futuristic, neon, surreal, cyber, and reality-bending palettes. Use when the output must feel like it belongs to another dimension.

### Skin Tone
- Style: Warm, synthetic, soft sci-fi.
- Primary: #FFC6A8
- Secondary: #741A2F
- Accent: #FF8060
- Supporting: #E89078, #4A1020, #FFF0E8
- Best for: Futuristic beauty, surreal fashion, human-centered sci-fi visuals.
- WCAG: Secondary (#741A2F) on Primary (#FFC6A8) → **4.8:1 ✅** (AA).

### Vulcanico
- Style: Hot, aggressive, kinetic, ultra-digital.
- Primary: #FF4103
- Secondary: #001621
- Accent: #FFAA00
- Supporting: #CC2800, #002A3A, #FFD080
- Best for: Cyberpunk branding, bold interface accents, intense visual identity.
- WCAG: Accent (#FFAA00) on Secondary (#001621) → **9.2:1 ✅** (AAA).

### Silver Pulse
- Style: Minimal, electric, high-contrast, synthetic.
- Primary: #141414
- Secondary: #2BEE34
- Accent: #FFFFFF
- Supporting: #1E1E1E, #20B828, #A0FFA0
- Best for: Neon UI, digital systems, futuristic dashboards.
- WCAG: Accent (#FFFFFF) on Primary (#141414) → **18.1:1 ✅** (AAA).

### Turmeric Signal
- Style: Bright, sharp, experimental, energized.
- Primary: #FFBE0B
- Secondary: #2A2312
- Accent: #FF4000
- Supporting: #CC9800, #1A1508, #FF8040
- Best for: Concept art, tech branding, attention-grabbing interfaces.
- WCAG: Secondary (#2A2312) on Primary (#FFBE0B) → **9.4:1 ✅** (AAA).

### Milky Grove
- Style: Soft, organic, luminous, slightly alien.
- Primary: #FFFDF1
- Secondary: #59C749
- Accent: #1A5A10
- Supporting: #D8F8D0, #3A8A28, #F0FFF0
- Best for: Eco-futurism, wellness-tech, optimistic sci-fi visuals.
- WCAG: Accent (#1A5A10) on Primary (#FFFDF1) → **9.7:1 ✅** (AAA).

### Lime Oracle
- Style: Acidic, electric, strange, futuristic.
- Primary: #E4FD97
- Secondary: #2D3E2C
- Accent: #8FD400
- Supporting: #C0E060, #1A2818, #F0FFAA
- Best for: Experimental branding, cyber nature, bold futuristic systems.
- WCAG: Secondary (#2D3E2C) on Primary (#E4FD97) → **8.3:1 ✅** (AAA).

### Cyprus Echo
- Style: Deep, calm, balanced, futuristic-natural.
- Primary: #004741
- Secondary: #F0EDE4
- Accent: #00C8A8
- Supporting: #003028, #D8D4C8, #80E8D0
- Best for: Premium eco-tech, serene interfaces, modern organic branding.
- WCAG: Secondary (#F0EDE4) on Primary (#004741) → **11.4:1 ✅** (AAA).

### True Signal
- Style: Hot, vivid, synthetic, pop-futurist.
- Primary: #FD1843
- Secondary: #FFF9FA
- Accent: #0A0A0A
- Supporting: #C81030, #FFE8EC, #303030
- Best for: Youthful digital products, neon brand moments, sharp accent systems.
- WCAG: Accent (#0A0A0A) on Secondary (#FFF9FA) → **19.3:1 ✅** (AAA).

### Charcoal Violet
- Style: Dark, electric, surreal, high-contrast.
- Primary: #3C1A47
- Secondary: #B6FF00
- Accent: #FFFFFF
- Supporting: #280E30, #88CC00, #E0E0E0
- Best for: Futuristic editorial design, bold app themes, neon contrast work.
- WCAG: Secondary (#B6FF00) on Primary (#3C1A47) → **10.4:1 ✅** (AAA).

### Gradients

#### Neon Abyss
- Saturated Stop: #3C1A47 → Light Stop: #B6FF00
```css
background: linear-gradient(135deg, #3C1A47 0%, #B6FF00 100%);
```

#### Solar Flare
- Saturated Stop: #FF4103 → Light Stop: #FFBE0B
```css
background: linear-gradient(135deg, #FF4103 0%, #FFBE0B 100%);
```

#### Void Pulse
- Saturated Stop: #141414 → Light Stop: #2BEE34
```css
background: linear-gradient(135deg, #141414 0%, #2BEE34 100%);
```

---

## Acid Contemporary

Disruptive, urban, high-voltage palettes. Confrontational by design — street culture, bold editorial, event branding.

> **Agent rule:** These palettes are confrontational by design. Do not soften them. If the context calls for subtlety, switch to Luxury or Minimalist instead.

### Ink Volt
- Style: Maximum contrast, street editorial, aggressive typographic energy.
- Primary: #0A0A0A / Secondary: #F5E800 / Accent: #FFFFFF / Supporting: #1A1A1A, #CCCC00, #AAAAAA
- WCAG: Secondary (#F5E800) on Primary (#0A0A0A) → **17.4:1 ✅** (AAA).

### Crimson Grid
- Style: Dark tech, cinematic tension, high-drama red.
- Primary: #0D0D0D / Secondary: #CC0A20 / Accent: #FFFFFF / Supporting: #1A0A0A, #3A0010, #888888
- WCAG: Accent (#FFFFFF) on Primary (#0D0D0D) → **19.0:1 ✅** (AAA).

### Blood Stage
- Style: Raw, mythic, performance-driven, crowd energy.
- Primary: #C8102E / Secondary: #0A0A0A / Accent: #FFFFFF / Supporting: #8B0000, #5C0015, #AAAAAA
- WCAG: Accent (#FFFFFF) on Primary (#C8102E) → **4.7:1 ✅** (AA).

### Tactical Lime
- Style: Military edge, athletic aggression, acid-nature contrast.
- Primary: #3B3D2A / Secondary: #C2F03A / Accent: #FFFFFF / Supporting: #1A6B5C, #CC2B2B, #1A1A1A
- WCAG: Secondary (#C2F03A) on Primary (#3B3D2A) → **8.1:1 ✅** (AAA).

### Void Green
- Style: Digital underground, hacker aesthetic, neon life in darkness.
- Primary: #050F05 / Secondary: #1AE81A / Accent: #FFFFFF / Supporting: #0D4A0D, #002200, #111111
- WCAG: Secondary (#1AE81A) on Primary (#050F05) → **13.2:1 ✅** (AAA).

### Gradients

#### Volt Smear
```css
background: linear-gradient(135deg, #0A0A0A 0%, #F5E800 100%);
```

#### Crimson Fade
```css
background: linear-gradient(135deg, #CC0A20 0%, #0D0D0D 100%);
```

#### Acid Burn
```css
background: linear-gradient(135deg, #3B3D2A 0%, #C2F03A 100%);
```

---

## Refined Defaults

Smarter alternatives to the blunt base colors that beginners and lazy tools default to.

> **Agent rule:** If you are about to use #000000, #ffffff, #0000ff, #ff0000, #00ff00, or #9a4dff — stop. Use the refined alternatives below instead.

### Instead of Black (#000000)
- Use: #161616, #232323, #2C2C2C, #363636
- Why: Pure black feels flat and printed. These near-blacks read more intentional.

### Instead of White (#ffffff)
- Use: #F6F6F6, #EEEEF0, #DEDEDE, #E1E1E1
- Why: Pure white glows on screen. Off-whites feel considered and easier on the eye.

### Instead of Blue (#0000ff)
- Use: #347AEA, #1E2FB0, #1E4BA3, #223068
- Why: Pure blue is aggressive and dated. These carry authority without shouting.

### Instead of Red (#ff0000)
- Use: #F64547, #D7202D, #941020, #C92D31
- Why: Pure red is alarm-level intensity. These reds feel designed, not defaulted to.

### Instead of Green (#00ff42)
- Use: #91B96B, #5C985A, #56754B, #306C5F
- Why: Neon green screams synthetic. These greens feel grown, not coded.

### Instead of Purple (#9a4dff)
- Use: #361269, #6000D3, #7C44A5, #665090
- Why: Default bright purple feels accidental. These have weight and recognisability.

---

## Soft Gradients

Named two-stop gradient pairs for calm, breathable, emotionally gentle visuals.

> **Agent rule:** Direction is flexible — top-to-bottom and 135° diagonal both work well. Apply as linear or radial.

### Eucalyptus Glow
```css
background: linear-gradient(135deg, #A7C4A0 0%, #F4EFE6 100%);
```

### Pearl Mauve
```css
background: linear-gradient(135deg, #D8BFD8 0%, #FDFCFB 100%);
```

### Ocean Breeze
```css
background: linear-gradient(135deg, #7FCDFF 0%, #DFF7FF 100%);
```

### Peach Champagne
```css
background: linear-gradient(135deg, #FFD3B6 0%, #FFF7F0 100%);
```

### Dreamy Periwinkle
```css
background: linear-gradient(135deg, #B8C0FF 0%, #E7D8FF 100%);
```

### Mint Lagoon
```css
background: linear-gradient(135deg, #6DD5C4 0%, #DFF6F0 100%);
```

---

## Nature / Organic

Palettes rooted in the living world — soil, bark, moss, stone, sky, water.

### Forest Floor
- Style: Dense, shadowed, rich, deeply organic.
- Primary: #2C3A2A / Secondary: #4A5E3A / Accent: #A8C080 / Supporting: #7A6B52, #1E2A1A, #E8E0D0
- WCAG: Accent (#A8C080) on Primary (#2C3A2A) → **5.3:1 ✅** (AA).

### River Stone
- Style: Cool, muted, mineral, grounded.
- Primary: #5A6B6E / Secondary: #D4D8D0 / Accent: #3A8A78 / Supporting: #8A9A98, #2A3A3C, #F0EDE8

### Golden Meadow
- Style: Warm, open, harvest-light, pastoral.
- Primary: #C8A84B / Secondary: #F5EDD0 / Accent: #6B8A3A / Supporting: #A07840, #3A4A28, #FBF7EC
- WCAG: Accent (#6B8A3A) on Secondary (#F5EDD0) → **4.6:1 ✅** (AA).

### Bark & Sage
- Style: Rough, honest, textured, understated.
- Primary: #7A6248 / Secondary: #E8E0D0 / Accent: #7A9A68 / Supporting: #4A3A2C, #B0A888, #F5F0E8

### Deep Canopy
- Style: Lush, tropical-dense, vivid organic.
- Primary: #1A3A2A / Secondary: #2E5A3A / Accent: #C8D84A / Supporting: #4A7A50, #0E2018, #F0F0E0
- WCAG: Accent (#C8D84A) on Primary (#1A3A2A) → **8.9:1 ✅** (AAA).

### Gradients

#### Morning Moss
```css
background: linear-gradient(135deg, #4A5E3A 0%, #E8E0D0 100%);
```

#### Stone Wash
```css
background: linear-gradient(135deg, #5A6B6E 0%, #F0EDE8 100%);
```

#### Canopy Light
```css
background: linear-gradient(135deg, #1A3A2A 0%, #C8D84A 100%);
```

---

## Minimalist

Palettes built on restraint. One dominant neutral, one precise accent, maximum whitespace.

> **Agent rule:** Never add more than one accent color. If tempted to add a second, remove it — whitespace is the second color.

### Bone & Carbon
- Style: Warm-neutral base, dark anchor, zero decoration.
- Primary: #F5F0EB / Secondary: #1E1E1E / Accent: #B07840 / Supporting: #D8D0C8, #3A3A3A
- WCAG: Secondary (#1E1E1E) on Primary (#F5F0EB) → **15.8:1 ✅** (AAA).

### Chalk & Ink
- Style: Cool-white base, pure black type, clean.
- Primary: #F8F8F8 / Secondary: #111111 / Accent: #0057FF / Supporting: #E0E0E0, #444444
- WCAG: Accent (#0057FF) on Primary (#F8F8F8) → **6.2:1 ✅** (AA).

### Warm Mono
- Style: Single warm tone scaled across values, no contrast color.
- Primary: #FAF5EE / Secondary: #D4C4A8 / Accent: #8A6A40 / Supporting: #B8A888, #5A4830
- WCAG: Accent (#8A6A40) on Primary (#FAF5EE) → **4.8:1 ✅** (AA).

### Grey Scale Plus
- Style: Full greyscale with one surgical color pop.
- Primary: #F2F2F2 / Secondary: #2A2A2A / Accent: #E8341C / Supporting: #AAAAAA, #777777
- WCAG: Accent (#E8341C) on Primary (#F2F2F2) → **4.6:1 ✅** (AA).

### Ash & Mist
- Style: Soft cool grey, barely-there, silent presence.
- Primary: #ECEEF0 / Secondary: #5A6270 / Accent: #3A7A8A / Supporting: #B8C0C8, #2A3040
- WCAG: Accent (#3A7A8A) on Primary (#ECEEF0) → **4.5:1 ✅** (AA).

### Gradients

#### Bone Fade
```css
background: linear-gradient(135deg, #D8D0C8 0%, #F5F0EB 100%);
```

#### Ink Mist
```css
background: linear-gradient(135deg, #2A2A2A 0%, #F8F8F8 100%);
```

#### Ash Drift
```css
background: linear-gradient(135deg, #5A6270 0%, #ECEEF0 100%);
```

---

## Rustic / Craft

Warm amber, kraft paper, leather, raw linen, aged wood. For brands whose story is about hands, process, and authenticity.

### Amber Workshop
- Style: Warm, woody, handmade, artisan-rich.
- Primary: #8B5E3C / Secondary: #F5E6CC / Accent: #C8981A / Supporting: #6A4228, #D4B890, #FAF3E0
- WCAG: Use Supporting #6A4228 on Secondary → **5.4:1 ✅**.

### Leather & Linen
- Style: Raw, tactile, warm restraint.
- Primary: #A0784A / Secondary: #F0E8D8 / Accent: #5A3E28 / Supporting: #C8A878, #D8C8A8, #FAF6EE
- WCAG: Accent (#5A3E28) on Secondary (#F0E8D8) → **7.1:1 ✅** (AA).

### Smoked Oak
- Style: Dark, textured, aged, serious craft.
- Primary: #3A2A1E / Secondary: #8A7060 / Accent: #C89050 / Supporting: #6A5040, #D8C0A0, #F5EEE0
- WCAG: Accent (#C89050) on Primary (#3A2A1E) → **5.8:1 ✅** (AA).

### Kraft & Clay
- Style: Earthy, raw, unfinished, honest.
- Primary: #B8936A / Secondary: #F5EDD8 / Accent: #7A5840 / Supporting: #D8B890, #A07850, #FBF5EA

### Harvest Dusk
- Style: End-of-day warmth, rich amber sky, rural.
- Primary: #C07030 / Secondary: #F5D8A8 / Accent: #3A3020 / Supporting: #A05020, #E8C080, #FBF0D8
- WCAG: Accent (#3A3020) on Secondary (#F5D8A8) → **10.2:1 ✅** (AAA).

### Gradients

#### Amber Glow
```css
background: linear-gradient(135deg, #8B5E3C 0%, #F5E6CC 100%);
```

#### Smoked Drift
```css
background: linear-gradient(135deg, #3A2A1E 0%, #C89050 100%);
```

#### Linen Haze
```css
background: linear-gradient(135deg, #C8A878 0%, #FAF6EE 100%);
```

---

## Gothic / Dark Romance

Deep wine, bone white, charcoal smoke, velvet purple, cold iron. Dramatic, mysterious, emotionally intense.

> **Agent rule:** Gothic palettes must always include at least one near-white or bone tone as a contrast anchor. Pure black on pure black is a failure state.

### Velvet Crypt
- Style: Deep, opulent darkness, rich and suffocating.
- Primary: #1A0A1E / Secondary: #3A1A40 / Accent: #C8A0E0 / Supporting: #7A4A90, #F0E8F8, #0E0610
- WCAG: Accent (#C8A0E0) on Primary (#1A0A1E) → **8.1:1 ✅** (AAA).

### Bone & Wine
- Style: Contrast-driven, romantic, decadent, timeless.
- Primary: #1A0808 / Secondary: #8B1A2A / Accent: #F0E8D8 / Supporting: #5A0E18, #C8A090, #2A1010
- WCAG: Accent (#F0E8D8) on Primary (#1A0808) → **14.6:1 ✅** (AAA).

### Iron Fog
- Style: Cold, industrial, melancholic, restrained gothic.
- Primary: #1E2028 / Secondary: #3A3E48 / Accent: #8A90A8 / Supporting: #5A5E70, #C8CAD0, #0E1018
- WCAG: Accent (#8A90A8) on Primary (#1E2028) → **4.6:1 ✅** (AA).

### Midnight Bloom
- Style: Floral, dark, mysterious, romantically lush.
- Primary: #1A1028 / Secondary: #4A2050 / Accent: #E050A0 / Supporting: #7A1850, #F8C8E0, #0E0818
- WCAG: Accent (#E050A0) on Primary (#1A1028) → **6.3:1 ✅** (AA).

### Ash Raven
- Style: Stripped, cold, mournful minimalism.
- Primary: #18181C / Secondary: #2E2E34 / Accent: #E8E0D0 / Supporting: #4A4A52, #8A8A90, #F5F2EE
- WCAG: Accent (#E8E0D0) on Primary (#18181C) → **13.4:1 ✅** (AAA).

### Gradients

#### Velvet Smoke
```css
background: linear-gradient(135deg, #1A0A1E 0%, #C8A0E0 100%);
```

#### Crimson Bone
```css
background: linear-gradient(135deg, #8B1A2A 0%, #F0E8D8 100%);
```

#### Iron Veil
```css
background: linear-gradient(135deg, #1E2028 0%, #C8CAD0 100%);
```

---

## Warm Tropical / Resort

Mango, coral, turquoise, warm sand, palm shadow. Generous, joyful, physically warm.

### Mango Shore
- Style: Ripe, vivid, sun-drenched, joyful.
- Primary: #FF8C42 / Secondary: #FFF3E0 / Accent: #0097A7 / Supporting: #FF6B1A, #FFD580, #005F6B
- WCAG: Accent (#0097A7) on Secondary (#FFF3E0) → **4.7:1 ✅** (AA).

### Coral Lagoon
- Style: Warm, aquatic, fresh, resort-luxe.
- Primary: #FF6F61 / Secondary: #FFF8F5 / Accent: #48CAE4 / Supporting: #E8504A, #A0D8E0, #FFC5B0

### Palm & Sand
- Style: Calm, warm, natural resort, understated tropical.
- Primary: #E8C99A / Secondary: #FBF5E8 / Accent: #3A7A6A / Supporting: #B89870, #7AB090, #F5EDD8
- WCAG: Accent (#3A7A6A) on Secondary (#FBF5E8) → **5.0:1 ✅** (AA).

### Sunset Punch
- Style: Bold, saturated, cocktail-hour drama.
- Primary: #E84060 / Secondary: #FF9A3C / Accent: #FFF0A0 / Supporting: #A01830, #FF6820, #FFC850
- WCAG: Accent (#FFF0A0) on Primary (#E84060) → **4.9:1 ✅** (AA).

### Turquoise Drift
- Style: Cool tropical, sea glass, serene and open.
- Primary: #00B4C8 / Secondary: #E0F8FC / Accent: #FF8040 / Supporting: #007A8A, #80D8E8, #FFF5EE
- WCAG: Use Supporting #007A8A for text on Secondary → **5.2:1 ✅**. Accent is decorative only.

### Gradients

#### Mango Horizon
```css
background: linear-gradient(135deg, #FF8C42 0%, #FFF3E0 100%);
```

#### Lagoon Fade
```css
background: linear-gradient(135deg, #00B4C8 0%, #E0F8FC 100%);
```

#### Sunset Wash
```css
background: linear-gradient(135deg, #E84060 0%, #FF9A3C 100%);
```

---

## Retro / Vintage

Faded, sun-bleached, tobacco-stained, nostalgic. Controlled desaturation is the key.

> **Agent rule:** Retro palettes must feel slightly faded. If a color looks too clean or saturated, pull it back. Vintage is about imperfection, not freshness.

### Mustard Record
- Style: 70s warmth, vinyl culture, bold and worn.
- Primary: #C8980A / Secondary: #F5E8C0 / Accent: #A03820 / Supporting: #8A6808, #E0C870, #FAF0D8
- WCAG: Accent (#A03820) on Secondary (#F5E8C0) → **5.4:1 ✅** (AA).

### Avocado Dream
- Style: Late-60s/70s organic, muted, period-correct.
- Primary: #7A8A38 / Secondary: #F0EDD8 / Accent: #C87840 / Supporting: #5A6828, #D8D0A8, #FAF5E8

### Faded Denim
- Style: Washed, worn, American classic, 90s casual.
- Primary: #5A7090 / Secondary: #E8EEF5 / Accent: #C84830 / Supporting: #3A5070, #A8B8C8, #F5F0E8
- WCAG: Accent (#C84830) on Secondary (#E8EEF5) → **4.6:1 ✅** (AA).

### Rust & Cream
- Style: Industrial vintage, aged metal, warm patina.
- Primary: #B84820 / Secondary: #F5EAD8 / Accent: #3A3828 / Supporting: #8A3818, #D8C0A0, #FAF5EC
- WCAG: Accent (#3A3828) on Secondary (#F5EAD8) → **10.8:1 ✅** (AAA).

### Tobacco & Ivory
- Style: Aged paper, sepia warmth, old world editorial.
- Primary: #A08040 / Secondary: #F8F0DC / Accent: #3A2E20 / Supporting: #7A6030, #D8C898, #FAF5E4
- WCAG: Accent (#3A2E20) on Secondary (#F8F0DC) → **12.4:1 ✅** (AAA).

### Gradients

#### Mustard Haze
```css
background: linear-gradient(135deg, #C8980A 0%, #F5E8C0 100%);
```

#### Rust Fade
```css
background: linear-gradient(135deg, #B84820 0%, #F5EAD8 100%);
```

#### Denim Wash
```css
background: linear-gradient(135deg, #5A7090 0%, #E8EEF5 100%);
```

---

## Corporate / Enterprise

B2B SaaS, finance, legal, logistics, enterprise software. Project competence, reliability, and scalability — not personality.

> **Agent rule:** Corporate palettes must pass WCAG AA on all text elements. If a color fails 4.5:1 for normal text, do not use it for body copy.

### Slate Command
- Style: Authoritative, structured, data-forward, no-nonsense.
- Primary: #F4F6F8 / Secondary: #1C2B3A / Accent: #1D72C6 / Supporting: #4A6A88, #D8E2EC, #0A1A2A
- WCAG: Accent (#1D72C6) on Primary (#F4F6F8) → **5.8:1 ✅** (AA). Secondary on Primary → **13.2:1 ✅** (AAA).

### Finance Trust
- Style: Conservative, credible, wealth-adjacent, bank-grade.
- Primary: #FFFFFF / Secondary: #002244 / Accent: #005BBB / Supporting: #D4E1F0, #6688AA, #001A33
- WCAG: Accent (#005BBB) on Primary (#FFFFFF) → **7.2:1 ✅** (AA). Secondary on Primary → **16.8:1 ✅** (AAA).

### Legal Anchor
- Style: Sober, traditional, precise, institutional.
- Primary: #F8F7F4 / Secondary: #1A1A2E / Accent: #8B6914 / Supporting: #D0CCC0, #4A4A5A, #C8A840
- WCAG: Accent (#8B6914) on Primary (#F8F7F4) → **5.2:1 ✅** (AA).

### Ops Green
- Style: Operational, efficient, system-status, uptime-first.
- Primary: #F2F5F0 / Secondary: #1A2E1A / Accent: #2E7D32 / Supporting: #A8C8A0, #4A6A48, #E0EDD8
- WCAG: Accent (#2E7D32) on Primary (#F2F5F0) → **6.3:1 ✅** (AA).

### Steel Platform
- Style: Neutral, scalable, product-first, utility.
- Primary: #FAFAFA / Secondary: #212121 / Accent: #6200EE / Supporting: #E0E0E0, #757575, #3700B3
- WCAG: Accent (#6200EE) on Primary (#FAFAFA) → **8.9:1 ✅** (AAA).

### Gradients

#### Slate Rise
```css
background: linear-gradient(135deg, #1C2B3A 0%, #F4F6F8 100%);
```

#### Finance Depth
```css
background: linear-gradient(135deg, #002244 0%, #D4E1F0 100%);
```

#### Ops Pulse
```css
background: linear-gradient(135deg, #1A2E1A 0%, #E0EDD8 100%);
```

---

## Healthcare / Medical

Clinical, wellness-tech, pharma, telehealth, medical devices. Safe and trustworthy first, human second.

> **Agent rule:** Avoid pure red in healthcare UI — it reads as emergency/error. Reserve it for actual critical alerts only.

### Clinical Trust
- Style: Clean, professional, safe, sterile-but-human.
- Primary: #F7FAFC / Secondary: #1A5276 / Accent: #2E86C1 / Supporting: #AED6F1, #5D9BC4, #E8F4FD
- WCAG: Accent (#2E86C1) on Primary (#F7FAFC) → **4.8:1 ✅** (AA). Secondary on Primary → **10.4:1 ✅** (AAA).

### Wellness Sage
- Style: Calm, grounding, preventive care, holistic.
- Primary: #F4F9F4 / Secondary: #1E5E3A / Accent: #27AE60 / Supporting: #A9DFBF, #52BE80, #EAFAF1
- WCAG: Accent (#27AE60) on Primary (#F4F9F4) → **4.5:1 ✅** (AA).

### Pharma Precision
- Style: Exact, controlled, lab-grade, no ambiguity.
- Primary: #FFFFFF / Secondary: #0B3D6B / Accent: #007DC5 / Supporting: #CCE5F5, #4A90B8, #F0F8FF
- WCAG: Accent (#007DC5) on Primary (#FFFFFF) → **5.3:1 ✅** (AA). Secondary on Primary → **13.8:1 ✅** (AAA).

### Recovery Warmth
- Style: Gentle, supportive, post-acute care, human.
- Primary: #FDF8F2 / Secondary: #7D6148 / Accent: #E07B39 / Supporting: #F0D9C0, #B89070, #FAF0E6
- WCAG: Secondary (#7D6148) on Primary (#FDF8F2) → **5.6:1 ✅** (AA).

### Gradients

#### Clinical Calm
```css
background: linear-gradient(135deg, #1A5276 0%, #F7FAFC 100%);
```

#### Wellness Lift
```css
background: linear-gradient(135deg, #1E5E3A 0%, #F4F9F4 100%);
```

---

## Gaming / Esports

Dark, high-energy palettes for competitive gaming, streaming, esports teams, and gaming hardware.

> **Agent rule:** Use near-black as base (not pure #000000). Neon accents must be legible at small sizes. Never use more than two neon colors in one palette.

### Cyber Arena
- Style: Electric, competitive, tournament-grade, iconic.
- Primary: #0D0D1A / Secondary: #00F0FF / Accent: #FF0080 / Supporting: #1A1A2E, #00B8CC, #CC0066
- WCAG: Secondary (#00F0FF) on Primary (#0D0D1A) → **14.3:1 ✅** (AAA).

### Shadow Protocol
- Style: Tactical, military-game, stealth, professional.
- Primary: #111418 / Secondary: #1E2A1E / Accent: #4AFF6A / Supporting: #2A3A2A, #30CC50, #E0FFE8
- WCAG: Accent (#4AFF6A) on Primary (#111418) → **13.7:1 ✅** (AAA).

### Void Reactor
- Style: Sci-fi, high-tech, reactor-core energy, purple-dominant.
- Primary: #0A0010 / Secondary: #8000FF / Accent: #E0A0FF / Supporting: #3A0060, #6000CC, #F0D8FF
- WCAG: Accent (#E0A0FF) on Primary (#0A0010) → **12.1:1 ✅** (AAA).

### Fire Squad
- Style: Aggressive, loud, combat-energy, team identity.
- Primary: #120808 / Secondary: #FF3000 / Accent: #FFB800 / Supporting: #CC2000, #CC8800, #FF8060
- WCAG: Accent (#FFB800) on Primary (#120808) → **14.8:1 ✅** (AAA).

### Ice Cap
- Style: Cool, precise, clean competitive, speed-first.
- Primary: #08101A / Secondary: #00B8FF / Accent: #FFFFFF / Supporting: #0080CC, #0040A0, #D0F0FF
- WCAG: Accent (#FFFFFF) on Primary (#08101A) → **18.6:1 ✅** (AAA).

### Gradients

#### Cyber Grid
```css
background: linear-gradient(135deg, #0D0D1A 0%, #00F0FF 100%);
```

#### Reactor Core
```css
background: linear-gradient(135deg, #0A0010 0%, #8000FF 100%);
```

#### Fire Rush
```css
background: linear-gradient(135deg, #120808 0%, #FF3000 100%);
```

---



---

## Seasonal

Palettes calibrated to seasonal contexts — campaign refreshes, retail seasons, and holiday branding.

> **Agent rule:** Seasonal palettes are time-scoped. Always note the intended season/period in the Design Route block so downstream skills (effects, fonts) can align to the seasonal mood.

### Spring Bloom
- Style: Fresh, light, renewal, optimistic.
- Primary: #F0F7E6
- Secondary: #5BA85C
- Accent: #FF7EB3
- Supporting: #B5D5A8, #E8F5D8, #FFD6EB
- Best for: Spring campaign hero sections, Easter branding, garden/lifestyle seasonal refresh.
- WCAG: Secondary (#5BA85C) on Primary (#F0F7E6) → **4.5:1 ✅** (AA). Accent (#FF7EB3) on Primary → **2.1:1 ⚠️** Decorative only.

### Summer Pulse
- Style: Hot, vivid, outdoor energy, peak season.
- Primary: #FF8C00
- Secondary: #005FA3
- Accent: #FFFFFF
- Supporting: #FFC04D, #0047A0, #E8F4FF
- Best for: Summer sale campaigns, beach/outdoor brands, peak season promotions, festival branding.
- WCAG: Accent (#FFFFFF) on Secondary (#005FA3) → **7.3:1 ✅** (AA).

### Autumn Harvest
- Style: Warm, rich, transitional, harvest depth.
- Primary: #C8601A
- Secondary: #F5E6C8
- Accent: #3A2808
- Supporting: #8B3A0A, #D4A86A, #FAF0DC
- Best for: Autumn campaigns, harvest themes, back-to-school, seasonal menu refreshes.
- WCAG: Accent (#3A2808) on Secondary (#F5E6C8) → **11.2:1 ✅** (AAA).

### Winter Silence
- Style: Cold, still, luxury-adjacent, cinematic.
- Primary: #0A1628
- Secondary: #C8D8E8
- Accent: #E8C84A
- Supporting: #1E3A5A, #8AAAC8, #F0F5F8
- Best for: Winter campaigns, holiday packaging, Christmas editorial, cold-season luxury.
- WCAG: Accent (#E8C84A) on Primary (#0A1628) → **8.9:1 ✅** (AAA).

### Holiday Warmth
- Style: Festive, warm, inclusive, celebratory.
- Primary: #C41E3A
- Secondary: #F5F0E8
- Accent: #D4AF37
- Supporting: #8B0000, #E8D5B0, #FAF8F0
- Best for: Christmas/holiday campaigns, festive retail, end-of-year celebration branding.
- WCAG: Use Secondary (#F5F0E8) for text on Primary → **8.4:1 ✅** (AAA). Accent on Primary → **3.2:1 ⚠️** Large text only.

### Gradients

#### Spring Rise
```css
background: linear-gradient(135deg, #5BA85C 0%, #F0F7E6 100%);
```

#### Summer Horizon
```css
background: linear-gradient(135deg, #FF8C00 0%, #005FA3 100%);
```

#### Amber Fall
```css
background: linear-gradient(135deg, #C8601A 0%, #F5E6C8 100%);
```

#### Winter Depth
```css
background: linear-gradient(135deg, #0A1628 0%, #C8D8E8 100%);
```

#### Holiday Glow
```css
background: linear-gradient(135deg, #C41E3A 0%, #D4AF37 100%);
```

---

## Brand Archetype Guide

Use this when the brief describes brand personality rather than industry.
Archetypes map directly to color category intent and can confirm or override an industry signal.

> **Agent rule:** Brand archetype is a secondary signal. It confirms or refines the category from the Decision Guide. If archetype contradicts industry, surface both options and let the user decide.

| Archetype | Core emotion | Recommended category | Notes |
|---|---|---|---|
| The Innocent | Purity, simplicity, trust | Soft Gradients, Luxury Facade / Soft Prestige | Light palettes, no aggression |
| The Everyman | Belonging, honesty, approachability | Rustic / Craft, Nature / Organic | Warm, unpretentious, no flash |
| The Hero | Courage, achievement, ambition | Luxury / Volcanic Intensity, Acid Contemporary | Bold, strong contrast |
| The Outlaw / Rebel | Disruption, freedom, revolution | Acid Contemporary, Gaming / Esports | Maximum contrast, confrontational |
| The Explorer | Adventure, discovery, freedom | Warm Tropical / Resort, Nature / Organic, Otherworldly | Open, expansive |
| The Creator | Craft, imagination, originality | Minimalist, Rustic / Craft, Retro / Vintage | Considered, intentional |
| The Ruler | Authority, control, prestige | Luxury / Golden Obsession, Corporate / Finance Trust | Commanding, structured |
| The Magician | Transformation, vision, mystery | Otherworldly, Gothic / Dark Romance | Surreal, transformational |
| The Lover | Intimacy, passion, beauty | Gothic / Bone & Wine, Luxury Facade / Soft Prestige | Sensual, emotionally rich |
| The Caregiver | Nurturing, warmth, service | Healthcare / Wellness Sage, Soft Gradients | Safe, gentle, human-first |
| The Jester | Fun, play, irreverence | Warm Tropical / Resort, Seasonal / Summer Pulse | Energy without aggression |
| The Sage | Knowledge, wisdom, clarity | Corporate / Steel Platform, Minimalist / Chalk & Ink | Clean, authoritative |

---

## Dark Mode Adaptation

When a brief requires dark mode, adapt any palette using these rules rather than guessing.

### Universal rules

1. **Swap Primary ↔ Secondary** — the dominant surface becomes dark; the secondary becomes the lighter surface element.
2. **Desaturate Accent by 10–15%** — pure saturated accents vibrate on dark backgrounds; pulling back reduces eye strain.
3. **Lift Supporting tones** — lighten supporting neutrals by 20–30% so they remain visible against dark surfaces.
4. **Never go below #111111** for dark backgrounds — pure #000000 creates harsh contrast and feels undesigned.
5. **Re-check WCAG after adapting** — contrast ratios change when colors are inverted.

### Per-category dark mode guidance

| Category | Dark mode approach |
|---|---|
| Luxury | Most already dark-first (Golden Obsession, Volcanic Intensity) — use as-is |
| Luxury Facade | Swap Primary/Secondary; keep Accent |
| Minimalist | Bone & Carbon already works; Chalk & Ink: swap to #111111 base, #F8F8F8 text |
| Corporate | Slate Command dark: use #0D1520 base, #D8E2EC surfaces, Accent unchanged |
| Healthcare | Avoid full dark mode for clinical UI — use "dim mode" (max bg: #1A2A3A) not true dark |
| Gothic | Already dark-first — no adaptation needed |
| Gaming | Already dark-first — no adaptation needed |
| Otherworldly | Already dark-first — no adaptation needed |
| Nature / Organic | Dark variant: use Deep Canopy palette as base |
| Warm Tropical | Reduce saturation by 20%; use dark base #0A1A1A with Sunset Punch Accent |
| Retro / Vintage | Use Smoked Oak (Rustic) as dark base; retain desaturated retro tones |
| Soft Gradients | Invert gradient direction; desaturate both stops by 15% |
## Color Discipline

Rules for *using* a palette — applied on top of whichever combo you choose.

### Pixel-share structure

Plan all four layers before writing any CSS. A coherent palette allocates screen
real-estate deliberately:

| Layer | Share of pixels | What it covers |
|---|---|---|
| **Neutrals** | 70–90% | Backgrounds, surfaces, body text, borders |
| **Accent** (one) | 5–10% | CTAs, chips, active states — never invent a second accent |
| **Semantic** | 0–5% | Success, warning, danger states only |
| **Effect** | < 1% | Glows, gradients — rarely justified |

### Accent discipline

The single biggest readability failure in AI-generated UIs is accent overuse.

- **At most 2 visible uses of accent per screen.** Typical pair: one chip/eyebrow label +
  one primary CTA. Or one accent card header + one tab indicator. Pick a pair.
- **Links count as accent.** If you already have a CTA on the same screen, demote links to
  underlined foreground colour instead.
- **Hover/focus rings count as accent.** Budget them in your 2-use cap.

### Dark surface borders

On dark backgrounds, prefer **semi-transparent white borders** over solid dark ones:
```css
border: 1px solid rgba(255, 255, 255, 0.08);
```
This reads as structure without adding visual noise. Solid dark borders on dark
surfaces disappear.

### Near-black / near-white floors

Avoid pure `#000000` and `#ffffff` — both cause vibration and feel undesigned:

| Token | Dark theme | Light theme |
|---|---|---|
| Background | `#0f0f0f` | `#fafafa` |
| Foreground text | `#f0f0f0` | `#111111` |

---

## Contributing

New color combinations welcome. Each submission should include:
- Palette name and category
- Primary, Secondary, Accent, Supporting hex codes
- Style description (2–3 words, evocative)
- Best for (2–3 specific use cases)
- WCAG contrast check: Accent on Primary ratio
- Gradient pair with CSS snippet (optional but encouraged)

Maintained by [@bilioveloso](https://github.com/bilioveloso).
