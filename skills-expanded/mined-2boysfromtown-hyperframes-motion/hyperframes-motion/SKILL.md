---
name: hyperframes-motion
description: Make After Effects-style motion graphics in plain HTML + GSAP — 3D camera moves, kinetic typography, cinematic transitions and four ready-to-edit 1080x1920 templates. Use when the user wants an animated product reveal, social-media ad, brand story or kinetic-text video built as a web page, or asks for "motion graphics", "animated title", "cinematic text" or a 9:16 video template.
---

# HyperFrames Motion Design Skill

After Effects-style motion graphics as plain HTML + GSAP. Turn a web page into a cinematic vertical video — 3D camera moves, kinetic typography, particle and film looks — with no After Effects and no build step.

## What this skill does

Makes HTML videos look like professional motion graphics instead of basic slideshows.

| Before | After |
|--------|-------|
| Simple fades | Motion blur + elastic bounce |
| Static text | Kinetic typography |
| Flat 2D | 3D camera moves (pan, tilt, zoom) |
| Hard cuts | Smooth scene transitions |

## Templates included

Each is a self-contained 1080×1920 HTML page under `templates/`.

1. **`cinematic-product.html`** — 4-scene product reveal: spotlight logo open, 3D product showcase, feature grid with stagger, gradient-text CTA.
2. **`kinetic-typo.html`** — aggressive typography: glitch, character-by-character reveals, elastic bounces.
3. **`brand-story.html`** — elegant narrative: smooth gradients, parallax, clip-path reveals.
4. **`social-ad.html`** — quick flash-sale ad: bold type, fast cuts, conversion CTA.

## Motion effects library

### CSS effects (`css/motion-effects.css`)

**3D camera moves:** `camera-dolly`, `camera-pan`, `camera-tilt`, `camera-orbit`
**Visual effects:** `motion-blur`, `light-leak`, `lens-flare`, `chromatic-aberration`, `film-grain`, `vignette`
**Scene transitions:** `transition-iris`, `transition-wipe`, `transition-morph`, `transition-glitch`

### Text animations (`js/text-animations.js`)

Every helper takes a **CSS selector string** as its first argument:

```javascript
// Split text into characters and animate them in
splitTextChars('.headline', { stagger: 0.05, duration: 0.8, ease: 'back.out(1.7)' });

// Word-by-word reveal
splitTextWords('.subtitle', { stagger: 0.1 });

// Typewriter effect
typewriter('.line', { speed: 0.05 });

// Scramble / decode reveal
scrambleText('.code', { duration: 1.5 });

// Mask wipe reveal
maskReveal('.title', { direction: 'left', duration: 1 });

// Count a number up
countUp('.stat', { suffix: '+' });
```

Also available: `waveText`, `textOnPath`, `gradientText`, `staggerReveal`.
If GSAP has not loaded, the split/mask helpers leave the text readable rather than hiding it.

## Usage

### Basic workflow

1. **Copy a template** from `templates/` into your workspace.
2. **Customize** the text, colours and icons.
3. **Preview** by opening the HTML in a browser.
4. **Export** to MP4 with any HTML-to-video method (headless-Chrome capture, a screen recorder, or your own renderer).

### Customizing templates

**Change brand name:**
```html
<h1 class="brand-logo">YOUR BRAND</h1>
```

**Change product icon:**
```html
<span class="product-icon">📦</span>
```

**Change colours:**
```css
.tagline { color: #ff0080; }
```

**Modify timing** in the template's GSAP timeline:
```javascript
.from('.element', { duration: 1.2 })
```

## Installation

From Claude Code:

```bash
npx skills add 2boysfromtown/hyperframes-motion --global --agent claude-code
```

Or clone the repo and copy a template into your own project:

```bash
git clone https://github.com/2boysfromtown/hyperframes-motion.git
```

## Requirements

- A modern browser (Chromium recommended for recording).
- GSAP 3.x — loaded from jsDelivr in each template, nothing to install.

## About 2BFT

Built by two founders in a jewellery shop in Vaniyambadi, Tamil Nadu, documenting the real process of building AI products from India.

- 🌐 https://2bft.in
- 📸 https://instagram.com/navaratan.ai
