---
name: landing-pages
description: Registry of landing page URLs with cached analysis and automatic language matching. Loaded automatically by /ads, /ads-batch, /ads-multi, and /ads-refresh so users don't have to paste URLs repeatedly. Edit this file to add your pages.
disable-model-invocation: false
---

# Landing Pages Registry

> ⚠️ CUSTOMIZE THIS FILE — add your landing page URLs below.
> Claude will analyze each page on first use and cache the results
> in this folder as `cache_[key]_[lang].md` files.

## How It Works

1. You register pages below with a short key (e.g., `homepage`, `pricing`, `demo`)
2. Each page can have multiple language variants under `urls:`
3. When you run `/ads`, just say: `landing page: pricing`
4. Claude automatically picks the right language variant based on the ad language
5. For `/ads-multi`, Claude resolves the correct URL per language automatically
6. Pages are analyzed once and cached — no re-fetching on subsequent runs

### Language Resolution Logic

When Claude needs a landing page for a specific ad language:

1. **Exact match** — if `urls:` has the ad language (e.g., `DE` for German ads) → use it
2. **Fallback to EN** — if the ad language isn't listed but `EN` exists → use EN
3. **Fallback to first** — if neither matches → use the first URL listed
4. **Warn** — if using a fallback, Claude notes the mismatch so message-match isn't broken

Example: ads in ES, page only has EN and DE → Claude uses EN and flags it:
_"Note: no Spanish landing page registered for 'pricing' — using EN version.
Consider adding an ES URL for better message match."_

## Pages

```yaml
homepage:
  urls:
    EN: https://example.com
    DE: https://example.com/de
    FR: https://example.com/fr
    ES: https://example.com/es
    AR: https://example.com/ar
    PL: https://example.com/pl
  notes: Main homepage — general brand messaging

pricing:
  urls:
    EN: https://example.com/pricing
    DE: https://example.com/de/preise
    FR: https://example.com/fr/tarifs
    ES: https://example.com/es/precios
    AR: https://example.com/ar/pricing
    PL: https://example.com/pl/cennik
  notes: Pricing page — plans, feature comparison, free trial CTA

demo:
  urls:
    EN: https://example.com/demo
    AR: https://example.com/ar/demo
  notes: Demo request page — form, social proof, trust badges (EN + AR only)

# Add more pages:
# product-feature:
#   urls:
#     EN: https://example.com/features/analytics
#     DE: https://example.com/de/funktionen/analytics
#   notes: Analytics feature page
```

### Single-language shortcut

If a page only exists in one language, you can use a flat URL:

```yaml
blog-post:
  url: https://example.com/blog/ai-marketing-guide
  language: EN
  notes: Blog post — single language, no variants
```

## Cache

On first use, Claude analyzes each page and saves the result as
`cache_[key]_[lang].md` in this folder. Example files:

```
.claude/skills/landing-pages/
├── SKILL.md                    # This file (registry)
├── cache_homepage_EN.md        # Cached analysis of EN homepage
├── cache_homepage_DE.md        # Cached analysis of DE homepage
├── cache_pricing_EN.md         # Cached analysis of EN pricing page
└── ...
```

### Cache file format

```markdown
# Landing Page Analysis: pricing (EN)
URL: https://example.com/pricing
Analyzed: 2026-03-14
Language: EN

## Value Propositions
- [extracted from page]

## Key Features
- [extracted from page]

## CTAs Found
- [extracted from page]

## Trust Signals
- [extracted from page]

## Tone
- [observed tone and style]

## Recommended Ad Angles
- [suggested headline angles based on page content]
```

## Managing Cache

- Cache files live in this folder (`.claude/skills/landing-pages/`)
- Delete a `cache_*` file to force re-analysis on next use
- `refresh landing page: pricing` → re-fetches all language variants of that page
- `refresh landing page: pricing DE` → re-fetches only the German variant
- `list landing pages` → shows all registered pages, languages, and cache status
