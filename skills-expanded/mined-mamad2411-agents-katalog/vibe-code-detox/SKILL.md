---
name: vibe-code-detox
description: Pre-ship audit that catches the five surface-level "obviously AI-generated" website tells — blue-purple gradients, em-dashes in copy, mobile cutoff, decorative hero badge pills, and missing legal footer pages. Use whenever building, editing, or reviewing a website, landing page, or SaaS UI before shipping.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [web-development, design, qa, landing-page, astro, anti-ai-slop, pre-ship]
    triggers:
      - vibe coded
      - vibe coding
      - looks ai generated
      - ai generated website
      - landing page audit
      - pre-ship website check
      - blue purple gradient
      - website looks generic
      - detox website
    related_skills: [website-landlord-astro-builder, local-service-niche-sites, local-service-websites, hallmark]
---

# Vibe Code Detox

Six specific "this site was obviously AI-generated" tells (source: JordanKodes, YouTube Short xz_lJKdODjw, Jul 2026 + the operator hard laws). These are the quick surface checks a skeptical viewer runs in the first 10 seconds — distinct from deep design-system anti-slop work. Run this audit on every site before shipping.

## Hard Design Law (the operator, Jul 2026)
These are not suggestions — they are hard rules. Every template, every generator, every site must be zero on all counts:
- **No badges, no pills, no chips** — no "Niche — City, Region" pills, "★ rated · Y clients" tags, trust chip sections, stamp badges, or decorative pill elements anywhere.
- **No em dashes (—)** — not in copy, not in meta descriptions, not in section headers, not in HTML comments. Use commas, periods, or spaces instead.
- **No star ratings (★ ☆) in rendered output** — no hero rating badges, no review card stars, no stats bar stars. Display review counts as plain numbers only.
- **No middle dot (·) separators** — no `{niche} · {city}` or `{rating} · {reviews}`. Use clean prose or commas.

## The Five Tells

### 1. Blue-purple gradients everywhere
The default AI hero treatment: `linear-gradient(... blue ... purple ...)`, indigo→violet, etc. Instantly reads as "vibe coded."
**Fix:** Brand/industry-aligned palette. No generic blue→purple anywhere — hero, cards, or buttons.

### 2. Em-dashes anywhere
LLMs overuse the em-dash (—) everywhere — headlines, body copy, meta descriptions, section headers, HTML comments. Real business sites use commas, periods, or colons.
**Fix:** Search-and-replace `—` in ALL source files before ship — `.astro`, `.ts`, comments, everything. Rewrite the sentence if the dash was load-bearing. Also remove decorative em dashes around section headers (`— Our Trades —` → `Our Trades`).

### 3. Mobile layout cutoff / broken responsive
Site looks fine on desktop, cut off or overflowing on a phone. The #1 giveaway of one-shot AI generation with no device testing.
**Fix:** Verify at 375px width before shipping — no horizontal scroll, no truncated CTAs. Cannot be checked statically; open it in a browser or use a mobile viewport emulation.

### 4. Badge / pill / chip elements anywhere
The hero badge above the H1 is one tell. But ALL badge/pill/chip elements scream AI-slop — trust chip sections (✓ Background-checked), stamp badges (✓ 4.9★ rated), stat pills, niche labels (Plumber · Albany, NY), and rating pills.
**Fix:** Remove EVERY pill/badge/chip element. Hero sections get clean headings. Niche/location info goes in prose. Trust signals go in a plain paragraph if at all. No rounded-full + px-* py-* + small text pattern anywhere.

### 5. Footer missing legal pages
No Terms of Service / Privacy Policy links in the footer. Real businesses have them; AI one-shots skip them.
**Fix:** Every site ships with /privacy and /terms pages (even template boilerplate) linked from the footer.

### 6. Star rating badges (★ ☆) in rendered content
Star ratings in hero badges, review cards, stats bars — any rendered output. Real sites show review counts as plain text, not decorative ★ displays. The stars() function in Astro templates that renders ★★★★★ is an instant AI giveaway.
**Fix:** Remove all ★ and ☆ characters from ALL template source files. Display {site.reviewCount} as a plain number. No const stars() function in any template. The ONLY exception is the JSON-LD aggregateRating schema — the data field uses ratingValue but the visual display must not show stars.
No Terms of Service / Privacy Policy links in the footer. Real businesses have them; AI one-shots skip them.
**Fix:** Every site ships with `/privacy` and `/terms` pages (even template boilerplate) linked from the footer.

## Running the Audit

`scripts/vibe_code_detox.py` (packaged with this skill) statically scans a built site directory for tells 1, 2, 4, 5, and 6:

```bash
python <skill-dir>/scripts/vibe_code_detox.py <site-dist-dir>
```

- **Exit 0 = clean, exit 1 = tells found** (each finding printed with file and line).
- Tell 3 (mobile cutoff) requires a real viewport check.
- **After static scan, also verify no ★ in any .astro or .ts source file** for tell 6.
- Run after the build step, before deploy. For fleet pipelines, wire it as a post-build gate.

## Workflow

1. Build the site (any stack).
2. Run `vibe_code_detox.py <dist-dir>` to check tells 1, 2, 4, 5, 6.
3. Manually grep for `★` and `—` in ALL source files.
4. Fix findings, rebuild, re-run until clean.
5. Manually verify 375px mobile layout.
6. Ship.

## Pitfalls

- **False positive on intentional gradients:** a brand that genuinely uses blue-purple should be exempted deliberately — edit the palette to a distinctive shade pairing (not the default `#3b82f6`→`#8b5cf6` family) rather than deleting the check.
- **Em-dash false positives in code samples:** the check scans built HTML text; if a code block legitimately contains `—`, ignore that finding rather than mangling the sample.
- **Badge check must cover ALL pills:** not just the hero H1 badge. Trust chips, stamp badges, stat pills, niche label pills are all equally AI-slop. Scan for any `rounded-full` + small-text + padding combination.
- **Star check must verify template source files:** The audit script checks rendered HTML, but `★` can hide in `const stars = () => ...` function definitions or inline `★★★★★` in templates. Grep ALL `.astro` files separately.
- **Footer check requires both links:** privacy AND terms. One without the other still fails.
- **Source comments with em dashes:** HTML comments (`<!-- ... -->`) with em dashes are invisible to users but the code-level text still signals AI authorship. Remove them.
- **Meta description generators:** The real source of em dashes and stars in rendered HTML is often `src/lib/seo.ts` — the `metaDescription()` function. Check this file specifically for `—` and `★`.
- **Astro SVG strings render as text (critical):** In Astro templates, `{condition && '<svg>...</svg>'}` renders the SVG source code as VISIBLE TEXT on the page. This is because string literals in Astro expressions are rendered as text, not HTML. Fix: use ternary expressions with actual Astro elements: `{condition ? (<svg>...</svg>) : null}`. Grep for `&& '<svg'` to catch this bug.
- **Motionsites design patterns:** When upgrading template aesthetics, extract patterns from `houssemzairihr6587-svg/motionsites-prompts` (63 free + 1 premium prompts on motionsites.ai). Key patterns: **pill-nav** (floating rounded-full navbar with backdrop-blur), **btn-roll** (text slides up on hover with `cubic-bezier(0.25,0.1,0.25,1)`), **arrow-rotate** (CTA arrows rotate -45deg on hover), **hero-title** (letter-spacing -0.04em, line-height 0.92), **liquid-glass** (glassmorphism utility with inset shadow), **fade-in-up** (0.7s ease-out entrance animation).

## References

- `references/vibe-code-tells-audit.md` — condensed source notes from the JordanKodes short and fix guidance per tell.
- Related: `website-landlord-astro-builder` (protected/manual skill) has broader anti-AI-slop design-system references for deep redesigns; this skill is the fast surface audit that runs on every build.
