---
name: pixelart-startup-aesthetic
description: Use when designing a modern startup website, landing page, or marketing site that should feel like a retro pixel-art video game — 8/16-bit nostalgia layered on top of a clean SaaS layout. Triggers on phrases like "pixel art website", "retro game aesthetic", "Vega Security style", "8-bit landing page", or any request to make a B2B/dev-tools/security/AI product site feel playful, nostalgic, and a little subversive without sacrificing modern conversion UX.
---

# Pixel-Art Startup Aesthetic

## Overview

A visual language where a **modern startup landing page** (hero, social proof, feature grid, CTA, footer) is rendered with the texture and personality of a **retro pixel-art game** — sprite mascots, chunky pixel borders, scanlines, dithered shadows, CRT glow, limited palettes — while keeping the typography, spacing, and interaction patterns of a 2025-era SaaS site.

**The core tension:** Pixel art is nostalgic, lo-fi, playful. Startup sites need to convert: scannable copy, clear CTAs, fast load, accessible contrast. This skill resolves that tension — **pixel art is the costume, not the skeleton**.

Inspired by [Vega Security](https://vega.io) — security/dev-tooling sites have led this aesthetic because the "hacker arcade" vibe maps perfectly to terminal/CTF nostalgia.

## When to Use

- B2B SaaS, dev tools, security, AI infra, or fintech that wants to feel **human and a little subversive**
- Brand wants to stand out from the sea of gradient-blob + Inter-font startup sites
- Product has a **mascot opportunity** (a critter, robot, agent, ghost, blob)
- Target audience is technical: engineers, hackers, gamers, indie devs
- Hackathon, launch-day, or "we ship things" energy

**Do NOT use when:**
- Enterprise buyer is a CFO/CISO who needs to feel "institutional safety" (use it as accent only, not whole site)
- Brand voice is luxurious, minimalist, or medical/healthcare-serious
- Accessibility audience is large and pixel fonts can't be made legible at body-text size

## The Five-Layer Recipe

A pixel-art startup site stacks these in order. Skip a layer and it looks like cosplay; include all five and it looks intentional.

### 1. Layout: Modern SaaS skeleton

Standard sections, standard spacing, standard responsive grid. Do **not** try to mimic an actual NES game layout — that breaks scannability.

- Hero: H1 + subhead + dual CTA + product visual on the right (or below)
- Logo bar / social proof row
- Feature grid (3 or 6 cells)
- "How it works" — 3-step diagram
- Testimonials, pricing, footer
- 12-column grid, ~1200–1280px max width, generous vertical rhythm

The skeleton is *boring on purpose*. The pixel layer is what makes it sing.

### 2. Typography: Pixel for accent, sans-serif for substance

| Where | Font | Why |
|---|---|---|
| Logo, H1, section headers (large) | Pixel display font — **Press Start 2P**, **Silkscreen**, **Pixelify Sans**, **VT323**, **Departure Mono** | Identity + nostalgia |
| Body, subheads, UI labels, long copy | Modern sans-serif — **Inter**, **Geist**, **IBM Plex Sans**, **Satoshi** | Readability above all |
| Code, terminal blocks, stat counters | Monospace — **JetBrains Mono**, **IBM Plex Mono**, **Berkeley Mono** | Terminal continuity |

**Rules:**
- Pixel fonts: only at ≥24px, ideally ≥32px. Below that they're illegible
- Pixel font letter-spacing: +1–4% — pixel fonts crowd themselves
- Never set a paragraph in pixel font. Ever
- Pair one pixel face with one sans — three fonts max total

### 3. Color: Limited palette, dark by default, one hot accent

Pixel art is defined by **palette constraint**. Pick 5–7 colors and stick to them. Most successful pixel-startup sites are dark-mode-first.

**Palette archetypes:**

- **Hacker terminal** — near-black bg (`#0A0E0A`), phosphor green (`#39FF14` / `#00FF66`), one warm accent (amber `#FFB627`)
- **Arcade neon** — deep purple bg (`#1A0B2E`), hot pink (`#FF2E88`), cyan (`#00E5FF`), yellow CTA (`#FFE600`)
- **Game Boy DMG** — four greens: `#0F380F`, `#306230`, `#8BAC0F`, `#9BBC0F` — niche but iconic
- **CRT amber** — `#1A0F00` bg, `#FFB000` primary, `#FF6B00` accent — feels like an Apple ][
- **Vega-ish** — desaturated near-black, off-white, one saturated red/orange accent, a muted lavender or sage for support

**Rules:**
- One CTA color. Used only on primary buttons and one or two key accent strokes. Scarcity = power
- All shadows are **solid color blocks** (offset 2–6px), never gaussian blur. If you must blur, use it for *glow* only (CRT bloom on the accent color)
- Hover states: invert palette or shift offset, don't fade opacity

### 4. Pixel-art assets: Sprites, mascots, scenes

This is where the site earns the label. Without real pixel art, you just have a chunky-fonts site.

**What to commission/generate:**

- **A mascot.** One character. Idle animation (2–4 frames), one reaction frame. The mascot appears in the hero, in empty states, in the 404, in the footer waving. Vega has its little hooded figure; you need yours
- **Feature icons** — 32×32 or 48×48 pixel-art icons, one per feature card. Not Lucide. Not Heroicons. Hand-pixeled (or AI-generated then cleaned up) so they share a visual language
- **Hero scene** — an isometric or side-scrolling pixel illustration that shows the product's *world*. For security: a server room, a CRT, a vault. For AI: a robot at a desk. For dev tools: a terminal with a sprite climbing out of it
- **Section dividers** — pixel-art horizontal rules, not `<hr>`. A row of bricks, a wavy pixel line, a sprite walking across the screen

**Sprite hygiene:**
- All sprites share **one pixel grid size** — usually 1 site-pixel = 3 or 4 CSS pixels (`image-rendering: pixelated` is mandatory)
- All sprites use the **same palette** as the site
- All sprites have **the same shadow language** (e.g., all use a dithered drop shadow 2px down/right, same opacity)

### 5. Effects: CRT, scanlines, dither, glitch — used like seasoning

The single biggest failure mode is over-effecting. Pick **two** of these and stop:

- **Scanline overlay** — fixed-position 2px horizontal lines at ~6% opacity, full-viewport, `pointer-events: none`. Subtle. If you can see it without looking, dial it down
- **CRT vignette** — radial gradient darkening corners, very faint
- **Phosphor glow** — `text-shadow` or `box-shadow` in the accent color, blurred, on key elements only (logo, CTA, hero numbers)
- **Dithered transitions** — section-to-section gradients done with a Bayer dither pattern instead of a smooth gradient
- **Glitch on hover** — RGB-split + 1px jitter on the logo or CTA on hover, max 200ms
- **Typewriter / cursor blink** — hero subhead types in, has a blinking `▌` cursor
- **Idle sprite animation** — mascot blinks every 4s, no other movement

**Never:** auto-playing arcade music. Don't.

## Quick Reference: CSS Building Blocks

```css
/* The two non-negotiable rules */
img, svg, canvas { image-rendering: pixelated; }
* { font-smooth: never; -webkit-font-smoothing: none; } /* on pixel-font elements only */

/* Pixel border — chunky, no anti-aliasing */
.pixel-border {
  border: 4px solid var(--ink);
  box-shadow:
    4px 0 0 var(--ink),
    0 4px 0 var(--ink),
    4px 4px 0 var(--shadow); /* solid offset shadow, no blur */
}

/* Pixel button */
.btn-pixel {
  font-family: 'Press Start 2P', monospace;
  padding: 14px 24px;
  background: var(--accent);
  color: var(--ink);
  border: none;
  box-shadow: 0 4px 0 var(--ink);
  transition: none; /* pixel art doesn't ease */
}
.btn-pixel:hover { transform: translateY(2px); box-shadow: 0 2px 0 var(--ink); }
.btn-pixel:active { transform: translateY(4px); box-shadow: 0 0 0 var(--ink); }

/* Scanlines */
.scanlines::after {
  content: '';
  position: fixed; inset: 0;
  background: repeating-linear-gradient(
    0deg,
    rgba(0,0,0,0.06) 0px,
    rgba(0,0,0,0.06) 1px,
    transparent 1px,
    transparent 3px
  );
  pointer-events: none;
  z-index: 9999;
}

/* CRT glow on accent text */
.glow { text-shadow: 0 0 8px var(--accent), 0 0 16px var(--accent); }
```

## Section-by-Section Cheat Sheet

| Section | Pixel layer | Modern layer |
|---|---|---|
| **Nav** | Pixel logo, monospace links, blinking cursor on hover | Sticky, blurred bg, normal spacing |
| **Hero** | Pixel H1, mascot sprite or scene on the right, scanline overlay | Sans-serif subhead, two CTAs (primary pixel-styled, secondary ghost), logo bar below |
| **Logo bar** | "Trusted by" in pixel font, logos in grayscale | Standard horizontal scroll, hover restores color |
| **Feature grid** | Pixel icons (32×32), chunky border on cards, solid-offset shadow | Sans-serif heading + body in each card, 3-column responsive |
| **How it works** | Numbered tiles like a level-select screen ("1-1", "1-2", "1-3"), arrows as pixel sprites | Sans-serif explanation below each tile |
| **Testimonial** | Quote in pixel font OR a CRT terminal frame around it | Avatar (can be pixelated headshot), name + role in sans |
| **Pricing** | Tier names as "level names" ("Hobbyist", "Pro", "Boss Mode"), pixel border on featured tier | Standard feature checklist, sans-serif, clear price |
| **Footer** | Mascot waving goodbye, pixel-art divider above | Standard 3-column link layout, sans-serif |
| **404** | Mascot looking sad, "Game Over" headline, "Continue?" CTA | Real link back to home |

## Reference sites (study the patterns, don't copy)

- **vega.security** — the canonical example: dark, restrained, one accent, pixel mascot, terminal vibe, but copy is professional B2B
- **railway.app** (historical iterations) — pixel-adjacent
- **resend.com**, **linear.app** — the modern SaaS skeleton you should borrow under the pixel layer
- **Itch.io game pages** — for *too much* pixel art; study these to see what NOT to bring to a B2B site

## Common Mistakes

| Mistake | Fix |
|---|---|
| Pixel font in body copy | Sans-serif for everything under 20px. Pixel font only for H1/H2/logo |
| Anti-aliased pixel art | Add `image-rendering: pixelated` on every image. Resize sprites by integer multiples only |
| Drop-shadows with blur on pixel elements | Use solid offset shadows (`box-shadow: 4px 4px 0 #000`). Reserve blur for CRT glow on accent color only |
| Five accent colors | One CTA color. One support accent. Stop |
| Mismatched sprite styles | Define one palette + one pixel grid size + one shadow rule. Every sprite obeys all three |
| Scanlines at 30% opacity | 4–8% max. If you notice them without looking, too strong |
| Mascot everywhere with no reason | Mascot earns its keep by reacting — to scroll, to hover, to empty states, to errors. Static mascot = sticker |
| Pixel-art product screenshots | Don't pixelate the product UI. The product is modern. Pixel art frames the product, doesn't replace it |
| Auto-playing chiptune music | Just don't |
| Treating the whole site as an arcade game | The site is a startup site. The pixel art is the wallpaper, not the architecture |

## The One-Sentence Test

If you removed every pixel-art asset and pixel font from the site and replaced them with generic SaaS equivalents, the site should **still convert** — same hierarchy, same CTAs in the same places, same scannable copy. The pixel layer is delight on top of a functional site, not a substitute for one.

If removing the pixel art breaks the site's usability, you went too far. If removing it doesn't change the *feeling* at all, you didn't go far enough.
