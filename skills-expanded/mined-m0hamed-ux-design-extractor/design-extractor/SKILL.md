---
name: design-extractor
description: >-
  Scrape a live website by its domain and generate a DESIGN.md that captures its
  full visual design system — colors, typography, spacing, components, and a
  rebuild guide — so the look and feel can be replicated on another project. Use
  this whenever the user gives a domain or URL and wants to "copy", "clone",
  "match", "reverse-engineer", "extract", or "document" a site's design, build
  something "in the style of" another site, create a design spec / style guide /
  design tokens from an existing website, or asks "make my site look like X".
  Trigger even if they don't say the words "DESIGN.md" or "design system".
---

# Design Extractor

Turn any live website into a reusable `DESIGN.md` — a design spec detailed enough
that another Claude (or a developer) could rebuild a new project in the same
visual language. You capture what the site *looks like* (via screenshots) and
what it's *made of* (computed colors, fonts, spacing), then synthesize both into
one document.

The screenshots are the source of truth. Token frequency data is a helpful cross-
check, but your eyes on the rendered page are what make the spec accurate — a
font name in CSS tells you less than seeing how type is actually used.

## Prerequisites

The capture script needs Python 3.9+ with a few packages. If a capture run fails
with a missing-module error, install them first:

```bash
python -m pip install -r "${CLAUDE_PLUGIN_ROOT}/requirements.txt"
python -m playwright install chromium
```

The `playwright install chromium` step downloads the headless browser (one-time,
per machine). The script also attempts this automatically on first run. If the
browser still can't run, the script falls back to a plain HTML/CSS scrape — lower
fidelity, but it keeps working on locked-down machines.

## Workflow

### 1. Capture the site

Run the capture script. It renders the homepage plus a few auto-discovered key
pages (pricing, about, features…), saves full-page and above-the-fold
screenshots, extracts computed style tokens, and writes everything to an output
directory.

```bash
python "${CLAUDE_PLUGIN_ROOT}/skills/design-extractor/scripts/capture_site.py" <domain> --out <workspace>/capture --max-pages 3
```

- `<domain>`: what the user gave you, e.g. `stripe.com` or `https://linear.app`.
- `--out`: a fresh directory, ideally named after the domain (e.g. `stripe-capture/`).
- `--max-pages`: total pages including the homepage. 3 is a good default; raise to
  4–5 only if the user wants exhaustive component coverage.

`${CLAUDE_PLUGIN_ROOT}` is set automatically to this plugin's install directory,
so the path works wherever the plugin lives. If for some reason that variable
isn't available, locate `capture_site.py` under the plugin's
`skills/design-extractor/scripts/` directory and call it directly.

The script prints a JSON summary (to stdout) listing the screenshots, the
`tokens.json` file, and any `warnings`. Read the warnings — they flag blank/blocked
pages or when it fell back to the no-screenshot scrape.

### 2. Look at what you captured

**Read the screenshots** — every `*__fold.png` and `*__full.png` in the capture
directory. This is the most important step; do not skip it and work from tokens
alone. As you look, form a point of view on:

- The overall vibe (minimal? playful? corporate? editorial? brutalist?)
- Primary/secondary/accent colors and how they're used (backgrounds vs. CTAs)
- Type: heading vs. body fonts, scale, weight contrast, letter-spacing
- Spacing rhythm, max content width, density (airy vs. compact)
- Component patterns: buttons, cards, nav bar, hero, forms, footers, badges
- Imagery & iconography style, use of gradients/shadows/borders, corner radius

**Then read `tokens.json`** to ground your observations in real values — pull
exact hex/rgb colors, font-family stacks, font sizes, radii, and shadows from the
most-frequent entries rather than guessing from the image. Note that some sites
report colors as `lab()`/`oklch()` — convert these to hex for the spec.

If the capture used the `requests-fallback` method (no screenshots), say so to the
user, work from the HTML/CSS tokens, and note in the DESIGN.md that it's based on
code only and may miss JS-rendered visuals.

### 3. Write DESIGN.md

Synthesize the screenshots + tokens into the structure below. Use real captured
values, not placeholders. The goal is a doc someone could hand to a developer or
to Claude and get back a site that feels unmistakably like the original — without
copying its content or trademarked assets.

Read `references/design_md_template.md` for the full annotated template with an
example of the level of detail expected. The top-level shape is:

```markdown
# DESIGN.md — <Site Name> (<domain>)

## 1. Overview
One paragraph on the brand's visual personality and who it's for.

## 2. Color palette
Table of every key color: token name, hex/rgb, and role (background, surface,
primary action, text, accent, border…).

## 3. Typography
Font families (with web-safe/Google-Font fallbacks), the type scale, weights,
and how headings vs. body differ.

## 4. Spacing & layout
Spacing scale, max content width, grid/column behavior, density notes.

## 5. Elevation, borders & radius
Corner radius scale, shadow definitions, border treatments.

## 6. Components
For each major component (button, card, nav, hero, input, footer, badge):
what it looks like and the key style values. This is where the screenshots pay off.

## 7. Imagery, icons & motion
Photo/illustration style, icon style, any notable transitions or hover effects.

## 8. Implementation guide
Ready-to-use tokens: CSS custom properties **and** a Tailwind config snippet,
plus 2–3 component code recipes (e.g. the primary button, a card).

## 9. Sources
The captured pages and screenshot filenames this spec is based on.
```

### 4. Deliver

Save `DESIGN.md` where the user wants it (default: alongside the capture
directory, or the project root if they're building something). Briefly tell them
what you found — the headline colors, fonts, and overall vibe — and point to the
screenshots so they can verify.

## Notes & boundaries

- This documents *design language* (reusable tokens and patterns), not the site's
  copy, photos, logos, or proprietary assets. Don't reproduce trademarked logos or
  copyrighted imagery; describe the style instead.
- Some sites block automated browsers or render nothing without interaction. If a
  page comes back blank or errors, the script flags it in `warnings` — note it and
  work from whatever did capture.
- For sites behind logins or heavy bot protection, the fallback scrape may be all
  you get — be honest about reduced fidelity.
- Only capture sites you're authorized to analyze, and respect their terms of use.
