---
name: recording-studio-imagegen-web
description: Generate one horizontal website-section image per section for Recording Studio hosts. Use when art-directing landing or marketing comps. This is an image job. Flatpack ViewComponents, tokens, and named themes apply only when the comps hand off to code.
---

# Recording Studio imagegen web

Taste and branding are direction. Implementation is always Flatpack ViewComponents, tokens, and named themes. The dummy default is `html data-theme="rounded"` plus core `UsesDefaultLayout`. Hosts get a named theme (for example `featured-in`), not forked CSS. Never Tailwind, shadcn, GSAP, custom CSS kits, or third-party UI libraries on gem, dummy, or Admin screens. If a look is missing, add a Flatpack token or component first.

Adapted from [leonxlnx/taste-skill](https://github.com/leonxlnx/taste-skill) `skills/imagegen-frontend-web` (MIT, Leonxlnx). See `docs/taste-skill-attribution.md`.

This skill generates section comps. It does not write Tailwind, shadcn, or GSAP. When the user wants the page built, hand off to `recording-studio-image-to-code` and `recording-studio-flatpack`. Taste: `recording-studio-taste`. Direction packs: `recording-studio-soft`, `recording-studio-minimalist`, `recording-studio-brutalist`. Brand: `recording-studio-brandkit`. Mobile images: `recording-studio-imagegen-mobile`.

## When to use

- Landing, marketing, product, or portfolio comps a host can later theme
- The user wants visual direction before Flatpack
- You need one clear image per section, not a collage

Do not code in this skill. Do not compress the whole site into one tall frame.

## Hard output rule

One separate horizontal image per section.

- 1 section → 1 image
- 8 sections → 8 images
- "landing page" with no count → 6 images
- "full website" → 8 images

If you can only render one image at a time, continue sequentially in the same response until the set is done. Label `Section X of N: Name`.

## Hero bias

Left-text / right-image is the most overused AI hero. Allowed, not default. Prefer centered-over-image, bottom-left, stacked center, image-as-canvas, off-grid editorial, mini minimalist, or inverted split.

Hero: short statement (about 5-10 words), one focal point, visible CTA, readable on a small laptop. No pill spam, fake stats, or version stamps.

## Dials

Defaults: variance 8, density 4, art direction 8, implementation clarity 9, image priority 9, spacing 8.

The brief wins. "Minimalist" → mini hero, solid or paper grounds, skip full-bleed. "Editorial" → stronger type and offset. "SaaS / product" → mid hero, clearer product framing (still an image, not coded Flatpack yet).

## Combinatorial picks (commit, do not mash)

Pick one theme paradigm: pristine light, deep dark, bold studio solid, quiet premium neutral.

Pick one type character: clean grotesk, refined grotesk, expressive display, compressed statement, editorial serif+sans, Swiss rational.

Pick one section system: bento, editorial blocks, poster stack, gallery, Swiss grid, asymmetric marketing.

Per section, pick a composition anchor and a background mode. Across the site, at least three anchors. Do not repeat the same anchor more than twice in a row.

CTA style may vary (pill, ghost, inline, banner) but the primary action stays obvious.

Pick one narrative spine (artifact, journey, instrument, garden, stage, archive) and exactly one second-read motif.

These are image cues. They are not a license to implement GSAP or custom CSS later.

## Anti-slop

No purple-blue AI glow, blob fields, cloned card rows, cloned splits, Elevate / Seamless / Unleash, Acme / Nexus names, fake KPI towers, mosquito logo marquees, beige-serif "luxury" as the only move.

One palette across every frame. Section mood shifts reuse that palette.

## Continuity

Same type scale, radius language, CTA family, image grade, and voice in every frame. A flip-through must read as one site.

## Handoff to code

When someone says build it:

- Use `recording-studio-image-to-code`
- Map the locked palette and type to a named Flatpack theme
- Dummy / gem / Admin stay rounded unless opted in
- Do not recreate the comps in Tailwind

A short Taste read of the set (what the site is, what is strong, what would look better in Flatpack tokens) helps the handoff.
